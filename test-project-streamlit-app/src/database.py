# File: src/database.py
import os
from databricks import sql
from databricks.sdk.core import Config
import pandas as pd

class DatabaseManager:
    """Class to handle all database operations"""
    
    def __init__(self):
        # Ensure environment variable is set correctly
        assert os.getenv('DATABRICKS_WAREHOUSE_ID'), "DATABRICKS_WAREHOUSE_ID must be set in app.yaml."
        self.cfg = Config()  # Pull environment variables for auth
    
    def query(self, query: str) -> pd.DataFrame:
        """Execute a SQL query and return results as a DataFrame"""
        with sql.connect(
            server_hostname=self.cfg.host,
            http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_WAREHOUSE_ID')}",
            credentials_provider=lambda: self.cfg.authenticate
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall_arrow().to_pandas()
    
    def execute(self, query: str, params=None) -> bool:
        """Execute SQL statement with optional parameters."""
        try:
            with sql.connect(
                server_hostname=self.cfg.host,
                http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_WAREHOUSE_ID')}",
                credentials_provider=lambda: self.cfg.authenticate
            ) as connection:
                with connection.cursor() as cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    connection.commit()
                    return True
        except Exception as e:
            print(f"Database error: {str(e)}")
            return False
    
    def get_all_countries(self):
        """Get all country data from the database"""
        return self.query("select * from test_project.country_code_to_currency.country_currency_table")
    
    def add_country(self, country_code, country_number, country, currency_name, currency_code, currency_number):
        """Add a new country to the database"""
        query = """
        INSERT INTO test_project.country_code_to_currency.country_currency_table 
        (country_code, country_number, country, currency_name, currency_code, currency_number)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (country_code, country_number, country, currency_name, currency_code, currency_number)
        return self.execute(query, params)
    
    def update_country(self, original_country_code, country_code, country_number, country, 
                      currency_name, currency_code, currency_number):
        """Update an existing country in the database"""
        query = """
        UPDATE test_project.country_code_to_currency.country_currency_table 
        SET country_code = ?, country_number = ?, country = ?, 
            currency_name = ?, currency_code = ?, currency_number = ?
        WHERE country_code = ?
        """
        params = (country_code, country_number, country, currency_name, currency_code, currency_number, original_country_code)
        return self.execute(query, params)
    
    def delete_country(self, country_code):
        """Delete a country from the database"""
        query = """
        DELETE FROM test_project.country_code_to_currency.country_currency_table 
        WHERE country_code = ?
        """
        params = (country_code,)
        return self.execute(query, params)
