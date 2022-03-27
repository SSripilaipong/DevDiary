from lambler.api_gateway.endpoint.marker import JSONBody
from lambler.api_gateway.router import APIGatewayRouter
from .event_factory import simple_post_event


def test_should_pass_json_body_as_dict():
    router = APIGatewayRouter()

    @router.post("/do/something")
    def do_something(my_body: dict = JSONBody()):
        do_something.data = my_body["data"]

    router.match(simple_post_event("/do/something", {"data": "Hello World"}), ...).handle()
    assert getattr(do_something, "data", "") == "Hello World"
