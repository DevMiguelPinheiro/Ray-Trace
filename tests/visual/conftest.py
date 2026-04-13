"""Visual test layer conftest - screenshot comparator setup."""

import pytest

from config.settings import Settings
from utils.screenshot_comparator import ScreenshotComparator


@pytest.fixture
def screenshot_comparator(settings: Settings) -> ScreenshotComparator:
    """Provide ScreenshotComparator instance with configured threshold.

    Args:
        settings: Settings fixture

    Returns:
        ScreenshotComparator instance
    """
    return ScreenshotComparator(threshold=settings.snapshot_threshold)
