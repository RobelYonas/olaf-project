# Stage 1: Build virtual environment with uv
FROM ghcr.io/astral-sh/uv:latest AS uv-bin
FROM python:3.14-slim-bookworm AS builder

WORKDIR /build

COPY --from=uv-bin /uv /uvx /bin/

# Isolate the virtualenv location outside the app source tree
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT="/opt/venv"

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Stage 2: Ephemeral runtime image
FROM python:3.14-slim-bookworm AS runtime

WORKDIR /app

RUN apt-get update && apt-get upgrade -y --no-install-recommends \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Copy isolated virtual environment into /opt/venv
COPY --from=builder /opt/venv /opt/venv

# Configure system PATH to prioritize the isolated venv
ENV VIRTUAL_ENV="/opt/venv" \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Copy project code into /app
COPY . .

ENTRYPOINT ["python", "tick_runner.py"]
CMD ["--spec-id", "SPEC-001"]
