import datetime
import uuid

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

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


def create_access_token(
        user: User,
        clock: Clock,
        secret: str,
        algorithm: str,
        expires_minutes: int
) -> str:
    now = clock.now()
    expires = now + datetime.timedelta(minutes=expires_minutes)

    payload = {
        "sub": str(user.id),
        "tenant_id": str(user.tenant_id),
        "role": user.role.value,
        "email": user.email,
        "exp": int(expires.timestamp()),
        "iat": int(now.timestamp()),
    }

    return jwt.encode(payload, secret, algorithm=algorithm)


def decode_access_token(token: str,secret: str, algorithm: str) -> User | None:
    try:
        payload = jwt.decode(
            token, secret, algorithms=[algorithm]
        )

        return User(
            id=UserId(uuid.UUID(payload["sub"])),
            tenant_id=TenantId(uuid.UUID(payload["tenant_id"])),
            email=payload["email"],
            role=Role(payload["role"]),
            created_at=datetime.datetime.fromtimestamp(payload["iat"], tz=datetime.UTC),
        )
    except (jwt.PyJWTError, ValueError):
        return None
