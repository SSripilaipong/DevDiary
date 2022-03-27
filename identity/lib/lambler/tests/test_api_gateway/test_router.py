from lambler.api_gateway.router import APIGatewayRouter, APIGatewayEventHandler
from .event_factory import simple_post_event, simple_get_event


def test_should_match_api_gateway_event():
    router = APIGatewayRouter()

    router.get("/default/something")(lambda: ...)

    assert isinstance(router.match(simple_get_event("/default/something"), ...), APIGatewayEventHandler)


def test_should_return_None_for_random_event():
    assert APIGatewayRouter().match({"Hello": "World"}, ...) is None


def test_should_handle_event_with_get_method():
    router = APIGatewayRouter()

    @router.get("/default/something")
    def get_something():
        get_something.is_called = True

    router.match(simple_get_event("/default/something"), ...).handle()
    assert getattr(get_something, "is_called", False)


def test_should_handle_event_with_post_method():
    router = APIGatewayRouter()

    @router.post("/default/something")
    def post_something():
        post_something.is_called = True

    router.match(simple_post_event("/default/something"), ...).handle()
    assert getattr(post_something, "is_called", False)


def test_should_select_endpoints_with_same_path_by_method():
    router = APIGatewayRouter()

    @router.post("/default/something")
    def post_something():
        post_something.is_called = True

    @router.get("/default/something")
    def get_something():
        get_something.is_called = True

    router.match(simple_post_event("/default/something"), ...).handle()
    assert getattr(post_something, "is_called", False) and not getattr(get_something, "is_called", False)
    post_something.is_called = False

    router.match(simple_get_event("/default/something"), ...).handle()
    assert not getattr(post_something, "is_called", False) and getattr(get_something, "is_called", False)


def test_should_select_endpoints_with_same_method_by_path():
    router = APIGatewayRouter()

    @router.get("/hello/one")
    def hello_one():
        hello_one.is_called = True

    @router.get("/hello/two")
    def hello_two():
        hello_two.is_called = True

    router.match(simple_get_event("/hello/one"), ...).handle()
    assert getattr(hello_one, "is_called", False) and not getattr(hello_two, "is_called", False)
    hello_one.is_called = False

    router.match(simple_get_event("/hello/two"), ...).handle()
    assert not getattr(hello_one, "is_called", False) and getattr(hello_two, "is_called", False)


def test_should_select_endpoint_with_longest_path():
    router = APIGatewayRouter()

    @router.get("/hello")
    def hello():
        hello.is_called = True

    @router.get("/hello/world")
    def hello_world():
        hello_world.is_called = True

    router.match(simple_get_event("/hello"), ...).handle()
    assert getattr(hello, "is_called", False) and not getattr(hello_world, "is_called", False)
    hello.is_called = False

    router.match(simple_get_event("/hello/world"), ...).handle()
    assert not getattr(hello, "is_called", False) and getattr(hello_world, "is_called", False)
