from datetime import date
from typing import Protocol


class LongevityHtmlFetcher(Protocol):
    def fetch(self, *, sex: str, dob: date) -> str: ...
