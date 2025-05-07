# Country Currency Database - Setup Guide

A comprehensive guide to set up the database and Streamlit application for the Country Currency Database project.

## 📌 Table of Contents

- [Database Setup](#database-setup)
- [Application Setup](#application-setup)
- [Environment Configuration](#environment-configuration)
- [Project Structure](#project-structure)
- [Running the Application](#running-the-application)

## 🗄️ Database Setup

### Creating Database Resources

1. **Create a Notebook**
   - Log into your Databricks workspace
   - Navigate to the workspace area
   - Create a new notebook named `Test_project_notebook`

2. **Set Up Database Structure**
   - Run the following SQL commands in order:

```sql
-- Create a new catalog for the project
CREATE CATALOG test_project;

-- Remove the default schema
DROP SCHEMA test_project.default CASCADE;

-- Create a dedicated schema for country-currency data
CREATE SCHEMA IF NOT EXISTS test_project.country_code_to_currency;

-- Create a volume to store CSV data
CREATE VOLUME IF NOT EXISTS test_project.csv_data;
```

### Loading Data

1. **Upload Source Data**
   - Upload the file `country_code_to_currency_code.csv` to the `test_project.csv_data` volume

2. **Create and Populate Table**
   - Run the following SQL to create and populate the table:

```sql
-- Define table structure
CREATE OR REPLACE TABLE test_project.country_code_to_currency.country_currency_table (
    country_code STRING,
    country_number INT,
    country STRING,
    currency_name STRING,
    currency_code STRING,
    currency_number INT
)
USING DELTA;

-- Load data from CSV
COPY INTO test_project.country_code_to_currency.country_currency_table
FROM '/Volumes/test_project/country_code_to_currency/csv_data/country_code_to_currency_code.csv'
FILEFORMAT = CSV
FORMAT_OPTIONS (
    'header' = 'true',
    'inferSchema' = 'true',
    'delimiter' = ','
);
```

## 🚀 Application Setup

### Creating the Streamlit App

1. **Create a New Application**
   - Navigate to `Compute > Create new app` in your Databricks workspace
   - Name the app `test-project-streamlit-app`
   - You can choose an existing template or start from scratch

2. **Locate the App Files**
   - After creation, find the application files at:
   - `Workspace/Users/<your account data>/databricks_apps/test-project-streamlit-app`

3. **Deploy the Code Structure**
   - Replace the default `app.py` with our modular application structure
   - Create the full directory structure as shown in the [Project Structure](#project-structure) section

## ⚙️ Environment Configuration

### Configuration Files

1. **Create `.env` File**
   - Create a new file named `.env` in the root of the app directory
   - Add the following configuration:

```
DATABRICKS_WAREHOUSE_ID=<contact the project owner for the value>
```

2. **App Configuration**
   - Ensure the application's `app.yaml` references the correct environment variables

## 📁 Project Structure

Deploy the following project structure in your Databricks app workspace:

```
test-project-streamlit-app/
│
├── app.py                  # Main entry point
├── requirements.txt        # Project dependencies
│
├── assets/                 # Static assets
│   └── styles.css          # CSS styles (dark theme)
│
├── src/                    # Source code
│   ├── __init__.py         # Makes src a proper package
│   ├── database.py         # Database manager
│   ├── ui.py               # UI components
│   └── utils.py            # Helper functions
│
└── templates/              # HTML templates
    └── html_components.py  # HTML templates as Python strings
```

## 🏃‍♂️ Running the Application

1. **Deploy the Application**
   - Make sure all files are properly uploaded to your Databricks workspace
   - Verify environment variables are correctly set

2. **Start the App**
   - In Databricks, navigate to your app
   - Click "Start" to run the application
   - The app will be available at the URL provided by Databricks

3. **Verify Functionality**
   - Test the View, Add, Edit, and Delete functionality
   - Ensure database connections are working properly
   - Verify the dark theme is displaying correctly