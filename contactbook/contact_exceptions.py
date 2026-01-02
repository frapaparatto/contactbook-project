# TODO: this module should be checked again to understand if I have to write some code inside errror functions

# Notes about production code
# - in production don't show contact_exceptions.Error but handle in a better way

class ContactError(Exception):
    """Base class for ContactEase domain errors."""

class ContactValidationError(ContactError):
    """Input failed validation (names/phone/email)."""

class InvalidPhoneError(ContactValidationError):
    """Phone format invalid."""

class InvalidEmailError(ContactValidationError):
    """Email format invalid."""

class MissingRequiredFieldError(ContactValidationError):
    """A required field is missing or empty."""

class DuplicateContactError(ContactError):
    """Phone or email already used by another contact."""

class ContactNotFoundError(ContactError):
    """Contact was not found."""

class StorageError(Exception):
    """Generic persistence failure."""

class FileCorruptionError(StorageError):
    """Loaded file is malformed or schema is invalid."""
