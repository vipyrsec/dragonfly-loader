"""Entry point for the loader."""

import logging

from httpx import Client, HTTPError, Request, Response
from letsbuilda.pypi import PyPIServices
from logging_config import configure_logger

from .loader import main

configure_logger()
logger = logging.getLogger(__name__)


def log_request(request: Request) -> None:
    """Log outgoing requests."""
    logger.debug("%s %s - Waiting for response", request.method, request.url)


def log_response(response: Response) -> None:
    """Log request responses."""
    request = response.request
    logger.debug("%s %s - Status %s", request.method, request.url, response.status_code)

    try:
        response.raise_for_status()
    except HTTPError:
        logger.exception("Response had a non 2xx status code")


if __name__ == "__main__":
    http_client = Client(event_hooks={"request": [log_request], "response": [log_response]})
    pypi_client = PyPIServices(http_client=http_client)

    main(http_client=http_client, pypi_client=pypi_client)
