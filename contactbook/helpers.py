from .addressbook import AddressBook
from .contacts import Contact
from .contact_validators import validate_name, validate_email, validate_phone_number
from .contact_exceptions import (
    ContactNotFoundError,
    InvalidEmailError,
    InvalidPhoneError,
    MissingRequiredFieldError,
)


def ask_name(prompt: str) -> str:
    while True:
        try:
            name = validate_name(input(prompt))
        except MissingRequiredFieldError as e:
            print(e)
            continue

        return name


def ask_phone_number() -> str:
    while True:
        try:
            phone_number = validate_phone_number(input("Phone number (required): "))

        except MissingRequiredFieldError as e:
            print(e)
            continue

        except InvalidPhoneError as e:
            print(e)
            continue

        return phone_number


def ask_email() -> str | None:
    while True:
        try:
            email = validate_email(input("Email (optional): "))

        except InvalidEmailError as e:
            print(e)
            continue

        return email


def prompt_contact_fields() -> dict:
    while True:
        first_name = ask_name("First name (required): ")
        last_name = ask_name("Last name (required): ")
        phone_number = ask_phone_number()
        email = ask_email()

        return {
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "email": email or None,
        }


def render_contacts(contacts):
    if not contacts:
        print("No contacts in address book.")
        return
    print(f"{'Last':15}  {'First':15}  {'Phone':17}  {'Email'}")
    print("-" * 90)
    for contact in contacts:
        # display phone number in international format so it's more readable
        render_phone_number = f"{contact.phone_number[:3]} {contact.phone_number[3:6]} {contact.phone_number[6:9]} {contact.phone_number[9:]}"
        print(
            f"{(contact.last_name):15}  {(contact.first_name):15}  {render_phone_number:17}  {contact.email or ''}"
        )


def get_contact(query: str, addressbook: AddressBook) -> Contact | None:
    while True:
        try:
            contact_found = addressbook.search_contact(query)
            if len(contact_found) == 1:
                return contact_found[0]

            elif len(contact_found) > 1:
                print("\nMultiple contacts found:")

                render_contacts(contact_found)
                print("\nThe query is too generic, refine it:")
                query = input("New search: ")

                if not query:
                    continue
                return addressbook.search_contact(query)[0]


        except ContactNotFoundError:
            print("No contacts found.")
            choice = input("Try again? (y/N): ").strip().lower()
            if choice != 'y':
                return None  # Allow exit

            query = input("\nSearch contact: ")



