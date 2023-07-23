from letsbuilda.pypi import PyPIServices
from requests import Session
from os import getenv
from dotenv import load_dotenv

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


def get_access_token(*, http_session: Session) -> str:
    payload = dict(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        username=USERNAME,
        password=PASSWORD,
        audience=AUDIENCE,
        grant_type="password",
    )

    with http_session.post(f"https://{AUTH0_DOMAIN}/oauth/token", json=payload) as res:
        json = res.json()
        return json["access_token"]


def main() -> None:
    http_session = Session()
    pypi_client = PyPIServices(http_session)

    access_token = get_access_token(http_session=http_session)

    packages = pypi_client.get_rss_feed(PyPIServices.PACKAGE_UPDATES_FEED_URL)
    payload = [dict(name=package.title, version=package.version) for package in packages]
    headers = {"Authorization": "Bearer " + access_token}

    http_session.post(f"{BASE_URL}/batch/package", json=payload, headers=headers)

    http_session.close()
