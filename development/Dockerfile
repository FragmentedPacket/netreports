ARG PYTHON_VER=3.10
FROM python:${PYTHON_VER}-bullseye AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"


# Configure poetry
RUN poetry config virtualenvs.create false \
    && poetry config installer.parallel false

# -------------------------------------------------------------------------------------
# Dependencies
# -------------------------------------------------------------------------------------
WORKDIR /tmp/install

# Copy in only pyproject.toml/poetry.lock to help with caching this layer if no updates to dependencies
COPY poetry.lock pyproject.toml /tmp/install/

# --no-root declares not to install the project package since we're wanting to
# take advantage of caching dependency installation
# and the project is copied in and installed after this step
RUN poetry install --no-interaction --no-ansi --no-root

# Copy in the rest of the source code and install local netreports plugin
WORKDIR /source
COPY . /source

RUN cp /tmp/install/* /source/
RUN poetry install --no-interaction --no-ansi

FROM python:${PYTHON_VER}-slim-bullseye
ARG PYTHON_VER

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /source

COPY --from=base /source /source
COPY --from=base /usr/local/lib/python${PYTHON_VER}/site-packages /usr/local/lib/python${PYTHON_VER}/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

ENTRYPOINT ["uvicorn", "netreports.main:app", "--host", "0.0.0.0", "--port", "8080"]
