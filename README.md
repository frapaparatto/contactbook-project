# Contact Book

A command-line contact book written in Python, with no dependencies outside the standard library.

## Features

- Add, edit, and delete contacts
- Search contacts by name
- Save and load a contact book as a JSON file
- Duplicate detection by phone number or email
- Validation of phone numbers and email addresses

## Usage

Run the application:

```bash
python main.py
```

You'll first be asked to either start fresh or load existing data:

- `new`: start with an empty contact book
- `load`: load contacts from a `.json` file (you'll be prompted for the path)

Once inside, the following commands are available:

- `add`: add a new contact
- `list`: list all contacts
- `search`: find a contact
- `edit`: edit a contact
- `delete`: delete a contact
- `save`: save changes to a JSON file
- `clear`: clear the screen
- `exit`: quit the application

## Roadmap

The project is due for a refactor to improve its internal design and maintainability.
