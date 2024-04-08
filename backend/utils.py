# pip install "passlib[bcrypt]"
from passlib.context import CryptContext # In this case it used for hashing the password


pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto') # password hashing using bcrypt algorithm

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)