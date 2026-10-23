import datetime
import uuid

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from annexa.config.settings import settings
from annexa.identity.domain.entities import Role, User
from annexa.shared.domain.ids import TenantId, UserId
from annexa.shared.domain.time import Clock

_hasher = PasswordHasher()


def hash_secret(secret: str) -> str:
    return _hasher.hash(secret)


def verify_secret(hash_str: str, secret: str) -> bool:
    try:
        return _hasher.verify(hash_str, secret)
    except VerifyMismatchError:
        return False


def create_access_token(user: User, clock: Clock) -> str:
    now = clock.now()
    expires = now + datetime.timedelta(minutes=settings.jwt_access_expiration_minutes)

    payload = {
        "sub": str(user.id),
        "tenant_id": str(user.tenant_id),
        "role": user.role.value,
        "email": user.email,
        "exp": int(expires.timestamp()),
        "iat": int(now.timestamp()),
    }

    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> User | None:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )

        return User(
            id=UserId(uuid.UUID(payload["sub"])),
            tenant_id=TenantId(uuid.UUID(payload["tenant_id"])),
            email=payload["email"],
            role=Role(payload["role"]),
            created_at=datetime.datetime.fromtimestamp(payload["iat"], tz=datetime.UTC),
        )
    except jwt.PyJWTError:
        return None
