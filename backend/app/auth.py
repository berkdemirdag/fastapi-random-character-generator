from datetime import datetime, timedelta, timezone
from typing import Annotated
import os

import jwt
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

import app.crud as crud
import app.schemas as schemas
import app.database

SECRET_KEY =  os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("HASHING_ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)



def get_user(username: str):
    with app.database.get_db_context() as conn:
        user = crud.get_user_by_username(conn, username)
        if user:
            return schemas.UserinDB(**user)
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> schemas.UserinDB:
    credidentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credidentials_exception
        user = get_user(username)
    except InvalidTokenError:
        raise credidentials_exception
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return user


router = APIRouter(
    prefix="/auth",
    tags=["auth"],  
)

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

@router.post("/register", response_model=schemas.UserRead)
def register_user(user: schemas.UserCreate, db = Depends(app.database.get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    created_user = crud.create_user(db, user, hashed_password)
    return schemas.UserRead(**created_user)

@router.get("/me", response_model=schemas.UserRead)
def read_users_me(current_user: Annotated[schemas.UserinDB, Depends(get_current_user)]):
    user = schemas.UserRead(
        id=current_user.id,
        username=current_user.username,
        created_at=current_user.created_at
    )
    return user