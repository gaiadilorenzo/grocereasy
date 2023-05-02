import datetime
import os
import unittest.mock
from typing import Any, Callable, Iterable

from google.cloud import bigquery

from tests import constants


def patch_required_config(_func: Callable):
    def inner():
        with unittest.mock.patch.dict(os.environ, {"GCP_PROJECT_ID": constants.GCP_PROJECT_ID}):
            _func()

    return inner


_FIELD_TYPE = {
    str: "STRING",
    bytes: "BYTES",
    int: "INTEGER",
    float: "FLOAT",
    bool: "BOOLEAN",
    datetime.datetime: "DATETIME",
    datetime.date: "DATE",
    datetime.time: "TIME",
    dict: "RECORD",
}


def assert_query_execution(
    client: bigquery.Client,
    input_data: Iterable[dict],
    input_schema: Iterable[bigquery.SchemaField],
    output_data: Iterable[dict],
    output_schema: Iterable[bigquery.SchemaField],
    query: Callable[[], str],
    **kwargs,
) -> None:
    """Assert query output and schema."""

    actual = [
        row
        for row in client.query(query(_generate_query_inputs(input_data, input_schema), **kwargs))
        .result()
        .to_dataframe()
        .to_dict(orient="records")
    ]
    entry = next((entry for entry in actual), {})

    if entry:
        actual_schema = _map_dict_to_bq_schema(entry)
        assert output_schema == actual_schema
    print(output_data)
    print(actual)
    assert output_data == actual


def _map_dict_to_bq_schema(source_dict: dict[str, Any]) -> list[bigquery.SchemaField]:
    schema = []
    for key, value in source_dict.items():
        try:
            schema_field = bigquery.SchemaField(
                key, _FIELD_TYPE[type(value)], mode="REQUIRED" if value is not None else "NULLABLE"
            )  # REQUIRED BY DEFAULT
        except KeyError:
            schema_field = bigquery.SchemaField(key, _FIELD_TYPE[type(value[0])], mode="REPEATED")
        schema.append(schema_field)
        if schema_field.field_type == "RECORD":
            schema_field._fields = _map_dict_to_bq_schema(value)

    return schema


def _generate_query_inputs(data: Iterable[dict], schema: Iterable[bigquery.SchemaField]) -> str:
    inputs = []
    for entry in data:
        statement = """SELECT """

        fields = [
            f"""{("'" + str(entry[field.name]) + "'") if entry[field.name] is not None else "NULL"} AS {field.name}"""
            for field in schema
        ]

        clause = statement + ",".join(fields)
        inputs.append(clause)
    return "(" + (" UNION ALL ".join(inputs)) + ")"
