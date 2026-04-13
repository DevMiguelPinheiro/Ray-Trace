"""Settings configuration using Pydantic."""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Environment
    app_env: str = "staging"  # staging | production
    base_url: str = "https://www.saucedemo.com/"

    # Playwright behavior
    headless: bool = True
    slow_mo_ms: int = 0  # Slow down browser actions (debug)
    default_timeout_ms: int = 15000  # Increased from 5000ms for CI environments

    # Viewport
    viewport_width: int = 1280
    viewport_height: int = 720

    # Recording
    video_mode: str = "retain-on-failure"  # off | on | retain-on-failure
    trace_mode: str = "retain-on-failure"  # off | on | retain-on-failure

    # Visual regression
    snapshot_threshold: float = 0.02  # 2% pixel diff tolerance
    update_snapshots: bool = False  # If True, overwrites baselines

    # Retry configuration
    test_retry_count: int = 2  # pytest-rerunfailures: test-level retries
    action_retry_count: int = 3  # RetryHelper: action-level retries

    # Reporting
    allure_results_dir: str = "allure-results"

    @field_validator("base_url")
    @classmethod
    def normalize_base_url(cls, value: str) -> str:
        """Ensure base URL always has a single trailing slash."""
        return value.rstrip("/") + "/"
