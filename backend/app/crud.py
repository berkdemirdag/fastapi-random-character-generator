import psycopg
from psycopg.rows import dict_row
import app.schemas as schemas

def create_user(conn, user: schemas.UserCreate, hashed_password: str):
    #Inserts a new user with just username and hash.
    query = """
    INSERT INTO users (username, hashed_password)
    VALUES (%s, %s)
    RETURNING id, username, created_at;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, (user.username, hashed_password))
        return cur.fetchone()
    
def create_character(conn, char: schemas.CharacterCreate, user_id: int):
    #Inserts a character for a given user.
    query = """
    INSERT INTO characters (
        user_id, name, race, gender, backstory,
        stat_str, stat_dex, stat_con, stat_int, stat_wis, stat_cha
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING *;
    """
    params = (
        user_id, char.name, char.race, char.gender, char.backstory,
        char.stat_str, char.stat_dex, char.stat_con, 
        char.stat_int, char.stat_wis, char.stat_cha
    )
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, params)
        return cur.fetchone()

def get_user_by_id(conn, user_id: int):
    #Fetch a user by their ID. DOES NOT RETURN HASHED PASSWORD!
    query = "SELECT id, username, created_at, disabled FROM users WHERE id = %s;"
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, (user_id,))
        return cur.fetchone()

def get_user_by_username(conn, username: str):
    query = "SELECT * FROM users WHERE username = %s;"
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, (username,))
        return cur.fetchone()
    
def get_character(conn, char_id: int):
    #Fetch a single character by its ID.
    query = "SELECT * FROM characters WHERE id = %s;"
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, (char_id,))
        return cur.fetchone()

def get_user_characters(conn, user_id: int):
    #Fetch all characters belonging to a specific user.
    query = "SELECT * FROM characters WHERE user_id = %s ORDER BY created_at DESC LIMIT 20 OFFSET 0;"
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, (user_id,))
        return cur.fetchall()
    
def get_random_seed(conn, category: str):
    #Fetch a random seed entry from the random_seeds table for a given category.
    query = "SELECT content FROM random_seeds WHERE category = %s ORDER BY RANDOM() LIMIT 1;"
    with conn.cursor() as cur:
        cur.execute(query, (category,))
        result = cur.fetchone()
        return result[0] if result else None
    
def update_character(conn, char_id: int, user_id: int, updates: schemas.CharacterUpdate):
    #Updates character fields based on provided data.
    #Extract only the fields that are set (not None)
    update_data = updates.model_dump(exclude_unset=True)
    if not update_data:
        return None # Nothing to update
    #Build the SET string: "name = %s, stat_str = %s"
    set_clause = ", ".join([f"{column} = %s" for column in update_data.keys()])
    # Automatically update the updated_at timestamp
    set_clause += ", updated_at = NOW()"
    
    values = list(update_data.values())
    values.append(char_id)
    values.append(user_id)

    query = f"""
    UPDATE characters 
    SET {set_clause} 
    WHERE id = %s AND user_id = %s
    RETURNING *;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, values)
        return cur.fetchone()

def delete_character(conn, char_id: int, user_id: int) -> bool: # Returns True if deleted
    #Deletes a character by its ID and user ID.
    query = "DELETE FROM characters WHERE id = %s AND user_id = %s RETURNING id;"
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(query, (char_id, user_id))
        return cur.rowcount > 0
    
def delete_user(conn, user_id: int) -> bool:
    #Permanently deletes a user. 
    #Foreign key CASCADE will handle the character cleanup.
    query = "DELETE FROM users WHERE id = %s;"
    with conn.cursor() as cur:
        cur.execute(query, (user_id,))
        return cur.rowcount > 0