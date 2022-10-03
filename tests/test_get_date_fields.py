from datetime import date

import pytest

from longevity import Requester


@pytest.mark.parametrize("name,dob,mm,dd,yyyy", [
    ("Keith Richards", date.fromisoformat("1943-12-18"), "11", "18", "1943"),
    ("Barack Obama", date.fromisoformat("1961-08-04"), "7", "04", "1961"),
])
def test_get_date_fields(name, dob, mm, dd, yyyy):
    assert (mm, dd, yyyy) == Requester.get_date_fields(dob)
