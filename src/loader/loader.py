"""Main entrypoint for the loader."""

from httpx import Client
from letsbuilda.pypi import PyPIServices

from loader.constants import Dragonfly


def get_access_token(*, http_client: Client) -> str:
    """Get an access token from Auth0."""
    payload = {
        "client_id": Dragonfly.client_id.get_secret_value(),
        "client_secret": Dragonfly.client_secret.get_secret_value(),
        "username": Dragonfly.username.get_secret_value(),
        "password": Dragonfly.password.get_secret_value(),
        "audience": Dragonfly.audience,
        "grant_type": "password",
    }

    res = http_client.post(f"https://{Dragonfly.auth0_domain}/oauth/token", json=payload)
    res.raise_for_status()
    json = res.json()
    return json["access_token"]


def main() -> None:
    """Run the loader."""
    http_client = Client()
    pypi_client = PyPIServices(http_client)

    access_token = get_access_token(http_client=http_client)

    packages = pypi_client.get_rss_feed(PyPIServices.PACKAGE_UPDATES_FEED_URL)
    payload = [{"name": package.title, "version": package.version} for package in packages]
    headers = {"Authorization": "Bearer " + access_token}

    res = http_client.post(f"{Dragonfly.base_url}/batch/package", json=payload, headers=headers)
    res.raise_for_status()

    http_client.close()
