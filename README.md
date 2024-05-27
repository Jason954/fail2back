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
Replace `/path/to/your/socket` and `/path/to/your/database` with the actual paths on your system.
- `SOCKET_PATH`: This is the path to the Fail2Ban socket folder.
- `DB_PATH`: This is the path to the SQLite database file used by Fail2Ban.

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

## Docker

This application can be run using Docker. To build the Docker image, navigate to the project root directory and run the following command:

```bash
docker build -t fail2back .
```

This will build a Docker image named fail2back using the Dockerfile in the current directory.  To run the application using the built Docker image, use the following command:

```bash
docker run -d --name fail2back -p 8000:8000 --env-file .env fail2back
```

## Docker Compose
This application can also be run using Docker Compose. This is particularly useful if you have multiple services that need to run in conjunction with this application.  To start the application with Docker Compose, navigate to the project root directory and run the following command:

```bash 
docker-compose up -d
```

This will start all services defined in the `docker-compose.yml` file. In this case, it will start the fail2back application in a Docker container, with the environment variables and port mappings defined in the docker-compose.yml file.  
Remember to replace both volumes in the docker-compose.yml file with the actual paths on your system:
- `/path/to/sock/fail2ban:/app/socket`: This is the path to the Fail2Ban socket folderg.
- `/path/to/sqlite3/fail2ban:/app/fail2ban.sqlite3`: This is the path to the SQLite database file used by Fail2Ban.