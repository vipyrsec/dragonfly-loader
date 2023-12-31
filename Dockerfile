FROM python:3.11-slim@sha256:edaf703dce209d774af3ff768fc92b1e3b60261e7602126276f9ceb0e3a96874

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
