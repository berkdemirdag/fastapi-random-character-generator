import os
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
import app.schemas as schemas
import app.crud as crud
import app.database as database
import app.security as security
from service.character_generator import generate_character


router = APIRouter(
    prefix="/character",
    tags=["character"],  
)

@router.post("/generate", response_model=schemas.CharacterCreate)
def character_generate(
    request: schemas.CharacterGenerateRequest,
    current_user: schemas.UserinDB = Depends(security.get_current_user),
    db=Depends(database.get_db)
):
    character = generate_character(request, db)
    return character

@router.post("/", response_model=schemas.CharacterinDB)
def save_character(
    character_in: schemas.CharacterCreate,
    current_user: Annotated[schemas.UserinDB, Depends(security.get_current_user)],
    db = Depends(database.get_db)
):
    new_character = crud.create_character(db, character_in, current_user.id)
    return new_character

@router.get("/", response_model=list[schemas.CharacterCreate])
def list_my_characters(
    current_user: Annotated[schemas.UserinDB, Depends(security.get_current_user)],
    db = Depends(database.get_db)
):
    """
    Returns all characters belonging to the authenticated user.
    """
    characters = crud.get_user_characters(db, current_user.id)
    return characters

@router.get("/{char_id}", response_model=schemas.CharacterinDB)
def get_character(
    char_id: int,
    current_user: Annotated[schemas.UserinDB, Depends(security.get_current_user)],
    db = Depends(database.get_db)
):
    """
    Fetch a specific character by its ID, ensuring it belongs to the authenticated user.
    """
    character = crud.get_character(db, char_id)
    if character is None or character["user_id"] != current_user.id:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@router.delete("/{char_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_character(
    char_id: int,
    current_user: Annotated[schemas.UserinDB, Depends(security.get_current_user)],
    db = Depends(database.get_db)
):
    """
    Deletes a specific character by its ID, ensuring it belongs to the authenticated user.
    """
    character = crud.get_character(db, char_id)
    if character is None or character["user_id"] != current_user.id:
        raise HTTPException(status_code=404, detail="Character not found")
    crud.delete_character(db, char_id, current_user.id)
    return

@router.patch("/{char_id}", response_model=schemas.CharacterinDB)
def update_character_endpoint(
    char_id: int,
    updates: schemas.CharacterUpdate,
    current_user: Annotated[schemas.UserinDB, Depends(security.get_current_user)],
    db = Depends(database.get_db)
):
    """
    Partially updates a character. Only fields provided in the request body will be changed.
    """
    updated_char = crud.update_character(db, char_id, current_user.id, updates)
    if updated_char is None:
        raise HTTPException(
            status_code=404, 
            detail="Character not found or you do not have permission to edit it"
        )
    return updated_char


