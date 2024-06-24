from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:************@localhost/fastapi"

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

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