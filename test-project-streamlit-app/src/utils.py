# File: src/utils.py

def load_css(css_file_path):
    """Load CSS from a file and inject it into the Streamlit app"""
    with open(css_file_path, 'r') as f:
        return f'<style>{f.read()}</style>'
