from db.database import SessionLocal
from sqlalchemy.orm import Session
import bcrypt

def verify_password(plain_password, hashed_password):
    try:
        # Password ah bytes ah maathi (encode), 72 limit panni check panrom
        return bcrypt.checkpw(plain_password.encode()[:72], hashed_password.encode())
    except ValueError:
        # Check if legacy plain-text password
        return plain_password == hashed_password

def get_password_hash(password):
    # Password ah bytes ah maathi, 72 limit panni hash panrom
    hashed = bcrypt.hashpw(password.encode()[:72], bcrypt.gensalt())
    return hashed.decode()

def connect_to_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()