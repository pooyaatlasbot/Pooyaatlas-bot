import re
from datetime import datetime


def normalize_digits(value: str) -> str:
    persian = "۰۱۲۳۴۵۶۷۸۹"
    arabic = "٠١٢٣٤٥٦٧٨٩"
    english = "0123456789"

    table = str.maketrans(
        persian + arabic,
        english + english,
    )
    return value.translate(table).strip()


def validate_phone(value: str) -> tuple[bool, str]:
    value = normalize_digits(value).replace(" ", "").replace("-", "")
    if not re.fullmatch(r"09\d{9}", value):
        return False, value
    return True, value


def validate_national_code(value: str) -> tuple[bool, str]:
    code = normalize_digits(value).replace(" ", "").replace("-", "")

    if not re.fullmatch(r"\d{10}", code):
        return False, code

    if len(set(code)) == 1:
        return False, code

    checksum = sum(int(code[i]) * (10 - i) for i in range(9))
    remainder = checksum % 11
    control = int(code[9])

    valid = (
        control == remainder
        if remainder < 2
        else control == 11 - remainder
    )
    return valid, code


def validate_birth_date(value: str) -> tuple[bool, str]:
    value = normalize_digits(value).strip()
    if not re.fullmatch(r"1[234]\d{2}/(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])", value):
        return False, value

    year, month, day = map(int, value.split("/"))
    if year < 1200 or year > 1499:
        return False, value

    # کنترل ساده روزهای ماه شمسی
    if month <= 6 and day > 31:
        return False, value
    if month >= 7 and day > 30:
        return False, value

    return True, value


def clean_name(value: str) -> tuple[bool, str]:
    value = " ".join(value.strip().split())
    if len(value) < 3 or len(value) > 80:
        return False, value
    if any(char.isdigit() for char in value):
        return False, value
    return True, value
