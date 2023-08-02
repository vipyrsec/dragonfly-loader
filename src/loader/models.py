"""Loader models."""

from pydantic import BaseModel


class Job(BaseModel):
    """Represents a job to be sent over the message queue."""

    name: str
    version: str
    distributions: list[str]
