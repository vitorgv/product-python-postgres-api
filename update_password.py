from passlib.context import CryptContext
import psycopg2
from dotenv import load_dotenv
import os

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# Test user credentials
test_password = "testpass123"
hashed_password = get_password_hash(test_password)

# Database connection parameters
db_params = {
    "host": "localhost",
    "database": "productdb",
    "user": "postgres",
    "password": "postgres",
    "port": "5432"
}

try:
    # Connect to the database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Update user's password
    cur.execute(
        "UPDATE users SET hashed_password = %s WHERE email = 'admin@example.com'",
        (hashed_password,)
    )
    conn.commit()

    print(f"\nPassword updated successfully!")
    print(f"Email: admin@example.com")
    print(f"Password: {test_password}")
    print(f"New hash: {hashed_password}")

    # Close cursor and connection
    cur.close()
    conn.close()

except Exception as e:
    print(f"Error: {str(e)}")
