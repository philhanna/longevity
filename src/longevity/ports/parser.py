"""LongevityHtmlParser port: abstract interface for parsing SSA longevity HTML."""
from typing import Protocol


class LongevityHtmlParser(Protocol):
    """Structural interface for any object that can parse SSA longevity HTML."""

    def parse(self, html: str) -> tuple[float, float, float]:
        """Parse HTML and return (current_age, additional_years, total_years)."""
        ...
