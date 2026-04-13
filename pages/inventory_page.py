"""Inventory (product catalog) page object."""

from playwright.async_api import Page

from config.settings import Settings
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Inventory page interactions - product listing, sorting, filtering."""

    # Locators
    PRODUCT_ITEM = "[data-test='inventory-item']"
    PRODUCT_NAME = "[data-test='inventory-item-name']"
    PRODUCT_PRICE = "[data-test='inventory-item-price']"
    PRODUCT_DESCRIPTION = "[data-test='inventory-item-desc']"
    SORT_DROPDOWN = "[data-test='product-sort-container']"
    CART_BADGE = "[data-test='shopping-cart-badge']"
    HEADER = "[data-test='secondary-header']"

    def __init__(self, page: Page, settings: Settings | None = None) -> None:
        """Initialize InventoryPage.

        Args:
            page: Playwright Page object
            settings: Settings object for configuration
        """
        super().__init__(page, settings)

    async def navigate_to_inventory(self) -> None:
        """Navigate to the inventory page."""
        await self.navigate("/inventory.html")
        # Wait for first product item to be visible
        await self.page.locator(self.PRODUCT_ITEM).first.wait_for(
            state="visible", timeout=self.timeout_ms
        )

    async def get_all_product_names(self) -> list[str]:
        """Get all visible product names on the page.

        Returns:
            List of product names
        """
        locator = self.page.locator(f"{self.PRODUCT_ITEM} {self.PRODUCT_NAME}")
        return list(await locator.all_text_contents())

    async def get_all_product_prices(self) -> list[float]:
        """Get all visible product prices on the page.

        Returns:
            List of product prices as floats
        """
        locator = self.page.locator(f"{self.PRODUCT_ITEM} {self.PRODUCT_PRICE}")
        prices_text = await locator.all_text_contents()
        # Parse prices (format: $X.XX)
        return [float(price.replace("$", "")) for price in prices_text]

    async def sort_by(self, option: str) -> None:
        """Sort products by the given option.

        Args:
            option: Sort option (e.g., "za", "lohi", "hilo")
        """
        select_element = self.page.locator(self.SORT_DROPDOWN)
        await select_element.select_option(option)
        # Wait for product items to remain visible after sort (client-side re-render)
        await self.page.locator(self.PRODUCT_ITEM).first.wait_for(
            state="visible", timeout=self.timeout_ms
        )

    async def add_to_cart(self, product_name: str) -> None:
        """Add a product to cart by name.

        Args:
            product_name: Name of the product to add
        """
        # Find the product item containing the product name, then find the Add to cart button within it
        product_item = self.page.locator(self.PRODUCT_ITEM).filter(has_text=product_name).first
        add_btn = product_item.get_by_role("button", name="Add to cart")
        await add_btn.click(timeout=self.timeout_ms)
        # Wait for button to change to "Remove" to confirm item was added
        remove_btn = product_item.get_by_role("button", name="Remove")
        await remove_btn.wait_for(state="visible", timeout=self.timeout_ms)

    async def remove_from_cart(self, product_name: str) -> None:
        """Remove a product from cart by name.

        Args:
            product_name: Name of the product to remove
        """
        # Find the product item containing the product name, then find the Remove button within it
        product_item = self.page.locator(self.PRODUCT_ITEM).filter(has_text=product_name).first
        remove_btn = product_item.get_by_role("button", name="Remove")
        await remove_btn.click(timeout=self.timeout_ms)

    async def get_cart_count(self) -> int:
        """Get the number of items in the cart.

        Returns:
            Number of items in cart (0 if badge is not visible)
        """
        badge = self.page.locator(self.CART_BADGE)
        # Short-circuit if badge doesn't exist or isn't visible
        if await badge.count() == 0 or not await badge.is_visible():
            return 0
        try:
            badge_text = await badge.text_content()
            return int(badge_text) if badge_text else 0
        except (ValueError, AttributeError):
            return 0

    async def open_product(self, product_name: str) -> None:
        """Click on a product to open its detail page.

        Args:
            product_name: Name of the product to open
        """
        product_item = self.page.locator(self.PRODUCT_ITEM).filter(has_text=product_name)
        await product_item.click(timeout=self.timeout_ms)

    async def get_product_price(self, product_name: str) -> float:
        """Get the price of a specific product.

        Args:
            product_name: Name of the product

        Returns:
            Price as float
        """
        # Find the product item containing the name, then get price
        product_locator = self.page.locator(self.PRODUCT_ITEM).filter(has_text=product_name)
        price_text = await product_locator.locator(self.PRODUCT_PRICE).text_content()
        return float(price_text.replace("$", "")) if price_text else 0.0

    async def is_product_visible(self, product_name: str) -> bool:
        """Check if a product is visible on the page.

        Args:
            product_name: Name of the product

        Returns:
            True if product is visible, False otherwise
        """
        try:
            product_item = self.page.locator(self.PRODUCT_ITEM).filter(has_text=product_name)
            return bool(await product_item.is_visible(timeout=self.timeout_ms))
        except Exception:
            return False

    async def is_inventory_page_loaded(self) -> bool:
        """Check if inventory page is fully loaded.

        Returns:
            True if page is loaded, False otherwise
        """
        return await self.is_visible(self.HEADER)
