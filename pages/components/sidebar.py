"""Sidebar menu component."""

from playwright.async_api import Page


class SidebarMenu:
    """Slide-out sidebar menu component."""

    # Locators
    SIDEBAR = "[data-test='sidebar'], .bm-menu-wrap"
    LOGOUT_BUTTON = "[data-test='logout-sidebar-link']"
    RESET_APP_BUTTON = "[data-test='reset-sidebar-link']"
    CLOSE_BUTTON = (
        "[data-test='menu-button-close'], [data-test='close-menu'], #react-burger-cross-btn"
    )
    ABOUT_BUTTON = "[data-test='about-sidebar-link']"
    ALL_ITEMS_BUTTON = "[data-test='inventory-sidebar-link']"

    def __init__(self, page: Page) -> None:
        """Initialize SidebarMenu component.

        Args:
            page: Playwright Page object
        """
        self.page = page

    async def logout(self) -> None:
        """Click the logout button to logout."""
        # First ensure sidebar is visible by clicking hamburger menu if needed
        menu_btn = self.page.locator(
            "[data-test='hamburger-menu-btn'], [data-test='open-menu'], #react-burger-menu-btn"
        )
        if not await self.is_visible():
            await menu_btn.first.wait_for(state="visible", timeout=15000)
            await menu_btn.first.click(force=True, timeout=15000)
            await self._wait_until_open()

        logout_btn = self.page.locator(self.LOGOUT_BUTTON)
        await logout_btn.wait_for(state="visible", timeout=15000)
        await logout_btn.evaluate("el => el.click()")

    async def reset_app_state(self) -> None:
        """Click the reset app state button to clear cart and app state."""
        # First ensure sidebar is visible by clicking hamburger menu if needed
        menu_btn = self.page.locator(
            "[data-test='hamburger-menu-btn'], [data-test='open-menu'], #react-burger-menu-btn"
        )
        if not await self.is_visible():
            await menu_btn.first.wait_for(state="visible", timeout=15000)
            await menu_btn.first.click(force=True, timeout=15000)
            await self._wait_until_open()

        reset_btn = self.page.locator(self.RESET_APP_BUTTON)
        await reset_btn.wait_for(state="visible", timeout=15000)
        await reset_btn.evaluate("el => el.click()")

    async def close(self) -> None:
        """Click the close button to close the sidebar."""
        close_btn = self.page.locator(self.CLOSE_BUTTON)
        await close_btn.first.wait_for(state="visible", timeout=15000)
        await close_btn.first.click(timeout=15000)
        await self._wait_until_closed()

    async def is_visible(self) -> bool:
        """Check if sidebar is visible.

        Returns:
            True if sidebar is visible, False otherwise
        """
        sidebar = self.page.locator(self.SIDEBAR).first
        if not await sidebar.is_visible():
            return False
        box = await sidebar.bounding_box()
        if box is None:
            return False
        # react-burger-menu keeps element visible but shifted offscreen when closed.
        return box.get("x", -1) >= 0

    async def open_about(self) -> None:
        """Click the about button to open about page."""
        about_btn = self.page.locator(self.ABOUT_BUTTON)
        await about_btn.wait_for(state="visible", timeout=15000)
        await about_btn.click(timeout=15000)

    async def open_all_items(self) -> None:
        """Click all items button to return to inventory."""
        all_items_btn = self.page.locator(self.ALL_ITEMS_BUTTON)
        await all_items_btn.wait_for(state="visible", timeout=15000)
        await all_items_btn.click(timeout=15000)

    async def _wait_until_open(self) -> None:
        """Wait until sidebar animation finishes and panel is in viewport."""
        await self.page.wait_for_function(
            """() => {
                const el = document.querySelector('.bm-menu-wrap');
                if (!el) return false;
                const rect = el.getBoundingClientRect();
                return rect.x >= 0;
            }""",
            timeout=15000,
        )

    async def _wait_until_closed(self) -> None:
        """Wait until sidebar is moved out of viewport after closing."""
        await self.page.wait_for_function(
            """() => {
                const el = document.querySelector('.bm-menu-wrap');
                if (!el) return true;
                const rect = el.getBoundingClientRect();
                return rect.right <= 0 || rect.x < 0;
            }""",
            timeout=15000,
        )
