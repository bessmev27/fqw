from pydantic import BaseModel


class BasePydanticModel(BaseModel):

    class Config:

        orm_mode = True
