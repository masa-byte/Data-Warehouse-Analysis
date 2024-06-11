import socket
import threading
import json
from sseclient import SSEClient as EventSource


def handle_client(client_socket, url):

    relevant_info = {}

    for event in EventSource(url):
        if event.event == "message":
            try:
                event_info = json.loads(event.data)
            except ValueError:
                pass
            else:
                # discarding canary events
                if event_info["meta"]["domain"] == "canary":
                    continue

                try:
                    relevant_info["database"] = event_info["database"]
                except KeyError:
                    relevant_info["database"] = None

                try:
                    relevant_info["domain"] = event_info["meta"]["domain"]
                except KeyError:
                    relevant_info["domain"] = None

                try:
                    relevant_info["stream"] = event_info["meta"]["stream"]
                except KeyError:
                    relevant_info["stream"] = None

                try:
                    relevant_info["timestamp"] = event_info["meta"]["dt"]
                except KeyError:
                    relevant_info["timestamp"] = None

                try:
                    relevant_info["page_title"] = event_info["page_title"]
                except KeyError:
                    relevant_info["page_title"] = None

                try:
                    relevant_info["user_text"] = event_info["performer"]["user_text"]
                except KeyError:
                    relevant_info["user_text"] = None

                try:
                    relevant_info["user_is_bot"] = event_info["performer"][
                        "user_is_bot"
                    ]
                except KeyError:
                    relevant_info["user_is_bot"] = None

                try:
                    value = event_info["comment"]
                    relevant_info["comment"] = True
                except KeyError:
                    relevant_info["comment"] = False

                json_data = json.dumps(relevant_info)
                json_data += "\n"
                print("sending")
                print(json_data)
                try:
                    client_socket.send(json_data.encode())
                except:
                    print("error while sending to the client")
        else:
            print(event.event)

    client_socket.close()


def start_server(host, port, url):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Client connected from {address[0]}:{address[1]}")
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, url)
        )
        client_thread.start()


if __name__ == "__main__":
    host = "localhost"
    port = 9999
    url = "https://stream.wikimedia.org/v2/stream/mediawiki.page-create,page-delete"

    start_server(host, port, url)
