import datetime

from google.cloud import bigquery

from project.orchestrator import table
from project.orchestrator.orchestrator import Orchestrator
from tests import helpers
from tests.constants import DATE

INPUT_DATA = [
    {
        "supermarket": "a-supermarket",
        "url": "a-url1",
        "timestamp": DATE,
        "last_executed": DATE - datetime.timedelta(hours=1),
    },
    {"supermarket": "a-supermarket", "url": "a-url2", "timestamp": DATE, "last_executed": None},
    {
        "supermarket": "another-supermarket",
        "url": "another-supermarket-url1",
        "timestamp": DATE - datetime.timedelta(days=1),
        "last_executed": DATE - datetime.timedelta(days=1),
    },
    {
        "supermarket": "another-supermarket",
        "url": "another-supermarket-url2",
        "timestamp": DATE - datetime.timedelta(days=1),
        "last_executed": DATE - datetime.timedelta(hours=7),
    },
    {
        "supermarket": "another-another-supermarket",
        "url": "another-another-url",
        "timestamp": DATE - datetime.timedelta(days=1),
        "last_executed": DATE - datetime.timedelta(days=2),
    },
    {
        "supermarket": "another-another-supermarket",
        "url": "another-another-url",
        "timestamp": DATE - datetime.timedelta(days=1),
        "last_executed": DATE - datetime.timedelta(hours=1),
    },
]

OUTPUT_DATA = [
    {
        "supermarket": "a-supermarket",
        "url": "a-url2",
    },
]

OUTPUT_SCHEMA = [
    bigquery.SchemaField(
        name="supermarket",
        field_type=bigquery.enums.SqlTypeNames.STRING,
        mode="REQUIRED",
    ),
    bigquery.SchemaField(
        name="url",
        field_type=bigquery.enums.SqlTypeNames.STRING,
        mode="REQUIRED",
    ),
]


def test__get_n_jobs_query(client: bigquery.Client, the_orchestrator: Orchestrator) -> None:

    helpers.assert_query_execution(
        client=client,
        query=the_orchestrator._get_n_jobs_query,
        input_data=INPUT_DATA,
        input_schema=table.SCHEMA,
        output_data=OUTPUT_DATA,
        output_schema=OUTPUT_SCHEMA,
        limit=3,
    )
