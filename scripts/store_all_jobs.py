import dataclasses
import datetime

from project import runtime
from project.common import BigqueryManager, Config, Job, Supermarket
from project.orchestrator import table
from project.orchestrator.url_providers import (
    CoopURLProvider,
    LidlURLProvider,
    MigrosURLProvider,
)


def main():
    """Run entrypoint"""

    config = Config()
    runtime.setup(environment="dev")

    bigquery_manager = BigqueryManager(config.gcp_project_id)
    url_providers = (LidlURLProvider(), MigrosURLProvider(), CoopURLProvider())

    jobs = [
        Job(url=url, supermarket=Supermarket(url_provider.get_supermarket()))
        for url_provider in url_providers
        for url in url_provider.get_urls()
    ]

    bigquery_manager.store(
        dataset_id=table.DATASET,
        table_id=table.NAME,
        job_config=table.JOB_CONFIG,
        rows=[
            {**dataclasses.asdict(job), "timestamp": datetime.datetime.utcnow(), "last_executed": None} for job in jobs
        ],
    )


if __name__ == "__main__":
    main()
