"""longevity - SSA life expectancy scraper.

Public API is intentionally small: use `get_life_expectancy`.
"""

from .application.use_cases import get_life_expectancy
from .domain.models import LifeExpectancy

__all__ = ["get_life_expectancy", "LifeExpectancy"]
