import os
from databricks import sql
from databricks.sdk.core import Config
import streamlit as st
import pandas as pd

# Ensure environment variable is set correctly
assert os.getenv('DATABRICKS_WAREHOUSE_ID'), "DATABRICKS_WAREHOUSE_ID must be set in app.yaml."

def sqlQuery(query: str) -> pd.DataFrame:
    cfg = Config() # Pull environment variables for auth
    with sql.connect(
        server_hostname=cfg.host,
        http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_WAREHOUSE_ID')}",
        credentials_provider=lambda: cfg.authenticate
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall_arrow().to_pandas()

st.set_page_config(layout="wide")

@st.cache_data(ttl=30)  # only re-query if it's been 30 seconds
def getData():
    # Query to select data from the table
    return sqlQuery("select * from test_project.country_code_to_currency.country_currency_table")

data = getData()

# App title
st.title("Country and currency data visualization")

st.write("Full data table:")
st.dataframe(data)

# Filter by country
country = st.text_input("Enter country name for filtering:", "")
if country:
    filtered_data = data[data["country"].str.contains(country, case=False, na=False)]
    st.write(f"Search results for '{country}':")
    st.dataframe(filtered_data)

# Sort data
sort_column = st.selectbox("Select column for sorting:", data.columns)
sort_order = st.radio("Sort order:", ["Ascending", "Descending"])
ascending = True if sort_order == "Ascending" else False

sorted_data = data.sort_values(by=sort_column, ascending=ascending)
st.write("Sorted data:")
st.dataframe(sorted_data)