from letsbuilda.pypi import PyPIServices
from requests import Session

from cronjob.settings import Settings, get_settings


def get_access_token(*, http_session: Session, settings: Settings) -> str:
    payload = dict(
        client_id=settings.client_id,
        client_secret=settings.client_secret,
        username=settings.username,
        password=settings.password,
        audience=settings.audience,
        grant_type="password",
    )

    res = http_session.post(f"https://{settings.auth0_domain}/oauth/token", json=payload)
    json = res.json()
    return json["access_token"]


def main() -> None:
    http_session = Session()
    pypi_client = PyPIServices(http_session)
    settings = get_settings()

    access_token = get_access_token(http_session=http_session, settings=settings)

    packages = pypi_client.get_rss_feed(PyPIServices.PACKAGE_UPDATES_FEED_URL)
    payload = [dict(name=package.title, version=package.version) for package in packages]
    headers = {"Authorization": "Bearer " + access_token}

    http_session.post(f"{settings.base_url}/batch/package", json=payload, headers=headers)

    http_session.close()
