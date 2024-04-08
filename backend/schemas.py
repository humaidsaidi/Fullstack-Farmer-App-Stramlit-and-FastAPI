from pydantic import BaseModel, EmailStr # pydantic used for request and respond validation
from datetime import datetime
from typing import Optional


# This class is used for validating the data that sended from the frontend
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
        
# this class to make model for validating the response to frontend
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # This class for converting sqlalchemy model to pydantic model
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int

class TokenData(BaseModel):
    id: Optional[int] = None