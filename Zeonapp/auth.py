# authentication handler file
from typing import Annotated
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt
from passlib.context import CryptContext

from pydantic import BaseModel

# from models import User
from db import users_db
from helpers import user_serializer

SECRET_KEY = "fb2c5598e68564bd30f7d1a2662134244ce11ef22cd25025a88cfc2007677431"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter(tags=['AUTHENTICATION'])

class Token( BaseModel):
    access_token: str
    token_type: str

class TokenData( BaseModel):
    username: str | None = None
    
class AuthUser( BaseModel):
    id: str
    username: str
    email: str
    user_type: str

class UserInDB( AuthUser):
    password: str

def verify_password( plain_password, hashed_password):
    # return pwd_context.verify( plain_password, hashed_password)
    if plain_password == hashed_password:
        return True
    return False
    
def authenticate_user( username: str, password: str):
    user = users_db.find_one({"username": username})
    if not user:
        return False
    if not verify_password( password, user['password']):
        return False
    user = user_serializer( user)
    return user
    
def create_access_token( data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta( minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode( to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    user = users_db.find_one({"username": token_data.username})
    if user is None:
        raise credentials_exception
    user = user_serializer( user)
    # return user
    return {
        "id": user["_id"],
        "username": user["username"],
        "email": user["email"],
        "user_type": user["user_type"]
    }

def get_current_user_details( username: str):
    user = users_db.find_one({"username": username})
    user = user_serializer( user)
    return user["user_details"]

### ATUENTICATION Routes----------------------------------------------------------

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user( form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta( minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/password")
def update_user_password( new_password: str, old_passsword: str, current_user: Annotated[AuthUser, Depends( get_current_user)]):
    return None
# @auth_router.get("/me", response_model=AuthUser)
# async def get_me(
#     current_user: Annotated[AuthUser, Depends(get_current_user)]
# ):
#     return current_user

# @auth_router.get("/my_details")
# async def get_my_details(
#     current_user: Annotated[AuthUser, Depends( get_current_user)]
# ):
#     print(current_user["username"])
#     details = get_current_user_details( current_user["username"])
#     return details

###----------------------------------------------------------------------------