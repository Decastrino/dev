from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2, time
from app.config import settings

#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:************@localhost/fastapi"
#SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

# Create the engine that enables/is responsible for connection to the database
# engine = create_engine("postgresql+psycopg2://<hname>:<password>@localhost/fastapi")
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True) # echo=True


# Create the local session class for all connections to the db
# Enables talking/creating sessions to the database via the engine created
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Create the dependency
# Create a session to the database with every request to the api endpoint
def get_db():
    db = SessionLocal()
    print(f"Loggining In: username: {settings.database_username}, password: {settings.database_password}")
    try:
        yield db
    finally:
        db.close()
        
# ===============================    DB Connection  ========================================

"""
Using Dtabase SQL driver "Psycopg" 
"""
# from ..database import get_db, connection, cursor  ===> in other files to use connection
# and cusor.


# import psycopg2, time
# from psycopg2.extras import RealDictCursor  # --> Allows for column to value mapping. Will return a nice python dict upon return

# Using a database driver and raw sql query option
# while True:
#     try:
#         connection = psycopg2.connect(host='localhost', database='fastapi', 
#                                 user='postgres', password='Decastrino1.')
#         cursor = connection.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as e:
#         print(e)
#         print("Database connection was not successful")
#         # Good way to handle database connection issues and retries besides wrong authentication details.
#         time.sleep(3)

# =================================================================================================================================