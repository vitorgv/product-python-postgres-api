import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Get database connection details from environment variables
db_url = os.getenv("DATABASE_URL")

# Parse the URL to get connection parameters
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

    # Query to check users
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()

    print("\nUsers in database:")
    for user in users:
        print(f"ID: {user[0]}")
        print(f"Email: {user[1]}")
        print(f"Password Hash: {user[2]}")
        print(f"Active: {user[3]}")
        print("-" * 50)

    # Close cursor and connection
    cur.close()
    conn.close()

except Exception as e:
    print(f"Error: {str(e)}")
