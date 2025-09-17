# Product Management System API

A Python FastAPI-based Product Management System with PostgreSQL integration for GCP.

## Features

- CRUD operations for products and categories
- Token-based authentication with 10-minute expiration
- Product filtering by category and name
- Export products to CSV or JSON
- RESTful API endpoints

## Requirements

- Python 3.8+
- PostgreSQL database
- Required Python packages (installed via pip):
  - fastapi
  - uvicorn
  - sqlalchemy
  - psycopg2-binary
  - python-jose[cryptography]
  - passlib[bcrypt]
  - python-multipart
  - python-dotenv

## Setup

1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file with the following variables:
   ```
   DATABASE_URL=postgresql://user:password@host:5432/database
   SECRET_KEY=your-secret-key-for-jwt
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=10
   ```
5. Run the application:
   ```
   python run.py
   ```

## API Endpoints

### Authentication
- POST `/token` - Get access token

### Categories
- POST `/categories/` - Create category
- GET `/categories/` - List categories
- GET `/categories/{category_id}` - Get category details

### Products
- POST `/products/` - Create product
- GET `/products/` - List products (with optional filters)
- GET `/products/{product_id}` - Get product details
- PUT `/products/{product_id}` - Update product
- DELETE `/products/{product_id}` - Delete product

### Export
- GET `/export/products/json` - Export products as JSON
- GET `/export/products/csv` - Export products as CSV

## Usage

1. First, create a user in the database
2. Get an access token by sending a POST request to `/token` with username and password
3. Use the token in the Authorization header for all other requests:
   ```
   Authorization: Bearer <your-token>
   ```

## Security

- Token-based authentication using JWT
- Tokens expire after 10 minutes
- Secure password hashing using bcrypt
- PostgreSQL connection with SSL support
