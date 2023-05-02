import logging

from project import runtime
from project.common import BigqueryManager, Publisher
from project.worker.config import Config
from project.worker.worker import Worker

_LOGGER = logging.getLogger(__name__)


def main():

    config = Config()
    runtime.setup(config.environment)

    with Worker(
        language=config.language,
        gcp_project_id=config.gcp_project_id,
        subscription=config.subscription_id,
        publisher_storer=Publisher(config.gcp_project_id, config.topic_id),
        bigquery_manager=BigqueryManager(config.gcp_project_id),
    ) as worker:
        worker.run()


if __name__ == "__main__":
    main()
