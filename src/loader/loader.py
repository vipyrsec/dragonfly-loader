"""Main entrypoint for the loader."""

from httpx import Client
from letsbuilda.pypi import PyPIServices

from loader.settings import Settings, get_settings


def get_access_token(*, http_client: Client, settings: Settings) -> str:
    """Get an access token from Auth0."""
    payload = {
        "client_id": settings.client_id,
        "client_secret": settings.client_secret,
        "username": settings.username,
        "password": settings.password,
        "audience": settings.audience,
        "grant_type": "password",
    }

    res = http_client.post(f"https://{settings.auth0_domain}/oauth/token", json=payload)
    res.raise_for_status()
    json = res.json()
    return json["access_token"]


def main() -> None:
    """Run the loader."""
    http_client = Client()
    pypi_client = PyPIServices(http_client)
    settings = get_settings()

    access_token = get_access_token(http_client=http_client, settings=settings)

    packages = pypi_client.get_rss_feed(PyPIServices.PACKAGE_UPDATES_FEED_URL)
    payload = [{"name": package.title, "version": package.version} for package in packages]
    headers = {"Authorization": "Bearer " + access_token}

    res = http_client.post(f"{settings.base_url}/batch/package", json=payload, headers=headers)
    res.raise_for_status()

    http_client.close()
