from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


# --- TOKEN SCHEMA ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- USER SCHEMAS ---
class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    created_at: datetime

class UserinDB(UserRead):
    hashed_password: str


# --- CHARACTER SCHEMAS ---
class Character_Race(str, Enum): 
    HUMAN = "human"
    ELF = "elf"
    DWARF = "dwarf"

class Character_Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NONBINARY = "nonbinary"

class CharacterGenerateRequest(BaseModel):
    race: Character_Race
    gender: Character_Gender

class CharacterCreate(BaseModel):
    name: str
    race: Character_Race
    gender: Character_Gender
    stat_str: int = 10
    stat_dex: int = 10
    stat_con: int = 10
    stat_int: int = 10
    stat_wis: int = 10
    stat_cha: int = 10
    backstory: str

class CharacterRead(CharacterGenerateRequest):
    id: int
    user_id: int
    name: str
    created_at: datetime

class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    race: Optional[str] = None
    gender: Optional[str] = None
    backstory: Optional[str] = None
    stat_str: Optional[int] = None
    stat_dex: Optional[int] = None
    stat_con: Optional[int] = None
    stat_int: Optional[int] = None
    stat_wis: Optional[int] = None
    stat_cha: Optional[int] = None