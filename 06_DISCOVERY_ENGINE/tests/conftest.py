from datetime import datetime, timedelta, timezone

import pytest


class FakeClock:
    """Deterministic, strictly-increasing clock for non-flaky timestamp tests.

    Each call returns the current instant then advances by ``step``, so
    tests can assert ordering (``history[i].at < history[i + 1].at``)
    without ever touching a real wall clock.
    """

    def __init__(self, start: datetime | None = None, step: timedelta = timedelta(seconds=1)):
        self._current = start or datetime(2026, 1, 1, tzinfo=timezone.utc)
        self._step = step

    def __call__(self) -> datetime:
        now = self._current
        self._current = self._current + self._step
        return now


@pytest.fixture
def fake_clock() -> FakeClock:
    return FakeClock()
