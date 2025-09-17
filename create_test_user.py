from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User
from app.auth import get_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

# Create test user with known credentials
user_email = "admin@example.com"
user_password = "testpass123"
hashed_password = get_password_hash(user_password)

print(f"Test user email: {user_email}")
print(f"Test user password: {user_password}")
print(f"Hashed password: {hashed_password}")

# Connect to database and create user
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Create the user
test_user = User(
    email=user_email,
    hashed_password=hashed_password,
    is_active=1
)

try:
    db.add(test_user)
    db.commit()
    print("\nTest user created successfully!")
except Exception as e:
    print(f"\nError creating user: {str(e)}")
finally:
    db.close()
