import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dao.OrderProcessorRepository import OrderProcessorRepository
from typing import List, Dict, Optional, Tuple
from entity.customer import Customer
from entity.product import Product
from entity.cart import Cart
from exception.customernotfound import CustomerNotFound
from exception.productnotfound import ProductNotFound
from util.DBConnection import DBConnection

class OrderProcessorRepositoryImpl(OrderProcessorRepository):
    def __init__(self):
        self.connection = DBConnection.get_connection()

    def create_product(self, product: Product) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO products (product_id, name, price, description, stockQuantity) VALUES (?, ?, ?, ?, ?)",
                (product.get_product_id(), product.get_name(), product.get_price(), product.get_description(), product.get_stockQuantity())
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error creating product: {e}")
            return False

    def create_customer(self, customer: Customer) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO customers (customer_id, name, email, password) VALUES (?, ?, ?, ?)",
                (customer.get_customer_id(), customer.get_name(), customer.get_email(), customer.get_password())
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error creating customer: {e}")
            return False

    def delete_product(self, product_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
            if cursor.fetchone() is None:
                raise ProductNotFound(f"Product ID {product_id} does not exist.")
            
            cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
            self.connection.commit()
            return True
        except ProductNotFound as e:
            print(e)
            return False
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False

    def delete_customer(self, customer_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
            if cursor.fetchone() is None:
                raise CustomerNotFound(f"Customer ID {customer_id} does not exist.")
            
            cursor.execute("DELETE FROM customers WHERE customer_id = ?", (customer_id,))
            self.connection.commit()
            return True
        except CustomerNotFound as e:
            print(e)
            return False
        except Exception as e:
            print(f"Error deleting customer: {e}")
            return False

    def add_to_cart(self, customer: Customer, product: Product, quantity: int) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(cart_id) FROM cart")
            max_cart_id = cursor.fetchone()[0]
            new_cart_id = 1 if max_cart_id is None else max_cart_id + 1
            
            cursor.execute(
                "INSERT INTO cart (cart_id, customer_id, product_id, quantity) VALUES (?, ?, ?, ?)",
                (new_cart_id, customer.get_customer_id(), product.get_product_id(), quantity)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding to cart: {e}")
            return False

    def remove_product_from_cart(self, customer_id: int, product_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute("""DELETE FROM cart WHERE customer_id = ? AND product_id = ?""", (customer_id, product_id))
            self.connection.commit()
            return cursor.rowcount > 0  # Returns True if a row was deleted
        except Exception as e:
            print(f"Error removing product from cart: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def get_all_from_cart(self, customer: Customer) -> List[Dict[Product, int]]:
        cart_items = []
        cursor = self.connection.cursor()
    
        try:
            cursor.execute("SELECT p.product_id, p.name, p.price, c.quantity "
                           "FROM cart c "
                           "JOIN products p ON c.product_id = p.product_id "
                           "WHERE c.customer_id = ?", (customer.get_customer_id(),))
        
            rows = cursor.fetchall()
        
            for row in rows:
                product = Product(
                    product_id=row[0],
                    name=row[1],
                    price=row[2],
                    description='',  # Assuming description is not needed in the cart view
                    stockQuantity=0  # Not needed here, but you can set it to 0 or leave it
                )
                cart_items.append({'product': product, 'quantity': row[3]})  # Use row[3] for quantity
        
        except Exception as e:
            print("Error retrieving cart items:", e)
        finally:
            cursor.close()
    
        return cart_items

    def place_order(self, customer: Customer, product_quantity_map: List[Tuple[Product, int]], shipping_address: str) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(order_id) FROM orders")
            max_order_id = cursor.fetchone()[0]
            new_order_id = 1 if max_order_id is None else max_order_id + 1
            
            total_price = self.calculate_total_price(product_quantity_map)
            cursor.execute(
                "INSERT INTO orders (customer_id, order_id, order_date, total_price, shipping_address) VALUES (?, ?, GETDATE(), ?, ?)",
                (customer.get_customer_id(), new_order_id, total_price, shipping_address)
            )
            
            # Fetch the max order_item_id from the order_items table
            cursor.execute("SELECT MAX(order_item_id) FROM order_items")
            max_order_item_id = cursor.fetchone()[0]
            new_order_item_id = 1 if max_order_item_id is None else max_order_item_id + 1
            
            for product, quantity in product_quantity_map:
                cursor.execute(
                    "INSERT INTO order_items (order_item_id, order_id, product_id, quantity) VALUES (?, ?, ?, ?)",
                    (new_order_item_id, new_order_id, product.get_product_id(), quantity)
                )
                new_order_item_id += 1  # Increment for each order item

                cursor.execute(""" 
                UPDATE products 
                SET stockQuantity = stockQuantity - ? 
                WHERE product_id = ? 
                """, (quantity, product.get_product_id()))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error placing order: {e}")
            self.connection.rollback()  # Rollback in case of any errors
            return False
        finally:
            cursor.close()

    def get_orders_by_customer(self, customer_id: int) -> Dict[Product, int]:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT oi.product_id, oi.quantity, p.price, p.description, p.stockQuantity "
                "FROM orders o "
                "JOIN order_items oi ON o.order_id = oi.order_id "
                "JOIN products p ON oi.product_id = p.product_id "
                "WHERE o.customer_id = ?", 
                (customer_id,)
            )
            rows = cursor.fetchall()
            orders = {}
            for row in rows:
                product_id = row[0]          # product_id from order_items
                quantity = row[1]            # quantity from order_items
                price = row[2]               # price from products
                description = row[3]         # description from products
                stock_quantity = row[4]      # stockQuantity from products

                product = Product(
                    product_id=product_id, 
                    name=None,
                    price=price,
                    description=description, 
                    stockQuantity=stock_quantity
                ) 
                orders[product] = quantity  # quantity
            return orders
        except Exception as e:
            print(f"Error retrieving orders: {e}")
            return {}

    def calculate_total_price(self, product_quantity_map: List[Tuple[Product, int]]) -> float:
        total_price = 0.0
        for product, quantity in product_quantity_map:
            total_price += float(product.get_price() * quantity)
        return total_price
    
    def get_customer_by_id(self, customer_id: int) -> Customer:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
            row = cursor.fetchone()
            if row:
                return Customer(row[0], row[1], row[2], row[3])  # Adjust index based on your schema
            else:
                return None  # No customer found
        except Exception as e:
            print(f"Error retrieving customer: {e}")
            return None

    def get_product_by_id(self, product_id: int) -> Optional[Tuple[int, str, float, str, int]]:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
            return cursor.fetchone()  # Returns a tuple of product details
        except Exception as e:
            print(f"Error retrieving product: {e}")
            return None

    def get_all_customers(self) -> List[Customer]:
        customers = []
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM customers")
            rows = cursor.fetchall()
            for row in rows:
                customer = Customer(row[0], row[1], row[2], row[3])
                customers.append(customer)
        except Exception as e:
            print(f"Error retrieving customers: {e}")
        finally:
            cursor.close()
        return customers

    def get_all_products(self) -> List[Product]:
        products = []
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            for row in rows:
                product = Product(row[0], row[1], row[2], row[3], row[4])
                products.append(product)
        except Exception as e:
            print(f"Error retrieving products: {e}")
        finally:
            cursor.close()
        return products

    def update_customer(self, customer: Customer) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE customers SET name = ?, email = ?, password = ? WHERE customer_id = ?",
                (customer.get_name(), customer.get_email(), customer.get_password(), customer.get_customer_id())
            )
            self.connection.commit()
            return cursor.rowcount > 0  # Return True if a row was updated
        except Exception as e:
            print(f"Error updating customer: {e}")
            return False
