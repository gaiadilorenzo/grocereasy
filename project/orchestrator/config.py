from pydantic.fields import Field

from project import common


class Config(common.Config):
    """Worker specific configs."""

    topic_id: str = Field(description="The worker topic ID.", default="orchestrator_completed")
    subscription_id: str = Field(description="The orchestrator subscription ID.", default="triggers")
