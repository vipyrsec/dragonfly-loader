"""Stub test file."""

from dataclasses import dataclass
from unittest.mock import Mock

import pytest

from loader import loader
from loader.constants import Settings


@dataclass
class MockPackage:
    """Mock package data."""

    title: str
    version: str


ENV = {
    "BASE_URL": "https://example.com",
    "CF_ACCESS_CLIENT_ID": "test client id",
    "CF_ACCESS_CLIENT_SECRET": "test client secret",
    "DISABLE_AUTH": False,
}


@pytest.fixture(autouse=True)
def mock_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock the environment variables."""
    for k, v in ENV.items():
        monkeypatch.setattr(Settings, k.lower(), v)


def test_build_access_headers() -> None:
    """Test that building Cloudflare Access headers works properly."""
    expected_payload = {
        "CF-Access-Client-Id": ENV["CF_ACCESS_CLIENT_ID"],
        "CF-Access-Client-Secret": ENV["CF_ACCESS_CLIENT_SECRET"],
    }

    assert loader.build_access_headers() == expected_payload


def test_fetch_packages() -> None:
    """Test that getting packages from the RSS feed works properly."""
    mock_packages = [
        MockPackage(title="a", version="1.0.0"),
        MockPackage(title="b", version="1.0.1"),
    ]
    mock_pypi_client = Mock()
    mock_pypi_client.get_rss_feed.return_value = mock_packages

    actual = loader.fetch_packages(pypi_client=mock_pypi_client)
    expected = [("a", "1.0.0"), ("b", "1.0.1")]

    assert actual == expected


def test_load_packages() -> None:
    """Test that loading packages into the Dragonfly API works properly."""
    mock_client = Mock()
    mock_client.post = Mock()
    mock_packages = [
        ("a", "1.0.0"),
        ("b", "1.0.1"),
    ]

    headers: dict[str, str] = {
        "CF-Access-Client-Id": str(ENV["CF_ACCESS_CLIENT_ID"]),
        "CF-Access-Client-Secret": str(ENV["CF_ACCESS_CLIENT_SECRET"]),
    }
    loader.load_packages(mock_packages, http_client=mock_client, headers=headers)

    expected_payload = [{"name": name, "version": version} for name, version in mock_packages]
    mock_client.post.assert_called_once_with(
        f"{ENV['BASE_URL']}/batch/package",
        json=expected_payload,
        headers=headers,
    )


def test_main(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that everything works together."""
    mock_packages = [
        ("a", "1.0.0"),
        ("b", "1.0.1"),
    ]

    mock_http_client = Mock()
    mock_pypi_client = Mock()

    fetch_packages_mock = Mock(return_value=mock_packages)
    build_access_headers_mock = Mock(
        return_value={
            "CF-Access-Client-Id": "abc",
            "CF-Access-Client-Secret": "def",
        },
    )
    load_packages_mock = Mock()
    monkeypatch.setattr("loader.loader.fetch_packages", fetch_packages_mock)
    monkeypatch.setattr("loader.loader.build_access_headers", build_access_headers_mock)
    monkeypatch.setattr("loader.loader.load_packages", load_packages_mock)

    loader.main(http_client=mock_http_client, pypi_client=mock_pypi_client)
    build_access_headers_mock.assert_called_once_with()
    fetch_packages_mock.assert_any_call(pypi_client=mock_pypi_client)
    load_packages_mock.assert_any_call(
        mock_packages,
        http_client=mock_http_client,
        headers={
            "CF-Access-Client-Id": "abc",
            "CF-Access-Client-Secret": "def",
        },
    )


def test_main_disable_auth(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that auth bypass requires explicit configuration."""
    mock_packages = [
        ("a", "1.0.0"),
        ("b", "1.0.1"),
    ]

    mock_http_client = Mock()
    mock_pypi_client = Mock()

    fetch_packages_mock = Mock(return_value=mock_packages)
    build_access_headers_mock = Mock(return_value={"should": "not be used"})
    load_packages_mock = Mock()
    monkeypatch.setattr(Settings, "disable_auth", True)
    monkeypatch.setattr("loader.loader.fetch_packages", fetch_packages_mock)
    monkeypatch.setattr("loader.loader.build_access_headers", build_access_headers_mock)
    monkeypatch.setattr("loader.loader.load_packages", load_packages_mock)

    loader.main(http_client=mock_http_client, pypi_client=mock_pypi_client)

    build_access_headers_mock.assert_not_called()
    load_packages_mock.assert_any_call(mock_packages, http_client=mock_http_client, headers={})
