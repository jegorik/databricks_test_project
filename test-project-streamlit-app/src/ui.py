# File: src/ui.py
import streamlit as st
import pandas as pd
from templates.html_components import *

class CountryCurrencyUI:
    """Class to handle the Streamlit UI"""
    
    # File: src/ui.py (modified __init__ method)
    def __init__(self, db_manager):
        self.db_manager = db_manager
        
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
        """Display operation feedback messages with custom styling"""
        if st.session_state.operation_performed:
            if st.session_state.operation_status == "success":
                st.markdown(success_message(st.session_state.operation_message), unsafe_allow_html=True)
            else:
                st.markdown(error_message(st.session_state.operation_message), unsafe_allow_html=True)
            # Reset the flag after displaying
            st.session_state.operation_performed = False
    
    def render_view_tab(self):
        """Render the View tab with enhanced styling"""
        st.markdown(section_header("📊", "View Countries and Currencies"), unsafe_allow_html=True)
        
        # Search card
        st.markdown(card_start(), unsafe_allow_html=True)
        st.markdown(
            field_label("Search by Country Name", "Enter a partial or full country name to filter the data."), 
            unsafe_allow_html=True
        )
        
        country = st.text_input("", placeholder="Type country name here...", key="view_country_filter")
        
        if country:
            filtered_data = self.data[self.data["country"].str.contains(country, case=False, na=False)]
            
            count = len(filtered_data)
            st.markdown(f"""
            <div style="margin-top: 15px;">
                Found <span class="badge">{count}</span> results for '{country}'
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(dataframe_container_start(), unsafe_allow_html=True)
            st.dataframe(filtered_data, use_container_width=True)
            st.markdown(dataframe_container_end(), unsafe_allow_html=True)
        st.markdown(card_end(), unsafe_allow_html=True)
        
        # Sort card
        st.markdown(card_start(), unsafe_allow_html=True)
        st.markdown(
            field_label("Sort Data", "Choose a column and sort direction to organize the data."), 
            unsafe_allow_html=True
        )
        
        col1, col2 = st.columns(2)
        with col1:
            sort_column = st.selectbox("Column", self.data.columns)
        with col2:
            sort_order = st.radio("Order", ["Ascending", "Descending"])
        
        ascending = True if sort_order == "Ascending" else False
        sorted_data = self.data.sort_values(by=sort_column, ascending=ascending)
        
        st.markdown(dataframe_container_start(), unsafe_allow_html=True)
        st.dataframe(sorted_data, use_container_width=True)
        st.markdown(dataframe_container_end(), unsafe_allow_html=True)
        st.markdown(card_end(), unsafe_allow_html=True)
    
    def render_add_tab(self):
        """Render the Add Entry tab with enhanced styling"""
        st.markdown(section_header("➕", "Add New Country/Currency Entry"), unsafe_allow_html=True)
        
        st.markdown(card_start(), unsafe_allow_html=True)
        # Form for creating a new entry
        with st.form(key="add_entry_form"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(field_label("Country Information"), unsafe_allow_html=True)
                
                st.markdown(
                    tooltip_field("Country Code (ISO Alpha-3)", "Three-letter country code (e.g., USA, GBR)"), 
                    unsafe_allow_html=True
                )
                new_country_code = st.text_input("", placeholder="e.g. USA", max_chars=3, key="add_code").upper()
                
                st.markdown(
                    tooltip_field("Country Number", "Numeric code assigned to the country"), 
                    unsafe_allow_html=True
                )
                new_country_number = st.text_input("", placeholder="e.g. 840", key="add_country_num")
                
                st.markdown(
                    tooltip_field("Country Name", "Full official name of the country"), 
                    unsafe_allow_html=True
                )
                new_country = st.text_input("", placeholder="e.g. UNITED STATES", key="add_country_name").upper()
            
            with col2:
                st.markdown(field_label("Currency Information"), unsafe_allow_html=True)
                
                st.markdown(
                    tooltip_field("Currency Name", "Full name of the country's currency"), 
                    unsafe_allow_html=True
                )
                new_currency_name = st.text_input("", placeholder="e.g. US Dollar", key="add_currency_name")
                
                st.markdown(
                    tooltip_field("Currency Code", "Three-letter currency code (e.g., USD, EUR)"), 
                    unsafe_allow_html=True
                )
                new_currency_code = st.text_input("", placeholder="e.g. USD", max_chars=3, key="add_currency_code").upper()
                
                st.markdown(
                    tooltip_field("Currency Number", "Numeric code assigned to the currency"), 
                    unsafe_allow_html=True
                )
                new_currency_number = st.text_input("", placeholder="e.g. 840", key="add_currency_num")
            
            st.markdown('<br>', unsafe_allow_html=True)
            submit_button = st.form_submit_button(label="➕ Add New Entry")
            
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
        st.markdown(card_end(), unsafe_allow_html=True)
    
    def render_edit_tab(self):
        """Render the Edit Entry tab with enhanced styling"""
        st.markdown(section_header("✏️", "Edit Existing Entry"), unsafe_allow_html=True)
        
        st.markdown(card_start(), unsafe_allow_html=True)
        st.markdown(
            field_label("Select Country to Edit", "Choose the country record you want to modify."), 
            unsafe_allow_html=True
        )
        
        # First, select a country to edit
        country_to_edit = st.selectbox(
            "",
            options=self.data['country'].tolist(),
            format_func=lambda x: x,
            index=0
        )
        
        # Get the selected country's data
        selected_row = self.data[self.data['country'] == country_to_edit].iloc[0]
        
        # Display current data
        st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
        st.markdown(field_label("Current Data:"), unsafe_allow_html=True)
        st.markdown(dataframe_container_start(), unsafe_allow_html=True)
        st.dataframe(pd.DataFrame([selected_row]), use_container_width=True)
        st.markdown(dataframe_container_end(), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Form for editing
        with st.form(key="edit_entry_form"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(field_label("Country Information"), unsafe_allow_html=True)
                
                st.markdown(
                    tooltip_field("Country Code (ISO Alpha-3)", "Three-letter country code (e.g., USA, GBR)"), 
                    unsafe_allow_html=True
                )
                edit_country_code = st.text_input("", 
                                               value=selected_row['country_code'], 
                                               max_chars=3,
                                               key="edit_code").upper()
                
                st.markdown(
                    tooltip_field("Country Number", "Numeric code assigned to the country"), 
                    unsafe_allow_html=True
                )
                edit_country_number = st.text_input("", 
                                                 value=str(selected_row['country_number']),
                                                 key="edit_country_num")
                
                st.markdown(
                    tooltip_field("Country Name", "Full official name of the country"), 
                    unsafe_allow_html=True
                )
                edit_country = st.text_input("", 
                                          value=selected_row['country'],
                                          key="edit_country_name").upper()
            
            with col2:
                st.markdown(field_label("Currency Information"), unsafe_allow_html=True)
                
                st.markdown(
                    tooltip_field("Currency Name", "Full name of the country's currency"), 
                    unsafe_allow_html=True
                )
                edit_currency_name = st.text_input("", 
                                               value=selected_row['currency_name'],
                                               key="edit_currency_name")
                
                st.markdown(
                    tooltip_field("Currency Code", "Three-letter currency code (e.g., USD, EUR)"), 
                    unsafe_allow_html=True
                )
                edit_currency_code = st.text_input("", 
                                               value=selected_row['currency_code'], 
                                               max_chars=3,
                                               key="edit_currency_code").upper()
                
                st.markdown(
                    tooltip_field("Currency Number", "Numeric code assigned to the currency"), 
                    unsafe_allow_html=True
                )
                edit_currency_number = st.text_input("", 
                                                 value=str(selected_row['currency_number']),
                                                 key="edit_currency_num")
            
            st.markdown('<br>', unsafe_allow_html=True)
            submit_button = st.form_submit_button(label="✅ Update Entry")
            
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
        st.markdown(card_end(), unsafe_allow_html=True)
    
    def render_delete_tab(self):
        """Render the Delete Entry tab with enhanced styling"""
        st.markdown(section_header("🗑️", "Delete Entry"), unsafe_allow_html=True)
        st.markdown(delete_warning(), unsafe_allow_html=True)
        
        st.markdown(card_start(), unsafe_allow_html=True)
        st.markdown(
            field_label("Select Country to Delete", "Choose the country record you want to remove from the database."), 
            unsafe_allow_html=True
        )
        
        # Select a country to delete
        country_to_delete = st.selectbox(
            "",
            options=self.data['country'].tolist(),
            format_func=lambda x: x,
            key="delete_country"
        )
        
        # Get the selected country's data
        if country_to_delete:
            selected_row = self.data[self.data['country'] == country_to_delete].iloc[0]
            
            # Display the selected entry
            st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
            st.markdown(field_label("Entry to delete:"), unsafe_allow_html=True)
            st.markdown(dataframe_container_start("#e74c3c"), unsafe_allow_html=True)
            st.dataframe(pd.DataFrame([selected_row]), use_container_width=True)
            st.markdown(dataframe_container_end(), unsafe_allow_html=True)
            
            # Confirmation
            confirmation_container = st.container()
            with confirmation_container:
                st.markdown(delete_confirmation(), unsafe_allow_html=True)
                delete_confirmation_checkbox = st.checkbox("I confirm that I want to delete this entry")
            
            # Using custom CSS for the delete button
            if delete_confirmation_checkbox:
                if st.button("🗑️ Delete Entry", type="primary"):
                    try:
                        success = self.db_manager.delete_country(selected_row['country_code'])
                        
                        if success:
                            self.set_operation_status("Entry deleted successfully!", "success")
                        else:
                            self.set_operation_status("Failed to delete entry. Please try again.", "error")
                    except Exception as e:
                        self.set_operation_status(f"Error: {str(e)}", "error")
            else:
                st.markdown(disabled_button(), unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(card_end(), unsafe_allow_html=True)
    
    def render(self):
        """Render the full UI with enhanced styling"""
        # App title with HTML
        st.markdown(app_header(), unsafe_allow_html=True)
        
        # Display operation feedback if any
        self.display_operation_feedback()
        
        # Create tabs for different operations with emojis
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 View Data", 
            "➕ Add Entry", 
            "✏️ Edit Entry", 
            "🗑️ Delete Entry"
        ])
        
        # Render each tab
        with tab1:
            self.render_view_tab()
        
        with tab2:
            self.render_add_tab()
        
        with tab3:
            self.render_edit_tab()
        
        with tab4:
            self.render_delete_tab()
        
        # Footer
        st.markdown(footer(), unsafe_allow_html=True)
