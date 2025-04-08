FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install netcat for database connection check
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

RUN mkdir /dev_backend
WORKDIR /dev_backend

COPY pyproject.toml .
COPY .env .

RUN --mount=type=cache,target=/root/.cache/uv uv sync --group backend

COPY /backend .

# Create a startup script
COPY backend/start.sh /dev_backend/start.sh
RUN chmod +x /dev_backend/start.sh

# Run the startup script instead of directly running the application
CMD ["/dev_backend/start.sh"]
