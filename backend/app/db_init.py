import time
import psycopg
import os

import app.auth as auth
import app.schemas as schemas
import app.crud as crud
import app.database as database

# Grab these from your environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

def connect_with_retry(url, retries=10, delay=3):
    """Attempts to connect to the database with a progressive wait."""
    for i in range(retries):
        try:
            conn = psycopg.connect(url)
            print("Successfully connected to the database!")
            return conn
        except (psycopg.OperationalError, Exception) as e:
            if i == retries - 1:
                print("Could not connect to database after several attempts.")
                raise e
            print(f"Database not ready ({e}). Retrying in {delay}s... ({i+1}/{retries})")
            time.sleep(delay)

def initialize_all_tables():
    commands = [
        # 1. Users Table
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            disabled BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        # 2. Characters Table
        """
        CREATE TABLE IF NOT EXISTS characters (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            name TEXT NOT NULL,
            race TEXT,
            gender TEXT,
            backstory TEXT,
            stat_str INT DEFAULT 10,
            stat_dex INT DEFAULT 10,
            stat_con INT DEFAULT 10,
            stat_int INT DEFAULT 10,
            stat_wis INT DEFAULT 10,
            stat_cha INT DEFAULT 10,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """,
        "CREATE INDEX IF NOT EXISTS idx_char_user_id ON characters(user_id);",
        # 3. Random Seeds Table
        """
        CREATE TABLE IF NOT EXISTS random_seeds (
            id SERIAL PRIMARY KEY,
            category VARCHAR(50) NOT NULL, -- e.g., 'name_male_human', 'surname_elf'
            content TEXT NOT NULL,          -- the actual name or backstory fragment
            UNIQUE(category, content)
        );
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_seed_category ON random_seeds(category);
        """
    ]

    try:
        with connect_with_retry(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                for cmd in commands:
                    cur.execute(cmd)
            print("Database schema initialized successfully.")
    except Exception as e:
        print(f"Error during table initialization: {e}")

RANDOM_SEED_DATA =  {
    'human_male': ["Alaric", "Beron", "Cedric", "Donovan", "Eamon", "Finnian", "Garrick", "Hugo", "Ives", "Joram"],
    'human_female':["Adelaide", "Beatrix", "Clara", "Dorothea", "Elspeth", "Felicity", "Gwendolyn", "Hazel", "Ida", "Juliana"],
    
    'elf_male': ["Aelar", "Baelir", "Caelum", "Daeron", "Erevan", "Faelar", "Gaelith", "Haemir", "Ithilion", "Jaedon"],
    'elf_female': ["Arianna", "Briala", "Caelynn", "Dara", "Eilistraee", "Faylinn", "Galanodel", "Hathlyn", "Ilbryn", "Jaelynn"],
    
    "dwarf_male": ["Adrik", "Alberich", "Baern", "Bruenor", "Dain", "Einkil", "Fargrim", "Flint", "Gardain", "Harbek"],
    "dwarf_female": ["Amber", "Artin", "Audhild", "Bardryn", "Dagnal", "Diesa", "Eldeth", "Falkrunn", "Finellen", "Gunnloda"],
    
    "human_surname": ["Brightwood", "Davenport", "Gallowglass", "Holloway", "Ironwood", "Kingsley", "Northumberland", "Stonewright", "Thatcher", "Whitlock"],
    "elf_surname": ["Amakiir", "Amastacia", "Galanodel", "Holimion", "Ilphelkiir", "Liadon", "Meliamne", "Nailo", "Siannodel", "Xiloscient"],
    "dwarf_surname": ["Balderk", "Battlehammer", "Brawnanvil", "Dankil", "Fireforge", "Frostbeard", "Loderr", "Lutgehr", "Strakeln", "Ungart"],
    
    "backstory_start_fragment": [
        "{name} grew up in a small farming community",
        "{name} was raised in a busy city tenement",
        "{name} spent their childhood in a remote military outpost",
        "{name} lived among a group of traveling merchants",
        "{name} was an apprentice in a local smithy",
        "{name} grew up in the slums of a major port",
        "{name} was raised by a strictly religious family",
        "{name} lived in a quiet village near the border",
        "{name} spent their early years in a lakeside fishing town",
        "{name} was part of a large, struggling family in the capital",
        "{name} was raised by an uncle who ran a local tavern",
        "{name} spent their youth working in the family stables"
    ],
   
   "backstory_middle_fragment": [
        "{pronoun} eventually worked as a low-level guard",
        "{pronoun} spent several years working on a merchant ship",
        "{pronoun} made a living as a small-time thief",
        "{pronoun} joined a local militia to pay off a debt",
        "{pronoun} left home to find work in a neighboring kingdom",
        "{pronoun} spent time as a messenger for the local lord",
        "{pronoun} worked as a bouncer in a rough dockside bar",
        "{pronoun} was forced to flee after a deal went wrong",
        "{pronoun} earned coin by hunting small game in the woods",
        "{pronoun} served as an assistant to a traveling scholar",
        "{pronoun} spent a few years drifting from town to town",
        "{pronoun} took up odd jobs in various mining camps"
    ],
    
    "backstory_end_fragment": [
        "but {pronoun} left that life behind after a dispute over gold.",
        "and now {pronoun} is looking for a fresh start elsewhere.",
        "until {pronoun} was framed for a crime {pronoun} didn't commit.",
        "but a sudden attack on the road changed everything.",
        "and {pronoun} is currently trying to save up enough to go home.",
        "before deciding to try {possessive} luck as an adventurer.",
        "but {pronoun} is still being followed by old enemies.",
        "until {pronoun} realized there was more money in adventuring.",
        "and now {pronoun} carries a map to a supposed treasure.",
        "but {pronoun} is tired of working for other people.",
        "before a chance meeting led to a much better offer.",
        "and {pronoun} is now searching for a missing family member."
    ]
    }

def seed_random_data():
    insert_command = """
    INSERT INTO random_seeds (category, content)
    VALUES (%s, %s)
    ON CONFLICT (category, content) DO NOTHING;
    """
    try:
        with connect_with_retry(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                for category, contents in RANDOM_SEED_DATA.items():
                    for content in contents:
                        cur.execute(insert_command, (category, content))
            print("Random seed data inserted successfully.")
    except Exception as e:
        print(f"Error during seeding random data: {e}")

def seed_sample_users():
    sample_users = [
        ("testuser_1", "password_1"),
        ("testuser_2", "password_2"),
        ("testuser_3", "password_3"),
    ]
    try:
        with database.get_db_context() as conn:
            for username, password in sample_users:
                hashed_password = auth.get_password_hash(password)
                user_in = schemas.UserCreate(username=username, password=hashed_password)
                crud.create_user(conn, user_in)
        print("Sample users inserted successfully.")
    except Exception as e:
        print(f"Error during seeding sample users: {e}")

def seed_sample_characters():
    # This function can be implemented to add sample characters if needed
    pass

if __name__ == "__main__":
    initialize_all_tables()
    seed_random_data()
    seed_sample_users()