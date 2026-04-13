"""Base page object containing shared methods for all pages."""

from pathlib import Path
from typing import Optional

from playwright.async_api import Locator, Page

from config.settings import Settings


class BasePage:
    """Abstract parent class for all page objects."""

    def __init__(self, page: Page, settings: Optional[Settings] = None) -> None:
        """Initialize BasePage with a Playwright Page instance.

        Args:
            page: Playwright Page object
            settings: Settings object for configuration
        """
        self.page = page
        self.settings = settings or Settings()
        self.base_url = self.settings.base_url
        self.timeout_ms = self.settings.default_timeout_ms

    async def navigate(self, path: str = "") -> None:
        """Navigate to base_url + path and wait for page to load.

        Args:
            path: Path to append to base_url (defaults to empty string for root)
        """
        normalized_base = self.base_url.rstrip("/")
        normalized_path = path.lstrip("/")
        url = f"{normalized_base}/{normalized_path}" if normalized_path else f"{normalized_base}/"
        await self.page.goto(url, wait_until="load", timeout=60000)

    async def wait_for_url_contains(self, fragment: str, timeout_ms: Optional[int] = None) -> None:
        """Wait for URL to contain a specific fragment.

        Args:
            fragment: URL fragment to wait for
            timeout_ms: Timeout in milliseconds
        """
        timeout = timeout_ms or self.timeout_ms
        await self.page.wait_for_url(f"**/{fragment}**", timeout=timeout)

    async def take_named_screenshot(self, name: str) -> Path:
        """Take a named screenshot and save it to test-results directory.

        Args:
            name: Name for the screenshot (without extension)

        Returns:
            Path to the saved screenshot
        """
        test_results_dir = Path("test-results")
        test_results_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = test_results_dir / f"{name}.png"
        await self.page.screenshot(path=str(screenshot_path))
        return screenshot_path

    async def wait_for_network_idle(self, timeout_ms: Optional[int] = None) -> None:
        """Wait for network to become idle.

        Args:
            timeout_ms: Timeout in milliseconds
        """
        timeout = timeout_ms or self.timeout_ms * 2  # Double timeout for network
        await self.page.wait_for_load_state("networkidle", timeout=timeout)

    def get_element(self, locator: str) -> Locator:
        """Get a Locator object for the given selector.

        This is the single source of truth for element selection. All page objects
        should use this method to retrieve elements.

        Args:
            locator: Playwright locator string

        Returns:
            Locator object
        """
        return self.page.locator(locator)

    async def is_visible(self, locator: str) -> bool:
        """Check if an element is visible.

        Args:
            locator: Playwright locator string

        Returns:
            True if element is visible, False otherwise
        """
        element = self.get_element(locator)
        return bool(await element.is_visible(timeout=self.timeout_ms))

    async def is_enabled(self, locator: str) -> bool:
        """Check if an element is enabled.

        Args:
            locator: Playwright locator string

        Returns:
            True if element is enabled, False otherwise
        """
        element = self.get_element(locator)
        return bool(await element.is_enabled(timeout=self.timeout_ms))

    async def get_text(self, locator: str) -> str:
        """Get text content of an element.

        Args:
            locator: Playwright locator string

        Returns:
            Text content of the element
        """
        element = self.get_element(locator)
        return await element.text_content() or ""

    async def fill_input(self, locator: str, value: str) -> None:
        """Fill an input field with text.

        Args:
            locator: Playwright locator string
            value: Text to fill
        """
        element = self.get_element(locator)
        await element.fill(value)

    async def click(self, locator: str) -> None:
        """Click an element.

        Args:
            locator: Playwright locator string
        """
        element = self.get_element(locator)
        await element.click(timeout=self.timeout_ms)

    async def wait_for_element_visible(
        self, locator: str, timeout_ms: Optional[int] = None
    ) -> None:
        """Wait for an element to become visible.

        Args:
            locator: Playwright locator string
            timeout_ms: Timeout in milliseconds
        """
        timeout = timeout_ms or self.timeout_ms
        element = self.get_element(locator)
        await element.wait_for(state="visible", timeout=timeout)

    async def wait_for_element_hidden(self, locator: str, timeout_ms: Optional[int] = None) -> None:
        """Wait for an element to become hidden.

        Args:
            locator: Playwright locator string
            timeout_ms: Timeout in milliseconds
        """
        timeout = timeout_ms or self.timeout_ms
        element = self.get_element(locator)
        await element.wait_for(state="hidden", timeout=timeout)
