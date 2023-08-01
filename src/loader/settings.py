"""Settings for the Dragonfly Loader."""

from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass
class Settings:
    """Settings for the Dragonfly Loader."""

    base_url: str
    auth0_domain: str

    client_id: str
    client_secret: str

    username: str
    password: str

    audience: str


def get_settings() -> Settings:
    """Get the settings for the Dragonfly Loader."""
    load_dotenv()

    base_url = getenv("DRAGONFLY_API_URL", "https://dragonfly.vipyrsec.com")
    auth0_domain = getenv("AUTH0_DOMAIN", "vipyrsec.us.auth0.com")

    client_id = getenv("CLIENT_ID")
    client_secret = getenv("CLIENT_SECRET")
    username = getenv("USERNAME")
    password = getenv("PASSWORD")
    audience = getenv("AUDIENCE", "https://dragonfly.vipyrsec.com")

    if not client_id:
        msg = "`CLIENT_ID` is a required environment variable!"
        raise Exception(msg)  # noqa: TRY002 - TODO @Robin5605: Use a custom exception
        # https://github.com/vipyrsec/dragonfly-loader/issues/10

    if not client_secret:
        msg = "`CLIENT_SECRET` is a required environment variable!"
        raise Exception(msg)  # noqa: TRY002 - TODO @Robin5605: Use a custom exception
        # https://github.com/vipyrsec/dragonfly-loader/issues/10

    if not username:
        msg = "`USERNAME` is a required environment variable!"
        raise Exception(msg)  # noqa: TRY002 - TODO @Robin5605: Use a custom exception
        # https://github.com/vipyrsec/dragonfly-loader/issues/10

    if not password:
        msg = "`PASSWORD` is a required environment variable!"
        raise Exception(msg)  # noqa: TRY002 - TODO @Robin5605: Use a custom exception
        # https://github.com/vipyrsec/dragonfly-loader/issues/10

    return Settings(
        base_url=base_url,
        auth0_domain=auth0_domain,
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        audience=audience,
    )
