from app import dependency
from app.api.handler import get_api_gateway_handler
from lambda_handler.mapper import ServiceEventHandlerMapper


event_handler_mapper = ServiceEventHandlerMapper.from_list([
    get_api_gateway_handler(),
])


dependency.inject()


def handler(event, _):
    event_handler = event_handler_mapper.map(event)
    return event_handler.handle(event)
