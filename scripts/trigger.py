import datetime

from pydantic.env_settings import BaseSettings
from pydantic.fields import Field

from project.common import OrchestratorMessage, Publisher


class Config(BaseSettings):
    """Trigger config."""

    gcp_project_id: str = Field(..., description="GCP Project ID.")
    topic_id: str = Field(..., description="The trigger topic ID.")


def main() -> None:

    config = Config()
    Publisher(config.gcp_project_id, config.topic_id).publish(OrchestratorMessage(date=datetime.date.today()))


if __name__ == "__main__":
    main()
