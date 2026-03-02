import os
from datetime import date

import pytest

from longevity.application.use_cases import get_life_expectancy


@pytest.mark.skipif(os.environ.get("RUN_LIVE_SSA") != "1", reason="set RUN_LIVE_SSA=1 to run live SSA smoke test")
def test_live_request_smoke():
    resp = get_life_expectancy("m", date(1943, 12, 18))
    assert resp.current_age >= 80.0
