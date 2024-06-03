from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, utils, oauth2, schema
from .. database import get_db
from sqlalchemy.orm import Session

from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


#async def login(loginInfo: schema.Login, db: Session = Depends(get_db)):

#loginInfo: OAuth2PasswordRequestForm = Depends() Basically makes use of fastapi's security oauth2 lib
# Instead of getting credentials from the request body, we get it from the OAuth2PasswordRequestForm
# which acts as a dependency for the loginInfo. The OAuth2PasswordRequestForm get's the credentials from the 
# form body in postman (username and password fields) and provide a dictionary representation of this data
# to LoginInfo.

# This basically creates access token and returns it to the user/client
# Client then uses this token for further communication with the backend.

@router.post('/login', response_model=schema.Token)
async def login(loginInfo: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"The login info is: {loginInfo}")
    print(f"OAuth2PasswordRequestForm is {OAuth2PasswordRequestForm.__str__}")
    username = loginInfo.username
    user_password = loginInfo.password
    
    # get the user from the database
    user = db.query(models.User).filter(models.User.email == username).first()
    
    if not user:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Invalid credentials")
    
    # verify user provided password with the user's password stored in the database.
    if not utils.verify(user_password, user.password):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Invalid Credentials")
        
    # Create Token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # Return Token
    return {"access_token": access_token, "token_type": "bearer"}