import dataclasses
import datetime

from project.common.item import Item
from project.common.job import Job


@dataclasses.dataclass(frozen=True)
class AppBaseMessage:
    pass


@dataclasses.dataclass(frozen=True)
class OrchestratorMessage(AppBaseMessage):
    """A project orchestrator base message."""

    date: datetime.date | None = None


@dataclasses.dataclass(frozen=True)
class WorkerMessage(AppBaseMessage):
    """A worker base message."""

    jobs: list[Job]
    date: datetime.date | None = None


@dataclasses.dataclass(frozen=True)
class StorerMessage(AppBaseMessage):
    """A storer base message."""

    items: list[Item]
    date: datetime.date | None = None
