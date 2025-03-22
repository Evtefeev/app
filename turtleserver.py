import json
import socket
import threading


HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5556


class TurtleServer:
    next_player_id = 0
    clients = []

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def sendall(self, data: dict):
        for client in self.clients:
            try:
                client.sendall(json.dumps(data).encode())
            except Exception as e:
                print(e)

    def start(self):
        # Start server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)  # Allow up to 5 players
        print("Server started, waiting for players...")
        while True:
            conn, addr = self.server.accept()
            player_id = f"player{self.next_player_id}"
            self.next_player_id += 1
            self.clients.append(conn)
            threading.Thread(target=self.handle_client, args=(
                conn, player_id), daemon=True).start()
            print(f"{player_id} connected from {addr}")
            self.sendall({'player': player_id, 'command': 'connected'})

    def handle_client(self, conn: socket.socket, player_id):
        try:
            while True:
                command = conn.recv(1024).decode()
                if not command:
                    break
                data = {
                    'player': player_id,
                    'command': command
                }
                print(data)
                self.sendall(data)

        except (ConnectionResetError, BrokenPipeError):
            print(f"Player {player_id} disconnected.")
        finally:
            self.clients.remove(conn)
            conn.close()
            self.sendall({'player': player_id, 'command': 'disconnected'})


class TurtleClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.player_id = self.get_command()['player']

    def send_command(self, command):
        self.client.sendall(command.encode())

    def get_command(self):
        return json.loads(self.client.recv(1024).decode())

    def close(self):
        self.client.close()
