import traceback
import os
import pickle
import socket
import sqlite3

from dotenv import load_dotenv

END_COMMAND = "<F2B_END_COMMAND>"
load_dotenv()

socket_path = os.getenv("SOCKET_PATH")
db_path = os.getenv("DB_PATH")


def send_command(command):
    try:
        # instance socket
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(socket_path)
        # if space in command, split it
        # Format the command into pickle to be understood by the socket

        if " " in command:
            command = command.split(" ")
        else:
            command = [command]

        command = pickle.dumps(command)

        client.sendall(command)
        # send end_command to tell the socket that the command is over
        client.sendall(END_COMMAND.encode())

        response = client.recv(4096)
        # convert response pickle into json
        response = pickle.loads(response)
        # Afficher la réponse
        print("Réponse du socket Fail2Ban:", response)

        client.close()
        return response[1]
    except Exception as e:
        # get traceback
        print(traceback.format_exc())
        print("Erreur lors de la connexion au socket Fail2Ban:", e)


def query_db(query, args=()):
    print("Query:", query)
    print("Args:", args)
    print("DB Path:", db_path)
    conn = sqlite3.connect(db_path)

    # ## show all tables
    # cur = conn.cursor()
    # cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # # get all tables
    # tables = cur.fetchall()
    # print("Tables:", tables)
    # # show all data in the tables
    # for table in tables:
    #     cur.execute(f"SELECT * FROM {table[0]};")
    #     print(f"Data in {table[0]}:")
    #     print(cur.fetchall())
    #
    # cur.close()

    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    # iterate over the rows and convert them to a dictionary
    rv = [dict(row) for row in rv]
    cur.close()
    conn.close()
    return rv


