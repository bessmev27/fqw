from .base import BasePydanticModel

from .user import User

class UserCatalog(BasePydanticModel):

    name: str
    users: list[User]
