"""Product card component (reusable in inventory list)."""

from playwright.async_api import Locator, Page


class ProductCard:
    """Reusable product card component."""

    def __init__(self, page: Page, product_name: str) -> None:
        """Initialize ProductCard component.

        Args:
            page: Playwright Page object
            product_name: Name of the product this card represents
        """
        self.page = page
        self.product_name = product_name
        # Build a locator for this specific product card
        self.card_locator = page.locator(
            f"[data-test='inventory-item'] >> text={product_name}"
        ).first.locator("..")

    async def get_name(self) -> str:
        """Get the product name.

        Returns:
            Product name
        """
        name_element = self.card_locator.locator("[data-test='inventory-item-name']")
        return await name_element.text_content() or ""

    async def get_price(self) -> float:
        """Get the product price.

        Returns:
            Price as float
        """
        price_element = self.card_locator.locator("[data-test='inventory-item-price']")
        price_text = await price_element.text_content() or "$0.00"
        return float(price_text.replace("$", ""))

    async def get_description(self) -> str:
        """Get the product description.

        Returns:
            Product description
        """
        desc_element = self.card_locator.locator("[data-test='inventory-item-desc']")
        return await desc_element.text_content() or ""

    async def add_to_cart(self) -> None:
        """Click the add to cart button."""
        add_btn = self.card_locator.locator("button:has-text('Add to cart')")
        await add_btn.click()

    async def remove_from_cart(self) -> None:
        """Click the remove from cart button."""
        remove_btn = self.card_locator.locator("button:has-text('Remove')")
        await remove_btn.click()

    async def click_product(self) -> None:
        """Click on the product to open detail page."""
        product_link = self.card_locator.locator("[data-test='inventory-item-name']")
        await product_link.click()

    async def is_add_button_visible(self) -> bool:
        """Check if add to cart button is visible.

        Returns:
            True if button is visible, False otherwise
        """
        add_btn = self.card_locator.locator("button:has-text('Add to cart')")
        return bool(await add_btn.is_visible())

    async def is_remove_button_visible(self) -> bool:
        """Check if remove button is visible.

        Returns:
            True if button is visible, False otherwise
        """
        remove_btn = self.card_locator.locator("button:has-text('Remove')")
        return bool(await remove_btn.is_visible())

    def get_card_locator(self) -> Locator:
        """Get the underlying card locator.

        Returns:
            Locator object for this card
        """
        return self.card_locator
