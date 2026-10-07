import uuid
from typing import NewType

TenantId = NewType("TenantId", uuid.UUID)
UserId = NewType("UserId", uuid.UUID)
SystemId = NewType("SystemId", uuid.UUID)


def generate_uuid() -> uuid.UUID:
    """Generate a standard UUIDv4"""
    return uuid.uuid4()
