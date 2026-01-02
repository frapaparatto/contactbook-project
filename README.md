# Contact Book

A simple but powerful command-line (CLI) contact book application written in Python.

## Features

- **Add, Edit, and Delete Contacts**: Manage your contacts with ease.
- **Search Functionality**: Quickly find contacts by name.
- **Data Persistence**: Save your contact book to a JSON file and load it back.
- **Duplicate Prevention**: Avoid duplicate entries based on phone number or email.
- **Input Validation**: Ensures data integrity for phone numbers and emails.

## How to Use

1.  **Run the application**:
    ```bash
    python main.py
    ```

2.  **Start a new contact book or load an existing one**:
    - Type `new` to start with a fresh contact book.
    - Type `load` and provide the path to a `.json` file to load existing contacts.

3.  **Use the main commands to manage your contacts**:
    - `add`: Add a new contact.
    - `list`: Show all contacts.
    - `search`: Find a specific contact.
    - `edit`: Modify an existing contact.
    - `delete`: Remove a contact.
    - `save`: Save your changes to a JSON file.
    - `exit`: Exit the application.

## Project Structure

The project is organized as follows:

- `main.py`: The main entry point for the CLI application.
- `contactbook/`: The core Python package for the contact book.
  - `contacts.py`: Defines the `Contact` data model.
  - `addressbook.py`: Contains the `AddressBook` class for managing contacts.
  - `storage.py`: Handles saving and loading contacts (e.g., `JsonStorage`).
  - `contact_validators.py`: Provides validation for contact fields like phone and email.
  - `contact_exceptions.py`: Defines custom exceptions for the application.
  - `helpers.py`: Includes helper functions for the CLI.
- `tests/`: Contains unit tests for the project.

## Future Plans

-   **Refactoring**: The project will undergo a refactoring process to improve its design and maintainability.