FROM python:3.13.3-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    UV_PROJECT_ENVIRONMENT=/usr/local

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

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" vscode
