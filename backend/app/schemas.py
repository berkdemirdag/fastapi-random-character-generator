from pydantic import BaseModel
from enum import Enum
from service.character_generator import Character_Race, Character_Gender


class Character_Request(BaseModel):
    race: Character_Race | None = None
    gender: Character_Gender | None = None