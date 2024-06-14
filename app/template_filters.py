from app import app
from datetime import date

@app.template_filter("format_date")
def format_date(value):
    if value:
        format="%d. %m. %Y"
        return date.strftime(value, format)
    else:
        return ""