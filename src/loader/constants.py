"""Loader settings."""

from os import getenv

from pydantic_settings import BaseSettings

GIT_SHA = getenv("GIT_SHA", "development")


class _Settings(BaseSettings):
    """Settings for the Dragonfly Loader."""

    base_url: str = "https://dragonfly.vipyrsec.com"
    cf_access_client_id: str = ""
    cf_access_client_secret: str = ""
    disable_auth: bool = False


Settings = _Settings()
