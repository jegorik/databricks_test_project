# Country Currency Database

A professional Streamlit application for managing country and currency data with full CRUD functionality.

## 📌 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **View & Filter Data**: Browse, search, and sort country and currency information
- **Create Records**: Add new country/currency entries with validation
- **Update Records**: Edit existing country information
- **Delete Records**: Remove countries with confirmation
- **Modern UI**: Sleek dark-themed interface with responsive design
- **Professional Structure**: Modular codebase with separation of concerns

## 📁 Project Structure

```
test-project-streamlite-app/
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

## 🚀 Installation

1. Clone the repository:
```bash
git https://github.com/jegorik/databricks_test_project.git
cd databricks_test_project
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

Set the required environment variables:

```bash
# Required for database connection
export DATABRICKS_WAREHOUSE_ID=your_warehouse_id
export DATABRICKS_HOST=your_host.cloud.databricks.com
export DATABRICKS_TOKEN=your_access_token

# Optional - to use custom config files
export DATABRICKS_CONFIG_FILE=/path/to/config
```

## 🏃‍♂️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at http://localhost:8501

## 💻 Technology Stack

- **Frontend**: Streamlit, HTML, CSS
- **Backend**: Python
- **Database**: Databricks SQL
- **Authentication**: Databricks SDK
- **Styling**: Custom CSS with dark theme

## 🔧 Architecture

The application follows a modular architecture with clear separation of concerns:

1. **Database Layer**: 
   - `DatabaseManager` class encapsulates all database operations
   - Handles connections, queries, and data manipulation
   - Provides a clean API for CRUD operations

2. **UI Layer**:
   - `CountryCurrencyUI` class manages the Streamlit interface
   - Renders different tabs and components
   - Handles user input and validation

3. **Templates**:
   - HTML components are stored as functions in `html_components.py`
   - Each function returns specific HTML markup

4. **Styling**:
   - CSS is stored in an external file for easy customization
   - Dark theme optimized for readability

5. **Utils**:
   - Helper functions for common operations
   - CSS loading utility

## 🎨 Customization

### Changing the Theme

The application comes with a dark theme by default. To switch to a light theme or create your own:

1. Modify the `assets/styles.css` file
2. Adjust color variables and component styles

### Adding New Features

To extend the application:

1. **New Database Operations**:
   - Add methods to `DatabaseManager` in `src/database.py`

2. **New UI Components**:
   - Add rendering methods to `CountryCurrencyUI` in `src/ui.py`
   - Create new tabs or sections as needed

3. **New HTML Templates**:
   - Add functions to `templates/html_components.py`