"""Network interceptor utility for route mocking and failure injection."""

import json
from typing import Any

from playwright.async_api import Page, Route


class NetworkInterceptor:
    """Wraps Playwright's page.route() API with pre-built failure presets."""

    def __init__(self, page: Page) -> None:
        """Initialize NetworkInterceptor.

        Args:
            page: Playwright Page object
        """
        self.page = page
        self.intercepted_routes: dict[str, bool] = {}

    async def intercept_with_500(self, url_pattern: str) -> None:
        """Intercept a URL and return a synthetic 500 error response.

        Args:
            url_pattern: URL pattern to intercept (e.g., "**/api/inventory**")
        """

        async def handler(route: Route) -> None:
            await route.abort(error_code="failed")

        await self.page.route(url_pattern, handler)
        self.intercepted_routes[url_pattern] = True

    async def intercept_with_401(self, url_pattern: str) -> None:
        """Intercept a URL and return a 401 Unauthorized response.

        Args:
            url_pattern: URL pattern to intercept
        """

        async def handler(route: Route) -> None:
            await route.fulfill(
                status=401,
                content_type="application/json",
                body=json.dumps({"error": "Unauthorized"}),
            )

        await self.page.route(url_pattern, handler)
        self.intercepted_routes[url_pattern] = True

    async def intercept_with_timeout(self, url_pattern: str) -> None:
        """Intercept a URL and simulate a timeout by aborting the request.

        Args:
            url_pattern: URL pattern to intercept
        """

        async def handler(route: Route) -> None:
            await route.abort(error_code="timedout")

        await self.page.route(url_pattern, handler)
        self.intercepted_routes[url_pattern] = True

    async def intercept_with_custom(
        self, url_pattern: str, status: int, body: Any, content_type: str = "application/json"
    ) -> None:
        """Intercept a URL with a custom response.

        Args:
            url_pattern: URL pattern to intercept
            status: HTTP status code
            body: Response body (will be JSON-encoded if dict)
            content_type: Content-Type header value
        """

        async def handler(route: Route) -> None:
            response_body = body if isinstance(body, str) else json.dumps(body)
            await route.fulfill(status=status, content_type=content_type, body=response_body)

        await self.page.route(url_pattern, handler)
        self.intercepted_routes[url_pattern] = True

    async def restore(self, url_pattern: str) -> None:
        """Remove interception for a specific URL pattern.

        Args:
            url_pattern: URL pattern to stop intercepting
        """
        await self.page.unroute(url_pattern)
        self.intercepted_routes.pop(url_pattern, None)

    async def restore_all(self) -> None:
        """Remove all active route interceptions."""
        for url_pattern in list(self.intercepted_routes.keys()):
            await self.restore(url_pattern)

    async def __aenter__(self) -> "NetworkInterceptor":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit - restore all routes."""
        await self.restore_all()
