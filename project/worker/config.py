from pydantic.fields import Field

from project import common


class Config(common.Config):
    """Worker specific configs."""

    topic_id: str = Field(description="The storer topic ID.", default="worker_completed")
    subscription_id: str = Field(description="The worker subscription ID.", default="orchestrator_completed")
