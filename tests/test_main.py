from datetime import date

import pytest

from longevity import Main


@pytest.fixture
def subject():
    parms = {
        "name": "Keith Richards",
        "dob": "1943-12-18",
        "sex": "m",
        "monthofbirth": "11",
        "dayofbirth": "18",
        "yearofbirth": "1943",
    }
    main = Main(**parms)
    requester = main.run()
    return requester


def test_subject(subject):
    assert subject.sex == "m"
    assert subject.dob == date.fromisoformat("1943-12-18")
    assert subject.death_date.year == 2032
