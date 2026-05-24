from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import NotFoundError

T = TypeVar("T")


class BaseRepository(Generic[T]):
    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: UUID) -> T:
        obj = await self.session.get(self.model, id)
        if obj is None:
            raise NotFoundError(f"{self.model.__name__} not found")
        return obj

    async def list_paginated(self, limit: int, offset: int) -> tuple[list[T], int]:
        total = await self.session.scalar(select(func.count()).select_from(self.model))
        items = list(await self.session.scalars(select(self.model).limit(limit).offset(offset)))
        return items, total or 0
