from dataclasses import dataclass, fields

from litestar import Router, get, patch
from sqlalchemy.ext.asyncio import AsyncSession

from users.dto import UserReadDTO
from users.models import User
from users.repository import UserRepository


@dataclass
class UserUpdateBody:
    nickname: str | None = None
    first_name: str | None = None
    second_name: str | None = None
    last_name: str | None = None
    qualification: str | None = None
    image: str | None = None


@get("/me", return_dto=UserReadDTO)
async def get_me(current_user: User) -> User:
    return current_user


@patch("/me", return_dto=UserReadDTO)
async def update_me(data: UserUpdateBody, current_user: User, db: AsyncSession) -> User:
    updates = {f.name: getattr(data, f.name) for f in fields(data) if getattr(data, f.name) is not None}
    user = await UserRepository(db).update(current_user, updates)
    await db.commit()
    return user


users_router = Router(path="/users", route_handlers=[get_me, update_me])
