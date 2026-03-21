from datetime import date, datetime

FORMATS = [
    "%Y-%m-%d",       # 1957-12-18  (ISO 8601 — try first)
    "%m/%d/%Y",       # 12/18/1957  (US conventional)
    "%d/%m/%Y",       # 18/12/1957  (European conventional)
    "%B %d, %Y",      # December 18, 1957
    "%b %d, %Y",      # Dec 18, 1957
    "%d %B %Y",       # 18 December 1957
    "%d %b %Y",       # 18 Dec 1957
    "%d-%B-%Y",       # 18-December-1942
    "%d-%b-%Y",       # 18-Jun-1942
]


def parse_date(text: str, fmt: str | None = None) -> date:
    """Parse a date string, trying common formats if no explicit fmt is given.

    Args:
        text: The date string to parse.
        fmt:  An explicit strptime format string. When provided, only that
              format is tried and ValueError is raised immediately on failure.

    Returns:
        A datetime.date.

    Raises:
        ValueError: If the string cannot be parsed.
    """
    if fmt is not None:
        return datetime.strptime(text, fmt).date()

    for f in FORMATS:
        try:
            return datetime.strptime(text, f).date()
        except ValueError:
            continue

    tried = ", ".join(FORMATS)
    raise ValueError(f"cannot parse date {text!r}. Formats tried: {tried}")
