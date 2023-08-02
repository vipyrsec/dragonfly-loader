"""Loader settings."""

from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    """Settings for the loader."""

    amqp_host: str = "localhost"
    amqp_port: int = 5672


Settings = _Settings()
