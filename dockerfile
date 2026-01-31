FROM ghcr.io/astral-sh/uv:debian-slim


RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
    
COPY pyproject.toml uv.lock /app/
WORKDIR /app
RUN uv sync --locked
COPY . /app

CMD ["uv", "run", "python", "main.py"]