from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from .models import TokenData, User
import json
from pathlib import Path

# Security configuration
SECRET_KEY = "your-secret-key-here"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(email: str) -> Optional[User]:
    # In a real app, this would query a database
    # For MVP, we'll use a JSON file
    users_file = Path(__file__).parent / "users.json"
    if users_file.exists():
        with open(users_file) as f:
            users = json.load(f)
            if email in users:
                user_data = users[email]
                return User(
                    id=user_data["id"],
                    email=email,
                    hashed_password=user_data["hashed_password"],
                    is_active=user_data["is_active"],
                    created_at=datetime.fromisoformat(user_data["created_at"])
                )
    return None

def authenticate_user(email: str, password: str) -> Optional[User]:
    user = get_user(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user 