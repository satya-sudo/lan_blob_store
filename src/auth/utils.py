"""
    Utils to handle jwt tokens 
    and pasword management
"""

from datetime import datetime, timedelta
import jwt
import bcrypt

def hash_password(password: str) -> str:
    """
        return hashed password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    """
        check if the password matched with the hashed one
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def create_jwt(username: str, secret: str, expiry_hours: int) -> str:
    """
        create jwt token
    """
    expiry = datetime.utcnow() + timedelta(hours=expiry_hours)
    return jwt.encode({"username": username, "exp": expiry}, secret, algorithm="HS256")

def decode_jwt(token: str, secret: str):
    """
        decode jwt token
    """
    return jwt.decode(token, secret, algorithms=["HS256"])
