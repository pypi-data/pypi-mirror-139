import stringcase
from troposphere.sqs import Queue
from typing import Optional

from serverless.aws.types import SQSArn
from serverless.service.types import Identifier, YamlOrderedDict


class Function(YamlOrderedDict):
    yaml_tag = "!Function"

    def __init__(self, service, name, description, handler=None, timeout=None, layers=None, force_name=None, **kwargs):
        super().__init__()
        self._service = service
        self.key = stringcase.pascalcase(stringcase.snakecase(name).lower())
        if force_name:
            self.name = force_name
        else:
            self.name = Identifier(
                self._service.service.spinal.lower() + "-${sls:stage}" + "-" + stringcase.spinalcase(name).lower()
            )
        self.description = description

        if not handler:
            handler = f"{self._service.service.snake}.{stringcase.snakecase(name)}.handler"

        self.handler = handler
        self.events = []

        if layers:
            self.layers = layers

        if timeout:
            self.timeout = timeout

        for name, value in kwargs.items():
            setattr(self, name, value)

    def trigger(self, event):
        self.events.append(event)

        return event

    def apply(self, **kwargs):
        for event in self.events:
            for k, v in kwargs.items():
                event[k] = v

    def use_async_dlq(self, onErrorDLQArn: Optional[str] = None, MessageRetentionPeriod: int = 1209600) -> None:
        """
        @param onErrorDLQArn: Optional[str]
        @param MessageRetentionPeriod: integer – defaults to 14 days in seconds
        @return None
        """
        if not onErrorDLQArn:
            name = f"{self.name.spinal}-dlq"
            queue = Queue(
                QueueName=f"{self.name.spinal}-dlq",
                title=f"{self.name.pascal}DLQ",
                MessageRetentionPeriod=MessageRetentionPeriod,
            )
            self._service.resources.add(queue)

            onErrorDLQArn = SQSArn(name)
            self._service.provider.iam.allow(
                sid=f"{queue.title}Writer",
                permissions=["sqs:GetQueueUrl", "sqs:SendMessageBatch", "sqs:SendMessage"],
                resources=[onErrorDLQArn],
            )

        self.onError = onErrorDLQArn

    def use_destination_dlq(self, onFailuredlqArn: Optional[str] = None, MessageRetentionPeriod: int = 1209600) -> None:
        """
        @param onFailuredlqArn: Optional[str]
        @param MessageRetentionPeriod: integer – defaults to 14 days in seconds
        @return None
        """
        if not onFailuredlqArn:
            name = f"{self.name.spinal}-dlq"
            queue = Queue(
                QueueName=f"{self.name.spinal}-dlq",
                title=f"{self.name.pascal}DLQ",
                MessageRetentionPeriod=MessageRetentionPeriod,
            )
            self._service.resources.add(queue)
            onFailuredlqArn = SQSArn(name)

        self.destinations = dict(onFailure=onFailuredlqArn)

    @classmethod
    def to_yaml(cls, dumper, data):
        events = data.events
        data.pop("_service", None)
        data.pop("key", None)

        if not data.events:
            del data["events"]
        else:
            data.events = [{event.yaml_tag: event} for event in events]

        return dumper.represent_dict(data)
