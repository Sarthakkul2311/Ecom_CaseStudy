class PropertyUtil:
    @staticmethod
    def get_property_string():
        hostname = "SARTHAKKULKARNI"  # Your SQL Server instance name
        dbname = "Ecommerce_Application"           # Your database name

        connection_string = (
            f"Driver={{SQL Server}};"
            f"Server={hostname};"
            f"Database={dbname};"
            "Trusted_Connection=yes;"
        )
        return connection_string


