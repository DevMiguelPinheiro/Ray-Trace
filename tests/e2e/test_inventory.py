"""Inventory page tests - product listing, sorting, filtering."""

import pytest

from pages.inventory_page import InventoryPage


@pytest.mark.regression
async def test_inventory_page_loads(inventory_page: InventoryPage, settings) -> None:
    """Test that inventory page loads successfully."""
    await inventory_page.navigate_to_inventory()
    assert await inventory_page.is_inventory_page_loaded()


@pytest.mark.regression
async def test_get_all_products(inventory_page: InventoryPage) -> None:
    """Test retrieving all product names."""
    await inventory_page.navigate_to_inventory()
    products = await inventory_page.get_all_product_names()
    assert len(products) == 6
    assert "Sauce Labs Backpack" in products


@pytest.mark.regression
async def test_product_prices_visible(inventory_page: InventoryPage) -> None:
    """Test that product prices are visible and valid."""
    await inventory_page.navigate_to_inventory()
    prices = await inventory_page.get_all_product_prices()
    assert len(prices) > 0
    assert all(price > 0 for price in prices)


@pytest.mark.regression
async def test_add_product_to_cart(inventory_page: InventoryPage) -> None:
    """Test adding a product to cart."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")
    assert await inventory_page.get_cart_count() == 1


@pytest.mark.regression
async def test_add_multiple_products_to_cart(inventory_page: InventoryPage) -> None:
    """Test adding multiple products to cart."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")
    await inventory_page.add_to_cart("Sauce Labs Bike Light")
    assert await inventory_page.get_cart_count() == 2


@pytest.mark.regression
async def test_remove_product_from_cart(inventory_page: InventoryPage) -> None:
    """Test removing a product from cart."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.add_to_cart("Sauce Labs Backpack")
    assert await inventory_page.get_cart_count() == 1
    await inventory_page.remove_from_cart("Sauce Labs Backpack")
    assert await inventory_page.get_cart_count() == 0


@pytest.mark.regression
async def test_sort_products_z_to_a(inventory_page: InventoryPage) -> None:
    """Test sorting products Z to A."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.sort_by("za")
    products = await inventory_page.get_all_product_names()
    # Verify products are in reverse alphabetical order
    assert products == sorted(products, reverse=True)


@pytest.mark.regression
async def test_sort_products_a_to_z(inventory_page: InventoryPage) -> None:
    """Test sorting products A to Z."""
    await inventory_page.navigate_to_inventory()
    await inventory_page.sort_by("az")
    products = await inventory_page.get_all_product_names()
    # Verify products are in alphabetical order
    assert products == sorted(products)


@pytest.mark.regression
async def test_product_is_visible(inventory_page: InventoryPage) -> None:
    """Test checking if a product is visible."""
    await inventory_page.navigate_to_inventory()
    assert await inventory_page.is_product_visible("Sauce Labs Backpack")
    assert not await inventory_page.is_product_visible("Non-existent Product")
