from project import runtime
from project.common import BigqueryManager, Publisher
from project.orchestrator.config import Config
from project.orchestrator.orchestrator import Orchestrator
from project.orchestrator.url_providers import (
    CoopURLProvider,
    LidlURLProvider,
    MigrosURLProvider,
)


def main():
    """Run entrypoint"""

    config = Config()
    runtime.setup(config.environment)

    with Orchestrator(
        publisher_worker=Publisher(config.gcp_project_id, config.topic_id),
        gcp_project_id=config.gcp_project_id,
        subscription=config.subscription_id,
        bigquery_manager=BigqueryManager(config.gcp_project_id),
        url_providers=(
            LidlURLProvider(config.language),
            MigrosURLProvider(config.language),
            CoopURLProvider(config.language),
        ),
    ) as orchestrator:
        orchestrator.run()


if __name__ == "__main__":
    main()
