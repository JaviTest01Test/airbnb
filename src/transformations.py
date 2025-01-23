from datetime import datetime

def format_date(date_str):
    """Formats a date string (YYYY-MM-DD) into a readable format."""
    if not date_str or date_str.lower() == "null":  # Handle None, empty or "null" strings
        return "no review"
    
    try:
        # Parse the string into a datetime object
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        # Return the formatted date as "Day DD Month YYYY"
        return date_obj.strftime("%A %d %B %Y")
    except ValueError:
        return "invalid date"  # Return in case of an invalid date format
