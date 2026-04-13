"""Custom browser and context factory fixtures."""

import pytest
from playwright.async_api import Browser, BrowserContext, async_playwright

from config.settings import Settings


@pytest.fixture(scope="function")
async def browser(settings: Settings) -> Browser:
    """Create a new browser instance for each test.

    Args:
        settings: Settings fixture

    Yields:
        Playwright Browser object
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=settings.headless,
            slow_mo=settings.slow_mo_ms,
        )
        yield browser
        await browser.close()


@pytest.fixture(scope="function")
async def context(browser: Browser, settings: Settings) -> BrowserContext:
    """Create a new browser context for each test.

    Args:
        browser: Browser fixture
        settings: Settings fixture

    Yields:
        Playwright BrowserContext object
    """
    context = await browser.new_context(
        viewport={"width": settings.viewport_width, "height": settings.viewport_height},
        record_video_dir="test-results" if settings.video_mode != "off" else None,
        record_har_path=None,
    )

    # Enable tracing if configured
    if settings.trace_mode != "off":
        await context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True,
        )

    yield context

    # Stop tracing and save
    if settings.trace_mode != "off":
        await context.tracing.stop(path="test-results/trace.zip")

    await context.close()


@pytest.fixture
async def page(context: BrowserContext):
    """Create a new page for each test.

    Args:
        context: BrowserContext fixture

    Yields:
        Playwright Page object
    """
    page = await context.new_page()
    yield page
    await page.close()
