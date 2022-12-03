'''Password hashing stuff'''
from hashlib import scrypt

def check_password_hash(password_hash: str, password: str, password_salt: str) -> bool:
    return scrypt(password.encode(), salt=password_salt.encode(), n=16384, r=8, p=1, dklen=16).hex() == password_hash

def generate_password_hash(password: str, password_salt: str) -> str:
    return scrypt(password.encode(), salt=password_salt.encode(), n=16384, r=8, p=1, dklen=16).hex()
