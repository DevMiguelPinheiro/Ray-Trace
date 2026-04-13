"""Offline/network abort tests - simulate network unavailability."""

import pytest
from playwright.async_api import Page

from utils.network_interceptor import NetworkInterceptor


@pytest.mark.network
async def test_network_abort_all_requests(
    page: Page, network_interceptor: NetworkInterceptor, settings
) -> None:
    """Test aborting all network requests (offline mode)."""
    async with network_interceptor:
        await network_interceptor.intercept_with_timeout("**/*")

        try:
            await page.goto(settings.base_url, timeout=2000)
        except Exception as e:
            # Timeout is expected when aborting all requests
            error_text = str(e).lower()
            assert "timeout" in error_text or "timed_out" in error_text or "failed" in error_text


@pytest.mark.network
async def test_selective_offline_mode(
    page: Page, network_interceptor: NetworkInterceptor, settings
) -> None:
    """Test selective requests being aborted while others work."""
    async with network_interceptor:
        # Abort API calls but allow HTML/JS
        await network_interceptor.intercept_with_timeout("**/api/**")

        await page.goto(settings.base_url)
        # Page HTML should load, but API calls will fail
        assert page.url == settings.base_url
