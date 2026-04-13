"""Site header component."""

from playwright.async_api import Page


class SiteHeader:
    """Top navigation header component."""

    # Locators
    CART_BADGE = "[data-test='shopping-cart-badge']"
    CART_LINK = "[data-test='shopping-cart-link']"
    MENU_BUTTON = (
        "[data-test='hamburger-menu-btn'], [data-test='open-menu'], #react-burger-menu-btn"
    )
    HEADER = "[data-test='primary-header']"

    def __init__(self, page: Page) -> None:
        """Initialize SiteHeader component.

        Args:
            page: Playwright Page object
        """
        self.page = page

    async def get_cart_badge_count(self) -> int:
        """Get the number displayed in the cart badge.

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
            pass
        return 0

    async def open_cart(self) -> None:
        """Click the cart link to open the cart page."""
        cart_link = self.page.locator(self.CART_LINK)
        await cart_link.wait_for(state="visible", timeout=15000)
        await cart_link.click(timeout=15000)

    async def open_sidebar_menu(self) -> None:
        """Click the hamburger menu button to open the sidebar."""
        menu_btn = self.page.locator(self.MENU_BUTTON)
        # Ensure button is visible and actionable before clicking
        await menu_btn.first.wait_for(state="visible", timeout=15000)
        await menu_btn.first.click(timeout=15000)
        await self.page.wait_for_function(
            """() => {
                const el = document.querySelector('.bm-menu-wrap');
                if (!el) return true;
                const rect = el.getBoundingClientRect();
                return rect.x >= 0;
            }""",
            timeout=15000,
        )

    async def is_visible(self) -> bool:
        """Check if header is visible.

        Returns:
            True if header is visible, False otherwise
        """
        return bool(await self.page.locator(self.HEADER).is_visible())
