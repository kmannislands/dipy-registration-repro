FROM python:3.7.6 as base_image

ARG PIPX_VERSION=0.15.4.0
ARG POETRY_VERSION=1.0.8

WORKDIR /home/dipy-repro

ENV PATH=$PATH:/root/.local/bin

# Install poetry
RUN python -m pip install --user pipx==0.15.4.0 && \
    pipx install poetry==1.0.8

# Copy in project poetry info
COPY ./pyproject.toml ./poetry.lock ./

RUN poetry install

FROM base_image as source_code

COPY ./repro ./repro

FROM source_code as test

CMD poetry run pytest

