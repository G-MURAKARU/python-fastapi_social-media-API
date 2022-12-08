# utility functions, used to carry out specialised actions within the app
#
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    """Hashes a password string using bcrypt algorithm"""
    return pwd_context.hash(password)


def verify(input_password: str, hashed_password):
    """Verifies input password by comparing with hash"""
    return pwd_context.verify(input_password, hashed_password)
