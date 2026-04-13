"""Authentication fixtures with storage_state caching."""

import json
from pathlib import Path

import pytest
from playwright.async_api import async_playwright

from config.settings import Settings
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
async def auth_context(settings: Settings) -> dict:
    """Create authenticated context by saving storage_state.

    This fixture logs in once per session and saves the authentication state
    to disk to avoid re-logging in for every test.

    Returns:
        Dictionary containing storage_state for authenticated context
    """
    auth_dir = Path(".auth")
    auth_dir.mkdir(parents=True, exist_ok=True)
    storage_state_path = auth_dir / f"{settings.app_env}_standard_user.json"

    # Always regenerate auth state to ensure fresh credentials
    # (Cached state can become stale when session expires)
    if storage_state_path.exists():
        try:
            storage_state_path.unlink()
        except OSError:
            pass

    # Otherwise, create it by logging in
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=settings.headless)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            login_page = LoginPage(page, settings)
            await login_page.navigate_to_login()
            await login_page.login_as("standard_user")

            # Verify login was successful by checking for error message
            if await login_page.is_error_displayed():
                error_msg = await login_page.get_error_message()
                raise RuntimeError(f"Login failed: {error_msg}")

            # Wait for inventory page to load by navigating there
            await page.goto(f"{settings.base_url}/inventory.html", wait_until="load")
            # Wait for header to be visible to ensure page is fully loaded
            await page.locator("[data-test='primary-header']").wait_for(
                state="visible", timeout=30000
            )

            # Save storage state
            storage_state = await context.storage_state()
            with open(storage_state_path, "w") as f:
                json.dump(storage_state, f, indent=2)

            return storage_state
        finally:
            await context.close()
            await browser.close()


@pytest.fixture
async def authenticated_context(browser, auth_context):
    """Create a new browser context with pre-authenticated storage state.

    Args:
        browser: Playwright browser fixture
        auth_context: Authenticated storage state from session fixture

    Returns:
        BrowserContext with authentication already loaded
    """
    context = await browser.new_context(storage_state=auth_context)
    yield context
    await context.close()
