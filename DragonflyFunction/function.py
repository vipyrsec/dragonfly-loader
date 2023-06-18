from letsbuilda.pypi import PyPIServices
import aiohttp
from typing import Final
from os import getenv

BASE_URL: Final[str] = "https://dragonfly.vipyrsec.com"
AUTH0_URL: Final[str] = "https://vipyrsec.us.auth0.com"

CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")
USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")


async def get_access_token(*, http_session: aiohttp.ClientSession) -> str:
    payload = dict(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        username=USERNAME,
        password=PASSWORD,
    )

    async with http_session.post(f"{AUTH0_URL}/oauth/token", json=payload) as res:
        json = await res.json()
        return json["access_token"]

async def main(timer) -> None:
    http_session = aiohttp.ClientSession()
    pypi_client = PyPIServices(http_session=http_session)

    access_token = await get_access_token(http_session=http_session)

    packages = await pypi_client.get_rss_feed(PyPIServices.PACKAGE_UPDATES_FEED_URL)
    payload = [dict(name=package.title, version=package.version) for package in packages]
    headers = { "Authorization": "Bearer " + access_token }

    await http_session.post(f"{BASE_URL}/batch/package", json=payload, headers=headers)

    await http_session.close()