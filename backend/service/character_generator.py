import random
import app.schemas as schemas
import app.crud as crud
import app.database as database

def get_status_message():
    return "Character Generator Module is imported properly."

def generate_character(request: schemas.CharacterGenerateRequest) -> schemas.CharacterCreate:
    race = request.race
    gender = request.gender
    name = generate_character_name(race, gender)
    backstory = generate_backstory(name, gender)
    stats = {
        "stat_str": roll_4d6_drop_lowest(),
        "stat_dex": roll_4d6_drop_lowest(),
        "stat_con": roll_4d6_drop_lowest(),
        "stat_int": roll_4d6_drop_lowest(),
        "stat_wis": roll_4d6_drop_lowest(),
        "stat_cha": roll_4d6_drop_lowest(),
    }
    character = schemas.CharacterCreate(
        name=name,
        race=race,
        gender=gender,
        backstory=backstory,
        **stats
    )
    return character

def generate_character_name(race: schemas.Character_Race, gender: schemas.Character_Gender) -> str:
    with database.get_db_context() as conn:
        if gender.value == "nonbinary":
            name_gender = random.choice(["male", "female"])
        else:
            name_gender = gender.value
        first_name = crud.get_random_seed(conn, f"{race.value}_{name_gender}")
        last_name = crud.get_random_seed(conn, f"{race.value}_surname")
    full_name = f"{first_name} {last_name}"
    return full_name

def generate_backstory(name: str, gender: schemas.Character_Gender) -> str:
    with database.get_db_context() as conn:
        origin = crud.get_random_seed(conn, "backstory_start_fragment")
        middle = crud.get_random_seed(conn, "backstory_middle_fragment")
        conclusion = crud.get_random_seed(conn, "backstory_end_fragment")
    name_mapping = {
        "name": name,
        "pronoun": "he" if gender == schemas.Character_Gender.MALE else "she" if gender == schemas.Character_Gender.FEMALE else "they",
        "possessive": "his" if gender == schemas.Character_Gender.MALE else "her" if gender == schemas.Character_Gender.FEMALE else "their"     
    }
    origin = origin.format(**name_mapping)
    middle = middle.format(**name_mapping).capitalize()
    conclusion = conclusion.format(**name_mapping)
    return f"{origin}. {middle} {conclusion}"

def roll_4d6_drop_lowest() -> int:
    rolls = [random.randint(1, 6) for _ in range(4)]
    rolls.remove(min(rolls))
    return sum(rolls)