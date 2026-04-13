"""Checkout Complete page object (confirmation page)."""

from playwright.async_api import Page

from config.settings import Settings
from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    """Checkout complete page - order confirmation."""

    # Locators
    CONFIRMATION_HEADER = "[data-test='complete-header']"
    CONFIRMATION_MESSAGE = "[data-test='complete-text']"
    BACK_HOME_BUTTON = "[data-test='back-to-products']"
    PONY_EXPRESS = "[data-test='pony-express']"

    def __init__(self, page: Page, settings: Settings | None = None) -> None:
        """Initialize CheckoutCompletePage.

        Args:
            page: Playwright Page object
            settings: Settings object for configuration
        """
        super().__init__(page, settings)

    async def navigate_to_checkout_complete(self) -> None:
        """Navigate to the checkout complete page."""
        await self.navigate("/checkout-complete.html")
        await self.wait_for_element_visible(self.CONFIRMATION_HEADER)

    async def is_order_confirmed(self) -> bool:
        """Check if order was successfully confirmed.

        Returns:
            True if confirmation elements are visible, False otherwise
        """
        return await self.is_visible(self.CONFIRMATION_HEADER)

    async def get_confirmation_header(self) -> str:
        """Get the confirmation header text.

        Returns:
            Confirmation header text
        """
        return await self.get_text(self.CONFIRMATION_HEADER)

    async def get_confirmation_message(self) -> str:
        """Get the confirmation message text.

        Returns:
            Confirmation message text
        """
        header = (await self.get_text(self.CONFIRMATION_HEADER)).strip()
        body = (await self.get_text(self.CONFIRMATION_MESSAGE)).strip()
        return f"{header} {body}".strip()

    async def back_to_home(self) -> None:
        """Click back to home button to return to inventory."""
        await self.click(self.BACK_HOME_BUTTON)
        await self.wait_for_url_contains("inventory")

    async def is_pony_express_visible(self) -> bool:
        """Check if the pony express icon is visible.

        Returns:
            True if pony express image is visible, False otherwise
        """
        return await self.is_visible(self.PONY_EXPRESS)
