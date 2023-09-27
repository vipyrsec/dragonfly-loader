FROM python:3.11-slim@sha256:c4992301d47a4f1d3e73c034494c080132f9a4090703babfcfa3317f7ba54461

RUN adduser --disabled-password loader
USER loader

# Define Git SHA build argument for sentry
ARG git_sha="development"
ENV GIT_SHA=$git_sha

WORKDIR /home/loader

COPY requirements.txt .
RUN python -m pip install --requirement requirements.txt

COPY --chown=loader:loader . .
RUN python -m pip install .

CMD ["python", "-m", "loader"]
