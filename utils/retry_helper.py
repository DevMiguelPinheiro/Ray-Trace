"""Retry helper utilities for flaky test handling."""

import asyncio
import time
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, Awaitable, Callable, Type

from playwright.async_api import Page


def retry(
    max_attempts: int = 3,
    delay_ms: int = 500,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
) -> Callable:
    """Decorator for retrying a function on failure.

    Args:
        max_attempts: Maximum number of attempts
        delay_ms: Delay between attempts in milliseconds
        exceptions: Tuple of exception types to catch

    Returns:
        Decorated function that retries on failure
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(delay_ms / 1000.0)
            raise last_exception or Exception("Max retry attempts reached")

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay_ms / 1000.0)
            raise last_exception or Exception("Max retry attempts reached")

        # Return async or sync wrapper based on function
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


@asynccontextmanager
async def retry_action(max_attempts: int = 3, delay_ms: int = 200) -> Any:
    """Async context manager for retrying actions.

    Usage:
        async with retry_action(max_attempts=3, delay_ms=200):
            await page.click(selector)

    Args:
        max_attempts: Maximum number of attempts
        delay_ms: Delay between attempts in milliseconds

    Yields:
        None
    """
    last_exception = None
    for attempt in range(max_attempts):
        try:
            yield
            return
        except Exception as e:
            last_exception = e
            if attempt < max_attempts - 1:
                await asyncio.sleep(delay_ms / 1000.0)

    if last_exception:
        raise last_exception


async def retry_click(page: Page, locator: str, max_attempts: int = 3, delay_ms: int = 200) -> None:
    """Retry clicking an element.

    Args:
        page: Playwright Page object
        locator: Element locator
        max_attempts: Maximum number of attempts
        delay_ms: Delay between attempts in milliseconds
    """

    async def click_action() -> None:
        await page.click(locator)

    async with retry_action(max_attempts=max_attempts, delay_ms=delay_ms):
        await click_action()


async def wait_and_retry(
    fn: Callable[..., Awaitable[Any]],
    condition: Callable[[Any], bool],
    timeout_ms: int = 5000,
    poll_interval_ms: int = 100,
) -> Any:
    """Wait for a function to return a value that matches a condition.

    Args:
        fn: Async function to call repeatedly
        condition: Condition to check on the result
        timeout_ms: Timeout in milliseconds
        poll_interval_ms: Interval between polls in milliseconds

    Returns:
        The result value when condition is met

    Raises:
        TimeoutError: If timeout is exceeded
    """
    start_time = time.time()
    timeout_sec = timeout_ms / 1000.0

    while time.time() - start_time < timeout_sec:
        result = await fn()
        if condition(result):
            return result
        await asyncio.sleep(poll_interval_ms / 1000.0)

    raise TimeoutError(f"Condition not met within {timeout_ms}ms")
