from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    amqp_host: str = "localhost"
    amqp_port: int = 5672


Settings = _Settings()  # pyright: ignore
