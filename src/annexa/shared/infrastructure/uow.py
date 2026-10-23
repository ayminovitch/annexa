from typing import Any, Self

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from annexa.shared.application.uow import UnitOfWork
from annexa.shared.infrastructure.tenant_context import get_tenant_id


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> Self:
        self.session = self._session_factory()

        tenant_id = get_tenant_id()
        if tenant_id:
            await self.session.execute(
                text("SELECT set_config('ap.current_tenant', :t, true)"),
                {"t": str(tenant_id)},
            )

        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, traceback: Any) -> None:
        if exc_type is not None and self.session is not None:
            await self.rollback()

        if self.session is not None:
            await self.session.close()
            self.session = None

    async def commit(self) -> None:
        if self.session is not None:
            await self.session.commit()

    async def rollback(self) -> None:
        if self.session is not None:
            await self.session.rollback()
