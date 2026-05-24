from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.dto import DTOConfig

from users.models import User


class UserReadDTO(SQLAlchemyDTO[User]):
    config = DTOConfig(exclude={"oauth_accounts", "phone_num_verified", "email_verified"})
