import argparse
import logging
import time

from project import common, runtime
from project.common import BigqueryManager, Publisher
from project.orchestrator.config import Config
from project.orchestrator.orchestrator import Orchestrator
from project.orchestrator.url_providers import (
    CoopURLProvider,
    LidlURLProvider,
    MigrosURLProvider,
)
from project.storer.storer import Storer, table
from project.worker.worker import Worker

_LOGGER = logging.getLogger(__name__)


def main(products: list[str], weight_cost: float, language: str, choices: int):
    """Run entrypoint"""

    config = Config(language=language)
    runtime.setup(config.environment)

    bigquery_manager = BigqueryManager(config.gcp_project_id)

    orchestrator = Orchestrator(
        publisher_worker=Publisher(config.gcp_project_id, config.topic_id),
        gcp_project_id=config.gcp_project_id,
        subscription=config.subscription_id,
        bigquery_manager=bigquery_manager,
        url_providers=(
            LidlURLProvider(config.language),
            MigrosURLProvider(config.language),
            CoopURLProvider(config.language),
        ),
    )

    worker = Worker(
        gcp_project_id=config.gcp_project_id,
        subscription=config.subscription_id,
        publisher_storer=Publisher(config.gcp_project_id, config.topic_id),
        bigquery_manager=bigquery_manager,
        language=config.language,
    )

    bigquery_manager.create_table(
        dataset_id=table.DATASET,
        table_id=table.NAME,
        clustering_fields=table.CLUSTERING_FIELDS,
        schema=table.SCHEMA,
        description=table.DESCRIPTION,
    )

    storer = Storer(
        gcp_project_id=config.gcp_project_id,
        subscription=config.subscription_id,
        bigquery_manager=bigquery_manager,
    )

    jobs = orchestrator.store_new_jobs(products=products)
    while True:
        jobs = orchestrator.get_n_jobs(jobs)
        if len(jobs) == 0:
            break
        items = worker.get_items(jobs)
        storer.store_items(items)
        orchestrator.store_jobs(jobs)
        time.sleep(1 * common.constants.Time.MINUTE)

    worker.automatic_grocery(products, weight_cost, choices)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Automate grocery.")
    parser.add_argument("-p", "--products", nargs="+", help="Categories", required=True)
    parser.add_argument(
        "-w",
        "--weight",
        help="The weight of the cost with respect to quality in the decision (Default to 0.7 cost - 0.3 quality)",
        required=False,
        default=0.7,
    )
    parser.add_argument(
        "-l",
        "--language",
        help="The language of the text (Default to it)",
        required=False,
        choices=("it", "de", "fr"),
        default="it",
    )
    parser.add_argument(
        "-n",
        "--choices",
        help="The number of choices to show (Default to 1)",
        required=False,
        default=1,
    )
    args = parser.parse_args()
    main(args.products, args.weight, args.language, int(args.choices))
