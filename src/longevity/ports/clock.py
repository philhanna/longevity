"""Clock port: abstract interface for obtaining the current time."""
from datetime import datetime
from typing import Protocol


class Clock(Protocol):
    """Structural interface for any object that can supply the current datetime."""

    def now(self) -> datetime:
        """Return the current datetime."""
        ...
