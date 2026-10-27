from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from annexa.entrypoints.dependencies import get_current_user
from annexa.entrypoints.di import Container, get_container
from annexa.entrypoints.exception_handlers import domain_error_handler
from annexa.identity.domain.entities import User
from annexa.shared.domain.exceptions import DomainError
from annexa.shared.infrastructure.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    setup_logging()
    yield


app = FastAPI(
    title="Annexa API",
    description="EU AI Act Compliance-as-Code Platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_exception_handler(DomainError, domain_error_handler)


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


@app.get("/health", response_model=HealthResponse, tags=["Platform"])
def health_check(container: Container = Depends(get_container)) -> HealthResponse:
    now = container.clock.now()
    return HealthResponse(status="ok", timestamp=now)

class AskRequest(BaseModel):
    prompt: str

@app.post("/ask-the-act", tags=["Regulation"])
async def ask_the_act(
        request: AskRequest,
        container: Container = Depends(get_container),
        user: User = Depends(get_current_user),
) -> StreamingResponse:
    async def sse_generator() -> AsyncGenerator[str, None]:
        async for text_chunk in container.llm_provider.generate_text_stream(request.prompt):
            yield f"data: {text_chunk}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(sse_generator(), media_type="text/event-stream")
