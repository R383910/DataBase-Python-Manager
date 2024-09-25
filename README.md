# SQLite Database Manager

This program is a SQLite database manager that allows users to manage their databases interactively. It offers features to retrieve, add, delete information, create and delete tables, configure settings, and more.

## Features

- **Retrieve Information** : Allows retrieving information from a specific table based on ID or name.
- **Add Information** : Allows adding information to a specific table.
- **Delete Information** : Allows deleting information from a specific table.
- **Create New Table** : Allows creating a new table with columns specified by the user.
- **Delete Table** : Allows deleting an existing table.
- **Configure Settings** : Allows configuring various application settings, such as recording the results of retrieval commands and log files.
- **Open Logs Folder** : Opens the logs folder in the file explorer.
- **Clear Console** : Clears the console for better readability.

## Prerequisites

- Python 3.x
- SQLite3 (included with Python)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/R383910/DataBase-Python-Manager.git
    cd your-repository
    ```

2. Ensure you have Python 3.x installed on your machine.

## Usage

1. Run the main script:

    ```bash
    python BDD.py
    ```

2. Follow the on-screen instructions to navigate the menu and use the different features.

## Project Structure

- `main.py` : The main script containing the application menu and functions to manage the database.
- `logs/` : Folder containing log files.
- `config.json` : Configuration file to store application settings.

## Configuration

On the first run, the program will ask you to specify the database path. You can also configure other settings by selecting the "Configure Settings" option in the main menu.

---

Thank you for using this SQLite Database Manager!
