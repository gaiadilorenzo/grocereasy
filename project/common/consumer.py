from __future__ import annotations

import logging
import threading
from contextlib import contextmanager
from datetime import timedelta
from typing import Any, Callable, ContextManager, Generator, Optional, Type

from google.cloud.pubsub_v1 import SubscriberClient, subscriber, types
from google.cloud.pubsub_v1.subscriber.message import Message

from project.common import messages
from project.common.publisher import Publisher

semaphore = threading.Semaphore(value=1)

_LOGGER = logging.getLogger(__name__)


@contextmanager
def _default_message_middleware(message: Message) -> Generator[None, None, None]:
    """
    The default message middleware used by the subscriber.
    :param message: the Pub/Sub message received by the subscriber.
    """

    with AckMiddleware().ack_message(message):
        yield


MessageMiddlewareType = Callable[[Message], ContextManager[None]]


class Consumer:
    def __init__(
        self,
        gcp_project_id: str,
        subscription: str,
        publisher: Publisher | None = None,
        num_workers: int = 1,
        max_messages_outstanding: int = 1,
        max_lease: timedelta = timedelta(hours=1),
        max_bytes: int = 10_000_000,
        message_middleware: MessageMiddlewareType | None = _default_message_middleware,
    ):
        self._gcp_project = gcp_project_id
        self._subscriber = SubscriberClient()
        self._subscription_path = self._subscriber.subscription_path(gcp_project_id, subscription)
        self._num_workers = num_workers
        self._max_messages_outstanding = max_messages_outstanding
        self._max_lease = max_lease
        self._max_bytes = max_bytes
        self._message_middleware = message_middleware
        self._publisher = publisher
        self._streaming_pull_future: Optional[subscriber.futures.StreamingPullFuture] = None

    def __enter__(self) -> Consumer:
        """Enter the subscriber context and start the subscription."""

        flow_control = types.FlowControl(
            max_bytes=self._max_bytes,
            max_messages=self._max_messages_outstanding,
            max_lease_duration=self._max_lease.total_seconds(),
            max_duration_per_lease_extension=0,  # disabled
        )

        self._streaming_pull_future = self._subscriber.subscribe(
            subscription=self._subscription_path,
            callback=self._handle_message,
            flow_control=flow_control,
            await_callbacks_on_shutdown=True,
        )
        _LOGGER.info(f"🔕 Listening on {self._subscription_path}.")
        return self

    def run(self) -> None:
        """Indefinitely consume messages from the message queue."""
        try:
            if self._streaming_pull_future:
                self._streaming_pull_future.result()
        except KeyboardInterrupt:
            _LOGGER.info("🔕 Gracefully shutting down subscriber due to termination interrupt being received.")

    def _handle_message(self, message: Message) -> None:
        """Handle the message."""
        with semaphore:
            _LOGGER.info("🛬 Received message.")
            if self._message_middleware is not None:
                with self._message_middleware(message):
                    _LOGGER.info("🔕 Start task.")
                    try:
                        self.run_task(message)
                    except Exception as e:
                        _LOGGER.exception("🔕 End task.", e)
                        raise

    def run_task(self, message: messages.AppBaseMessage) -> messages.AppBaseMessage | None:
        pass

    def _ack(self, results: Any) -> None:
        self._publisher.publish(results) if self._publisher else None

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        _LOGGER.exception("🔕 Exiting.")
        if self._streaming_pull_future:
            self._streaming_pull_future.cancel()
            self._streaming_pull_future.result()
        self._subscriber.close()


class AckMiddleware:
    """
    Middleware for PubSub message.
    """

    def __init__(
        self,
        ack_exceptions: tuple[Type[BaseException], ...] = (),
        nack_exceptions: tuple[Type[BaseException], ...] = (),
    ):
        self._ack_exceptions = ack_exceptions
        self._nack_exceptions = nack_exceptions

    @contextmanager
    def ack_message(self, message: Message) -> Generator[None, None, None]:
        """
        Ack or nack the message upon completion.

        :param message: the Pub/Sub message
        """
        # pylint: disable=bare-except
        try:
            yield
        except self._nack_exceptions:
            message.nack()
        except self._ack_exceptions:
            message.ack()
        except:  # noqa: E722
            message.nack()
        else:
            message.ack()
