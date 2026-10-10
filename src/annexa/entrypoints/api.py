from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from annexa.entrypoints.exception_handlers import domain_error_handler
from annexa.shared.domain.exceptions import DomainError
from annexa.shared.infrastructure.di import Container, get_container
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
