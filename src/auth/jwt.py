from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

from config import settings

_ALGORITHM = "HS256"
_EXPIRY_DAYS = 30


def create_token(user_id: UUID) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(days=_EXPIRY_DAYS),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=_ALGORITHM)


def decode_token(token: str) -> UUID:
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[_ALGORITHM])
    return UUID(payload["sub"])
