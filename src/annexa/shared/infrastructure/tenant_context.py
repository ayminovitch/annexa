from contextvars import ContextVar

from annexa.shared.domain.ids import TenantId

_current_tenant_id: ContextVar[TenantId | None] = ContextVar(
    "current_tenant_id", default=None
)


def set_tenant_id(tenant_id: TenantId) -> None:
    _current_tenant_id.set(tenant_id)


def get_tenant_id() -> TenantId | None:
    return _current_tenant_id.get()
