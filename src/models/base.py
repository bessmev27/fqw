from pydantic import BaseModel

class BasePydanticModel(BaseModel):
    
    id: int
    
    class Config:

        orm_mode = True
 