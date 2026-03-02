from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class LifeExpectancy:
    """Parsed result from SSA longevity calculator."""

    current_age: float
    additional_years: float
    total_years: float
    estimated_death_date: datetime
