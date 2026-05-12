"""Pure domain utilities shared across the longevity package."""
import math


FLOAT64_EQUALITY_THRESHOLD = 1e-9


def almost_equal(a: float, b: float, threshold: float = FLOAT64_EQUALITY_THRESHOLD) -> bool:
    """Return True if a and b differ by no more than threshold."""
    return math.fabs(a - b) <= threshold


def parse_float(text: str) -> float:
    """Convert text to float, returning -1.0 if conversion fails."""
    try:
        return float(text)
    except Exception:
        return -1.0
