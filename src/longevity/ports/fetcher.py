"""LongevityHtmlFetcher port: abstract interface for retrieving SSA longevity HTML."""
from datetime import date
from typing import Protocol


class LongevityHtmlFetcher(Protocol):
    """Structural interface for any object that can fetch the SSA longevity page."""

    def fetch(self, *, sex: str, dob: date) -> str:
        """Fetch and return the raw HTML for the given sex and date of birth."""
        ...
