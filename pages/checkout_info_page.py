"""Checkout Information page object (step 1 of checkout)."""

from playwright.async_api import Page

from config.settings import Settings
from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    """Checkout info page - shipping/billing information."""

    # Locators
    FIRST_NAME_FIELD = "[data-test='firstName']"
    LAST_NAME_FIELD = "[data-test='lastName']"
    POSTAL_CODE_FIELD = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    CANCEL_BUTTON = "[data-test='cancel']"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page, settings: Settings | None = None) -> None:
        """Initialize CheckoutInfoPage.

        Args:
            page: Playwright Page object
            settings: Settings object for configuration
        """
        super().__init__(page, settings)

    async def navigate_to_checkout_info(self) -> None:
        """Navigate to the checkout info page."""
        await self.navigate("/checkout-step-one.html")
        await self.wait_for_element_visible(self.FIRST_NAME_FIELD)

    async def fill_first_name(self, value: str) -> None:
        """Fill the first name field.

        Args:
            value: First name to fill
        """
        await self.fill_input(self.FIRST_NAME_FIELD, value)

    async def fill_last_name(self, value: str) -> None:
        """Fill the last name field.

        Args:
            value: Last name to fill
        """
        await self.fill_input(self.LAST_NAME_FIELD, value)

    async def fill_postal_code(self, value: str) -> None:
        """Fill the postal code field.

        Args:
            value: Postal code to fill
        """
        await self.fill_input(self.POSTAL_CODE_FIELD, value)

    async def fill_shipping_info(self, first: str, last: str, postal: str) -> None:
        """Fill all shipping information fields.

        Args:
            first: First name
            last: Last name
            postal: Postal code
        """
        await self.fill_first_name(first)
        await self.fill_last_name(last)
        await self.fill_postal_code(postal)

    async def continue_to_overview(self) -> None:
        """Click continue button to proceed to checkout overview page."""
        await self.click(self.CONTINUE_BUTTON)
        # In validation scenarios, the page may stay on step one and show an error.
        try:
            await self.wait_for_url_contains("checkout-step-two", timeout_ms=5000)
        except Exception:
            pass

    async def cancel_checkout(self) -> None:
        """Click cancel button to return to cart."""
        await self.click(self.CANCEL_BUTTON)
        await self.wait_for_url_contains("cart")

    async def get_form_validation_error(self) -> str:
        """Get the form validation error message.

        Returns:
            Error message text
        """
        return await self.get_text(self.ERROR_MESSAGE)

    async def is_error_displayed(self) -> bool:
        """Check if validation error is displayed.

        Returns:
            True if error is displayed, False otherwise
        """
        return await self.is_visible(self.ERROR_MESSAGE)

    async def is_continue_button_enabled(self) -> bool:
        """Check if continue button is enabled.

        Returns:
            True if button is enabled, False otherwise
        """
        return await self.is_enabled(self.CONTINUE_BUTTON)

    async def are_all_fields_visible(self) -> bool:
        """Check if all form fields are visible.

        Returns:
            True if all fields are visible, False otherwise
        """
        return (
            await self.is_visible(self.FIRST_NAME_FIELD)
            and await self.is_visible(self.LAST_NAME_FIELD)
            and await self.is_visible(self.POSTAL_CODE_FIELD)
        )
