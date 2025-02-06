from dataclasses import dataclass
import socket
import turtle
import threading
import json

from player import Player

# Setup screen
screen = turtle.Screen()
screen.setup(800, 600)
screen.tracer(0)

# Player turtle
player = turtle.Turtle()
player.shape("turtle")
player.penup()


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


def receive_updates():
    global opponents

    try:
        while True:
            data = client.recv(1024).decode()
            if not data:
                break

            positions = json.loads(data)

            for key, pos in positions.items():
                if key not in opponents:
                    # Create a new turtle for new players

                    # new_turtle = turtle.Turtle()
                    # new_turtle.shape("turtle")
                    # new_turtle.color("gray")
                    # new_turtle.penup()

                    new_player = Player(
                        pos['x'],
                        pos['y'],
                        pos['shape'],
                        pos['color'],
                        True,
                        pos['penup']
                    )
                    opponents[key] = new_player

                # Update opponent positions
                opponents[key].goto(pos["x"], pos["y"])

    except ConnectionResetError:
        print("Disconnected from server.")
    finally:
        client.close()


# Start receiving updates in a separate thread
threading.Thread(target=receive_updates, daemon=True).start()
screen.listen()

# Game loop
while True:
    for opponent in opponents.values():
        opponent.update()

    screen.update()
