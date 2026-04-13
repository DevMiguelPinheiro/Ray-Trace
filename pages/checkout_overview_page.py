"""Checkout Overview page object (step 2 of checkout)."""

from playwright.async_api import Page

from config.settings import Settings
from pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    """Checkout overview page - order review and final confirmation."""

    # Locators
    CART_ITEM = "[data-test='cart-item'], [data-test='inventory-item'], .cart_item"
    ITEM_NAME = "[data-test='inventory-item-name']"
    ITEM_PRICE = "[data-test='inventory-item-price']"
    ITEM_QUANTITY = "[data-test='item-quantity']"
    SUBTOTAL_LABEL = "[data-test='subtotal-label']"
    TAX_LABEL = "[data-test='tax-label']"
    TOTAL_LABEL = "[data-test='total-label']"
    FINISH_BUTTON = "[data-test='finish']"
    CANCEL_BUTTON = "[data-test='cancel']"

    def __init__(self, page: Page, settings: Settings | None = None) -> None:
        """Initialize CheckoutOverviewPage.

        Args:
            page: Playwright Page object
            settings: Settings object for configuration
        """
        super().__init__(page, settings)

    async def navigate_to_checkout_overview(self) -> None:
        """Navigate to the checkout overview page."""
        await self.navigate("/checkout-step-two.html")
        await self.wait_for_element_visible(self.FINISH_BUTTON)

    async def get_order_items(self) -> list[dict]:
        """Get all items in the order.

        Returns:
            List of dictionaries with item details
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

    async def get_subtotal(self) -> float:
        """Get the subtotal from the order summary.

        Returns:
            Subtotal amount as float
        """
        subtotal_text = await self.get_text(self.SUBTOTAL_LABEL)
        # Extract the price from text like "Subtotal: $X.XX"
        return self._parse_price_from_label(subtotal_text)

    async def get_tax(self) -> float:
        """Get the tax from the order summary.

        Returns:
            Tax amount as float
        """
        tax_text = await self.get_text(self.TAX_LABEL)
        return self._parse_price_from_label(tax_text)

    async def get_total(self) -> float:
        """Get the total from the order summary.

        Returns:
            Total amount as float
        """
        total_text = await self.get_text(self.TOTAL_LABEL)
        return self._parse_price_from_label(total_text)

    async def finish_purchase(self) -> None:
        """Click finish button to complete the purchase."""
        await self.click(self.FINISH_BUTTON)
        # Wait for navigation to checkout complete
        await self.wait_for_url_contains("checkout-complete")

    async def cancel_order(self) -> None:
        """Click cancel button to return to inventory."""
        await self.click(self.CANCEL_BUTTON)
        await self.wait_for_url_contains("inventory")

    async def get_item_count(self) -> int:
        """Get the number of items in the order.

        Returns:
            Total number of items
        """
        items = await self.get_order_items()
        return sum(item["quantity"] for item in items)

    async def is_overview_page_loaded(self) -> bool:
        """Check if overview page is fully loaded.

        Returns:
            True if page is loaded, False otherwise
        """
        return await self.is_visible(self.FINISH_BUTTON)

    @staticmethod
    def _parse_price_from_label(label_text: str) -> float:
        """Parse price from a label string.

        Args:
            label_text: Label text containing a price

        Returns:
            Price as float
        """
        # Extract price like "$X.XX" from text
        import re

        match = re.search(r"\$([0-9]+\.[0-9]{2})", label_text)
        return float(match.group(1)) if match else 0.0
