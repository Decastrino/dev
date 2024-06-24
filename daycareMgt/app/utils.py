# Password hashing using passlib and bcrypt
from passlib.context import CryptContext

# from . import crud, schema, oauth2, database, models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
