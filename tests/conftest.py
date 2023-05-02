import datetime
from unittest.mock import MagicMock

import pytest
from google.cloud import bigquery

from project.common import Publisher
from project.orchestrator.orchestrator import Orchestrator
from project.storer.storer import Storer
from project.worker.worker import Worker
from tests import constants
from tests.constants import DATE


@pytest.fixture
def client() -> bigquery.Client:
    return bigquery.Client(project=constants.GCP_PROJECT_ID_BIGQUERY)


@pytest.fixture
def publisher() -> Publisher:
    return Publisher(project_id=constants.GCP_PROJECT_ID, topic_id=constants.TOPIC_ID)


@pytest.fixture
def the_orchestrator(publisher: Publisher) -> Orchestrator:
    return Orchestrator(
        publisher_worker=publisher,
        gcp_project_id=constants.GCP_PROJECT_ID,
        subscription=constants.SUBSCRIPTION_ID,
        url_providers=(),
        bigquery_manager=MagicMock(),
        _datetime_generator=get_today,
    )


@pytest.fixture
def the_worker(publisher: Publisher) -> Worker:
    return Worker(
        publisher_storer=publisher,
        gcp_project_id=constants.GCP_PROJECT_ID,
        subscription=constants.SUBSCRIPTION_ID,
    )


@pytest.fixture
def the_storer(publisher: Publisher) -> Storer:
    return Storer(
        bigquery_manager=MagicMock(),
        gcp_project_id=constants.GCP_PROJECT_ID,
        subscription=constants.SUBSCRIPTION_ID,
    )


def get_today() -> datetime.date:
    return DATE.date()
