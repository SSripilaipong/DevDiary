import uuid
from typing import Dict

from chamber.aggregate.version_increase import AggregateVersionIncrease
from chamber.repository import EntityOutdated
from domain.identity.registration.exception import (
    EmailAlreadyRegisteredException, RegistrationNotFoundException, )
from domain.identity.user.exception import UsernameAlreadyRegisteredException
from domain.identity.registration.registration import Registration
from domain.identity.registration.repository import AllRegistrations
from domain.identity.value_object.email import Email
from domain.identity.value_object.username import Username


class AllRegistrationsInDynamodb(AllRegistrations):
    def __init__(self, dynamodb_client, table_name: str):
        self._client = dynamodb_client
        self._table_name = table_name

        try:
            import boto3.dynamodb.types
            self.__serializer = boto3.dynamodb.types.TypeSerializer()
            self.__deserializer = boto3.dynamodb.types.TypeDeserializer()
        except ImportError:
            self.__serializer = None
            self.__deserializer = None

    def create(self, registration: Registration) -> Registration:
        """
        :raises:
            EmailAlreadyRegisteredException
            UsernameAlreadyRegisteredException
        """
        self.__dynamodb_verify_unique_email_and_username(registration.email, registration.username)
        self.__dynamodb_create_registration(registration)
        registration.clear_aggregate_outbox_messages()

        return registration

    def from_email(self, email: Email) -> Registration:
        """
        :raises:
            RegistrationNotFoundException
        """
        data = self.__dynamodb_get_registration_by_email(email)
        return Registration.from_dict(data)

    def save(self, registration: Registration):
        """
        :raises:
            EntityOutdated
            RegistrationNotFoundException
        """
        self.__dynamodb_update_registration(registration)
        registration.clear_aggregate_outbox_messages()

        return registration

    def generate_confirmation_code(self) -> str:
        return str(uuid.uuid4())

    def __dynamodb_get_registration_by_email(self, email: Email) -> Dict:
        """
        :raises:
            RegistrationNotFoundException
        """
        response = self._client.get_item(
            TableName=self._table_name,
            Key={
                "_Partition": {"S": f"registration#{email.str()}"},
                "_SortKey": {"S": f"registration#{email.str()}"},
            },
        )
        item = response.get('Item', None)
        if item is None:
            raise RegistrationNotFoundException()
        return self.__deserializer.deserialize(item)

    def __dynamodb_create_registration(self, registration: Registration):
        data = registration.to_dict()
        item = {key: self.__serializer.serialize(value) for key, value in data.items()}

        item['_Partition'] = f"registration#{registration.email.str()}"
        item['_SortKey'] = f"registration#{registration.email.str()}"
        item['_Events'] = [message.to_dict() for message in registration.get_aggregate_outbox_messages()]
        item['_Version'] = registration.aggregate_version.int()

        condition = f"attribute_not_exists(_Partition) OR attribute_not_exists(_SortKey)"

        try:
            self._client.put_item(
                TableName=self._table_name,
                Item=item,
                ConditionExpression=condition,
            )
        except self._client.exceptions.ConditionalCheckFailedException:
            raise NotImplementedError()  # should not happen

    def __dynamodb_update_registration(self, registration: Registration):
        data = registration.to_dict()
        item = {key: self.__serializer.serialize(value) for key, value in data.items()}
        current_version = registration.aggregate_version.int()
        registration.increase_aggregate_version_by(AggregateVersionIncrease.create(1))

        item['_Partition'] = f"registration#{registration.username.str()}"
        item['_SortKey'] = f"registration#{registration.username.str()}"
        item['_Events'] = [message.to_dict() for message in registration.get_aggregate_outbox_messages()]
        item['_Version'] = registration.aggregate_version.int()

        condition = f"_Version == {current_version}"

        try:
            self._client.put_item(
                TableName=self._table_name,
                Item=item,
                ConditionExpression=condition,
            )
        except self._client.exceptions.ConditionalCheckFailedException:
            raise EntityOutdated()

    def __dynamodb_verify_unique_email_and_username(self, email: Email, username: Username):
        """
        :raises:
            EmailAlreadyRegisteredException
            UsernameAlreadyRegisteredException
        """
        email_partition = f"registration#{email.str()}"
        username_partition = f"registeredUsername#{username.str()}"

        response = self._client.batch_get_item(
            RequestItems={
                self._table_name: {
                    "Keys": [
                        {
                            "_Partition": {"S": email_partition},
                            "_SortKey": {"S": email_partition},
                        },
                        {
                            "_Partition": {"S": username_partition},
                            "_SortKey": {"S": username_partition},
                        },
                    ],
                    "ConsistentRead": True,
                },
            },
        )

        for matched in response["Responses"].get(self._table_name, []):
            entity_type = matched.get("EntityType", None)
            if entity_type == "RegisteredEmail":
                raise EmailAlreadyRegisteredException()
            elif entity_type == "Registration":
                raise UsernameAlreadyRegisteredException()
            else:
                raise NotImplementedError()
