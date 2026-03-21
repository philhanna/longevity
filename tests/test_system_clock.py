from datetime import datetime

from longevity.adapters.system_clock import SystemClock


def test_system_clock_returns_datetime():
    result = SystemClock().now()
    assert isinstance(result, datetime)
