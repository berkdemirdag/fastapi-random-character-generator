from fastapi import FastAPI
import psycopg
import os

import app.schemas as schemas
from app.auth import router as auth_router
from service.character_generator import generate_character, get_status_message



app = FastAPI()
app.include_router(auth_router)

@app.get("/test")
def test_connection():
    # 1. Test the Module Import
    logic_data = get_status_message()
    
    # 2. Test the Database Connection
    db_url = os.getenv("DATABASE_URL")
    conn_status = "Failed"
    try:
        # We just try to connect and check the version
        conn = psycopg.connect(db_url)
        conn_status = "Success! Postgres is reachable."
        conn.close()
    except Exception as e:
        conn_status = f"Error: {str(e)}"

    return {
        "module_import": logic_data,
        "database_connectivity": conn_status,
    }

@app.post("/generate_character", response_model=schemas.CharacterCreate)
def generate_character_endpoint(request: schemas.CharacterGenerateRequest):
    character = generate_character(request)
    return character