# Fail2Back

This project is a Python FastAPI application that provides a RESTful API for Fail2Ban.
The project will allow you to view jails, bans, and associated configurations.
## Technologies Used

- Python
- FastAPI
- Pydantic

## Configuration

This application uses environment variables for configuration. You need to create a `.env` file in the root directory of the project and set the following variables:

```bash
SOCKET_PATH=/path/to/your/socket
DB_PATH=/path/to/your/database
```
Replace /path/to/your/socket and /path/to/your/database with the actual paths on your system.
- `SOCKET_PATH`: This is the path to the Fail2Ban socket file.
- `DB_PATH`: This is the path to the SQLite database file used by Fail2Ban.

Assurez-vous de remplacer `/path/to/your/socket` et `/path/to/your/database` par les chemins réels sur votre système.

## Installation

1. Clone this repository to your local machine.
2. Install the dependencies with pip:
```bash
pip install -r requirements.txt
```
3. run the application with uvicorn
```bash
uvicorn main:app --reload
```
