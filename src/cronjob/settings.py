from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass
class Settings:
    base_url: str
    auth0_domain: str

    client_id: str
    client_secret: str

    username: str
    password: str

    audience: str

def get_settings() -> Settings:
    load_dotenv()

    BASE_URL = getenv("DRAGONFLY_API_URL", "https://dragonfly.vipyrsec.com")
    AUTH0_DOMAIN = getenv("AUTH0_DOMAIN", "vipyrsec.us.auth0.com")

    CLIENT_ID = getenv("CLIENT_ID")
    CLIENT_SECRET = getenv("CLIENT_SECRET")
    USERNAME = getenv("USERNAME")
    PASSWORD = getenv("PASSWORD")
    AUDIENCE = getenv("AUDIENCE", "https://dragonfly.vipyrsec.com")

    if not CLIENT_ID:
        raise Exception("`CLIENT_ID` is a required environment variable!")

    if not CLIENT_SECRET:
        raise Exception("`CLIENT_SECRET` is a required environment variable!")

    if not USERNAME:
        raise Exception("`USERNAME` is a required environment variable!")

    if not PASSWORD:
        raise Exception("`PASSWORD` is a required environment variable!")

    return Settings(
        base_url=BASE_URL,
        auth0_domain=AUTH0_DOMAIN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        username=USERNAME,
        password=PASSWORD,
        audience=AUDIENCE,
    )
