# Multi-stage Dockerfile for Ray-Trace

# Stage 1: base
FROM python:3.11-slim AS base
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

# Stage 2: deps - Install Poetry and project dependencies
FROM base AS deps
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip install poetry==1.8.3
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root --without dev

# Stage 3: playwright-install - Install Playwright browsers
FROM deps AS playwright-install
RUN poetry run playwright install chromium
RUN poetry run playwright install-deps chromium

# Stage 4: test (final) - Full test environment
FROM playwright-install AS test
COPY . .
RUN poetry install --no-root
ENV PYTHONPATH=/app
ENTRYPOINT ["poetry", "run", "pytest"]
CMD ["-m", "smoke", "--tb=short", "-v"]
