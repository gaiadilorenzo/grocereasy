from google.cloud import bigquery

DATASET = "jobs"
DESCRIPTION = "Table storing all jobs computed."
NAME = "jobs"
SCHEMA = [
    bigquery.SchemaField(
        name="supermarket",
        field_type=bigquery.enums.SqlTypeNames.STRING,
        mode="REQUIRED",
        description="The name of the supermarket.",
    ),
    bigquery.SchemaField(
        name="url",
        field_type=bigquery.enums.SqlTypeNames.STRING,
        mode="REQUIRED",
        description="The ID of the item.",
    ),
    bigquery.SchemaField(
        name="timestamp",
        field_type=bigquery.enums.SqlTypeNames.TIMESTAMP,
        mode="REQUIRED",
        description="The timestamp of the insertion.",
    ),
    bigquery.SchemaField(
        name="last_executed",
        field_type=bigquery.enums.SqlTypeNames.TIMESTAMP,
        mode="NULLABLE",
        description="The timestamp of the last execution.",
    ),
]

JOB_CONFIG = bigquery.LoadJobConfig(
    schema=SCHEMA,
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
)
TIME_PARTITIONING = bigquery.TimePartitioning(type_=bigquery.TimePartitioningType.HOUR, field="timestamp")
