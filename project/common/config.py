from pydantic.env_settings import BaseSettings
from pydantic.fields import Field


class Config(BaseSettings):
    """Components common config."""

    gcp_project_id: str = Field(..., description="GCP Project ID.")
    environment: str = Field(description="GCP Project ID.", default="development")
    language: str = Field(description="The language of the text.", default="it")
