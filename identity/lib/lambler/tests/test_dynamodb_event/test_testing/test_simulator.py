from typing import Dict

from lambler import Lambler
from lambler.dynamodb_event import DynamodbEventProcessor
from lambler.dynamodb_event.data.view import DynamodbStreamView
from lambler.dynamodb_event.marker import EventBody
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
