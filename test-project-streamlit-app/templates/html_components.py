# File: templates/html_components.py

def app_header(title="Country and Currency Database", 
               subtitle="A comprehensive management system for country and currency information"):
    """Render the application header"""
    return f"""
    <h1>
        <span style="color: #3498db;">🌎</span> 
        {title}
    </h1>
    
    <p style="text-align: center; margin-bottom: 30px;">
        {subtitle}
    </p>
    """

def section_header(icon, title):
    """Render a section header with icon"""
    return f"""
    <div class="section-header">
        <div class="section-header-icon">{icon}</div>
        <h2>{title}</h2>
    </div>
    """

def card_start():
    """Start a card container"""
    return '<div class="card">'

def card_end():
    """End a card container"""
    return '</div>'

def field_label(label, help_text=None):
    """Render a field label with optional help text"""
    html = f'<div class="field-label">{label}</div>'
    if help_text:
        html += f'<div class="field-help">{help_text}</div>'
    return html

def tooltip_field(label, tooltip_text):
    """Render a field with tooltip"""
    return f"""
    <div class="tooltip">{label}
        <span class="tooltiptext">{tooltip_text}</span>
    </div>
    """

def success_message(message):
    """Render a success message"""
    return f"""
    <div class="success-message">
        <strong>Success!</strong> {message}
    </div>
    """

def error_message(message):
    """Render an error message"""
    return f"""
    <div class="error-message">
        <strong>Error!</strong> {message}
    </div>
    """

def dataframe_container_start(border_color=None):
    """Start a dataframe container with optional border color"""
    style = f'border: 2px solid {border_color};' if border_color else ''
    return f'<div class="dataframe-container" style="{style}">'

def dataframe_container_end():
    """End a dataframe container"""
    return '</div>'

def footer(version="v1.0.0"):
    """Render the application footer"""
    return f"""
    <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #e0e0e0;">
        <p style="color: #7f8c8d; font-size: 14px;">
            Country Currency Database © {2023} | Built with Streamlit 
            <span style="color: #3498db;">{version}</span>
        </p>
    </div>
    """

def delete_warning():
    """Render a delete warning message"""
    return """
    <div style="color: #e74c3c; padding: 10px; background-color: #fadbd3; border-radius: 5px; margin-bottom: 20px;">
        <strong>Warning:</strong> Deleting an entry is permanent and cannot be undone.
    </div>
    """

def delete_confirmation():
    """Render a delete confirmation message"""
    return """
    <div style="background-color: #FF8C00; padding: 15px; border-radius: 5px; margin: 20px 0;">
        <strong>Confirmation Required</strong>
        <p>Please confirm that you want to permanently delete this entry.</p>
    </div>
    """

def disabled_button(label="Delete Entry"):
    """Render a disabled button"""
    return f"""
    <div style="text-align: center; padding: 10px;">
        <button disabled style="background-color: #cccccc; color: #666666; padding: 10px 20px; border: none; border-radius: 5px; cursor: not-allowed;">
            🗑️ {label}
        </button>
        <p style="color: #666666; font-size: 12px; margin-top: 5px;">
            Please confirm deletion by checking the box above
        </p>
    </div>
    """
