import random
import string
from typing import Dict

def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))

def random_email() -> str:
    return f"{random_lower_string()}@example.com"

def random_phone() -> str:
    return "".join(random.choices(string.digits, k=10))

def random_password() -> str:
    # Generate a password that meets requirements
    lowercase = random.choices(string.ascii_lowercase, k=4)
    uppercase = random.choices(string.ascii_uppercase, k=4)
    digits = random.choices(string.digits, k=4)
    special = random.choices("!@#$%^&*", k=2)
    all_chars = lowercase + uppercase + digits + special
    random.shuffle(all_chars)
    return "".join(all_chars)

def get_test_db_url() -> str:
    from app.core.config import get_settings
    settings = get_settings()
    return f"{settings.SQLALCHEMY_DATABASE_URI}_test"

def dict_to_json_string(d: Dict) -> str:
    import json
    return json.dumps(d, sort_keys=True)

def get_server_api() -> str:
    from app.core.config import get_settings
    settings = get_settings()
    return f"http://localhost:{settings.PORT}{settings.API_V1_STR}"