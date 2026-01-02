from typing import Dict, List, Optional
from contacts import Contact
from contact_exceptions import DuplicateContactError, ContactNotFoundError
from storage import Storage

class AddressBook:
    def __init__(self, storage: Storage):
        self.contacts: Dict[str, Contact] = {}
        # Dictionaries created for duplicates check in order to search faster
        self._phone_idx: Dict[str, str] = {}  # maps phone -> id
        self._email_idx: Dict[str, str] = {}  # maps email -> id
        self.storage: Storage = storage

        # Flag used to keep track of the changes
        self.is_changed = False

    def add_contact(self, contact: Contact) -> None:
        self._check_duplicate_contact(contact)

        self.contacts[contact.id] = contact
        self._phone_idx[contact.phone_number] = contact.id

        if contact.email:
            self._email_idx[contact.email] = contact.id

        self.is_changed = True

    def delete_contact(self, contact: Contact) -> None:
        deleted_contact = self.contacts.pop(contact.id, None)

        if deleted_contact is None:
            raise ContactNotFoundError("Contact not found")


        # Remove it also from second indexes dictionaries
        self._phone_idx.pop(contact.phone_number, None)

        if contact.email:
            self._email_idx.pop(contact.email, None)

        self.is_changed = True

    def update_contact(
        self, contact_to_update: Contact, updated_contact: Contact
    ) -> None:
        if contact_to_update.id not in self.contacts:
            raise ContactNotFoundError("Contact not found.")

        self._check_duplicate_contact(updated_contact, exclude_id=contact_to_update.id)
        self._replace_contact(contact_to_update, updated_contact)
        self.is_changed = True

    def list_contacts(self) -> List[Contact]:
        return [
            contact
            for contact in sorted(
                # sort first for last name, then for first name and then for id
                self.contacts.values(),
                key=lambda contact: (contact.last_name, contact.first_name, contact.id),
            )
        ]

    def search_contact(self, query: str) -> List[Contact]:
        normalized_query = query.strip().lower()

        contacts_found = []
        # The user can search contact by first or last name typing them entirely or typing  sub-string
        for contact in self.contacts.values():
            if normalized_query in contact.get_full_name().lower():
                contacts_found.append(contact)

        if not contacts_found:
            raise ContactNotFoundError("No contacts found")

        return sorted(
            contacts_found,
            key=lambda contact: (contact.last_name, contact.first_name, contact.id),
        )

    # Helper functions for other methods in this class
    def _check_duplicate_contact(
        self, contact: Contact, exclude_id: Optional[str] = None
    ) -> None:
        id = self._phone_idx.get(contact.phone_number)

        if id is not None and id != exclude_id:
            raise DuplicateContactError("Phone number already used by another contact")

        if contact.email:
            id = self._email_idx.get(contact.email)

            if id is not None and id != exclude_id:
                raise DuplicateContactError("Email already used by another contact")

    def _replace_contact(self, old_contact: Contact, new_contact: Contact) -> Contact:
        self.contacts[old_contact.id] = new_contact

        if new_contact.phone_number != old_contact.phone_number:
            self._phone_idx.pop(old_contact.phone_number, None)
            self._phone_idx[new_contact.phone_number] = new_contact.id

        if (old_contact.email or None) != (new_contact.email or None):
            if old_contact.email:
                self._email_idx.pop(old_contact.email, None)

            if new_contact.email:
                self._email_idx[new_contact.email] = new_contact.id

        return new_contact

    def save(self, path: str):
        # serialize data from json to a Dict[str, dict]
        data = {contact.id: contact.to_dict() for contact in self.contacts.values()}

        self.storage.save(data, path)
        # if it fails, the storage will raise a StorageError
        self.is_changed = False

    def load(self, path: str):
        contacts_loaded = self.storage.load(path)

        self.contacts.clear()
        self._phone_idx.clear()
        self._email_idx.clear()

        self.contacts = {
            id: Contact.from_dict(contact) for id, contact in contacts_loaded.items()
        }

        self._phone_idx = {
            contact.phone_number: contact.id for contact in self.contacts.values()
        }

        self._email_idx = {
            contact.email: contact.id
            for contact in self.contacts.values()
            if contact.email
        }

        self.is_changed = False

    def __len__(self):
        return len(self.contacts)
