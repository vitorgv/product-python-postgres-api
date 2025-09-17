from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Get all users
users = db.query(User).all()
print("\nCurrent users in database:")
for user in users:
    print(f"ID: {user.id}")
    print(f"Email: {user.email}")
    print(f"Password hash: {user.hashed_password}")
    print(f"Active: {user.is_active}")
    print("-" * 50)

db.close()
