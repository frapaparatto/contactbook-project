import unittest
from contactbook.contact_validators import validate_name, validate_email, validate_phone_number
from contactbook.contact_exceptions import (
    InvalidEmailError,
    InvalidPhoneError,
    MissingRequiredFieldError,
)


class TestValidators(unittest.TestCase):
    def test_validate_name(self):
        first_name = "    Isaac"
        last_name = "  newton  "
        self.assertEqual("Isaac", validate_name(first_name))
        self.assertEqual("Newton", validate_name(last_name))

    def test_missing_name(self):
        with self.assertRaises(MissingRequiredFieldError):
            user_input = ""
            validate_name(user_input)

    def test_valid_email(self):
        self.assertEqual(None, validate_email(""))
        self.assertEqual("user@domain.com", validate_email("user@domain.com"))

    def test_invalid_email(self):
        invalid_emails = ["emailaddress", "user@", "@domain.com", "user@example", "user@.com"]
        for email in invalid_emails:
            with self.assertRaises(InvalidEmailError):
                validate_email(email)

    def test_valid_phone(self):
        self.assertEqual("+393445554466", validate_phone_number("344 555 4466"))
        self.assertEqual("+393445554466", validate_phone_number("+39 344 555 4466"))
        self.assertEqual("+393445554466", validate_phone_number("    +39 344 555 4466"))


    def test_invalid_phone(self):
        invalid_phone_numbers = ["+348 283 2938", "34423", "ab344 589483", "344 338 38394 030"]

        for invalid_number in invalid_phone_numbers:
                with self.assertRaises(InvalidPhoneError):
                    validate_phone_number(invalid_number)

if __name__ == "__main__":
    unittest.main()
