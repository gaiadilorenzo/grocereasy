from typing import TypeVar

from project.orchestrator.url_providers.base import URLProvider

S = TypeVar("S", bound=URLProvider)
