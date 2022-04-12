from typing import Dict

from lambler import Lambler
from lambler.dynamodb_event import DynamodbEventProcessor
from lambler.dynamodb_event.data.view import DynamodbStreamView
from lambler.dynamodb_event.marker import EventBody
from lambler.dynamodb_event.response import DynamodbEventBatchResponse
from lambler.testing.dynamodb_event.simulator import DynamodbEventSimulator


def test_should_simulate_insert_event():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @processor.insert()
    def on_insert():
        on_insert.is_called = True

    lambler = Lambler()
    lambler.include_pattern(processor)

    simulator = DynamodbEventSimulator(lambler, stream_view_type=DynamodbStreamView.NEW_IMAGE)
    simulator.insert({"Partition": "Hello", "Sort": 0, "num": 123}, partition_key="Partition", sort_key="Sort")

    assert getattr(on_insert, "is_called", False)


def test_should_pass_body_data():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @processor.insert()
    def on_insert(data: Dict = EventBody()):
        on_insert.data = data

    lambler = Lambler()
    lambler.include_pattern(processor)

    simulator = DynamodbEventSimulator(lambler, stream_view_type=DynamodbStreamView.NEW_IMAGE)
    simulator.insert({"Partition": "Hello", "Sort": 0, "num": 123}, partition_key="Partition", sort_key="Sort")

    assert getattr(on_insert, "data", None) == {"Partition": "Hello", "Sort": 0, "num": 123}


def test_should_return_response():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @processor.insert()
    def on_insert(data: Dict = EventBody()):
        on_insert.data = data

    lambler = Lambler()
    lambler.include_pattern(processor)

    simulator = DynamodbEventSimulator(lambler, stream_view_type=DynamodbStreamView.NEW_IMAGE)
    data = {"Partition": "Hello", "Sort": 0, "num": 123}
    response = simulator.insert(data, partition_key="Partition", sort_key="Sort")

    assert isinstance(response, DynamodbEventBatchResponse) and response.all_success()


def test_should_return_response_with_failure_item():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @processor.insert()
    def on_insert():
        raise Exception()

    lambler = Lambler()
    lambler.include_pattern(processor)

    simulator = DynamodbEventSimulator(lambler, stream_view_type=DynamodbStreamView.NEW_IMAGE)
    data = {"Partition": "Hello", "Sort": 0, "num": 123}
    response = simulator.insert(data, partition_key="Partition", sort_key="Sort")

    assert not response.all_success()
