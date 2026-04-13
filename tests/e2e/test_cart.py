"""Shopping cart tests - add/remove items, cart persistence."""

import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


@pytest.mark.regression
async def test_add_item_to_cart_and_view(
    inventory_page: InventoryPage, cart_page: CartPage
) -> None:
    """Test adding an item and viewing it in cart."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")

    await cart_page.navigate_to_cart()
    items = await cart_page.get_cart_items()
    assert len(items) == 1
    assert items[0]["name"] == "Sauce Labs Backpack"


@pytest.mark.regression
async def test_cart_empty(cart_page: CartPage) -> None:
    """Test that empty cart is empty."""
    await cart_page.navigate_to_cart()
    assert await cart_page.is_empty()


@pytest.mark.regression
async def test_remove_item_from_cart(inventory_page: InventoryPage, cart_page: CartPage) -> None:
    """Test removing an item from cart."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")

    await cart_page.navigate_to_cart()
    assert not await cart_page.is_empty()

    await cart_page.remove_item("Sauce Labs Backpack")
    assert await cart_page.is_empty()


@pytest.mark.regression
async def test_cart_item_quantity(inventory_page: InventoryPage, cart_page: CartPage) -> None:
    """Test getting item quantity from cart."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")

    await cart_page.navigate_to_cart()
    quantity = await cart_page.get_item_quantity("Sauce Labs Backpack")
    # SauceDemo allows one unit per product in the standard flow.
    assert quantity == 1


@pytest.mark.regression
async def test_cart_total_items_count(inventory_page: InventoryPage, cart_page: CartPage) -> None:
    """Test getting total item count in cart."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")
    await inventory_page.add_to_cart("Sauce Labs Bike Light")

    await cart_page.navigate_to_cart()
    total = await cart_page.get_total_items_count()
    assert total >= 2


@pytest.mark.regression
async def test_continue_shopping_returns_to_inventory(
    inventory_page: InventoryPage, cart_page: CartPage
) -> None:
    """Test that continue shopping button returns to inventory."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")

    await cart_page.navigate_to_cart()
    await cart_page.continue_shopping()

    assert "inventory" in inventory_page.page.url


@pytest.mark.critical
async def test_proceed_to_checkout(inventory_page: InventoryPage, cart_page: CartPage) -> None:
    """Test proceeding from cart to checkout."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")

    await cart_page.navigate_to_cart()
    await cart_page.proceed_to_checkout()

    assert "checkout-step-one" in cart_page.page.url
