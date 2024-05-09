from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from .. import models, schema, oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

# import Depends allows the use of dependency in the path operation.
# Allows testing to become easier. Simply states that the db in the path operation
# function uses/has dependency on the get_db() function to create and close db sessions.

# import models and schema so queries can be made to the tables/models and schema to actually help
# validate the query values/input.

# APIRouter class, used to group *path operations*, for example to structure an app in multiple files. 
# It would then be included in the FastAPI app, or in another APIRouter (ultimately included in the app).



# Post response schema
PostResponse = schema.PostResponse
PostOut = schema.PostOut

router = APIRouter(prefix="/posts",
                   tags=['Posts'])

# Create a Post
@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(data: schema.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # 1. Type the database fields individually
    # new_post = models.Post(title=data.title, content=data.content, published=data.published)
    
    # 2. Unpack the data using pythonic operation ---> **post.dict()
    new_post = models.Post(owner_id=current_user.id, **data.dict())
    #new_post = models.Post(**data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    
# Get all Posts
# Use the LIST from typying to handle the response validation
# This endpoint returns a list of records from the database
# and the schema will try to group all into a single response value
# resulting in an error.
@router.get("/", response_model= List[PostOut])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10,
                    offset: int = 0, search: Optional[str] = ""):

    # posts = db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(offset).all()
    # print(posts)
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # Get all posts relating to the logged in user
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(offset).all()
    if not posts:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"No Posts found")
    return posts

    

# Get a specific post
@router.get("/{id}", response_model=PostOut, status_code=status.HTTP_200_OK)
async def get_one_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    entry = db.query(models.Post).filter(models.Post.id == int(id)).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == int(id)).first()

    if not post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"Post with id {id} not found")
    
    return post



# Delete a post
@router.delete("/{id}", status_code=status.HTTP_404_NOT_FOUND)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == int(id))
    post = post_query.first()

    if not post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"Entry with id {id} not found")

    post_owner = post.owner_id
    if current_user.id != post_owner:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Current user not authorized to delete post")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update Post
@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
async def update_post(id: int, updated_post: schema.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == int(id))
    post = post_query.first()

    if not post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"Post with id {id} not found")
        
    post_owner = post.owner_id
    if current_user.id != post_owner:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Current user not authorized to delete post")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post

    

# Root page of the API
current_posts = [{"title":"Title for post 1", "content": "content for post1", "id":1},
                 {"title":"Favorite food", "content": "Chicken is Awsome" , "id":2}
                 ]
@router.get("/")
async def root():
    # print(current_posts.json())
    return {"Posts": current_posts}
     