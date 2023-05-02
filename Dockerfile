#syntax=docker/dockerfile:1

FROM python:3.10 as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

WORKDIR /app
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ARG PYPROJECT_ROOT="."
COPY ${PYPROJECT_ROOT}/poetry.lock ${PYPROJECT_ROOT}/pyproject.toml ./
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN export PATH="/root/.local/bin:${PATH}" && poetry install --sync


FROM python:3.10 as runtime

# install google chrome
RUN  wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
# set display port to avoid crash
ENV DISPLAY=:99

WORKDIR /app

ARG COMPONENT
ARG ENVIRONMENT
ARG GCP_PROJECT_ID

ENV HOME=/app \
    PYTHONFAULTHANDLER=1 \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv \
    GCP_PROJECT_ID=${GCP_PROJECT_ID} \
    ENVIRONMENT=${ENVIRONMENT}

ENV PATH "$VIRTUAL_ENV/bin:$PATH"

COPY project/$COMPONENT project/$COMPONENT
COPY project/main.py project/main.py
COPY project/common project/common
COPY project/runtime project/runtime
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ENTRYPOINT ["/bin/bash", "-c", "python project/main.py"]
