from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User
from app.auth import get_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Create test user
test_user = User(
    email="test@example.com",
    hashed_password=get_password_hash("testpassword123")
)

db.add(test_user)
db.commit()
print("Test user created successfully!")
db.close()
