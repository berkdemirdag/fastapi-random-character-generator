from fastapi import APIRouter, Depends, HTTPException, status
import app.schemas as schemas
import app.crud as crud
import app.database as database
import app.security as security

router = APIRouter(
    prefix="/user",
    tags=["user"],  
)

@router.post("/register", response_model=schemas.UserRead)
def register_user(user: schemas.UserCreate, db = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = security.get_password_hash(user.password)
    created_user = crud.create_user(db, user, hashed_password)
    return schemas.UserRead(**created_user)

@router.get("/me", response_model=schemas.UserRead)
def read_current_user(current_user: schemas.UserRead = Depends(security.get_current_user)):
    current_user_data = schemas.UserRead(
        id=current_user.id,
        username=current_user.username,
        created_at=current_user.created_at
    )
    return current_user_data

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(db = Depends(database.get_db), current_user: schemas.UserinDB = Depends(security.get_current_user)):
    crud.delete_user(db, current_user.id)
    return None