from project import runtime
from project.common import BigqueryManager, table
from project.storer.config import Config
from project.storer.storer import Storer


def main():
    """Run entrypoint."""

    config = Config()
    runtime.setup(config.environment)

    bigquery_manager = BigqueryManager(config.gcp_project_id)

    bigquery_manager.create_table(
        dataset_id=table.DATASET,
        table_id=table.NAME,
        clustering_fields=table.CLUSTERING_FIELDS,
        schema=table.SCHEMA,
        description=table.DESCRIPTION,
    )

    with Storer(
        gcp_project_id=config.gcp_project_id,
        subscription=config.subscription_id,
        bigquery_manager=bigquery_manager,
    ) as storer:
        storer.run()


if __name__ == "__main__":
    main()
