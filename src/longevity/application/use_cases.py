from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta

from ..domain.models import LifeExpectancy
from .ports import Clock, LongevityHtmlFetcher, LongevityHtmlParser
from ..adapters.bs4_parser import Bs4LongevityParser
from ..adapters.http_requests import RequestsLongevityFetcher
from ..adapters.system_clock import SystemClock


class LongevityError(RuntimeError):
    pass


def _validate_inputs(sex: str, dob: date) -> None:
    if sex not in {"m", "f"}:
        raise LongevityError('sex must be "m" or "f"')
    if not isinstance(dob, date):
        raise LongevityError("dob must be a datetime.date")


def get_life_expectancy(
    sex: str,
    dob: date,
    *,
    fetcher: LongevityHtmlFetcher | None = None,
    parser: LongevityHtmlParser | None = None,
    clock: Clock | None = None,
) -> LifeExpectancy:
    """Use case: fetch SSA longevity HTML and return a parsed LifeExpectancy.

    Hexagonal notes:
    - This function is the "application service" / use case.
    - It depends only on *ports* (interfaces) and domain models.
    - Default implementations are provided via adapters (requests + bs4).
    """
    _validate_inputs(sex, dob)

    fetcher = fetcher or RequestsLongevityFetcher()
    parser = parser or Bs4LongevityParser()
    clock = clock or SystemClock()

    content = fetcher.fetch(sex=sex, dob=dob)

    try:
        current_age, additional_years, total_years = parser.parse(content)
    except Exception as e:
        raise LongevityError(f"failed to parse SSA response: {e}") from e

    # mimic Go logic: estimated death date = now + additionalYears * 365.25 days
    hours = additional_years * 365.25 * 24.0
    estimated_death_date = clock.now() + timedelta(hours=hours)

    return LifeExpectancy(
        current_age=current_age,
        additional_years=additional_years,
        total_years=total_years,
        estimated_death_date=estimated_death_date,
    )
