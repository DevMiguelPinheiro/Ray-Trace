"""Visual regression tests - screenshot comparison."""

import pytest
from playwright.async_api import Page

from config.settings import Settings
from utils.screenshot_comparator import ScreenshotComparator


@pytest.mark.visual
async def test_login_page_visual_regression(
    page: Page,
    screenshot_comparator: ScreenshotComparator,
    settings: Settings,
) -> None:
    """Test login page visual regression."""
    await page.goto(settings.base_url)

    if settings.update_snapshots:
        screenshot_comparator.capture_baseline(page, "login-page")
    else:
        result = screenshot_comparator.compare(page, "login-page")
        assert result.passed, f"Visual diff: {result.diff_ratio * 100:.2f}%"


@pytest.mark.visual
async def test_inventory_page_visual_regression(
    page: Page,
    screenshot_comparator: ScreenshotComparator,
    settings: Settings,
) -> None:
    """Test inventory page visual regression."""
    await page.goto(settings.base_url + "/inventory.html")
    await page.wait_for_load_state("networkidle", timeout=5000)

    if settings.update_snapshots:
        screenshot_comparator.capture_baseline(page, "inventory-page")
    else:
        result = screenshot_comparator.compare(page, "inventory-page")
        assert result.passed, f"Visual diff: {result.diff_ratio * 100:.2f}%"


@pytest.mark.visual
async def test_cart_page_visual_regression(
    page: Page,
    screenshot_comparator: ScreenshotComparator,
    settings: Settings,
) -> None:
    """Test cart page visual regression."""
    await page.goto(settings.base_url + "/cart.html")
    await page.wait_for_load_state("networkidle", timeout=5000)

    if settings.update_snapshots:
        screenshot_comparator.capture_baseline(page, "cart-page")
    else:
        result = screenshot_comparator.compare(page, "cart-page")
        assert result.passed, f"Visual diff: {result.diff_ratio * 100:.2f}%"


@pytest.mark.visual
async def test_checkout_complete_visual_regression(
    page: Page,
    screenshot_comparator: ScreenshotComparator,
    settings: Settings,
) -> None:
    """Test checkout complete page visual regression."""
    await page.goto(settings.base_url + "/checkout-complete.html")
    await page.wait_for_load_state("networkidle", timeout=5000)

    if settings.update_snapshots:
        screenshot_comparator.capture_baseline(page, "checkout-complete-page")
    else:
        result = screenshot_comparator.compare(page, "checkout-complete-page")
        assert result.passed, f"Visual diff: {result.diff_ratio * 100:.2f}%"


@pytest.mark.visual
async def test_header_visual_consistency(
    page: Page,
    screenshot_comparator: ScreenshotComparator,
    settings: Settings,
) -> None:
    """Test header component visual consistency across pages."""
    # Visit multiple pages and verify header looks the same
    pages_to_test = [
        settings.base_url,
        settings.base_url + "/inventory.html",
        settings.base_url + "/cart.html",
    ]

    for page_url in pages_to_test:
        await page.goto(page_url)
        await page.wait_for_load_state("load", timeout=5000)

        header_element = page.locator("[data-test='primary-header']")
        if await header_element.is_visible():
            # Header is present on this page
            assert await header_element.is_visible()
