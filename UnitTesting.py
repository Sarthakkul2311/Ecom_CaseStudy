import sys
import os
import unittest
from entity.product import Product
from entity.customer import Customer
from dao.OrderProcessorRepositoryImpl import OrderProcessorRepositoryImpl
from exception.customernotfound import CustomerNotFound
from exception.productnotfound import ProductNotFound

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestEcommerceSystem(unittest.TestCase):
    def setUp(self):
        self.repository = OrderProcessorRepositoryImpl()


        # Create a sample customer and product for testing
        self.customer = Customer(customer_id=220, name="Aman", email="aman32@gmail.com", password="pass@45")
        self.product = Product(product_id=2002, name="Belt", price=499.99, description="Stylish belt for students", stockQuantity=20)

        # Add sample customer and product to the repository for testing
        self.repository.create_customer(self.customer)
        self.repository.create_product(self.product)

    def test_product_created_successfully(self):
        """Test case to check if product is created successfully."""
        product = self.repository.get_product_by_id(2002)  # Use the new product ID
        self.assertIsNotNone(product)
        self.assertEqual(product.get_name(), "Belt")  # Check product name

    def test_product_added_to_cart_successfully(self):
        """Test case to check if product is added to cart successfully."""
        quantity = 2
        result = self.repository.add_to_cart(self.customer, self.product, quantity)
        self.assertTrue(result)  # Ensure product was added successfully

    def test_product_ordered_successfully(self):
        """Test case to check if product is ordered successfully."""
        quantity = 1
        shipping_address = "456 Oak St"
        result = self.repository.place_order(self.customer, [(self.product, quantity)], shipping_address)
        self.assertTrue(result)  # Ensure the order was placed successfully

    def test_exception_thrown_when_customer_not_found(self):
        """Test case to check if exception is thrown when customer ID not found."""
        with self.assertRaises(CustomerNotFound):
            self.repository.get_customer_by_id(20)  # Using a non-existent customer ID

    def test_exception_thrown_when_product_not_found(self):
        """Test case to check if exception is thrown when product ID not found."""
        with self.assertRaises(ProductNotFound):
            self.repository.get_product_by_id(200)  # Using a non-existent product ID

if __name__== "__main__":
   unittest.main()