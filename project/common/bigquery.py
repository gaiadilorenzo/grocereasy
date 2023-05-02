from typing import Any, Iterable, Optional

import pandas
from google.cloud import bigquery

from project.common import constants


class BigqueryManager:
    """A Bigquery manager."""

    def __init__(self, gcp_project_id: str):
        self._project_id = gcp_project_id
        self._client = bigquery.Client(project=gcp_project_id)

    def _get_table_ref(
        self,
        table_id: str,
        dataset_id: str,
    ) -> bigquery.TableReference:
        """Get the table reference of the project."""

        return bigquery.TableReference.from_string(f"{self._project_id}.{dataset_id}.{table_id}")

    def create_table(
        self,
        table_id: str,
        dataset_id: str,
        schema: Iterable[bigquery.SchemaField],
        time_partitioning: bigquery.TimePartitioning | None = None,
        clustering_fields: Iterable[str] | None = None,
        description: Optional[str] = None,
        fail_if_exists: bool = False,
    ) -> bigquery.Table:
        """Create a table."""

        table = bigquery.Table(self._get_table_ref(table_id=table_id, dataset_id=dataset_id))
        table.schema = schema
        table.description = description

        if clustering_fields:
            table.clustering_fields = clustering_fields
        if time_partitioning:
            table.time_partitioning = time_partitioning

        self._client.create_table(table=table, exists_ok=not fail_if_exists)
        return self._client.update_table(table=table, fields=["schema"])

    def store(
        self,
        table_id: str,
        dataset_id: str,
        rows: Iterable[dict[str, Any]],
        job_config: bigquery.LoadJobConfig,
        *,
        project_id: str | None = None,
    ) -> None:
        """Store entities in a given table."""

        table = self._client.get_table(self._get_table_ref(table_id=table_id, dataset_id=dataset_id))

        job = self._client.load_table_from_dataframe(
            dataframe=pandas.DataFrame(rows),
            destination=table,
            job_config=job_config,
            timeout=30 * constants.Time.SECONDS,
            num_retries=1,
        )

        job.result()
        return

    def query_table(
        self,
        query: str,
        job_id_prefix: str,
    ) -> bigquery.table.RowIterator | bigquery.table._EmptyRowIterator:
        """Store entities in a given table."""

        query_job = self._client.query(
            query,
            location="US",
            job_id_prefix=job_id_prefix,
        )

        return query_job.result()
