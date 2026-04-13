"""Network test layer conftest - route interception setup."""

import pytest
from playwright.async_api import Page

from utils.network_interceptor import NetworkInterceptor


@pytest.fixture
async def page(authenticated_context) -> Page:
    """Provide authenticated page for network tests.

    Args:
        authenticated_context: Context with auth storage state

    Yields:
        Authenticated page
    """
    test_page = await authenticated_context.new_page()
    yield test_page
    await test_page.close()


@pytest.fixture
async def network_interceptor(page) -> NetworkInterceptor:
    """Provide NetworkInterceptor instance for network-level testing.

    Args:
        page: Page fixture

    Yields:
        NetworkInterceptor instance
    """
    interceptor = NetworkInterceptor(page)
    yield interceptor
    await interceptor.restore_all()
