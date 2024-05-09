from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

# data validation schema from frontend
# Defines the structure of a request and response

###############################################################
#User Schema
###############################################################

class UserCreate(BaseModel):
    email: EmailStr
    password: str
  
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

###############################################################
# Post schema
###############################################################

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[float] = None
    
# Response Schema
# With this Schema, we can limit the fields of what we send back to the client/postman
# here, we don't send the id field. 
class PostResponse(Post):
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
    # To tell the pydantic model to read the data even
    # if it's not a dict, but an ORM model or any arbitrary object with attributes
    class Config:
        orm_mode = True
        
class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True

        
###############################################################
#Login info Schema
###############################################################

class Login(BaseModel):
    email: EmailStr
    password: str
  
    class Config:
        orm_mode = True
        

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)
    #direction: Annotated[int, Field(strict=True, gt=0)]

