from longevity.domain.services import almost_equal, parse_float


def test_parse_float():
    assert parse_float("29.95") == 29.95
    assert parse_float("13") == 13.0
    assert parse_float("") == -1.0


def test_almost_equal_exact():
    assert almost_equal(1.0, 1.0)


def test_almost_equal_within_threshold():
    assert almost_equal(1.0, 1.0 + 1e-10)


def test_almost_equal_outside_threshold():
    assert not almost_equal(1.0, 1.1)


def test_almost_equal_custom_threshold():
    assert almost_equal(1.0, 1.05, threshold=0.1)
    assert not almost_equal(1.0, 1.2, threshold=0.1)
