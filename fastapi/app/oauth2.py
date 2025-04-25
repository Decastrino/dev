from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema, database, models
from sqlalchemy.orm import Session

from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

"""
Anytime there's aspecific endpoint that should be protected, where user needs
to login inorder to use it e.g create a post. We can just add an extra dependency
into the path operation function to validate the credentials.

Basically add a get_curr_user function as a dependency, which will call the
get_current_user(token: str = Depends(oauth2_scheme)) function with the access token
gottem from the request. This then calls the "verify_access_token(token, credential_exceptions)"
function with the token and added credential_exception for failure cases.
this verify function decodes the token from the user, using the SECRET_KEY and ALGORITHM.
This gives a payload and we can retrieve the value in the payload we want to check for with 
the payload.get() method.

"payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)"
"id: str = payload.get("user_id")"
"token_data = schema.TokenData(id=id)"


"""

# Secretkey
# Algorithm
# Expiration time

# to get a string like this run:
# openssl rand -hex 32

from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scopes={"read": "Read access", "write": "Write access"})

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # print(f"Created access token for user: {data}")
    # print(f"Created token is {encoded_token}")

    return encoded_token
    
def verify_access_token(token: str, credential_exceptions):
    # Remove 'Bearer ' prefix if it exists
    if token.startswith("Bearer "):
        token = token[len("Bearer "):]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(f"After decoding: {payload}") # After decoding: {'user_id': 8, 'exp': 1714704712}
        # print(f"Type of payload[user_id] is: {type(payload['user_id'])}") # Typr of payload[user_id] is: <class 'int'>
        id: str = payload.get("user_id")
        # print(f"Type of id is: {type(id)}")
        if not id:
            raise  credential_exceptions

        #token_data = schema.TokenData(id=id)
        token_data = schema.TokenData(id=str(id))
        # print(f"In verify, token data is {token_data}")
    except JWTError:
        raise  credential_exceptions
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    print(f"Token string entering the function {token}")
    credential_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token, credential_exceptions)
    # print(f"In get_current, returned token from verify_access_token is {token}")
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    #return verify_access_token(token, credential_exceptions)
    return user
    