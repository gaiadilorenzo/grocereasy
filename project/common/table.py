from google.cloud import bigquery

DATASET = "supermarket"
DESCRIPTION = "Table storing all supermarket items."
NAME = "items"
SCHEMA = [
    bigquery.SchemaField(
        name="name",
        field_type=bigquery.enums.SqlTypeNames.STRING,
        mode="REQUIRED",
        description="The name of the item.",
    ),
    bigquery.SchemaField(
        name="id",
        field_type=bigquery.enums.SqlTypeNames.STRING,
        mode="REQUIRED",
        description="The ID of the item.",
    ),
    bigquery.SchemaField(
        name="supermarket",
        field_type=bigquery.enums.SqlTypeNames.STRING,
        mode="REQUIRED",
        description="The supermarket of the item.",
    ),
    bigquery.SchemaField(
        name="product",
        field_type=bigquery.enums.SqlTypeNames.STRING,
        mode="REQUIRED",
        description="The category of the item.",
    ),
    bigquery.SchemaField(
        name="brand",
        field_type=bigquery.enums.SqlTypeNames.STRING,
        mode="REQUIRED",
        description="The brand of the item.",
    ),
    bigquery.SchemaField(
        name="price",
        field_type=bigquery.enums.SqlTypeNames.FLOAT64,
        mode="REQUIRED",
        description="The price of the item.",
    ),
    bigquery.SchemaField(
        name="quantity",
        field_type=bigquery.enums.SqlTypeNames.FLOAT64,
        mode="REQUIRED",
        description="The dimension of the item.",
    ),
    bigquery.SchemaField(
        name="timestamp",
        field_type=bigquery.enums.SqlTypeNames.TIMESTAMP,
        mode="REQUIRED",
        description="The timestamp of the insertion.",
    ),
    bigquery.SchemaField(
        name="link",
        field_type=bigquery.enums.SqlTypeNames.STRING,
        mode="NULLABLE",
        description="The link of the item.",
    ),
    bigquery.SchemaField(
        name="rank",
        field_type=bigquery.enums.SqlTypeNames.INT64,
        mode="NULLABLE",
        description="The rank of the item.",
    ),
    bigquery.SchemaField(
        name="offer",
        field_type=bigquery.enums.SqlTypeNames.STRING,
        mode="NULLABLE",
        description="The offer on the item.",
    ),
]
CLUSTERING_FIELDS = ("product",)

JOB_CONFIG = bigquery.LoadJobConfig(
    schema=SCHEMA,
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
)
