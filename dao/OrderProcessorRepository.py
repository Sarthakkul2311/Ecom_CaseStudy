from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple
from entity.customer import Customer
from entity.product import Product
from entity.cart import Cart

class OrderProcessorRepository(ABC):
    @abstractmethod
    def create_customer(self, customer: Customer) -> bool:
        pass

    @abstractmethod
    def create_product(self, product: Product) -> bool:
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> bool:
        pass

    @abstractmethod
    def delete_customer(self, customer_id: int) -> bool:
        pass

    @abstractmethod
    def add_to_cart(self, customer: Customer, product: Product, quantity: int) -> bool:
        pass

    @abstractmethod
    def remove_product_from_cart(self, customer_id: int, product_id: int) -> bool:
        pass

    @abstractmethod
    def get_all_from_cart(self, customer: Customer) -> List[Dict[Product, int]]:
        pass

    @abstractmethod
    def place_order(self, customer: Customer, product_quantity_map: List[Tuple[Product, int]], shipping_address: str) -> bool:
        pass

    @abstractmethod
    def get_orders_by_customer(self, customer_id: int) -> Dict[Product, int]:
        pass

    @abstractmethod
    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Optional[Tuple[int, str, float, str, int]]:
        pass

    @abstractmethod
    def get_all_customers(self) -> List[Customer]:
        pass
