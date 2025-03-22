import random
import socket
import threading
import turtle
import json

from player import Player

# Setup screen
screen = turtle.Screen()
screen.setup(800, 600)
screen.tracer(0)

COLORS = ["red", "green", "blue", "yellow", "pink", "gray"]
SHAPES = ['arrow', 'turtle', 'circle', 'square', 'triangle', 'classic']

# Player turtles storage
players = {}

# Networking setup
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5555
clients = {}
next_player_id = 1
lock = threading.Lock()

# Function to handle each client


def send_positions():
    global players, clients
    # Send updated positions to all players
    data = {p: {
        "x": t.xcor(),
        "y": t.ycor(),
        "shape": t.shape,
        "color": t.color,
        "penup": t.penup
    }
        for p, t in players.items()}
    for c in clients.values():
        c.sendall(json.dumps(data).encode())

def handle_client(conn, player_id):
    global players, clients
    send_positions()
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            command = json.loads(data)
            if "x" in command and "y" in command:
                print("move")
                with lock:
                    players[player_id].goto(command["x"], command["y"])

            send_positions()

    except (ConnectionResetError, BrokenPipeError):
        print(f"Player {player_id} disconnected.")
    finally:
        conn.close()
        with lock:
            players[player_id].turtle.hideturtle()
            del clients[player_id]
            del players[player_id]

# Function to accept new players


def accept_players():
    global next_player_id
    while True:
        conn, addr = server.accept()
        player_id = f"player{next_player_id}"
        next_player_id += 1

        # Create a turtle for the player
        with lock:
            color = random.choice(COLORS)
            shape = random.choice(SHAPES)
            x = 0
            y = (next_player_id - 2) * 50 - 100  # Spread out players
            new_player = Player(
                0,
                0,
                shape,
                color,
                False,
                None
            )
            new_player.goto(x, y)

            players[player_id] = new_player
            clients[player_id] = conn
            data = {
                "color": color,
                "shape": shape,
                "x": x,
                "y": y,
                "penup": players[player_id].penup
            }
            print(data)
            conn.sendall(json.dumps(data).encode())

        # Start a new thread for the player
        threading.Thread(target=handle_client, args=(
            conn, player_id), daemon=True).start()
        print(f"{player_id} connected from {addr}")


# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)  # Allow up to 5 players
print("Server started, waiting for players...")

# Start accepting players in a separate thread
threading.Thread(target=accept_players, daemon=True).start()

# # Game loop - Continuously update screen
try:
    while True:
        try:
            for player in players.values():
                player.update()
            screen.update()
        except AttributeError as e:
            # print(e)
            pass
finally:
    server.close()


screen.exitonclick()
