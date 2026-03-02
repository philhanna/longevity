from longevity.domain.services import almost_equal, parse_current_age, parse_float


def test_parse_current_age_cases():
    assert parse_current_age("68") == 68.0
    assert almost_equal(parse_current_age("68 and 3 months"), 68.25)
    assert almost_equal(parse_current_age("68 and 1 month"), 68.0 + 1.0/12.0)
    assert parse_current_age("bogus") == 0.0


def test_parse_float():
    assert parse_float("29.95") == 29.95
    assert parse_float("13") == 13.0
    assert parse_float("") == -1.0
