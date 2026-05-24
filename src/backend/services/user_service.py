import json
import os
from src.backend.security.auth import get_password_hash

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(BASE_DIR, "users.json")

def _load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def get_user_by_email(email: str):
    users = _load_users()
    for u in users:
        if u["email"] == email:
            return u
    return None

def get_all_users():
    return _load_users()

def create_user(email: str, full_name: str, role: str, password: str):
    users = _load_users()
    if any(u["email"] == email for u in users):
        return None

    scopes_map = {
        "admin": ["admin:all", "patients:read", "patients:write", "appointments:read", "appointments:write", "practitioners:read", "practitioners:write"],
        "medico": ["patients:read", "appointments:read", "appointments:write", "practitioners:read"],
        "secretaria": ["patients:read", "patients:write", "appointments:read", "appointments:write", "practitioners:read"],
    }

    new_user = {
        "email": email,
        "full_name": full_name,
        "role": role,
        "hashed_password": get_password_hash(password),
        "scopes": scopes_map.get(role, ["patients:read"]),
    }
    users.append(new_user)
    _save_users(users)
    return new_user

def delete_user(email: str):
    users = _load_users()
    filtered = [u for u in users if u["email"] != email]
    if len(filtered) == len(users):
        return False
    _save_users(filtered)
    return True
