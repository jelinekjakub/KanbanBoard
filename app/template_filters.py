from datetime import date
from app import app

@app.template_filter("format_date")
def format_date(value):
    """Format a date as 'dd. mm. yyyy'."""
    if value:
        date_format = "%d. %m. %Y"
        return date.strftime(value, date_format)
    return ""
