CREATE DATABASE price_tracker;

USE price_tracker;

-- Table to store product details
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    url VARCHAR(255) UNIQUE,
    current_price INT,
    last_updated DATETIME
);

-- Table to store historical price data
CREATE TABLE price_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_url VARCHAR(255),
    price INT,
    timestamp DATETIME,
    FOREIGN KEY (product_url) REFERENCES products(url)
);
