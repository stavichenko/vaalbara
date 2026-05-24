from litestar import Request
from litestar.exceptions import NotAuthorizedException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.jwt import decode_token
from users.models import User
from users.repository import UserRepository


async def provide_current_user(request: Request, db: AsyncSession) -> User:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise NotAuthorizedException()
    try:
        user_id = decode_token(auth_header.removeprefix("Bearer "))
    except Exception:
        raise NotAuthorizedException()
    return await UserRepository(db).get_by_id(user_id)
