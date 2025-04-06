FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir /dev_backend
WORKDIR /dev_backend

COPY pyproject.toml .

RUN --mount=type=cache,target=/root/.cache/uv uv sync --group backend

COPY /app .

# Run the application.
CMD ["/dev_backend/.venv/bin/fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]