from pydantic import BaseModel

class UserCreate(BaseModel):
    users_id: int
    login: str
    password: str

class UserLogin(BaseModel):
    login: str
    password: str

class UserResponse(BaseModel):
    id: int
    users_id: int
    login: str

    class Config:
        from_attributes = True
