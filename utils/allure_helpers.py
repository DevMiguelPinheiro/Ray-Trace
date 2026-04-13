"""Allure reporting helper utilities."""

import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Optional

from playwright.async_api import Page

try:
    import allure
except ImportError:
    allure = None  # type: ignore


logger = logging.getLogger(__name__)


@contextmanager
def allure_step(title: str) -> Generator[None, None, None]:
    """Context manager for creating an Allure step with console logging.

    Args:
        title: Title of the step

    Yields:
        None
    """
    logger.info(f"Step: {title}")
    if allure:
        with allure.step(title):
            yield
    else:
        yield


def attach_screenshot(page: Page, name: str) -> Optional[Path]:
    """Capture and attach a screenshot to the Allure report.

    Args:
        page: Playwright Page object
        name: Name for the screenshot

    Returns:
        Path to the saved screenshot, or None if Allure is not available
    """
    test_results_dir = Path("test-results")
    test_results_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = test_results_dir / f"{name}.png"

    try:
        page.screenshot(path=str(screenshot_path))
        if allure:
            allure.attach.file(
                str(screenshot_path),
                name=f"{name}.png",
                attachment_type=allure.attachment_type.PNG,
            )
        logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
    except Exception as e:
        logger.error(f"Failed to capture screenshot: {e}")
        return None


def attach_page_source(page: Page, name: str) -> Optional[Path]:
    """Capture and attach page HTML source to the Allure report.

    Args:
        page: Playwright Page object
        name: Name for the attachment

    Returns:
        Path to the saved HTML file, or None if Allure is not available
    """
    test_results_dir = Path("test-results")
    test_results_dir.mkdir(parents=True, exist_ok=True)
    html_path = test_results_dir / f"{name}_source.html"

    try:
        content = page.content()
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)

        if allure:
            allure.attach.file(
                str(html_path),
                name=f"{name}_source.html",
                attachment_type=allure.attachment_type.HTML,
            )
        logger.info(f"Page source saved: {html_path}")
        return html_path
    except Exception as e:
        logger.error(f"Failed to capture page source: {e}")
        return None


def attach_trace(trace_path: Path) -> None:
    """Attach a Playwright trace file to the Allure report.

    Args:
        trace_path: Path to the trace.zip file
    """
    if not trace_path.exists():
        logger.warning(f"Trace file not found: {trace_path}")
        return

    try:
        if allure:
            allure.attach.file(
                str(trace_path),
                name="trace.zip",
                attachment_type=allure.attachment_type.ZIP,
            )
        logger.info(f"Trace attached: {trace_path}")
    except Exception as e:
        logger.error(f"Failed to attach trace: {e}")
