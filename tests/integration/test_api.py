import datetime

from httpx import ASGITransport, AsyncClient

from annexa.entrypoints.api import app
from annexa.shared.infrastructure.di import Container, get_container


class FakeClock:
    def __init__(self, fixed_time: datetime.datetime) -> None:
        self._fixed_time = fixed_time

    def now(self) -> datetime.datetime:
        return self._fixed_time


async def test_health_check_returns_ok_with_injected_clock() -> None:
    fixed_now = datetime.datetime(2026, 10, 7, 12, 0, 0, tzinfo=datetime.UTC)
    fake_container = Container()
    fake_container.clock = FakeClock(fixed_now)

    app.dependency_overrides[get_container] = lambda: fake_container

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["timestamp"] == "2026-10-07T12:00:00Z"

    app.dependency_overrides.clear()
