import dataclasses
import datetime
import logging
import time
from typing import Callable, Sequence, TypeVar

from project.common import (
    BigqueryManager,
    Consumer,
    Job,
    Publisher,
    Supermarket,
    constants,
    log,
    messages,
    serializer,
)
from project.orchestrator import table
from project.orchestrator.url_providers import URLProvider

_LOGGER = logging.getLogger(__name__)

_JOBS_PER_MESSAGE = 20

S = TypeVar("S", bound=URLProvider)


class Orchestrator(Consumer):
    """
    The orchestrator.

    Creates jobs and sends them in batches to the worker.
    """

    def __init__(
        self,
        publisher_worker: Publisher,
        gcp_project_id: str,
        subscription: str,
        bigquery_manager: BigqueryManager,
        url_providers: Sequence[S],
        *,
        _datetime_generator: Callable[[], datetime.date] = datetime.date.today,
    ):
        super().__init__(gcp_project_id, subscription, publisher_worker)
        self._jobs_computed = 0
        self._bigquery_manager = bigquery_manager
        self._date_generator = _datetime_generator
        self._url_providers = url_providers
        self._bigquery_manager = bigquery_manager

    def run_task(self, message: serializer.T) -> None:
        """Indefinitely send jobs to the workers."""

        while True:
            jobs = self.get_n_jobs()

            if len(jobs) == 0:
                break

            _LOGGER.info("🛒 Submitting new jobs to the worker.")
            self._publisher.publish(messages.WorkerMessage(jobs=jobs))  # type: ignore[union-attr]
            self.store_jobs(jobs)

            time.sleep(20 * constants.Time.MINUTE)
        _LOGGER.exception("😴 Shutting down due to no new jobs to fetch.")

    @log(message="Storing new jobs executed.", emoji="🛒")
    def store_jobs(self, jobs: list[Job]) -> None:
        """Store the jobs to database."""

        self._bigquery_manager.store(
            dataset_id=table.DATASET,
            table_id=table.NAME,
            job_config=table.JOB_CONFIG,
            rows=[
                {
                    **dataclasses.asdict(job),
                    "timestamp": datetime.datetime.utcnow(),
                    "last_executed": datetime.datetime.utcnow(),
                }
                for job in jobs
            ],
        )

    @log(message="Getting new jobs executed.", emoji="🛒")
    def get_n_jobs(self, jobs: list[Job] | None = None) -> list[Job]:
        """Get the next n jobs to be executed."""

        return [
            Job(supermarket=Supermarket(row.supermarket), url=row.url)
            for row in self._bigquery_manager.query_table(
                query=self._get_n_jobs_query(
                    f"{self._gcp_project}.{table.DATASET}.{table.NAME}",
                    urls=[job.url for job in jobs] if jobs is not None else None,
                ),
                job_id_prefix="orchestrator",
            )
        ]

    def _get_n_jobs_query(self, table: str, urls: list[str] | None, limit: int = _JOBS_PER_MESSAGE) -> str:
        if urls is None:
            return f"""SELECT supermarket, url
            FROM {table}
            WHERE url NOT IN (SELECT url
                FROM {table}
                WHERE DATE(last_executed) > DATE_SUB('{self._date_generator()}', INTERVAL 7 DAY)
                )
            AND TIMESTAMP_TRUNC(TIMESTAMP(timestamp), DAY) = (SELECT MAX(TIMESTAMP_TRUNC(TIMESTAMP(timestamp), DAY))
                            FROM {table}
            )
            GROUP BY supermarket, url
            LIMIT {limit}
            """
        else:
            return f"""SELECT supermarket, url
                FROM {table}
                WHERE url NOT IN (SELECT url
                    FROM {table}
                    WHERE DATE(last_executed) > DATE_SUB('{self._date_generator()}', INTERVAL 7 DAY)
                    ) AND url in UNNEST({urls})
                AND TIMESTAMP_TRUNC(TIMESTAMP(timestamp), DAY) = (SELECT MAX(TIMESTAMP_TRUNC(TIMESTAMP(timestamp), DAY))
                                FROM {table}
                )
                GROUP BY supermarket, url
                LIMIT {limit}
                """

    @log(message="Storing new jobs.", emoji="📦")
    def store_new_jobs(self, products: list[str]) -> list[Job]:
        """Store the jobs to database."""

        executed_jobs = [
            row.url
            for row in self._bigquery_manager.query_table(
                query=self._get_executed_jobs_query(f"{self._gcp_project}.{table.DATASET}.{table.NAME}"),
                job_id_prefix="orchestrator",
            )
        ]

        jobs = [
            Job(url=url, supermarket=Supermarket(url_provider.get_supermarket()))
            for url_provider in self._url_providers
            for url in url_provider.get_urls(products)
            if url not in executed_jobs
        ]

        _LOGGER.debug(f"📦 {len(jobs)} new jobs created.")

        self._bigquery_manager.store(
            dataset_id=table.DATASET,
            table_id=table.NAME,
            job_config=table.JOB_CONFIG,
            rows=[
                {**dataclasses.asdict(job), "timestamp": datetime.datetime.utcnow(), "last_executed": None}
                for job in jobs
            ],
        )
        return jobs

    def _get_executed_jobs_query(self, table: str, limit: int = 7) -> str:
        return f"""SELECT supermarket, url
        FROM {table}
        WHERE url IN (SELECT url
                      FROM {table}
                      WHERE DATE(last_executed) < DATE_SUB('{self._date_generator()}', INTERVAL {limit} DAY))
        GROUP BY supermarket, url
        """
