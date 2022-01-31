from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at:datetime

    class Config: #this is for orm model only, pydanmic needs a dictionary 
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# don't do anything to validate a post create other than title, content, published
class PostCreate(PostBase):
    pass

#define the data we want to send back in the response_model on main.py # response_model=schemas.Post
class Post(PostBase): #this extends PostBase
    id: int
    created_at:datetime
    owner_id: int
    owner: UserOut  #part of Post models, will now also get/show user details when getting a post

    class Config: #this is for orm model only, pydanmic needs a dictionary 
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    
    email: EmailStr
    password:str

    class Config: #this is for orm model only, pydanmic needs a dictionary 
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)