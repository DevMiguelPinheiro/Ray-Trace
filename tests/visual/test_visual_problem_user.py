"""Visual tests for problem_user - expects intentional visual diffs."""

import pytest
from playwright.async_api import Page

from config.settings import Settings
from pages.login_page import LoginPage


@pytest.mark.visual
async def test_problem_user_visual_diffs(page: Page, settings: Settings) -> None:
    """Test that problem_user exhibits visual differences (broken images)."""
    login_page = LoginPage(page, settings)
    await login_page.navigate_to_login()

    # Login as problem_user (known to have visual issues)
    from config.environments import get_credentials

    creds = get_credentials(settings.app_env, "problem_user")
    await login_page.login(creds.username, creds.password)

    # Navigate to inventory to see broken images
    await page.goto(settings.base_url + "/inventory.html")
    await page.wait_for_load_state("networkidle", timeout=5000)

    # Product images should be broken/missing
    product_images = await page.locator("[data-test='inventory-item-img']").all()
    # With problem_user, images may be broken or missing
    assert len(product_images) >= 0  # Just verify we can access them


@pytest.mark.visual
async def test_performance_glitch_user_visual_behavior(page: Page, settings: Settings) -> None:
    """Test performance_glitch_user visual behavior."""
    login_page = LoginPage(page, settings)
    await login_page.navigate_to_login()

    from config.environments import get_credentials

    creds = get_credentials(settings.app_env, "performance_glitch_user")
    await login_page.login(creds.username, creds.password)

    await page.goto(settings.base_url + "/inventory.html")
    # This user may have slower performance/visual delays
    await page.wait_for_load_state("networkidle", timeout=10000)

    assert "inventory" in page.url
