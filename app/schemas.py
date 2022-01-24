from datetime import datetime
import profile
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    email: EmailStr
    password: str

class EditUser(BaseModel):
    email: Optional[EmailStr]
    phone: Optional[str]
    profile_pic: Optional[str]

class EditPassword(BaseModel):
    email: EmailStr
    old_password: str
    password: str

class ResponseUser(BaseModel):
    id: int
    email: EmailStr
    phone: Optional[str]
    CreatedAt: datetime
    profile_pic: str

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    User: ResponseUser
    followers: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class Body(BaseModel):
    content: str
    parent_post: Optional[int]

class EditPost(BaseModel):
    content: str

class ResponsePost(BaseModel):
    id: int
    content: str
    user_id: int
    CreatedAt: datetime
    user: ResponseUser
    parent_post: Optional[int]

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: ResponsePost
    votes: int

    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id:int
    vote_dir:bool



class ResponseVote(BaseModel):
    post_id:Optional[int]
    user_id:Optional[int]

    class Config:
        orm_mode = True

class FollowingIn(BaseModel):
    following_id: int
    follow_dir: bool

class FollowingOut(BaseModel):
    follower_id: Optional[int]
    following_id: Optional[int]

    class Config:
        orm_mode = True