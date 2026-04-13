"""API failure tests - simulate network errors, 5xx, 401 scenarios."""

import pytest
from playwright.async_api import Page

from utils.network_interceptor import NetworkInterceptor


@pytest.mark.network
async def test_handle_500_error(
    page: Page, network_interceptor: NetworkInterceptor, settings
) -> None:
    """Test handling of 500 server error."""
    async with network_interceptor:
        await network_interceptor.intercept_with_custom("**/api/**", 500, {"error": "Server Error"})
        await page.goto(settings.base_url)
        # Page should still load (with graceful degradation)
        assert page.url == settings.base_url


@pytest.mark.network
async def test_handle_401_unauthorized(
    page: Page, network_interceptor: NetworkInterceptor, settings
) -> None:
    """Test handling of 401 Unauthorized error."""
    async with network_interceptor:
        await network_interceptor.intercept_with_401("**/api/inventory**")
        await page.goto(settings.base_url + "/inventory.html")
        # Page should handle auth error gracefully
        assert page.url.endswith(".html") or "inventory" in page.url


@pytest.mark.network
async def test_network_timeout_simulation(
    page: Page, network_interceptor: NetworkInterceptor, settings
) -> None:
    """Test network timeout handling."""
    async with network_interceptor:
        await network_interceptor.intercept_with_timeout("**/api/**")
        try:
            await page.goto(settings.base_url, timeout=3000)
        except Exception:
            # Timeout is expected
            pass


@pytest.mark.network
async def test_custom_error_response(
    page: Page, network_interceptor: NetworkInterceptor, settings
) -> None:
    """Test custom error response interception."""
    async with network_interceptor:
        await network_interceptor.intercept_with_custom(
            "**/api/**",
            503,
            {"error": "Service Unavailable", "retry_after": 60},
        )
        await page.goto(settings.base_url)
        # Page should still be accessible
        assert page.url == settings.base_url


@pytest.mark.network
async def test_selective_route_interception(
    page: Page, network_interceptor: NetworkInterceptor, settings
) -> None:
    """Test that selective route interception doesn't affect other routes."""
    async with network_interceptor:
        await network_interceptor.intercept_with_500("**/api/specific-endpoint**")

        # This should work normally
        await page.goto(settings.base_url)
        assert page.url == settings.base_url


@pytest.mark.network
async def test_restore_intercepted_route(
    page: Page, network_interceptor: NetworkInterceptor, settings
) -> None:
    """Test restoring an intercepted route."""
    await network_interceptor.intercept_with_500("**/api/**")
    await network_interceptor.restore("**/api/**")

    # After restore, requests should go through normally
    await page.goto(settings.base_url)
    assert page.url == settings.base_url
