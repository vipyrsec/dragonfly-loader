FROM python:3.12-slim@sha256:babc0d450bf9ed2b369814bc2f466e53a6ea43f1201f6df4e7988751f755c52c

# Define Git SHA build argument for Sentry
ARG git_sha="development"
ENV GIT_SHA=$git_sha

COPY requirements/requirements.txt .
RUN python -m pip install --requirement requirements.txt

COPY pyproject.toml pyproject.toml
COPY src/ src/
RUN python -m pip install .

RUN adduser --disabled-password loader
USER loader

CMD [ "python", "-m", "loader" ]
