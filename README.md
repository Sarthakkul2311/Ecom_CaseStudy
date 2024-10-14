# E-Commerce Application

This is a Python-based E-commerce Application with MS SQL connectivity. The system enables customers to browse and purchase products, add items to a cart, and place orders. The system is designed with Object-Oriented Programming principles and is modular, scalable, and includes unit tests.

## Features

- Customer registration and management
- Product creation, deletion, and listing
- Add or remove products from the shopping cart
- Place orders and view customer order history
- View all products and customers
- Manage cart contents
- Update customer information
- MS SQL Server database integration

## Project Structure
ecommerce_project/
│
├── entity/
│   ├── cart.py
│   ├── customer.py
│   ├── order.py
│   ├── order_item.py
│   └── product.py
|   └── __init__.py
│
├── dao/
│   ├── OrderProcessorRepository.py
│   └── OrderProcessorRepositoryImpl.py
|   └── __init__.py
│
├── exception/
│   ├── customernotfound.py
│   ├── ordernotfound.py
│   └── productnotfound.py
|   └── __init__.py
│
├── util/
│   ├── DBConnection.py
│   └── db_connector.py
|   └── __init__.py
│
├── main/
│   └── mainmodule.py
|   └── __init__.py
│
└── __init__.py
└── UnitTesting.py


## Technologies
--> Python 3.x
--> MS SQL Server (PyODBC)
--> Object-Oriented Programming (OOP)
--> Unit testing (unittest)
--> SQL Server

### Clone the repository:
git clone https://github.com/your-username/ecommerce_project.git

### Install required dependencies:
pip install pyodbc
python UnitTesting.py

### Configure the database connection:
Modify the DBConnection.py or db_connector.py file under the util/ package with your MS SQL Server configuration (server name, database, username, and password).

### Set up the database schema:
Use the schema provided below to create the necessary tables in the MS SQL Server database.

## Database Schema
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(20),
    email VARCHAR(300),
    password VARCHAR(300)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(30),
    price DECIMAL(10,2),
    description VARCHAR(200),
    stockQuantity INT
);

CREATE TABLE cart (
    cart_id INT PRIMARY KEY,
    customer_id INT FOREIGN KEY REFERENCES customers(customer_id) ON DELETE CASCADE,
    product_id INT FOREIGN KEY REFERENCES products(product_id) ON DELETE CASCADE,
    quantity INT
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT FOREIGN KEY REFERENCES customers(customer_id) ON DELETE CASCADE,
    order_date DATE,
    total_price DECIMAL(10,2),
    shipping_address VARCHAR(50)
);

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT FOREIGN KEY REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INT FOREIGN KEY REFERENCES products(product_id) ON DELETE SET NULL,
    quantity INT
);

#### Author: Sarthak Niranjan Kulkarni
