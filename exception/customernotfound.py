class CustomerNotFound(Exception):
    def __init__(self, message="Customer not found."):
        self.message = message
        super().__init__(self.message)
