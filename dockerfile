FROM ghcr.io/astral-sh/uv:debian-slim
COPY pyproject.toml uv.lock /app/
WORKDIR /app
RUN uv sync --locked
COPY . /app
