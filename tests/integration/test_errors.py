import pytest
from httpx import ASGITransport, AsyncClient

from annexa.entrypoints.api import app
from annexa.shared.domain.exceptions import ResourceNotFoundError


@app.get("/_test_error")
def dummy_error_route() -> None:
    raise ResourceNotFoundError(resource_type="User", resource_id="123")


@pytest.mark.asyncio
async def test_domain_error_returns_rfc9457_problem_details() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/_test_error")

    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/problem+json"

    data = response.json()
    assert data["status"] == 404
    assert data["code"] == "RESOURCE_NOT_FOUND"
    assert data["title"] == "User not found"
    assert "user with id 123" in data["detail"]
