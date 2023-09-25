"""Stub test file."""

from dataclasses import dataclass
from unittest.mock import DEFAULT, MagicMock, Mock, patch

import pytest
from loader import loader


@dataclass
class MockPackage:
    """Mock package data."""

    title: str
    version: str


environment_variables = {
    "DRAGONFLY_API_URL": "https://example.com",
    "AUTH0_DOMAIN": "example-auth.com",
    "USERNAME": "test username",
    "PASSWORD": "test password",
    "CLIENT_ID": "test client id",
    "CLIENT_SECRET": "test client secret",
    "AUDIENCE": "test audience",
}


@pytest.fixture()
def mock_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock the environment variables."""
    for k, v in environment_variables.items():
        monkeypatch.setenv(k, v)


@pytest.fixture()
def mock_rss_data() -> list[MockPackage]:
    """Mock the RSS data."""
    return [
        MockPackage(title="a", version="1.0.0"),
        MockPackage(title="b", version="1.0.1"),
        MockPackage(title="c", version="1.0.2"),
    ]


def mock_http_session_post_side_effect(*args: list, **_kwargs: dict) -> Mock:
    """Mock the HTTP auth call."""
    if args[0] == "https://" + environment_variables["AUTH0_DOMAIN"] + "/oauth/token":
        mock = Mock()
        mock.json = Mock()
        mock.json.return_value = {
            "access_token": "test-access-token",
            "token_type": "Bearer",
            "expires_in": 86400,
        }

        return mock

    return DEFAULT


def test_loader(mock_env, mock_rss_data: list[MockPackage]) -> None:  # noqa: ANN001 - unclear
    """Test the loader."""
    mock_http_client = MagicMock()
    mock_http_client.post = MagicMock(side_effect=mock_http_session_post_side_effect)

    mock_pypi_client = MagicMock()
    mock_pypi_client.get_rss_feed = MagicMock(return_value=mock_rss_data)

    with patch.multiple(
        "loader.loader",
        Client=Mock(return_value=mock_http_client),
        PyPIServices=Mock(return_value=mock_pypi_client),
    ):
        loader.main()
        mock_http_client.post.assert_any_call(
            f"https://{environment_variables['AUTH0_DOMAIN']}/oauth/token",
            json={
                "client_id": environment_variables["CLIENT_ID"],
                "client_secret": environment_variables["CLIENT_SECRET"],
                "username": environment_variables["USERNAME"],
                "password": environment_variables["PASSWORD"],
                "audience": environment_variables["AUDIENCE"],
                "grant_type": "password",
            },
        )

        mock_http_client.post.assert_any_call(
            f"{environment_variables['DRAGONFLY_API_URL']}/batch/package",
            json=[{"name": p.title, "version": p.version} for p in mock_rss_data],
            headers={"Authorization": "Bearer test-access-token"},
        )
