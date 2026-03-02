import math


FLOAT64_EQUALITY_THRESHOLD = 1e-9


def almost_equal(a: float, b: float, threshold: float = FLOAT64_EQUALITY_THRESHOLD) -> bool:
    return math.fabs(a - b) <= threshold


def parse_float(text: str) -> float:
    try:
        return float(text)
    except Exception:
        return -1.0
