# In app/core/security.py

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

# --- FIX: Import the 'settings' object instead of individual variables ---
from app.core.config import settings

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) # Use settings
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM) # Use settings
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    # You will need to import and use passlib here
    # from passlib.context import CryptContext
    # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # return pwd_context.verify(plain_password, hashed_password)
    # Placeholder for now
    return plain_password == hashed_password

def hash_password(password: str):
    # You will need to import and use passlib here
    # from passlib.context import CryptContext
    # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # return pwd_context.hash(password)
    # Placeholder for now
    return password