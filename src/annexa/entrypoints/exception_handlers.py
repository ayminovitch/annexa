import structlog
from fastapi import Request
from fastapi.responses import JSONResponse

from annexa.shared.domain.exceptions import DomainError

logger = structlog.get_logger()


async def domain_error_handler(request: Request, exc: Exception) -> JSONResponse:

    if not isinstance(exc, DomainError):
        raise exc

    logger.warning(
        "domain_error",
        code=exc.code,
        path=request.url.path,
        detail=exc.detail,
    )

    return JSONResponse(
        status_code=exc.status,
        content={
            "type": "about:blank",
            "title": exc.title,
            "status": exc.status,
            "detail": exc.detail,
            "code": exc.code,
        },
        headers={"Content-Type": "application/problem+json"},
    )
