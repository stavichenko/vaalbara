from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.repository import BaseRepository
from users.models import User, UserOAuthAccount


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_oauth(self, provider: str, provider_user_id: str) -> User | None:
        result = await self.session.scalars(
            select(User)
            .join(UserOAuthAccount, UserOAuthAccount.user_id == User.id)
            .where(
                UserOAuthAccount.provider == provider,
                UserOAuthAccount.provider_user_id == provider_user_id,
            )
        )
        return result.first()

    async def create_with_oauth(
        self,
        email: str,
        first_name: str | None,
        last_name: str | None,
        image: str | None,
        provider: str,
        provider_user_id: str,
    ) -> User:
        user = User(
            email=email,
            email_verified=True,
            first_name=first_name,
            last_name=last_name,
            image=image,
        )
        self.session.add(user)
        self.session.add(UserOAuthAccount(user=user, provider=provider, provider_user_id=provider_user_id))
        await self.session.flush()
        return user

    async def update(self, user: User, data: dict) -> User:
        for key, value in data.items():
            setattr(user, key, value)
        await self.session.flush()
        return user
