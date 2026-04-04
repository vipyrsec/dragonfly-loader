"""Main entrypoint for the loader."""

from httpx import Client
from letsbuilda.pypi import PyPIServices

from loader.constants import Settings


def build_access_headers() -> dict[str, str]:
    """Build Cloudflare Access service-token headers."""
    return {
        "CF-Access-Client-Id": Settings.cf_access_client_id,
        "CF-Access-Client-Secret": Settings.cf_access_client_secret,
    }


def fetch_packages(*, pypi_client: PyPIServices) -> list[tuple[str, str]]:
    """Return a list of name, version tuples in the updated packages RSS feed."""
    packages = pypi_client.get_rss_feed(PyPIServices.PACKAGE_UPDATES_FEED_URL)

    # All packages in the feed are guaranteed to have both a name and version
    return [(package.title, package.version) for package in packages if package.version is not None]


def load_packages(packages: list[tuple[str, str]], *, http_client: Client, headers: dict[str, str]) -> None:
    """Load all of the given packages into the Dragonfly API."""
    payload = [{"name": name, "version": version} for name, version in packages]

    res = http_client.post(f"{Settings.base_url}/batch/package", json=payload, headers=headers)
    res.raise_for_status()


def main(*, http_client: Client, pypi_client: PyPIServices) -> None:
    """Run the loader."""
    headers = {} if Settings.disable_auth else build_access_headers()

    packages = fetch_packages(pypi_client=pypi_client)

    load_packages(packages, http_client=http_client, headers=headers)
