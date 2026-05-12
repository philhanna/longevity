from typing import Protocol


class LongevityHtmlParser(Protocol):
    def parse(self, html: str) -> tuple[float, float, float]: ...
    # returns (current_age, additional_years, total_years)
