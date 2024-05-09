
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

from fastapi.middleware.cors import CORSMiddleware

# ORM... Using SQLAlchemy's engine
# import database engine, the get_db function and db connections so db interaction can occur
# models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(auth.router)

@app.get('/')
async def home():
    return {"Message": "Welcome to the home page"}


# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)



















#############################################################################################################

"""
Using Dtabase SQL driver "Psycopg" 
"""

# ========  DB Connection  ========
# Using a database driver and raw sql query option
# conn = connection
# cur = cursor

# import psycopg2, time
# from psycopg2.extras import RealDictCursor  # --> Allows for column to value mapping. Will return a nice python dict upon return

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='user', password='password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection successful!!!")
#         break
#     except Exception as e:
#         print("Connection Failed!!")
#         print(f"Error: {e}")
#         time.sleep(3)

# Basically use the cursor to interact with the database.

# <<<<<------------   Path operation or route    ------------->>>>>
# The decorator turns the function into an actual path operation
# To change the default status code for a specific path operation,
# modify the @app.get/post("/") decorator with status_code option.
# i.e @app.post("/post", status_code = status.HTTP_201_CREATED)

# # Create a Post
# @app.post("/create_post", status_code=status.HTTP_201_CREATED)
# async def create_post(data: Post):
#     cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,
#                 (data.title, data.content, data.published))
    
#     new_post = cur.fetchone()
#     conn.commit()
#     return {"data":new_post}

    
# # Get all Posts
# @app.get("/posts")
# async def get_posts():
#     cur.execute(""" SELECT * FROM posts """)
#     posts = cur.fetchall()
#     return {"data": posts}
    

# # Get a specific post
# @app.get("/posts/{id}", status_code=status.HTTP_200_OK)
# async def get_one_post(id: str):
#     cur.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
#     entry = cur.fetchone()
    
#     if not entry:
#         return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                              detail=f"Post with id {id} not found")
    
#     return {"data":entry, "response":Response(status_code=status.HTTP_200_OK)}


# # Delete a post
# @app.delete("/posts/{id}", status_code=status.HTTP_404_NOT_FOUND)
# async def delete_post(id: int):
#     cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
#     deleted_post = cur.fetchone()
#     conn.commit()

#     if deleted_post == None:
#         return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                              detail=f"Entry with id {id} not found")
#     else:
#         return Response(status_code=status.HTTP_204_NO_CONTENT)

# # Update Post
# @app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
# async def update_post(id: int, post: Post):
#     cur.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *  """,
#                 (post.title, post.content, post.published, (str(id),)))
    
#     updated_post = cur.fetchone()
#     conn.commit()
    
#     if updated_post == None:
#         return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                              detail=f"Post with id {id} not found")
#     return {"data": updated_post, "response":Response(status_code=status.HTTP_201_CREATED)}


# # Root page of the API
# current_posts = [{"title":"Title for post 1", "content": "content for post1", "id":1},
#                  {"title":"Favorite food", "content": "Chicken is Awsome" , "id":2}
#                  ]
# @app.get("/")
# async def root():
#     print(current_posts.json())
#     return {"Posts": current_posts}




#############################################################################################################





""" 
WITHOUT DATABASE
"""

# current_posts = [{"title":"Title for post 1", "content": "content for post1", "id":1},
#                  {"title":"Favorite food", "content": "Chicken is Awsome" , "id":2}
#                  ]


# @app.post("/create_post")
# async def create_post(data: dict = Body(...)):
#     print(data)
#     name = data["title"]
#     content = data["content"]
#     return {"name":name, "content":content}

# @app.post("/create_post", status_code=status.HTTP_201_CREATED)
# async def create_post(data: Post):
#     name = data.title
#     content = data.content
#     post_dict = data.dict()
#     id = len(current_posts) + 1
#     post_dict["id"] = id
    
#     current_posts.append({"name":name, "content":content, "id": id})
#     return {"name":name, "content":content}


# def get_post(id: int):
#     for entry in current_posts:
#         if entry["id"] == id:
#             return entry
#     return None

# # Get a specific post
# @app.get("/posts/{id}", status_code=status.HTTP_200_OK)
# async def get_one_post(id: int):
#     print(f"Getting post with id {id}")
#     content = get_post(id)
#     if not content:
#         return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                              detail=f"Post with id {id} not found")
#     return {"data":content}


# @app.get("/posts/{id}")
# async def get_one_post(id: int, res: Response):
#     print(id)
#     content = get_post(id)
#     if not content:
#         return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                              detail=f"Post with id {id} not found")
#         res.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": f"Post with id {id} not found"}
#     return {"data":content}

# App.put
 # post_dict = post.dict()
    # idx = find_post_idx(id)
    # if idx < 0:
    #     return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                          detail=f"Post with id {id} not found")
    # post_dict["id"] = id
    # print(id)
    # current_posts[idx] = post_dict
    
    # return {"data": current_posts}