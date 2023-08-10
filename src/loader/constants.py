"""Loader settings."""

from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    """Settings for the Dragonfly Loader."""

    base_url: str = "https://dragonfly.vipyrsec.com"
    auth0_domain: str = "vipyrsec.us.auth0.com"

    client_id: str = ""
    client_secret: str = ""

    username: str = ""
    password: str = ""

    audience: str = "https://dragonfly.vipyrsec.com"


Settings = _Settings()
