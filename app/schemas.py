from pydantic import BaseModel,EmailStr,Field,conint
from datetime import datetime
from typing import Optional
from typing import Literal



class PostBase(BaseModel):
    title: str
    content: str
    published:bool=True



class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        from_attributes = True


class Post(PostBase):
    id : int
    # title : str 
    # content : str
    # published : bool
    created_at : datetime
    owner_id : int
    owner : UserOut

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes : int

    class Config:
        from_attributes = True


class Usercreate(BaseModel):
    email : EmailStr
    password : str = Field(min_length=6,max_length=72) 

    class Config:
        from_attributes=True



class UserLogin(BaseModel):
    email : EmailStr
    password : str 
 

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None

class Vote(BaseModel):
    post_id : int
    dir: Literal[0, 1]