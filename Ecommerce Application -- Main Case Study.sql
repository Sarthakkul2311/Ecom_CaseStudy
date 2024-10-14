CREATE database Ecommerce_Application;

use Ecommerce_Application;

create table customers(
customer_id int PRIMARY KEY,
name varchar(20),
email varchar(300),
password varchar(300)
);


create table products(
product_id int PRIMARY KEY,
name varchar(30),
price decimal(10,2),
description varchar(200),
stockQuantity int
);


create table cart(
cart_id int PRIMARY KEY,
customer_id INT,
product_id INT,
quantity INT, 
FOREIGN KEY(customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
FOREIGN KEY(product_id) REFERENCES products(product_id) ON DELETE CASCADE
);


create table orders(
order_id int PRIMARY KEY,
customer_id INT,
order_date date,
total_price decimal(10,2), 
shipping_address varchar(50),
FOREIGN KEY(customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);


create table order_items(
order_item_id int PRIMARY KEY,
order_id INT,
product_id INT,
quantity INT, 
FOREIGN KEY(order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
FOREIGN KEY(product_id) REFERENCES products(product_id) ON DELETE SET NULL
);
select * from order_items;
-- Drop order_items table first due to foreign key constraints
DROP TABLE IF EXISTS order_items;

-- Drop orders table second due to foreign key constraints
DROP TABLE IF EXISTS orders;

-- Drop cart table third due to foreign key constraints
DROP TABLE IF EXISTS cart;

-- Drop products table last as it is referenced by other tables
DROP TABLE IF EXISTS products;

-- Finally, drop customers table
DROP TABLE IF EXISTS customers;

SELECT * FROM customers;
SELECT * FROM products;
SELECT * FROM cart;
SELECT * FROM orders;
SELECT * FROM order_items;

DELETE FROM cart WHERE cart_id = 2;

