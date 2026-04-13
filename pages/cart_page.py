"""Shopping cart page object."""

from playwright.async_api import Page

from config.settings import Settings
from pages.base_page import BasePage


class CartPage(BasePage):
    """Cart page interactions - review items, proceed to checkout."""

    # Locators
    CART_ITEM = "[data-test='cart-item'], [data-test='inventory-item'], .cart_item"
    ITEM_NAME = "[data-test='inventory-item-name']"
    ITEM_PRICE = "[data-test='inventory-item-price']"
    ITEM_QUANTITY = "[data-test='item-quantity']"
    REMOVE_BUTTON_TEMPLATE = (
        "//button[contains(., 'Remove') and ancestor::*[contains(., '{product_name}')]]"
    )
    CHECKOUT_BUTTON = "[data-test='checkout']"
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"
    CART_QUANTITY_LABEL = "[data-test='cart-quantity-label']"

    def __init__(self, page: Page, settings: Settings | None = None) -> None:
        """Initialize CartPage.

        Args:
            page: Playwright Page object
            settings: Settings object for configuration
        """
        super().__init__(page, settings)

    async def navigate_to_cart(self) -> None:
        """Navigate to the cart page."""
        await self.navigate("/cart.html")
        await self.wait_for_element_visible(self.CHECKOUT_BUTTON)

    async def get_cart_items(self) -> list[dict]:
        """Get all items in the cart.

        Returns:
            List of dictionaries with item details (name, price, quantity)
        """
        items = []
        item_elements = await self.page.locator(self.CART_ITEM).all()

        for item_element in item_elements:
            name = await item_element.locator(self.ITEM_NAME).text_content() or ""
            price_text = await item_element.locator(self.ITEM_PRICE).text_content() or "$0.00"
            quantity_text = await item_element.locator(self.ITEM_QUANTITY).text_content() or "1"

            items.append(
                {
                    "name": name,
                    "price": float(price_text.replace("$", "")),
                    "quantity": int(quantity_text),
                }
            )

        return items

    async def remove_item(self, product_name: str) -> None:
        """Remove an item from the cart.

        Args:
            product_name: Name of the product to remove
        """
        cart_item = self.page.locator(self.CART_ITEM).filter(has_text=product_name).first
        remove_btn = cart_item.get_by_role("button", name="Remove")
        await remove_btn.click(timeout=self.timeout_ms)
        # Wait for the item to be removed from DOM
        await cart_item.wait_for(state="detached", timeout=self.timeout_ms)

    async def proceed_to_checkout(self) -> None:
        """Click checkout button to proceed to checkout page."""
        await self.click(self.CHECKOUT_BUTTON)
        # Wait for navigation to checkout info page
        await self.wait_for_url_contains("checkout-step-one")

    async def continue_shopping(self) -> None:
        """Click continue shopping button to return to inventory."""
        await self.click(self.CONTINUE_SHOPPING_BUTTON)
        await self.wait_for_url_contains("inventory")

    async def get_total_items_count(self) -> int:
        """Get total number of items in cart.

        Returns:
            Total count of items
        """
        items = await self.get_cart_items()
        return sum(item["quantity"] for item in items)

    async def is_empty(self) -> bool:
        """Check if cart is empty.

        Returns:
            True if cart is empty, False otherwise
        """
        items = await self.get_cart_items()
        return len(items) == 0

    async def get_item_quantity(self, product_name: str) -> int:
        """Get the quantity of a specific item.

        Args:
            product_name: Name of the product

        Returns:
            Quantity of the item (0 if not found)
        """
        items = await self.get_cart_items()
        for item in items:
            if item["name"] == product_name:
                return int(item["quantity"])
        return 0

    async def get_subtotal(self) -> float:
        """Get the subtotal from the cart summary.

        Returns:
            Subtotal amount as float
        """
        # SauceDemo displays subtotal; we'll calculate it from items
        items = await self.get_cart_items()
        return float(sum(item["price"] * item["quantity"] for item in items))
