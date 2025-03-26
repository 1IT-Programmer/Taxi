from datetime import datetime

def validate_phone(phone: str) -> bool:
    return len(phone) >= 10 and phone.replace("+", "").isdigit()

def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def validate_time(time_str: str) -> bool:
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def validate_seats(seats_str: str) -> bool:
    try:
        seats = int(seats_str)
        return 1 <= seats <= 10
    except ValueError:
        return False

def sanitize_input(text: str) -> str:
    return text.replace("<", "&lt;").replace(">", "&gt;").strip()