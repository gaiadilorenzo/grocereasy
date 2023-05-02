import datetime
import logging
from collections import defaultdict
from typing import Callable

from ortools.linear_solver import pywraplp
from tabulate import tabulate

from project.common import (
    BigqueryManager,
    Consumer,
    Item,
    Job,
    Product,
    Publisher,
    StorerMessage,
    Supermarket,
    WorkerMessage,
    log,
    serializer,
    table,
)
from project.worker.scrapers.builder import get_scraper

_LOGGER = logging.getLogger(__name__)


class Worker(Consumer):
    """
    A worker.

    Receives jobs from the orchestrator and executes them.
    """

    def __init__(
        self,
        language: str,
        gcp_project_id: str,
        subscription: str,
        bigquery_manager: BigqueryManager,
        publisher_storer: Publisher | None = None,
        *,
        _datetime_generator: Callable[[], datetime.date] = datetime.datetime.now,
    ):
        super().__init__(gcp_project_id, subscription, publisher_storer)
        self._bigquery_manager = bigquery_manager
        self._datetime_generator = _datetime_generator
        self._language = language

    def run_task(self, message: serializer.T) -> None:
        """Get items callback."""

        if self._publisher is None:
            raise ValueError("❌ Publisher is not set. The callback can only be used via PubSub.")

        worker_message = serializer.deserialize(message.data, WorkerMessage)  # type: ignore[attr-defined]
        items = self.get_items(jobs=worker_message.jobs)
        self._publisher.publish(StorerMessage(items=items, date=worker_message.date))

    @log(message="Fetching items.", emoji="🛒")
    def get_items(self, jobs: list[Job]) -> list[Item]:
        """Get items."""

        supermarket_urls: dict[Supermarket, list[str]] = defaultdict(list)
        for job in jobs:
            supermarket_urls[job.supermarket].append(job.url)
        items = [
            item
            for supermarket in supermarket_urls.keys()
            for item in get_scraper(supermarket, self._language).get_items(supermarket_urls[supermarket])
        ]
        return items  # type: ignore[union-attr]

    def products(self, categories: list[str]) -> str:
        # TODO: fix query with search in similarity
        return f"""
        SELECT name, id, supermarket, link, product, brand, cost, price, quantity, timestamp, offer, popularity
        FROM (
            SELECT name, id, supermarket, link, product, brand, SAFE_DIVIDE(price, quantity) as cost, price, quantity, timestamp, offer
            FROM `{self._gcp_project}.{table.DATASET}.{table.NAME}`
            WHERE product in UNNEST({categories}))
            AS prod INNER JOIN (
                SELECT brand, product, PERCENTILE_CONT(rank, 0.5) OVER(PARTITION BY brand, product) as popularity
                FROM `{self._gcp_project}.{table.DATASET}.{table.NAME}`
                order by product, popularity
                ) AS pop USING (brand, product)
                INNER JOIN (SELECT  name, id, supermarket, link, product, brand, quantity, MAX(timestamp) as timestamp
                            FROM `{self._gcp_project}.{table.DATASET}.{table.NAME}`
                            GROUP BY name, id, supermarket, link, product, brand, quantity)
                            AS last
                            USING (name, id, supermarket, link, product, brand, quantity, timestamp)
        """

    @log(message="Doing grocery.", emoji="🛒")
    def automatic_grocery(
        self, categories: list[str] = Product.values, weight_cost: float = 0.5, n_choices: int = 1
    ) -> None:
        """Get items."""

        _LOGGER.debug("🛒 Fetching items.")
        products = self._bigquery_manager.query_table(self.products(categories=categories), job_id_prefix="products")
        pruducts_table = [
            {
                "name": row.name,
                "id": row.id,
                "supermarket": row.supermarket,
                "product": row.product,
                "cost": row.cost,
                "price": row.price,
                "quantity": row.quantity,
                "offer": row.offer,
                "link": row.link,
                "popularity": row.popularity,
            }
            for row in products
        ]

        _LOGGER.debug("🛒 Optimize grocery.")
        solver = pywraplp.Solver.CreateSolver("GLOP")

        x = {}
        for product in pruducts_table:
            x[product["link"]] = solver.BoolVar(f'x_{product["link"]}')

        objective = solver.Objective()
        for product in pruducts_table:
            objective.SetCoefficient(
                x[product["link"]], (1 - weight_cost) * product["popularity"] + weight_cost * product["cost"]
            )
        objective.SetMinimization()

        category_constraints = {}
        for product in pruducts_table:
            category = product["product"]
            if category not in category_constraints:
                category_constraints[category] = solver.Constraint(n_choices, n_choices)
            category_constraints[category].SetCoefficient(x[product["link"]], 1)

        status = solver.Solve()
        selected_products: list[dict] = []
        cost = 0
        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            for product in pruducts_table:
                if x[product["link"]].solution_value() > 0 and product["link"] not in [
                    prod["link"] for prod in selected_products
                ]:
                    selected_products.append(product)
                    cost += product["price"]
        else:
            _LOGGER.error("The problem does not have an optimal solution.")

        _LOGGER.info(f"💸 Cost {cost} CHF.")
        print(tabulate(selected_products, headers="keys"))
