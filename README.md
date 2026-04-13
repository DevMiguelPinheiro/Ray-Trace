# Ray-Trace

A production-grade Python/Playwright test automation framework demonstrating enterprise patterns and portfolio-quality test infrastructure.

## Languages

- English: this file
- Portuguese (Brazil): [README.pt-BR.md](README.pt-BR.md)

## Overview

**Ray-Trace** is an advanced test automation framework for the [SauceDemo](https://www.saucedemo.com) application, showcasing:

- **Enterprise Patterns**: Page Object Model with component hierarchy
- **Performance Optimization**: Cached authentication via `storage_state`
- **Observability**: Three-tier evidence collection (screenshots, videos, Playwright traces)
- **Network Resilience**: API mocking with preset failure scenarios
- **Visual Quality Gates**: Pixel-accurate regression detection
- **CI/CD Integration**: Multi-stage Docker builds, GitHub Actions matrix testing
- **Real-world Concerns**: Flakiness handling, environment parity, report publishing

## Tech Stack

- **Testing**: Playwright, pytest, pytest-xdist
- **Language**: Python 3.11+
- **Dependency Management**: Poetry
- **Code Quality**: Black, Ruff, mypy
- **Reporting**: Allure, pytest-html
- **Infrastructure**: Docker, GitHub Actions

## Quick Start

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url> && cd ray-trace
   ```

2. **Install Poetry:**
   ```bash
   pipx install poetry
   ```

3. **Install dependencies:**
   ```bash
   poetry install
   ```

4. **Install Playwright browsers:**
   ```bash
   poetry run playwright install chromium
   ```

5. **Configure environment:**
   ```bash
   cp .env.example .env
   ```

6. **Verify setup:**
   ```bash
   poetry run pytest --collect-only -m smoke
   ```

### Running Tests

**Smoke tests (quick validation):**
```bash
poetry run pytest -m smoke -v
```

**Regression tests (full suite):**
```bash
poetry run pytest -m regression -v
```

**Visual regression tests:**
```bash
poetry run pytest -m visual -v
```

**Network/API failure tests:**
```bash
poetry run pytest -m network -v
```

**Generate visual baselines (first run):**
```bash
UPDATE_SNAPSHOTS=true poetry run pytest -m visual -v
```

**Run specific test file:**
```bash
poetry run pytest tests/e2e/test_auth.py -v
```

**Run with headed browser (debug mode):**
```bash
HEADLESS=false SLOW_MO_MS=500 poetry run pytest -m smoke -k "test_login"
```

**Run in parallel:**
```bash
poetry run pytest -m regression -n 4 -v
```

### Docker Execution

**Build Docker image:**
```bash
docker build -t ray-trace:latest .
```

**Run tests in container:**
```bash
docker run --rm \
  -v $(pwd)/test-results:/app/test-results \
  -v $(pwd)/allure-results:/app/allure-results \
  ray-trace:latest \
  -m smoke --alluredir=allure-results
```

**Using docker-compose:**
```bash
docker-compose up
```

### Report Generation

**Generate Allure report:**
```bash
poetry run pytest -m regression --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
```

**View Playwright trace:**
```bash
poetry run playwright show-trace test-results/{test-name}/trace.zip
```

## Project Structure

```
ray-trace/
├── config/           # Configuration & test data
│   ├── settings.py   # Pydantic settings
│   └── environments.py # Credentials & product data
├── pages/            # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   ├── checkout_*.py
│   └── components/   # Reusable components
├── fixtures/         # Test fixtures
│   ├── auth.py       # Storage state management
│   ├── browsers.py   # Browser/context setup
│   └── pages.py      # POM fixtures
├── utils/            # Utility classes
│   ├── network_interceptor.py
│   ├── screenshot_comparator.py
│   ├── retry_helper.py
│   └── allure_helpers.py
├── tests/            # Test suites
│   ├── e2e/          # End-to-end tests
│   ├── network/      # Network failure tests
│   └── visual/       # Visual regression tests
├── assets/           # Test data & baselines
│   ├── snapshots/    # Visual regression baselines
│   └── test-data/    # JSON/CSV test data
└── .github/          # GitHub Actions workflows
```

## Test Markers

- `@pytest.mark.smoke` - Quick validation suite
- `@pytest.mark.regression` - Full regression suite
- `@pytest.mark.visual` - Visual regression tests
- `@pytest.mark.network` - Network failure scenarios
- `@pytest.mark.critical` - Critical business logic
- `@pytest.mark.slow` - Long-running tests

## Configuration

Create `.env` from `.env.example`:

```dotenv
APP_ENV=staging
HEADLESS=true
SLOW_MO_MS=0
SNAPSHOT_THRESHOLD=0.02
UPDATE_SNAPSHOTS=false
```

## Authentication

Tests use pre-cached authentication via Playwright's `storage_state`. The first test run creates `.auth/staging_standard_user.json`. Subsequent runs use this cached state for faster test execution.

## Code Quality

**Format code with Black:**
```bash
poetry run black .
```

**Lint with Ruff:**
```bash
poetry run ruff check . --fix
```

**Type check with mypy:**
```bash
poetry run mypy pages/ utils/ config/
```

## CI/CD Pipeline

GitHub Actions runs a multi-job pipeline:

1. **Lint & Type Check** - Code quality gates
2. **Smoke Tests** - Quick validation
3. **Regression Tests** (matrix) - Chromium, Firefox, WebKit
4. **Visual Tests** - Screenshot comparisons
5. **Report Publishing** - Allure reports to GitHub Pages

## Key Features

### Page Object Model
- `BasePage` provides shared utilities
- Each page encapsulates interactions
- Components for reusable UI elements

### Auth Caching
- Session-scoped `storage_state` fixture
- Eliminates per-test login overhead
- Enables fast test execution

### Network Resilience
- `NetworkInterceptor` for API failure injection
- Pre-built presets (500, 401, timeout)
- Async context manager for clean restoration

### Visual Regression
- `ScreenshotComparator` for pixel-level diffs
- Configurable tolerance thresholds
- Diff images saved on failure

### Observability
- Screenshots on failure
- Video recording on retry
- Playwright traces (chromium only)
- Allure report integration

## Best Practices

1. **Avoid Hardcoded Data** - Use `config/environments.py`
2. **Locator Priority** - `get_by_role` → `get_by_text` → CSS selectors
3. **Wait Strategies** - Prefer `wait_for_load_state()` over arbitrary `sleep()`
4. **Test Isolation** - Don't rely on test execution order
5. **Meaningful Assertions** - Assert on user-visible outcomes

## Troubleshooting

**Flaky Tests:**
- Increase timeout: `--timeout=10`
- Add explicit waits: `wait_for_element_visible()`
- Use `@retry` decorator for action-level retries

**Visual Test Failures:**
- Update baselines: `UPDATE_SNAPSHOTS=true pytest -m visual`
- Review diff images in `test-results/`
- Adjust threshold: `SNAPSHOT_THRESHOLD=0.05`

**Docker Issues:**
- Rebuild image: `docker build --no-cache -t ray-trace .`
- Check browser installation: `docker run ray-trace playwright --version`

## License

MIT

## Author

DevMiguelPinheiro
