import socket
import logging
from urllib.parse import unquote_plus
from mongo_handler import create_message

MAX_BYTES = 1024
SOCKET_HOST = socket.gethostbyname(socket.gethostname())
SOCKET_PORT = 5000    

#Save data to mongodb by parsing it
def save_to_db(data):
    try:
        data = unquote_plus(data)
        parse_data = dict([i.split("=") for i in data.split("&")])
        print(parse_data)
        create_message(parse_data)
    except Exception as e:
        logging.error(e)

#Get data from http server and forward it to socket server
def transfer_data(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SOCKET_HOST, SOCKET_PORT))
            s.sendall(data)
    except Exception as e:
        logging.error(f"Error while forwarding data to socket server: {e}")

#Function that is starting socket server and configuring it
def start_socket_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SOCKET_HOST, SOCKET_PORT))
    s.listen()
    print(f"Socket server started: socket://{SOCKET_HOST}:{SOCKET_PORT}")
    try:
        while True:
            conn, addr = s.accept()
            logging.info(f"Connected to {addr}")
            data = conn.recv(MAX_BYTES)
            logging.info(f"Received from {addr}: {data.decode()}")
            save_to_db(data.decode())
            conn.close()
    except Exception as e:
        logging.error(e)
    finally:
        logging.info("Server socket stopped")
        s.close()