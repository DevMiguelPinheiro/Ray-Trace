"""Checkout tests - complete purchase flows."""

import pytest

from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.inventory_page import InventoryPage


@pytest.mark.critical
async def test_complete_purchase_flow(
    inventory_page: InventoryPage,
    cart_page: CartPage,
    checkout_info_page: CheckoutInfoPage,
    checkout_overview_page: CheckoutOverviewPage,
    checkout_complete_page: CheckoutCompletePage,
) -> None:
    """Test complete end-to-end purchase flow."""
    # Add items to cart
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")
    await inventory_page.add_to_cart("Sauce Labs Bike Light")

    # Go to cart and checkout
    await cart_page.navigate_to_cart()
    assert not await cart_page.is_empty()
    await cart_page.proceed_to_checkout()

    # Fill checkout info
    await checkout_info_page.fill_shipping_info("John", "Doe", "12345")
    await checkout_info_page.continue_to_overview()

    # Review order
    await checkout_overview_page.navigate_to_checkout_overview()
    assert await checkout_overview_page.get_item_count() >= 2

    # Complete purchase
    await checkout_overview_page.finish_purchase()

    # Verify order confirmation
    assert await checkout_complete_page.is_order_confirmed()


@pytest.mark.critical
async def test_checkout_info_validation(
    inventory_page: InventoryPage,
    cart_page: CartPage,
    checkout_info_page: CheckoutInfoPage,
) -> None:
    """Test checkout info form validation."""
    # Add item and go to checkout
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")
    await cart_page.navigate_to_cart()
    await cart_page.proceed_to_checkout()

    # Try to submit without filling fields
    await checkout_info_page.navigate_to_checkout_info()
    await checkout_info_page.continue_to_overview()

    # Assert validation error is shown
    assert await checkout_info_page.is_error_displayed()


@pytest.mark.critical
async def test_checkout_cancel(
    inventory_page: InventoryPage,
    cart_page: CartPage,
    checkout_info_page: CheckoutInfoPage,
) -> None:
    """Test canceling checkout returns to cart."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")

    await cart_page.navigate_to_cart()
    await cart_page.proceed_to_checkout()

    await checkout_info_page.navigate_to_checkout_info()
    await checkout_info_page.cancel_checkout()

    assert "cart" in checkout_info_page.page.url


@pytest.mark.critical
async def test_order_summary_totals(
    inventory_page: InventoryPage,
    cart_page: CartPage,
    checkout_info_page: CheckoutInfoPage,
    checkout_overview_page: CheckoutOverviewPage,
) -> None:
    """Test that order summary shows correct totals."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")  # $29.99

    await cart_page.navigate_to_cart()
    await cart_page.proceed_to_checkout()

    await checkout_info_page.fill_shipping_info("John", "Doe", "12345")
    await checkout_info_page.continue_to_overview()

    await checkout_overview_page.navigate_to_checkout_overview()
    subtotal = await checkout_overview_page.get_subtotal()
    total = await checkout_overview_page.get_total()

    assert subtotal > 0
    assert total >= subtotal  # Total includes tax


@pytest.mark.critical
async def test_confirmation_page_message(
    inventory_page: InventoryPage,
    cart_page: CartPage,
    checkout_info_page: CheckoutInfoPage,
    checkout_overview_page: CheckoutOverviewPage,
    checkout_complete_page: CheckoutCompletePage,
) -> None:
    """Test confirmation page displays order confirmation message."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")

    await cart_page.navigate_to_cart()
    await cart_page.proceed_to_checkout()

    await checkout_info_page.fill_shipping_info("John", "Doe", "12345")
    await checkout_info_page.continue_to_overview()

    await checkout_overview_page.navigate_to_checkout_overview()
    await checkout_overview_page.finish_purchase()

    message = await checkout_complete_page.get_confirmation_message()
    assert len(message) > 0
    assert "complete" in message.lower() or "thank" in message.lower()
