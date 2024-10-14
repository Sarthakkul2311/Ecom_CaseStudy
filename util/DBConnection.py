import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pyodbc
from util.PropertyUtil import PropertyUtil  # Adjust import based on your package structure

class DBConnection:
    connection = None

    @staticmethod
    def get_connection():
        if DBConnection.connection is None:
            try:
                conn_str = PropertyUtil.get_property_string()
                DBConnection.connection = pyodbc.connect(conn_str)
                print("Connected Successfully")
            except Exception as e:
                print(f"Connection failed: {e}")
        return DBConnection.connection
    @staticmethod
    def test_connection():
        # This method will only test the connection without executing any queries
        connection = DBConnection.get_connection()
        if connection:
            print("Database connection is successful.")
        else:
            print("Failed to connect to the database.")

if __name__ == "__main__":
    DBConnection.test_connection()