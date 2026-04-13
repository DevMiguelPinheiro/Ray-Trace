"""Edge case tests - back button, cross-browser, session scenarios."""

import pytest

from pages.cart_page import CartPage
from pages.components.header import SiteHeader
from pages.components.sidebar import SidebarMenu
from pages.inventory_page import InventoryPage


@pytest.mark.regression
async def test_back_button_from_cart(inventory_page: InventoryPage, cart_page: CartPage) -> None:
    """Test back button from cart returns to inventory."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")

    await cart_page.navigate_to_cart()
    await cart_page.page.go_back()

    # Should be back on inventory
    assert "inventory" in cart_page.page.url


@pytest.mark.regression
async def test_cart_badge_updates(inventory_page: InventoryPage) -> None:
    """Test that cart badge updates when items are added."""
    await inventory_page.navigate_to_inventory()
    header = SiteHeader(inventory_page.page)

    initial_count = await header.get_cart_badge_count()
    await inventory_page.add_to_cart("Sauce Labs Backpack")
    new_count = await header.get_cart_badge_count()

    assert new_count > initial_count


@pytest.mark.regression
async def test_sidebar_menu_visibility(inventory_page: InventoryPage) -> None:
    """Test opening and closing sidebar menu."""
    await inventory_page.navigate_to_inventory()
    sidebar = SidebarMenu(inventory_page.page)
    header = SiteHeader(inventory_page.page)

    await header.open_sidebar_menu()
    assert await sidebar.is_visible()

    await sidebar.close()
    assert not await sidebar.is_visible()


@pytest.mark.regression
async def test_reset_app_state(inventory_page: InventoryPage) -> None:
    """Test reset app state clears cart."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")
    await inventory_page.add_to_cart("Sauce Labs Bike Light")
    assert await inventory_page.get_cart_count() == 2

    sidebar = SidebarMenu(inventory_page.page)
    header = SiteHeader(inventory_page.page)
    await header.open_sidebar_menu()
    await sidebar.reset_app_state()

    # Wait for cart badge to disappear after reset (async DOM update)
    badge_locator = inventory_page.page.locator("[data-test='shopping-cart-badge']")
    await badge_locator.wait_for(state="hidden", timeout=10000)

    # Cart should be reset
    assert await inventory_page.get_cart_count() == 0


@pytest.mark.slow
async def test_navigate_multiple_pages(
    inventory_page: InventoryPage,
    cart_page: CartPage,
) -> None:
    """Test navigating through multiple pages."""
    await inventory_page.navigate_to_inventory()
    assert "inventory" in inventory_page.page.url

    await cart_page.navigate_to_cart()
    assert "cart" in cart_page.page.url

    await cart_page.continue_shopping()
    assert "inventory" in inventory_page.page.url


@pytest.mark.regression
async def test_url_navigation_directly(inventory_page: InventoryPage, settings) -> None:
    """Test direct URL navigation."""
    await inventory_page.page.goto(f"{settings.base_url}/inventory.html")
    assert await inventory_page.is_inventory_page_loaded()


@pytest.mark.regression
async def test_page_reload(inventory_page: InventoryPage) -> None:
    """Test page reload maintains state."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")
    initial_count = await inventory_page.get_cart_count()

    await inventory_page.page.reload()

    # Cart should persist after reload
    assert await inventory_page.get_cart_count() == initial_count
