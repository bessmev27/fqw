
from .base import BasePydanticModel


class User(BasePydanticModel):

    name: str
    login: str
    
