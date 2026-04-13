"""Root test conftest - imports fixtures and sets up test environment."""

# Import all fixtures from fixtures package
from fixtures.auth import auth_context, authenticated_context
from fixtures.browsers import browser, context, page
from fixtures.pages import (
    cart_page,
    checkout_complete_page,
    checkout_info_page,
    checkout_overview_page,
    inventory_page,
    login_page,
    sidebar_menu,
    site_header,
)

__all__ = [
    "auth_context",
    "authenticated_context",
    "browser",
    "context",
    "page",
    "login_page",
    "inventory_page",
    "cart_page",
    "checkout_info_page",
    "checkout_overview_page",
    "checkout_complete_page",
    "site_header",
    "sidebar_menu",
]
