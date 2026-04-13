"""Page object factory fixtures."""

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
def login_page(page: Page, settings: Settings) -> LoginPage:
    """Fixture for LoginPage.

    Args:
        page: Page fixture
        settings: Settings fixture

    Returns:
        LoginPage instance
    """
    return LoginPage(page, settings)


@pytest.fixture
def inventory_page(page: Page, settings: Settings) -> InventoryPage:
    """Fixture for InventoryPage.

    Args:
        page: Page fixture
        settings: Settings fixture

    Returns:
        InventoryPage instance
    """
    return InventoryPage(page, settings)


@pytest.fixture
def cart_page(page: Page, settings: Settings) -> CartPage:
    """Fixture for CartPage.

    Args:
        page: Page fixture
        settings: Settings fixture

    Returns:
        CartPage instance
    """
    return CartPage(page, settings)


@pytest.fixture
def checkout_info_page(page: Page, settings: Settings) -> CheckoutInfoPage:
    """Fixture for CheckoutInfoPage.

    Args:
        page: Page fixture
        settings: Settings fixture

    Returns:
        CheckoutInfoPage instance
    """
    return CheckoutInfoPage(page, settings)


@pytest.fixture
def checkout_overview_page(page: Page, settings: Settings) -> CheckoutOverviewPage:
    """Fixture for CheckoutOverviewPage.

    Args:
        page: Page fixture
        settings: Settings fixture

    Returns:
        CheckoutOverviewPage instance
    """
    return CheckoutOverviewPage(page, settings)


@pytest.fixture
def checkout_complete_page(page: Page, settings: Settings) -> CheckoutCompletePage:
    """Fixture for CheckoutCompletePage.

    Args:
        page: Page fixture
        settings: Settings fixture

    Returns:
        CheckoutCompletePage instance
    """
    return CheckoutCompletePage(page, settings)


@pytest.fixture
def site_header(page: Page) -> SiteHeader:
    """Fixture for SiteHeader component.

    Args:
        page: Page fixture

    Returns:
        SiteHeader instance
    """
    return SiteHeader(page)


@pytest.fixture
def sidebar_menu(page: Page) -> SidebarMenu:
    """Fixture for SidebarMenu component.

    Args:
        page: Page fixture

    Returns:
        SidebarMenu instance
    """
    return SidebarMenu(page)
