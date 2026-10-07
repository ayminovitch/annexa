import datetime

from annexa.shared.domain.time import Clock, SystemClock


def test_system_clock_return_utc_datetime() -> None:
    clock = SystemClock()
    now = clock.now()

    assert isinstance(now, datetime.datetime)


def test_system_clock_satisfies_protocol() -> None:
    clock: Clock = SystemClock()
    assert clock is not None
