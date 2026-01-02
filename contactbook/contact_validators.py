
import re
from .contact_exceptions import (
    InvalidEmailError,
    InvalidPhoneError,
    MissingRequiredFieldError,
)

EMAIL_PATTERN = r"^[\w\.]+@([\w]+\.)+[\w]{2,3}$"
PHONE_NUMBER_PATTERN = r"^(?:\+39\s?)?3\d{2}\s?\d{3}\s?\d{4}$"
PREFIX = "+39"

# TODO: In the MissingRequiredFieldError I could add a field_name parameter in order to have something to print out and be specific, I have to understand how I should add it 


def validate_name(name: str) -> str:
    if not name:
        raise MissingRequiredFieldError("Missing required field")
    return name.strip().title()


def validate_phone_number(phone_number: str) -> str:
    if not phone_number:
        raise MissingRequiredFieldError("Phone is require")

    if not re.match(PHONE_NUMBER_PATTERN, phone_number.strip()):
        raise InvalidPhoneError(
            "Invalid phone: phone must contain only digits with optional leading + (e.g. +393491234567)"
        )

    if not phone_number.strip().startswith(PREFIX):
        phone_number = PREFIX + phone_number

    phone_number_parts = phone_number.split()

    return "".join(phone_number_parts)


def validate_email(email: str | None) -> str | None:
    if not email:
        return

    if not re.match(EMAIL_PATTERN, email):
        raise InvalidEmailError("Invalid email (expected email like name@example.com)")

    return email
