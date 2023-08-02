"""Main entrypoint for the loader."""

from letsbuilda.pypi import PyPIServices
from requests import Session
import pika
from loader.constants import Settings
from loader.models import Job

def main() -> None:
    """Run the loader."""
    http_session = Session()
    pypi_client = PyPIServices(http_session)

    rss_packages = pypi_client.get_rss_feed(PyPIServices.PACKAGE_UPDATES_FEED_URL)

    connection_parameters = pika.ConnectionParameters(host=Settings.amqp_host, port=Settings.amqp_port)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare("jobs")
    channel.exchange_declare("jobs")
    channel.queue_bind(queue="jobs", exchange="jobs")

    for rss_package in rss_packages:
        package = pypi_client.get_package_metadata(rss_package.title, rss_package.version)
        release = package.releases[0]
        distributions = release.distributions
        job = Job(
            name=package.title,
            version=release.version,
            distributions=[distribution.url for distribution in distributions],
        )
        body = job.model_dump_json()
        print(body)
        channel.basic_publish("jobs", routing_key="jobs", body=body)

    connection.close()

