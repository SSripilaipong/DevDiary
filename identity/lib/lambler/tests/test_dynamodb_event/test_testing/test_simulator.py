from lambler import Lambler
from lambler.dynamodb_event import DynamodbEventProcessor
from lambler.dynamodb_event.data.view import DynamodbStreamView
from lambler.testing.dynamodb_event.simulator import DynamodbEventSimulator


def test_should_simulate_insert_event():
    processor = DynamodbEventProcessor(stream_view_type=DynamodbStreamView.NEW_IMAGE)

    @processor.insert()
    def on_insert():
        on_insert.is_called = True

    lambler = Lambler()
    lambler.include_pattern(processor)

    simulator = DynamodbEventSimulator(lambler)
    simulator.insert({"num": 123}, partition="MyPartitionKey", sort="MySortKey")

    assert getattr(on_insert, "is_called", False)
