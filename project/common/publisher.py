import dataclasses
import logging

import google.cloud.pubsub as pubsub

from project.common import messages, serializer
from project.common.utility import log

_LOGGER = logging.getLogger(__name__)


class Publisher:
    """Publisher for messages."""

    _MAX_SIZE = 10_000_000

    def __init__(
        self,
        project_id: str,
        topic_id: str,
    ) -> None:
        self._project_id = project_id
        self._client = pubsub.PublisherClient()
        self._topic_path = self._client.topic_path(project_id, topic_id)

    @log(message="Publishing message.", emoji="✈️")
    def publish(self, message: messages.AppBaseMessage) -> None:
        """Publish a message to the topic."""

        if len(serializer.serialize(message)) >= self._MAX_SIZE and isinstance(message, messages.StorerMessage):
            params_first_message = dataclasses.asdict(message) | {"items": message.items[: len(message.items) // 2]}
            params_snd_message = dataclasses.asdict(message) | {"items": message.items[: len(message.items) // 2]}

            message_first_half = messages.StorerMessage(**params_first_message)  # type: ignore[arg-type]

            self.publish(message=message_first_half)

            message_second_half = messages.StorerMessage(**params_snd_message)  # type: ignore[arg-type]
            self.publish(message=message_second_half)

        return self._publish(payload=serializer.serialize(message=message))

    def _publish(self, payload: bytes) -> None:
        future = self._client.publish(topic=self._topic_path, data=payload)
        try:
            future.result()
        except KeyboardInterrupt:
            future.cancel()
