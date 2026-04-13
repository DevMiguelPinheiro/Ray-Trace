"""Root conftest: Bootstrap environment, load settings, and create runtime directories."""

from pathlib import Path

import pytest
from dotenv import load_dotenv

from config.settings import Settings

# Load .env before any imports that need settings
load_dotenv()


def pytest_configure(config):
    """Create runtime directories before tests run."""
    runtime_dirs = [
        Path(".auth"),
        Path("test-results"),
        Path("allure-results"),
        Path("assets/snapshots"),
        Path("assets/test-data"),
    ]
    for dir_path in runtime_dirs:
        dir_path.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Session-scoped settings fixture."""
    return Settings()
