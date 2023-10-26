FROM python:3.12-slim@sha256:babc0d450bf9ed2b369814bc2f466e53a6ea43f1201f6df4e7988751f755c52c

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
