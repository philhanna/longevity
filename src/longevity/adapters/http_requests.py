from __future__ import annotations

from datetime import date

import requests


SSA_URL = "https://www.ssa.gov/cgi-bin/longevity.cgi"
TIMEOUT_SECONDS = 15


class RequestsLongevityFetcher:
    """Outbound adapter: talks to SSA longevity CGI via HTTP POST."""

    def __init__(self, *, url: str = SSA_URL, timeout_seconds: int = TIMEOUT_SECONDS) -> None:
        self._url = url
        self._timeout = timeout_seconds

    def fetch(self, *, sex: str, dob: date) -> str:
        # SSA expects monthofbirth 0-based (Jan=0)
        values = {
            "sex": sex,
            "monthofbirth": str(dob.month - 1),
            "dayofbirth": str(dob.day),
            "yearofbirth": f"{dob.year:04d}",
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

        resp = requests.post(self._url, data=values, headers=headers, timeout=self._timeout)
        resp.raise_for_status()
        return resp.text
