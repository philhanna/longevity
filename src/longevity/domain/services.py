from __future__ import annotations

import math
import re


ISO_FORMAT = "%Y-%m-%d"
FLOAT64_EQUALITY_THRESHOLD = 1e-9


def almost_equal(a: float, b: float, threshold: float = FLOAT64_EQUALITY_THRESHOLD) -> bool:
    return math.fabs(a - b) <= threshold


def parse_current_age(text: str) -> float:
    """Parse strings like '68' or '68 and 3 months' into a float age."""
    age = 0.0
    m = re.search(r"(\d+)", text or "")
    if m:
        age = float(m.group(1))

    m2 = re.search(r" and (\d+) month", text or "")
    if m2:
        age += float(m2.group(1)) / 12.0
    return age


def parse_float(text: str) -> float:
    try:
        return float(text)
    except Exception:
        return -1.0
