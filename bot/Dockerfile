FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir /dev_bot
WORKDIR /dev_bot

COPY pyproject.toml .

RUN --mount=type=cache,target=/root/.cache/uv uv sync --group bot

COPY /bot .


CMD [ "uv", "run", "main.py" ]
