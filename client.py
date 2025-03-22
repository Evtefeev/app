from dataclasses import dataclass
import socket
import turtle
import threading
import json

from player import Player
from threaded_turtle.thread_serializer import ThreadSerializer
from threaded_turtle.turtle_thread import TurtleThread

# Setup screen
screen = turtle.Screen()
screen.setup(800, 600)
screen.tracer(0)

# Player turtle
player = turtle.Turtle()
player.shape("turtle")
player.penup()
mutex = threading.Lock()


# Opponent turtles
opponents = {}

# Networking setup
SERVER_IP = "127.0.0.1"  # Change this to match the server's IP
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))
data = json.loads(client.recv(1024).decode())
player.shape(data['shape'])
player.color(data['color'])
player.goto(data['x'], data['y'])
if data['penup']:
    player.penup()
else:
    player.pendown()

# Function to send player movement


def send_movement():
    data = json.dumps({"x": player.xcor(), "y": player.ycor()})
    client.sendall(data.encode())

# Move functions


def move_up():
    player.sety(player.ycor() + 10)
    send_movement()


def move_down():
    player.sety(player.ycor() - 10)
    send_movement()


def move_left():
    player.setx(player.xcor() - 10)
    send_movement()


def move_right():
    player.setx(player.xcor() + 10)
    send_movement()


# Key bindings

screen.onkeypress(move_up, "w")
screen.onkeypress(move_down, "s")
screen.onkeypress(move_left, "a")
screen.onkeypress(move_right, "d")

# Function to receive updates from the server
# Initialize one TurtleThreadSerializer
ctrl = ThreadSerializer()


def receive_updates(turtle):
        global opponents

        try:
            while True:
                data = client.recv(1024).decode()
                if not data:
                    break

                json_data = json.loads(data)

                for key, el in json_data.items():
                    if key not in opponents:
                        # Create a new turtle for new players

                        # new_turtle = turtle.Turtle()
                        # new_turtle.shape("turtle")
                        # new_turtle.color("gray")
                        # new_turtle.penup()

                        new_player = Player(
                            el['x'],
                            el['y'],
                            el['shape'],
                            el['color'],
                            True,
                            True if el['penup'] == "True" else False
                        )
                        with mutex:
                            opponents[key] = new_player

                    # Update opponent positions
                    opponents[key].goto(el["x"], el["y"])

        except ConnectionResetError:
            print("Disconnected from server.")
        finally:
            client.close()


# Start receiving updates in a separate thread
# threading.Thread(target=receive_updates, daemon=True).start()
TurtleThread(ctrl, target=receive_updates).start()
screen.listen()

# Game loop
while True:
    with mutex:
        for opponent in opponents.values():
            opponent.update()

    screen.update()
