from fastapi import FastAPI, Depends
from pydantic import BaseModel
from datetime import datetime

from annexa.shared.infrastructure.di import Container, get_container

app = FastAPI(
    title="Annexa API",
    description="EU AI Act Compliance-as-Code Platform",
    version="0.1.0",
)

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime

@app.get("/health", response_model=HealthResponse, tags=["Platform"])
def health_check(container: Container = Depends(get_container)) -> HealthResponse:
    now = container.clock.now()
    return HealthResponse(status="OK", timestamp=now)
