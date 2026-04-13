"""Login page object."""

from playwright.async_api import Locator, Page

from config.environments import get_credentials
from config.settings import Settings
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page interactions."""

    # Locators
    USERNAME_FIELD = "[data-test='username']"
    PASSWORD_FIELD = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page, settings: Settings | None = None) -> None:
        """Initialize LoginPage.

        Args:
            page: Playwright Page object
            settings: Settings object for configuration
        """
        super().__init__(page, settings)

    async def navigate_to_login(self) -> None:
        """Navigate to the login page."""
        await self.navigate("/")

    async def login(self, username: str, password: str) -> None:
        """Login with username and password.

        Args:
            username: Username to login with
            password: Password to login with
        """
        await self.fill_input(self.USERNAME_FIELD, username)
        await self.fill_input(self.PASSWORD_FIELD, password)
        await self.click(self.LOGIN_BUTTON)
        # Wait for page to settle (works for both success and error cases)
        await self.wait_for_network_idle()

    async def login_as(self, user_type: str) -> None:
        """Login with a predefined user type.

        Args:
            user_type: Type of user (standard_user, locked_out_user, etc.)
        """
        credentials = get_credentials(self.settings.app_env, user_type)
        await self.login(credentials.username, credentials.password)

    async def get_error_message(self) -> str:
        """Get the error message text.

        Returns:
            Error message text
        """
        return await self.get_text(self.ERROR_MESSAGE)

    async def is_error_displayed(self) -> bool:
        """Check if error message is displayed.

        Returns:
            True if error is displayed, False otherwise
        """
        return await self.is_visible(self.ERROR_MESSAGE)

    def get_username_field(self) -> Locator:
        """Get username input field locator.

        Returns:
            Locator for username field
        """
        return self.get_element(self.USERNAME_FIELD)

    def get_password_field(self) -> Locator:
        """Get password input field locator.

        Returns:
            Locator for password field
        """
        return self.get_element(self.PASSWORD_FIELD)

    async def is_login_button_visible(self) -> bool:
        """Check if login button is visible.

        Returns:
            True if login button is visible, False otherwise
        """
        return await self.is_visible(self.LOGIN_BUTTON)
