import argparse
import time
import threading
import os
import socket


def get_files():
    directory = os.path.dirname(os.path.realpath(__file__))
    ponds = []
    path = os.path.join(directory, "dataset")
    for file in os.listdir(path):
        if file.endswith(".csv"):
            ponds.append(os.path.join(path, file))
    return ponds


def load_data_from_csv(client_socket, pond_path, limit, offset):
    with open(pond_path, "r") as file:
        lines = file.readlines()
        lines = lines[1:]
        lines = lines[offset : offset + limit]

        for line in lines:
            print(line)
            client_socket.send(line.encode())


def process_pond_data(client_socket, pond_path, limit, sleep):
    offset = 0

    while True:
        load_data_from_csv(client_socket, pond_path, limit, offset)
        offset += limit
        time.sleep(sleep)


def process_client_data(client_socket, ponds, limit, sleep):
    for pond in ponds:
        pond_thread = threading.Thread(
            target=process_pond_data, args=(client_socket, pond, limit, sleep)
        )
        pond_thread.start()


def start_server(host, port, ponds, limit, sleep):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server listening on {host}:{port}")

    threads = []

    while True:
        client_socket, address = server_socket.accept()
        print(f"Client connected from {address[0]}:{address[1]}")
        client_thread = threading.Thread(
            target=process_client_data, args=(client_socket, ponds, limit, sleep)
        )
        threads.append(client_thread)
        client_thread.start()


if __name__ == "__main__":
    host = "localhost"
    port = 9999

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--limit", type=int, default=5, help="Limit the number of records to fetch"
    )
    parser.add_argument(
        "--sleep", type=int, default=10, help="Sleep time in seconds between each fetch"
    )

    args = parser.parse_args()

    limit = args.limit
    sleep = args.sleep

    ponds = get_files()

    start_server(host, port, ponds, limit, sleep)
