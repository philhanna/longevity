import os
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

from longevity.cli import main
from longevity.domain.models import LifeExpectancy


def _fake_life_expectancy():
    return LifeExpectancy(
        current_age=40.5,
        additional_years=20.3,
        total_years=60.8,
        estimated_death_date=datetime(2046, 4, 15),
    )


def test_invalid_date_format_returns_exit_code_2():
    assert main(["m", "not-a-date"]) == 2


def test_valid_args_return_exit_code_0(capsys):
    with patch("longevity.cli.get_life_expectancy", return_value=_fake_life_expectancy()):
        code = main(["m", "1986-01-01"])
    assert code == 0


def test_output_formatting(capsys):
    with patch("longevity.cli.get_life_expectancy", return_value=_fake_life_expectancy()):
        main(["m", "1986-01-01"])
    out = capsys.readouterr().out
    assert "current age      = 40.50" in out
    assert "additional years = 20.30" in out
    assert "total years      = 60.80" in out
    assert "estimated death  = 2046-04-15" in out


def test_use_case_error_returns_exit_code_1(capsys):
    with patch("longevity.cli.get_life_expectancy", side_effect=RuntimeError("boom")):
        code = main(["x", "1986-01-01"])
    assert code == 1
    assert "boom" in capsys.readouterr().out


def test_dob_parsed_correctly():
    captured_dob = {}

    def fake_use_case(sex, dob, **kwargs):
        captured_dob["dob"] = dob
        return _fake_life_expectancy()

    with patch("longevity.cli.get_life_expectancy", side_effect=fake_use_case):
        main(["f", "1990-06-15"])

    assert captured_dob["dob"] == date(1990, 6, 15)


def test_main_block_exit_code():
    src = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run(
        [sys.executable, "-m", "longevity.cli", "m", "not-a-date"],
        capture_output=True,
        env={**os.environ, "PYTHONPATH": src},
    )
    assert result.returncode == 2
