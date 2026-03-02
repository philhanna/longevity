from longevity.domain.services import parse_float


def test_parse_float():
    assert parse_float("29.95") == 29.95
    assert parse_float("13") == 13.0
    assert parse_float("") == -1.0
