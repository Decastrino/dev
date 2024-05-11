
# import Depends allows the use of dependency in the path operation.
# Allows testing to become easier. Simply states that the db in the path operation
# function uses/has dependency on the get_db() function to create and close db sessions.

# import models and schema so queries can be made to the tables/models and schema to actually help
# validate the query values/input.

# APIRouter class, used to group *path operations*, for example to structure an app in multiple files. 
# It would then be included in the FastAPI app, or in another APIRouter (ultimately included in the app).

from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from .. import models, schema, utils
from ..database import get_db
from sqlalchemy.orm import Session

# User Response schema
UserResponse = schema.UserResponse

router = APIRouter(tags=['Users'])

# Create a User
@router.post("/creatuser", status_code=status.HTTP_201_CREATED)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get all users
@router.get("/users", response_model=List[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


# Get a user
@router.get("/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_one_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == int(id)).first()

    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"User with id {id} not found")
        
    return user