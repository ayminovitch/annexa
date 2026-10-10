from typing import Any, Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from annexa.shared.application.uow import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> Self:
        self.session = self._session_factory()
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
