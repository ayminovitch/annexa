import uuid

from annexa.identity.application.security import (
    create_access_token,
    decode_access_token,
    hash_secret,
    verify_secret,
)
from annexa.identity.domain.entities import Role, User
from annexa.shared.domain.ids import TenantId, UserId
from annexa.shared.domain.time import SystemClock


def test_argon2_hashing_and_verification() -> None:
    secret = "my_api_key_123"
    hashed = hash_secret(secret)

    assert hashed != secret
    assert hashed.startswith("$argon2id$")

    # Valid verification
    assert verify_secret(hashed, secret) is True
    # Invalid verification
    assert verify_secret(hashed, "wrong_key") is False


def test_jwt_creation_and_decoding() -> None:
    clock = SystemClock()
    user = User(
        id=UserId(uuid.uuid4()),
        tenant_id=TenantId(uuid.uuid4()),
        email="compliance@annexa.com",
        role=Role.COMPLIANCE_OFFICER,
        created_at=clock.now(),
    )

    token = create_access_token(user, clock)
    decoded_user = decode_access_token(token)

    assert decoded_user is not None
    assert decoded_user.id == user.id
    assert decoded_user.tenant_id == user.tenant_id
    assert decoded_user.role == Role.COMPLIANCE_OFFICER


def test_invalid_jwt_returns_none() -> None:
    assert decode_access_token("not.a.real.token") is None
