README for the social media - like app developed using fastAPI. This gives a brief summary of what the project is about.

## Links

## Useful links/Resources for developing with fastAPI, SQLAlchemy, Alembic (DB migration)...:

FastAPI Documentation:
https://fastapi.tiangolo.com/tutorial/

FastAPI: OAuth2 for Authentication(Password hashing and bearer--JWT):
https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#__tabbed_1_4

Requests Library:
https://www.starlette.io/requests/

Gunicorn vs Uvicorn:
https://ismatsamadov.medium.com/gunicorn-vs-uvicorn-369635b92809#:~:text=In%20essence%2C%20both%20Gunicorn%20and,star%20for%20modern%20ASGI%20applications.

Deploying FastAPI with NginX and Gunicorn
https://dylancastillo.co/fastapi-nginx-gunicorn/#:~:text=Gunicorn%20is%20a%20popular%20web,server%20for%20Starlette%20and%20FastAPI.

SQLAlchemy (ORM for Python SQL):
https://www.sqlalchemy.org
https://fastapi.tiangolo.com/tutorial/sql-databases/

Alembic for database migrations. Alembic provides for the creation, management, and invocation of change management scripts for a relational database,
using SQLAlchemy as the underlying engine:
https://alembic.sqlalchemy.org/en/latest/tutorial.html

Data Validation using Pydantic Library:
https://docs.pydantic.dev/2.5/

PyTest, for testing API endpoints:
https://docs.pytest.org/en/8.0.x/getting-started.html

## The Project

Backend implementation of a social media app by using FastAPI

- Authentication
- CRUD Operations
- Input Validation
- Documentation

Tooling

- Python
- PostgreSQL
- SQL with Psycopg2, SQLALCHEMY as the ORM
- Postman to construct HTTP packets
- Alembic for database migrations
- Pydantic for input validation
- JWT for authentication, Passlib with Bcrtpt as its encryption engine
- Docker
- Nginx as a reverse proxy

---

## Routes

This backend application API has 4 routes.

1. Post route:
   This route is reponsible for creating posts from users, deleting users post from the database, updatings post and retrieving posts from the database.
   Basically performing all CRUD operations on the posts from different users of the application.

2. User route:
   This route is reponsible for creating users, and retrieving user data from the database.

3. Vote route:
   This route is about likes. Basically, users get to vote/like. This route contains implementation to code to add or remove a like from a post.
   With constrainst of users having the ability to like/vote once on a post only if that post exists.

4. Authentication route:
   This basically handles the login logic for users of the system. There's a need to log into the system before posting or retrieving posts, liking/voting on posts.
   Each user logs in with a valid email and password to get authenticated.

---

## How to run

git clone https://github.com/Decastrino/dev/fastapi.git

then

cd fastapi
Then install fastapi using "all" flag like:

pip install fastapi[all]

Then go this repo folder in your local computer run follwoing command

uvicorn main:app --reload

Then you can use following link to use the API

http://127.0.0.1:8000/docs

After running this API, you'll need a database in postgres

Create a database in postgres then create a file name .env and write the following things in your file (config file)

DATABASE_HOSTNAME = localhost

DATABASE_PORT = 5432

DATABASE_PASSWORD = passward_that_you_set

DATABASE_NAME = name_of_database

DATABASE_USERNAME = User_name

SECRET_KEY = 09d25e094faa2556c818166b7a99f6f0f4c3b88e8d3421

ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60(base)

Note: SECRET_KEY in this exmple is just a psudo key. You need to get a key for youself and you can get the SECRET_KEY from fastapi documantion
