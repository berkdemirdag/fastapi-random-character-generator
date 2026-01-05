from datetime import datetime, timedelta, timezone
from typing import Annotated
import os

import jwt
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

import app.database as database
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

def get_user(username: str, conn) -> schemas.UserinDB | None:
    user = crud.get_user_by_username(conn, username=username)
    return schemas.UserinDB(**user) if user else None

def authenticate_user(conn, username: str, password: str)-> schemas.UserinDB | bool:
    user = get_user(username, conn)
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

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db = Depends(database.get_db)
) -> schemas.UserinDB:
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
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError, Exception):
        raise credentials_exception

    # Use your crud function and pass the db connection
    user = crud.get_user_by_username(db, username=username)
    
    if user is None:
        # Standard security practice: return 401 even if user is missing
        # so attackers don't know which usernames exist
        raise credentials_exception
        
    return schemas.UserinDB(**user)