from __future__ import annotations

from datetime import date, datetime
from typing import Protocol


class LongevityHtmlFetcher(Protocol):
    def fetch(self, *, sex: str, dob: date) -> str: ...


class LongevityHtmlParser(Protocol):
    def parse(self, html: str) -> tuple[float, float, float]: ...
    # returns (current_age, additional_years, total_years)


class Clock(Protocol):
    def now(self) -> datetime: ...
