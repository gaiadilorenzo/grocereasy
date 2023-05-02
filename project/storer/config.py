from pydantic.fields import Field

from project import common


class Config(common.Config):
    """Storer specific configs."""

    subscription_id: str = Field(description="The storer subscription ID.", default="worker_completed")
