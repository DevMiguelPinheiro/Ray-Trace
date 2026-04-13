"""Authentication tests - login, logout, user scenarios."""

import pytest

from pages.login_page import LoginPage


@pytest.mark.smoke
async def test_login_standard_user(login_page: LoginPage) -> None:
    """Test login with standard user."""
    await login_page.navigate_to_login()
    await login_page.login_as("standard_user")
    # Assert we're on inventory page
    assert "inventory" in login_page.page.url


@pytest.mark.smoke
async def test_login_with_invalid_credentials(login_page: LoginPage) -> None:
    """Test login with invalid credentials."""
    await login_page.navigate_to_login()
    await login_page.login("invalid_user", "wrong_password")
    # Assert error is displayed
    assert await login_page.is_error_displayed()


@pytest.mark.smoke
async def test_locked_out_user_cannot_login(login_page: LoginPage) -> None:
    """Test that locked_out_user gets appropriate error."""
    await login_page.navigate_to_login()
    await login_page.login_as("locked_out_user")
    # Assert error is displayed
    assert await login_page.is_error_displayed()


@pytest.mark.regression
async def test_logout(inventory_page) -> None:
    """Test logout functionality."""
    await inventory_page.navigate_to_inventory()
    page = inventory_page.page

    # Verify we're on inventory page
    assert "inventory" in page.url

    # Click hamburger menu button with explicit wait
    hamburger = page.get_by_role("button").filter(has_text="Open Menu")
    await hamburger.click()

    # Wait for logout button and click it
    logout_btn = page.get_by_role("link", name="Logout")
    await logout_btn.wait_for(state="visible", timeout=10000)
    await logout_btn.click()

    # Wait for navigation to login page
    await page.wait_for_url("**/", timeout=10000)
    assert "inventory" not in page.url


@pytest.mark.regression
async def test_username_field_is_visible(login_page: LoginPage) -> None:
    """Test that username field is visible on login page."""
    await login_page.navigate_to_login()
    username_field = login_page.get_username_field()
    assert await username_field.is_visible()


@pytest.mark.regression
async def test_password_field_is_visible(login_page: LoginPage) -> None:
    """Test that password field is visible on login page."""
    await login_page.navigate_to_login()
    password_field = login_page.get_password_field()
    assert await password_field.is_visible()


@pytest.mark.regression
async def test_login_button_is_visible(login_page: LoginPage) -> None:
    """Test that login button is visible on login page."""
    await login_page.navigate_to_login()
    assert await login_page.is_login_button_visible()
