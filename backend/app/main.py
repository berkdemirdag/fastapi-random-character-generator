from fastapi import FastAPI
from app.schemas import Character_Request
from service.character_generator import Generated_Character, get_status_message
import psycopg2
import os  

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

@app.get("/test")
def test_connection():
    # 1. Test the Module Import
    logic_data = get_status_message()
    
    # 2. Test the Database Connection
    db_url = os.getenv("DATABASE_URL")
    conn_status = "Failed"
    try:
        # We just try to connect and check the version
        conn = psycopg2.connect(db_url)
        conn_status = "Success! Postgres is reachable."
        conn.close()
    except Exception as e:
        conn_status = f"Error: {str(e)}"

    return {
        "module_import": logic_data,
        "database_connectivity": conn_status,
    }