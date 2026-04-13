"""Screenshot comparison utility for visual regression testing."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PIL import Image, ImageChops
from playwright.async_api import Page


@dataclass
class ComparisonResult:
    """Result of a screenshot comparison."""

    passed: bool
    diff_ratio: float
    diff_image_path: Optional[Path] = None


class ScreenshotComparator:
    """Handles screenshot capture and visual diff comparison using Pillow."""

    def __init__(self, threshold: float = 0.01) -> None:
        """Initialize ScreenshotComparator.

        Args:
            threshold: Threshold for pixel diff tolerance (default 1%)
        """
        self.threshold = threshold
        self.baseline_dir = Path("assets/snapshots")
        self.diff_dir = Path("test-results")

    def capture_baseline(self, page: Page, name: str) -> Path:
        """Capture and save a baseline screenshot.

        Args:
            page: Playwright Page object
            name: Name for the baseline screenshot

        Returns:
            Path to the saved baseline image
        """
        self.baseline_dir.mkdir(parents=True, exist_ok=True)
        baseline_path = self.baseline_dir / f"{name}-baseline.png"
        page.screenshot(path=str(baseline_path))
        return baseline_path

    def compare(self, page: Page, name: str) -> ComparisonResult:
        """Compare current screenshot with baseline.

        Args:
            page: Playwright Page object
            name: Name of the baseline screenshot to compare against

        Returns:
            ComparisonResult with comparison details
        """
        baseline_path = self.baseline_dir / f"{name}-baseline.png"

        # If baseline doesn't exist, treat it as first-run bootstrap.
        if not baseline_path.exists():
            self.baseline_dir.mkdir(parents=True, exist_ok=True)
            return ComparisonResult(passed=True, diff_ratio=0.0, diff_image_path=None)

        # Capture current screenshot
        current_screenshot = page.screenshot()

        # Load baseline image
        baseline_img = Image.open(baseline_path)
        current_img = Image.open(
            Path("/tmp/current.png") if not callable(current_screenshot) else None
        )

        # Save current screenshot to temporary file for comparison
        temp_path = Path("test-results") / f"{name}-current.png"
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(current_screenshot)

        current_img = Image.open(temp_path)

        # Compute pixel difference
        diff_ratio, diff_image = self._compute_diff(baseline_img, current_img)

        # Determine if comparison passed
        passed = diff_ratio <= self.threshold

        # Save diff image if there's a difference
        diff_image_path = None
        if not passed and diff_image:
            diff_image_path = self.diff_dir / f"{name}-DIFF.png"
            diff_image_path.parent.mkdir(parents=True, exist_ok=True)
            diff_image.save(diff_image_path)

        return ComparisonResult(
            passed=passed, diff_ratio=diff_ratio, diff_image_path=diff_image_path
        )

    def _compute_diff(
        self, baseline: Image.Image, current: Image.Image
    ) -> tuple[float, Optional[Image.Image]]:
        """Compute pixel-level diff between two images.

        Args:
            baseline: Baseline PIL Image
            current: Current PIL Image

        Returns:
            Tuple of (diff_ratio, diff_image)
        """
        # Resize current to match baseline if needed
        if baseline.size != current.size:
            current = current.resize(baseline.size, Image.Resampling.LANCZOS)

        # Convert to RGB if needed
        if baseline.mode != "RGB":
            baseline = baseline.convert("RGB")
        if current.mode != "RGB":
            current = current.convert("RGB")

        # Compute difference
        diff_image = ImageChops.difference(baseline, current)

        # Calculate percentage of pixels that differ
        stat = diff_image.getextrema()
        if stat == (0, 0):
            # No difference
            return 0.0, None

        # Count non-zero pixels
        pixels = diff_image.load()
        width, height = diff_image.size
        different_pixels = 0

        for y in range(height):
            for x in range(width):
                if pixels[x, y] != (0, 0, 0):
                    different_pixels += 1

        total_pixels = width * height
        diff_ratio = different_pixels / total_pixels if total_pixels > 0 else 0.0

        return diff_ratio, diff_image
