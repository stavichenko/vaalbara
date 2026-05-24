from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    nickname: Mapped[str | None] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    email_verified: Mapped[bool] = mapped_column(default=False)
    phone_num: Mapped[str | None] = mapped_column(unique=True)
    phone_num_verified: Mapped[bool] = mapped_column(default=False)
    first_name: Mapped[str | None]
    second_name: Mapped[str | None]
    last_name: Mapped[str | None]
    qualification: Mapped[str | None]
    image: Mapped[str | None]
    karma: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    oauth_accounts: Mapped[list["UserOAuthAccount"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class UserOAuthAccount(Base):
    __tablename__ = "user_oauth_account"
    __table_args__ = (UniqueConstraint("provider", "provider_user_id"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    provider: Mapped[str]           # "google", "facebook", etc.
    provider_user_id: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    user: Mapped[User] = relationship(back_populates="oauth_accounts")
