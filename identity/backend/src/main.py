from api_gateway.service_event import ApiGatewayServiceEvent
from lambda_handler.mapper.mapper import ServiceEventMapper

service_event_mapper = ServiceEventMapper.from_list([
    ApiGatewayServiceEvent,
])


def handler(event, context):
    print('context:', context)
    print('service_event:', event)
    service_event = service_event_mapper.map(event)
    return service_event.handle()
