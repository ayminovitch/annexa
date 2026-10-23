from dataclasses import dataclass
from enum import StrEnum

from annexa.shared.domain.entity import BaseEntity
from annexa.shared.domain.ids import TenantId, UserId


class Role(StrEnum):
    OWNER = "owner"
    ADMIN = "admin"
    COMPLIANCE_OFFICER = "compliance_officer"
    ENGINEER = "engineer"
    AUDITOR = "auditor"

@dataclass(kw_only=True)
class Tenant(BaseEntity):
    id: TenantId
    name: str

@dataclass(kw_only=True)
class User(BaseEntity):
    id: UserId
    tenant_id: TenantId
    email: str
    role: Role
