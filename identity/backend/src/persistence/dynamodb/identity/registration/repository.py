import uuid
from typing import Dict

from chamber.aggregate.version import AggregateVersion
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
        del data["_Partition"], data["_SortKey"], data["_LatestEvents"]
        version = AggregateVersion(data["_Version"])
        return Registration.from_dict(data, _aggregate_version=version)

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
        item = self._dynamodb_registration_to_dynamodb_dict(
            registration, partition=f"registration#{registration.email.str()}",
            sort_key=f"registration#{registration.email.str()}",
        )
        condition = f"attribute_not_exists(#Partition) OR attribute_not_exists(#SortKey)"

        try:
            self._client.put_item(
                TableName=self._table_name,
                Item=item,
                ConditionExpression=condition,
                ExpressionAttributeNames={
                    "#Partition": "_Partition",
                    "#SortKey": "_SortKey",
                },
            )
        except self._client.exceptions.ConditionalCheckFailedException:
            raise NotImplementedError()  # should not happen

    def __dynamodb_update_registration(self, registration: Registration):
        item = self._dynamodb_registration_to_dynamodb_dict(
            registration, partition=f"registration#{registration.username.str()}",
            sort_key=f"registration#{registration.username.str()}",
        )

        current_version = registration.aggregate_version.int()
        registration.increase_aggregate_version_by(AggregateVersionIncrease(1))
        condition = f"#Version == {current_version}"

        try:
            self._client.put_item(
                TableName=self._table_name,
                Item=item,
                ConditionExpression=condition,
                ExpressionAttributeNames={
                    "#Version": "_Version",
                },
            )
        except self._client.exceptions.ConditionalCheckFailedException:
            raise EntityOutdated()

    def _dynamodb_registration_to_dynamodb_dict(self, registration: Registration, partition: str, sort_key: str) \
            -> Dict:
        data = registration.to_dict()
        data['_Partition'] = partition
        data['_SortKey'] = sort_key
        data['_LatestEvents'] = [message.to_dict() for message in registration.get_aggregate_outbox_messages()]
        data['_Version'] = registration.aggregate_version.int()
        item = {key: self.__serializer.serialize(value) for key, value in data.items()}
        return item

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
            partition: str = matched.get("_Partition", "")
            if partition == email_partition:
                raise EmailAlreadyRegisteredException()
            elif partition == username_partition:
                raise UsernameAlreadyRegisteredException()
            else:
                raise NotImplementedError()
