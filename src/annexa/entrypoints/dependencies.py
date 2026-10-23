from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from annexa.identity.application.security import decode_access_token
from annexa.identity.domain.entities import User
from annexa.shared.domain.exceptions import DomainError
from annexa.shared.infrastructure.tenant_context import set_tenant_id

bearer_scheme = HTTPBearer(auto_error=False)


class UnauthorizedError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            code="UNAUTHORIZED",
            title="Authentication Failed",
            detail="Invalid or expired access token.",
            status=401,
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> User:
    if not credentials:
        raise UnauthorizedError()

    user = decode_access_token(credentials.credentials)
    if not user:
        raise UnauthorizedError()

    set_tenant_id(user.tenant_id)

    return user
