import os
from databricks import sql
from databricks.sdk.core import Config
import streamlit as st
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


class CountryCurrencyUI:
    """Class to handle the Streamlit UI"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        
        # Setup page configuration
        st.set_page_config(layout="wide")
        
        # Initialize session state for tracking operations
        if 'operation_performed' not in st.session_state:
            st.session_state.operation_performed = False
        if 'operation_message' not in st.session_state:
            st.session_state.operation_message = ""
        if 'operation_status' not in st.session_state:
            st.session_state.operation_status = ""
        
        # Load data - this will refresh on each rerun
        self.data = self.db_manager.get_all_countries()
    
    def set_operation_status(self, message, status):
        """Set operation status in session state and trigger rerun"""
        st.session_state.operation_performed = True
        st.session_state.operation_message = message
        st.session_state.operation_status = status
        st.rerun()
    
    def display_operation_feedback(self):
        """Display operation feedback messages"""
        if st.session_state.operation_performed:
            if st.session_state.operation_status == "success":
                st.success(st.session_state.operation_message)
            else:
                st.error(st.session_state.operation_message)
            # Reset the flag after displaying
            st.session_state.operation_performed = False
    
    def render_view_tab(self):
        """Render the View tab"""
        st.header("View Countries and Currencies")
        
        # Filter by country
        country = st.text_input("Enter country name for filtering:", "", key="view_country_filter")
        if country:
            filtered_data = self.data[self.data["country"].str.contains(country, case=False, na=False)]
            st.write(f"Search results for '{country}':")
            st.dataframe(filtered_data)
        
        # Sort data
        col1, col2 = st.columns(2)
        with col1:
            sort_column = st.selectbox("Select column for sorting:", self.data.columns)
        with col2:
            sort_order = st.radio("Sort order:", ["Ascending", "Descending"])
        
        ascending = True if sort_order == "Ascending" else False
        sorted_data = self.data.sort_values(by=sort_column, ascending=ascending)
        st.write("Sorted data:")
        st.dataframe(sorted_data)
    
    def render_add_tab(self):
        """Render the Add Entry tab"""
        st.header("Add New Country/Currency Entry")
        
        # Form for creating a new entry
        with st.form(key="add_entry_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_country_code = st.text_input("Country Code (ISO Alpha-3)", max_chars=3).upper()
                new_country_number = st.text_input("Country Number", help="Numeric code for country")
                new_country = st.text_input("Country Name").upper()
            
            with col2:
                new_currency_name = st.text_input("Currency Name")
                new_currency_code = st.text_input("Currency Code", max_chars=3).upper()
                new_currency_number = st.text_input("Currency Number", help="Numeric code for currency")
            
            submit_button = st.form_submit_button(label="Add Entry")
            
            if submit_button:
                # Validate inputs
                if not (new_country_code and new_country_number and new_country and 
                        new_currency_name and new_currency_code and new_currency_number):
                    self.set_operation_status("All fields are required!", "error")
                else:
                    try:
                        # Check if country code already exists
                        existing = self.data[self.data['country_code'] == new_country_code]
                        if not existing.empty:
                            self.set_operation_status(f"Country code {new_country_code} already exists!", "error")
                        else:
                            success = self.db_manager.add_country(
                                new_country_code, new_country_number, new_country,
                                new_currency_name, new_currency_code, new_currency_number
                            )
                            
                            if success:
                                self.set_operation_status("Entry added successfully!", "success")
                            else:
                                self.set_operation_status("Failed to add entry. Please try again.", "error")
                    except Exception as e:
                        self.set_operation_status(f"Error: {str(e)}", "error")
    
    def render_edit_tab(self):
        """Render the Edit Entry tab"""
        st.header("Edit Existing Entry")
        
        # First, select a country to edit
        country_to_edit = st.selectbox(
            "Select a country to edit:",
            options=self.data['country'].tolist(),
            format_func=lambda x: x
        )
        
        # Get the selected country's data
        selected_row = self.data[self.data['country'] == country_to_edit].iloc[0]
        
        # Form for editing
        with st.form(key="edit_entry_form"):
            col1, col2 = st.columns(2)
            with col1:
                edit_country_code = st.text_input("Country Code (ISO Alpha-3)", 
                                                value=selected_row['country_code'], max_chars=3).upper()
                edit_country_number = st.text_input("Country Number", 
                                                  value=str(selected_row['country_number']))
                edit_country = st.text_input("Country Name", 
                                            value=selected_row['country']).upper()
            
            with col2:
                edit_currency_name = st.text_input("Currency Name", 
                                                value=selected_row['currency_name'])
                edit_currency_code = st.text_input("Currency Code", 
                                                value=selected_row['currency_code'], max_chars=3).upper()
                edit_currency_number = st.text_input("Currency Number", 
                                                  value=str(selected_row['currency_number']))
            
            submit_button = st.form_submit_button(label="Update Entry")
            
            if submit_button:
                # Validate inputs
                if not (edit_country_code and edit_country_number and edit_country and 
                        edit_currency_name and edit_currency_code and edit_currency_number):
                    self.set_operation_status("All fields are required!", "error")
                else:
                    try:
                        success = self.db_manager.update_country(
                            selected_row['country_code'],  # Original code
                            edit_country_code, edit_country_number, edit_country,
                            edit_currency_name, edit_currency_code, edit_currency_number
                        )
                        
                        if success:
                            self.set_operation_status("Entry updated successfully!", "success")
                        else:
                            self.set_operation_status("Failed to update entry. Please try again.", "error")
                    except Exception as e:
                        self.set_operation_status(f"Error: {str(e)}", "error")
    
    def render_delete_tab(self):
        """Render the Delete Entry tab"""
        st.header("Delete Entry")
        
        # Select a country to delete
        country_to_delete = st.selectbox(
            "Select a country to delete:",
            options=self.data['country'].tolist(),
            format_func=lambda x: x,
            key="delete_country"
        )
        
        # Get the selected country's data
        if country_to_delete:
            selected_row = self.data[self.data['country'] == country_to_delete].iloc[0]
            
            # Display the selected entry
            st.write("Entry to delete:")
            st.dataframe(pd.DataFrame([selected_row]))
            
            # Confirmation
            delete_confirmation = st.checkbox("I confirm that I want to delete this entry")
            
            if st.button("Delete Entry", disabled=not delete_confirmation):
                try:
                    success = self.db_manager.delete_country(selected_row['country_code'])
                    
                    if success:
                        self.set_operation_status("Entry deleted successfully!", "success")
                    else:
                        self.set_operation_status("Failed to delete entry. Please try again.", "error")
                except Exception as e:
                    self.set_operation_status(f"Error: {str(e)}", "error")
    
    def render(self):
        """Render the full UI"""
        # App title
        st.title("Country and Currency Database")
        
        # Display operation feedback if any
        self.display_operation_feedback()
        
        # Create tabs for different operations
        tab1, tab2, tab3, tab4 = st.tabs(["View Data", "Add Entry", "Edit Entry", "Delete Entry"])
        
        # Render each tab
        with tab1:
            self.render_view_tab()
        
        with tab2:
            self.render_add_tab()
        
        with tab3:
            self.render_edit_tab()
        
        with tab4:
            self.render_delete_tab()


def main():
    # Create database manager
    db_manager = DatabaseManager()
    
    # Create and render UI
    ui = CountryCurrencyUI(db_manager)
    ui.render()


if __name__ == "__main__":
    main()
