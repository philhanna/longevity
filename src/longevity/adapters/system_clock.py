from __future__ import annotations

from datetime import datetime, timezone


class SystemClock:
    def now(self) -> datetime:
        # Use local time (naive) like Go's time.Now() for parity
        return datetime.now()
