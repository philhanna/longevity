"""System clock adapter that returns the current local wall-clock time."""
from datetime import datetime


class SystemClock:
    """Clock implementation backed by the host system's local time."""

    def now(self) -> datetime:
        """Return the current local time as a naive datetime."""
        # Use local time (naive) like Go's time.Now() for parity
        return datetime.now()
