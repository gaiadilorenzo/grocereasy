import datetime
import logging

from project.common import (
    BigqueryManager,
    Consumer,
    Item,
    StorerMessage,
    log,
    serializer,
    table,
)

_LOGGER = logging.getLogger(__name__)


class Storer(Consumer):
    """
    The storer.

    Stores the worker results to bigquery.
    """

    def __init__(
        self,
        bigquery_manager: BigqueryManager,
        gcp_project_id: str,
        subscription: str,
    ):
        super().__init__(gcp_project_id, subscription)
        self._bigquery_manager = bigquery_manager

    def run_task(self, message: serializer.T) -> None:
        """Store the items to database callback."""

        storer_message = serializer.deserialize(message.data, StorerMessage)  # type: ignore[attr-defined]
        self.store_items(storer_message.items)

    @log(message="Storing items fetched.", emoji="📦")
    def store_items(self, items: list[Item]) -> None:
        """Store the items to database."""

        if not items:
            return _LOGGER.info("📦 No items to store.")

        for i in range(0, len(items), 100):
            self._bigquery_manager.store(
                table_id=table.NAME,
                dataset_id=table.DATASET,
                rows=[{**item.dict(), "timestamp": datetime.datetime.utcnow()} for item in items[i : i + 100]],
                job_config=table.JOB_CONFIG,
            )
