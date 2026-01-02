from fastapi import FastAPI
from app.schemas import Character_Request
from service.character_generator import Generated_Character

app = FastAPI()
@app.post("/generate_character")
async def generate_character(request: Character_Request):
    character = Generated_Character(race=request.race, gender=request.gender)
    character_data = {
        "name": character.name,
        "race": character.race,
        "gender": character.gender,
        "backstory": character.backstory
    }
    return character_data