import random
import json
from enum import Enum
from pathlib import Path
from pydantic import BaseModel


def load_json(file_path: Path):
    with open(file_path, "r") as f:
        return json.load(f)


STORY_DATA = load_json(Path(__file__).parent.parent / "sample_data" /"backstory_data.json")
NAME_DATA = load_json(Path(__file__).parent.parent / "sample_data" / "name_data.json")


class Character_Race(str, Enum): 
      
    HUMAN = "human"
    ELF = "elf"
    DWARF = "dwarf"


class Character_Gender(str, Enum):

    MALE = "male"
    FEMALE = "female"
    NONBINARY = "nonbinary"


class Generated_Character():

    def __init__(
            self, 
            race: Character_Race | None = None, 
            gender: Character_Gender | None = None):
        
        self.race = race or random.choice(list(Character_Race))
        self.gender = gender or random.choice(list(Character_Gender))
        self.name = generate_character_name(self.race, self.gender)
        self.backstory = generate_backstory(self.name, self.gender)


def get_first_names_list(race_val: str, gender: str):

    race_names = NAME_DATA["first_names"][race_val]
    if gender == "nonbinary":
        return race_names["male"] + race_names["female"]
    return race_names[gender]


def generate_character_name(race, gender):

    first_names = get_first_names_list(race.value, gender.value)
    last_names = NAME_DATA["last_names"][race.value]
    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    return full_name


def generate_backstory(name: str, gender: Character_Gender) -> str:

    name_mapping = {
        "name": name,
        "pronoun": "he" if gender == Character_Gender.MALE else "she" if gender == Character_Gender.FEMALE else "they",
        "possessive": "his" if gender == Character_Gender.MALE else "her" if gender == Character_Gender.FEMALE else "their"     
    }
    origin = random.choice(STORY_DATA["origins"]).format(**name_mapping)
    middle = random.choice(STORY_DATA["middles"]).format(**name_mapping).capitalize()
    conclusion = random.choice(STORY_DATA["conclusions"]).format(**name_mapping)
    return f"{origin}. {middle} {conclusion}"

def get_status_message():
    return "Character Generator Module is imported properly."