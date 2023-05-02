import dataclasses
import datetime

from project import runtime
from project.common import BigqueryManager, Publisher
from project.worker.config import Config
from project.worker.worker import Worker


def main():
    """Run entrypoint"""

    config = Config()
    runtime.setup(environment="dev")

    bigquery_manager = BigqueryManager(config.gcp_project_id)
    worker = Worker(
        gcp_project_id=config.gcp_project_id,
        subscription=config.subscription_id,
        publisher_storer=Publisher(config.gcp_project_id, config.topic_id),
        bigquery_manager=bigquery_manager,
    )
    worker.automatic_grocery()


if __name__ == "__main__":
    main()
