import dataclasses
import datetime
import json
import logging
from typing import Any, Type, TypeVar

from project.common import messages
from project.common.item import Item
from project.common.job import Job

_LOGGER = logging.getLogger(__name__)

T = TypeVar("T", bound=messages.AppBaseMessage)


class EmptyMessageException(Exception):
    """Raised when a PubSub message is empty."""


def default(o: Any) -> Any:
    """Default serializer."""

    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    elif isinstance(o, Item):
        return o.dict()
    raise TypeError(f"Type {type(o)} is not serializable")


def serialize(message: messages.AppBaseMessage) -> bytes:
    """Serialize an object into bytes."""

    return bytes(
        json.dumps(
            {**dataclasses.asdict(message), "date": datetime.date.today()},
            default=default,
        ),
        encoding="utf-8",
    )


def deserialize(raw: bytes, message_class: Type[T]) -> T:
    """Deserialize an object into buckets."""

    if raw == b"":
        raise EmptyMessageException("❌ Trying to deserialize an empty message.")

    fields = json.loads(raw)

    if not fields.get("date"):
        fields["date"] = datetime.date.today()
    if items := fields.get("items"):
        try:
            fields["items"] = [Item(**params) for params in items]
        except KeyError:
            pass
    if jobs := fields.get("jobs"):
        try:
            fields["jobs"] = [Job(**params) for params in jobs]
        except KeyError:
            pass

    return message_class(**fields)
