import dataclasses

from project.common.item import Supermarket


@dataclasses.dataclass(frozen=True)
class Job:
    """A job."""

    supermarket: Supermarket
    url: str
