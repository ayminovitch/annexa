import pytest
from collections.abc import AsyncGenerator
from httpx import ASGITransport, AsyncClient

from annexa.entrypoints.api import app
from annexa.entrypoints.di import Container, get_container
from annexa.identity.application.security import create_access_token
from annexa.identity.domain.entities import Role, User
from annexa.shared.domain.ids import TenantId, UserId
from annexa.shared.domain.time import SystemClock
from annexa.config.settings import settings

import uuid


# --- MOCKS ---

class FakeLLMProvider:
    async def generate_text(self, prompt: str) -> str:
        return "Not implemented in this test."

    async def generate_text_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        yield "According to "
        yield "Article 5 of the "
        yield "AI Act..."


def create_test_jwt() -> str:
    clock = SystemClock()
    user = User(
        id=UserId(uuid.uuid4()),
        tenant_id=TenantId(uuid.uuid4()),
        email="test@annexa.eu",
        role=Role.ENGINEER,
        created_at=clock.now()
    )
    return create_access_token(user, clock, settings.jwt_secret, settings.jwt_algorithm, 15)


# --- TESTS ---

@pytest.mark.asyncio
async def test_ask_the_act_streams_sse_events() -> None:
    fake_container = Container()
    fake_container.llm_provider = FakeLLMProvider()
    app.dependency_overrides[get_container] = lambda: fake_container

    jwt_token = create_test_jwt()
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        async with client.stream(
                "POST",
                "/ask-the-act",
                json={"prompt": "What does Article 5 say?"},
                headers={"Authorization": f"Bearer {jwt_token}"}
        ) as response:

            assert response.status_code == 200
            assert "text/event-stream" in response.headers["content-type"]

            chunks = []
            async for line in response.aiter_lines():
                if line:
                    chunks.append(line)

            assert chunks == [
                "data: According to ",
                "data: Article 5 of the ",
                "data: AI Act...",
                "data: [DONE]"
            ]

    app.dependency_overrides.clear()