"""E2E test layer conftest - authenticated context for all e2e tests."""

import pytest
from playwright.async_api import Page

from config.settings import Settings
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.components.header import SiteHeader
from pages.components.sidebar import SidebarMenu
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.fixture
async def auth_page(authenticated_context, settings) -> Page:
    """Create an authenticated page ready for testing.

    Args:
        authenticated_context: Context with pre-loaded auth storage_state
        settings: Settings fixture

    Returns:
        Authenticated Page object
    """
    page = await authenticated_context.new_page()

    # Ensure every E2E test starts authenticated.
    await page.goto(f"{settings.base_url}/inventory.html", wait_until="domcontentloaded")

    if "inventory.html" not in page.url:
        login_page = LoginPage(page, settings)
        await login_page.navigate_to_login()
        await login_page.login_as("standard_user")
        await page.goto(f"{settings.base_url}/inventory.html", wait_until="domcontentloaded")

    await page.locator("[data-test='inventory-container']").wait_for(state="visible", timeout=30000)

    # Best effort reset: do not fail test setup if sidebar elements are unavailable.
    try:
        menu_btn = page.locator("[data-test='hamburger-menu-btn']")
        if await menu_btn.count() > 0 and await menu_btn.is_visible():
            await menu_btn.click(timeout=8000)

            reset_btn = page.locator("[data-test='reset-sidebar-link']")
            if await reset_btn.count() > 0 and await reset_btn.is_visible():
                await reset_btn.click(timeout=8000)

            close_btn = page.locator("[data-test='menu-button-close']")
            if await close_btn.count() > 0 and await close_btn.is_visible():
                await close_btn.click(timeout=8000)
    except Exception:
        pass

    yield page
    await page.close()


# Authenticated page fixtures for regression tests
@pytest.fixture
async def login_page(page: Page, settings: Settings) -> LoginPage:
    """Unauthenticated fixture for LoginPage.

    Args:
        page: Page fixture
        settings: Settings fixture

    Returns:
        LoginPage instance
    """
    return LoginPage(page, settings)


@pytest.fixture
async def inventory_page(auth_page: Page, settings: Settings) -> InventoryPage:
    """Authenticated fixture for InventoryPage.

    Args:
        auth_page: Authenticated page fixture
        settings: Settings fixture

    Returns:
        InventoryPage instance
    """
    return InventoryPage(auth_page, settings)


@pytest.fixture
async def cart_page(auth_page: Page, settings: Settings) -> CartPage:
    """Authenticated fixture for CartPage.

    Args:
        auth_page: Authenticated page fixture
        settings: Settings fixture

    Returns:
        CartPage instance
    """
    return CartPage(auth_page, settings)


@pytest.fixture
async def checkout_info_page(auth_page: Page, settings: Settings) -> CheckoutInfoPage:
    """Authenticated fixture for CheckoutInfoPage.

    Args:
        auth_page: Authenticated page fixture
        settings: Settings fixture

    Returns:
        CheckoutInfoPage instance
    """
    return CheckoutInfoPage(auth_page, settings)


@pytest.fixture
async def checkout_overview_page(auth_page: Page, settings: Settings) -> CheckoutOverviewPage:
    """Authenticated fixture for CheckoutOverviewPage.

    Args:
        auth_page: Authenticated page fixture
        settings: Settings fixture

    Returns:
        CheckoutOverviewPage instance
    """
    return CheckoutOverviewPage(auth_page, settings)


@pytest.fixture
async def checkout_complete_page(auth_page: Page, settings: Settings) -> CheckoutCompletePage:
    """Authenticated fixture for CheckoutCompletePage.

    Args:
        auth_page: Authenticated page fixture
        settings: Settings fixture

    Returns:
        CheckoutCompletePage instance
    """
    return CheckoutCompletePage(auth_page, settings)


@pytest.fixture
async def site_header(auth_page: Page) -> SiteHeader:
    """Authenticated fixture for SiteHeader component.

    Args:
        auth_page: Authenticated page fixture

    Returns:
        SiteHeader instance
    """
    return SiteHeader(auth_page)


@pytest.fixture
async def sidebar_menu(auth_page: Page) -> SidebarMenu:
    """Authenticated fixture for SidebarMenu component.

    Args:
        auth_page: Authenticated page fixture

    Returns:
        SidebarMenu instance
    """
    return SidebarMenu(auth_page)
