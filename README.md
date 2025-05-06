# Step-by-Step Manual for Test Project

1. **Create a new notebook** in the workspace area named "Test_project_notebook".

2. **Create a new catalog** named "test_project" using SQL inside the "Test_project_notebook":
    ```sql
    CREATE CATALOG my_new_catalog;
    ```

3. **Drop the default schema** in the newly created catalog:
    ```sql
    DROP SCHEMA test_project.default CASCADE;
    ```

4. **Create "country_code_to_currency" schema** and a volume "csv_data" in the "test_project" catalog:
    ```sql
    CREATE SCHEMA IF NOT EXISTS test_project.country_code_to_currency;
    CREATE VOLUME IF NOT EXISTS test_project.csv_data;
    ```

5. **Upload the file** "country_code_to_currency_code.csv" to the "csv_data" volume.

6. **Create a new table** "country_currency_table" from `country_code_to_currency_code.csv`:
    ```sql
    CREATE OR REPLACE TABLE test_project.country_code_to_currency.country_currency_table (
        country_code STRING,
        country_number INT,
        country STRING,
        currency_name STRING,
        currency_code STRING,
        currency_number INT
    )
    USING DELTA;

    COPY INTO test_project.country_code_to_currency.country_currency_table
    FROM '/Volumes/test_project/country_code_to_currency/csv_data/country_code_to_currency_code.csv'
    FILEFORMAT = CSV
    FORMAT_OPTIONS (
        'header' = 'true',
        'inferSchema' = 'true',
        'delimiter' = ','
    );
    ```

7. **Create a new Streamlit app** "test-project-streamlit-app" using Compute > Create new app (you can choose an existing template or create from scratch).

8. After the application is created, **find `app.py`** in `Workspace/Users/<your account data>/databricks_apps/test-project-streamlit-app`.

9. **Refactor `app.py`** according to your needs.