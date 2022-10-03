from datetime import date

import pytest

from longevity import Requester


@pytest.mark.parametrize("name,dob,gender", [
    ("Keith Richards", date.fromisoformat("1943-12-18"), "m"),
    ("Barack Obama", date.fromisoformat("1961-08-04"), "m"),
])
def test_format_post_data(name, dob, gender):
    mm, dd, yyyy = Requester.get_date_fields(dob)
    expected = {
        "sex": gender,
        "monthofbirth": mm,
        "dayofbirth": dd,
        "yearofbirth": yyyy,
    }
    actual = Requester.format_post_data(gender, dob)
    assert actual == expected
