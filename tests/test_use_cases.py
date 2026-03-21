from datetime import date, datetime
from unittest.mock import MagicMock

import pytest

from longevity.application.use_cases import LongevityError, get_life_expectancy


def _make_mocks(current_age=40.0, additional_years=20.0, total_years=60.0, now=None):
    if now is None:
        now = datetime(2026, 1, 1)
    fetcher = MagicMock()
    fetcher.fetch.return_value = "<html/>"
    parser = MagicMock()
    parser.parse.return_value = (current_age, additional_years, total_years)
    clock = MagicMock()
    clock.now.return_value = now
    return fetcher, parser, clock


def test_returns_life_expectancy():
    fetcher, parser, clock = _make_mocks()
    result = get_life_expectancy("m", date(1986, 1, 1), fetcher=fetcher, parser=parser, clock=clock)
    assert result.current_age == 40.0
    assert result.additional_years == 20.0
    assert result.total_years == 60.0


def test_fetcher_receives_correct_args():
    fetcher, parser, clock = _make_mocks()
    dob = date(1990, 6, 15)
    get_life_expectancy("f", dob, fetcher=fetcher, parser=parser, clock=clock)
    fetcher.fetch.assert_called_once_with(sex="f", dob=dob)


def test_death_date_calculation():
    now = datetime(2026, 1, 1)
    fetcher, parser, clock = _make_mocks(additional_years=10.0, now=now)
    result = get_life_expectancy("m", date(1986, 1, 1), fetcher=fetcher, parser=parser, clock=clock)
    expected_hours = 10.0 * 365.25 * 24.0
    delta = result.estimated_death_date - now
    assert abs(delta.total_seconds() - expected_hours * 3600) < 1


def test_invalid_sex_raises():
    fetcher, parser, clock = _make_mocks()
    with pytest.raises(LongevityError, match="sex"):
        get_life_expectancy("x", date(1986, 1, 1), fetcher=fetcher, parser=parser, clock=clock)


def test_invalid_dob_type_raises():
    fetcher, parser, clock = _make_mocks()
    with pytest.raises(LongevityError, match="dob"):
        get_life_expectancy("m", "1986-01-01", fetcher=fetcher, parser=parser, clock=clock)  # type: ignore[arg-type]


def test_parser_exception_wrapped_in_longevity_error():
    fetcher, parser, clock = _make_mocks()
    parser.parse.side_effect = ValueError("bad HTML")
    with pytest.raises(LongevityError, match="failed to parse"):
        get_life_expectancy("m", date(1986, 1, 1), fetcher=fetcher, parser=parser, clock=clock)
