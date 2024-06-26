import time
import jwt
import os
from passlib.context import CryptContext
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


JWT_SECRET = os.environ.get("secret")
JWT_ALGORITHM = os.environ.get("algorithm")


def signJWT(username: str, user_role: str, department: str, hip_id: str):
    payload = {
        "username": username,
        "user_role": user_role,
        "department": department,
        "hip_id": hip_id,
        "expires": time.time() + 86400,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def encodePayload(payload):
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception:
        return None


def verify_hash_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def encrypt_password(password):
    return pwd_context.hash(password)
