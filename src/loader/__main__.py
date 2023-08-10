"""Entry point for the loader."""

from letsbuilda.pypi import PyPIServices
from httpx import Client

from .loader import main

if __name__ == "__main__":
    http_client = Client()
    pypi_client = PyPIServices(http_client=http_client)

    main(http_client=http_client, pypi_client=pypi_client)
