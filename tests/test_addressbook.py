import unittest
from contactbook.storage import JsonStorage
from contactbook.contacts import Contact
from contactbook.addressbook import AddressBook
from contactbook.contact_exceptions import DuplicateContactError, ContactNotFoundError


# In this class I will test CRUD operations so I will assume that data format is correct (tested in test contact module)
class TestAddressBook(unittest.TestCase):
    def setUp(self):
        self.storage = JsonStorage()
        self.addressbook = AddressBook(self.storage)
        self.contact = Contact(
            first_name="Albert",
            last_name="Einstein",
            phone_number="+39 339 3842348",
            email="alberteinstein@test.com",
        )

    def test_add_contact(self):
        self.addressbook.add_contact(self.contact)

        self.assertIn(self.contact, self.addressbook.contacts.values())
        self.assertIn(self.contact.phone_number, self.addressbook._phone_idx)
        self.assertIn(self.contact.email, self.addressbook._email_idx)

    def test_delete_contact(self):
        self.addressbook.add_contact(self.contact)
        self.assertIn(self.contact, self.addressbook.contacts.values())

        self.addressbook.delete_contact(self.contact)
        self.assertNotIn(self.contact, self.addressbook.contacts.values())
        self.assertNotIn(self.contact.phone_number, self.addressbook._phone_idx)
        self.assertNotIn(self.contact.email, self.addressbook._email_idx)

    def test_update_contact(self):
        self.addressbook.add_contact(self.contact)
        self.assertIn(self.contact, self.addressbook.contacts.values())

        updated_contact = Contact(
            first_name="Albert",
            last_name="Einstein",
            phone_number="+39 339 3842348",
            email="alberteinstein@newtest.com",
        )

        self.addressbook.update_contact(self.contact, updated_contact)
        self.assertIn(updated_contact.email, self.addressbook._email_idx)
        self.assertNotIn(self.contact.email, self.addressbook._email_idx)

        # I wrote self.contact.email but it access to the old email
        # to retrieve the correct value I have to access to the new contact object that has as key the same id as the object before
        self.assertEqual(
            self.addressbook.contacts[self.contact.id].email,
            "alberteinstein@newtest.com",
        )

        # test if id stays consistent after update
        # check if associated to the old id there is the contact updated
        # key id (self.contact.id) -> updated_contact: Contact
        self.assertIs(self.addressbook.contacts[self.contact.id], updated_contact)

    def test_check_duplicate_phone(self):
        self.addressbook.add_contact(self.contact)
        self.assertIn(self.contact, self.addressbook.contacts.values())

        new_contact = Contact(
            first_name="Leonardo",
            last_name="Da Vinci",
            phone_number="+39 339 3842348",
            email="leonardo@test.com",
        )

        with self.assertRaises(DuplicateContactError):
            self.addressbook.add_contact(new_contact)

    def test_search_contact(self):
        self.addressbook.add_contact(self.contact)
        self.assertIn(self.contact, self.addressbook.contacts.values())

        self.assertEqual(self.addressbook.search_contact("Alb")[0].first_name, "Albert")
        self.assertEqual(
            self.addressbook.search_contact("einst")[0].first_name, "Albert"
        )

        with self.assertRaises(ContactNotFoundError):
            self.addressbook.search_contact("leonardo")



if __name__ == "__main__":
    unittest.main()
