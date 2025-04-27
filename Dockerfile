FROM python:3.13.3-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    UV_PROJECT_ENVIRONMENT=/usr/local \
    PYTHONPATH=/app

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    gcc \
    git \
    vim \
    curl \
    sqlite3 \
    build-essential \
    python3-dev && \
    apt-get clean

COPY --from=ghcr.io/astral-sh/uv:0.6.17 /uv /uvx /bin/

WORKDIR /app

COPY . .

RUN uv sync && mkdir -p data
