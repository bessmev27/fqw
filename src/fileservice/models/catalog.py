from .base import BasePydanticModel

from .user import User

class UserCatalog(BasePydanticModel):
    
    id: int
    name: str
    users: list[User]
