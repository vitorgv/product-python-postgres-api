-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    category_id INTEGER REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster searches
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_category ON products(category_id);

-- Insert test data
-- Test user (password: testpass123)
INSERT INTO users (email, hashed_password) 
VALUES ('admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKpCQOCI1bHCYha');

-- Categories
INSERT INTO categories (name, description) VALUES
    ('Electronics', 'Electronic devices and accessories'),
    ('Books', 'Physical and digital books'),
    ('Clothing', 'Apparel and accessories'),
    ('Home & Garden', 'Home improvement and garden supplies'),
    ('Sports', 'Sports equipment and accessories');

-- Products
INSERT INTO products (name, description, price, quantity, category_id) VALUES
    ('Smartphone X', 'Latest model with 5G capability', 999.99, 50, 1),
    ('Laptop Pro', '15-inch laptop with SSD', 1299.99, 30, 1),
    ('Wireless Earbuds', 'Noise-cancelling earbuds', 199.99, 100, 1),
    
    ('Python Programming', 'Complete guide to Python', 49.99, 200, 2),
    ('Data Science Handbook', 'Comprehensive data science guide', 59.99, 150, 2),
    
    ('Running Shoes', 'Professional running shoes', 129.99, 75, 3),
    ('Sport T-Shirt', 'Breathable sport t-shirt', 29.99, 200, 3),
    
    ('Garden Tools Set', 'Complete set of garden tools', 89.99, 40, 4),
    ('Smart LED Bulb', 'WiFi-enabled LED bulb', 19.99, 300, 4),
    
    ('Tennis Racket', 'Professional tennis racket', 159.99, 25, 5),
    ('Yoga Mat', 'Non-slip yoga mat', 39.99, 150, 5);

-- Create a function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create a trigger to automatically update timestamps
CREATE TRIGGER update_products_updated_at
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
