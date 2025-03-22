import threading
import turtle
import turtleserver
from turtleserver import TurtleClient
import keyboard


class Game:

    TURTLE_SPEED = 20
    TURTLE_ANGLE = 15
    commands = []

    def __init__(self):
        self.turtles: dict[str, turtle.Turtle] = {}
        self.screen = turtle.Screen()
        self.t = turtle.Turtle()
        self.client = TurtleClient(turtleserver.HOST, turtleserver.PORT)
        self.client.connect()

    # Movement functions

    def move_forward(self):
        self.t.forward(self.TURTLE_SPEED)
        self.client.send_command('move_forward')
        

    def move_backward(self):
        self.t.backward(self.TURTLE_SPEED)
        self.client.send_command('move_backward')
        

    def turn_left(self):
        self.t.left(self.TURTLE_ANGLE)
        self.client.send_command('turn_left')
        

    def turn_right(self):
        self.t.right(self.TURTLE_ANGLE)
        self.client.send_command('turn_right')
        

    def clear(self):
        self.t.clear()
        self.client.send_command('clear')
        

    def reset(self):
        self.t.reset()
        self.client.send_command('reset')
        

    def handle_server_command(self):
        while 1:
            command = self.client.get_command()
            player_id = command['player']
            command = command['command']
            if player_id != self.client.player_id:
                if command == "connected":
                    self.turtles[player_id] = turtle.Turtle()
                if command == "move_forward":
                    self.turtles[player_id].forward(self.TURTLE_SPEED)
                if command == "move_backward":
                    self.turtles[player_id].backward(self.TURTLE_SPEED)
                if command == "turn_left":
                    self.turtles[player_id].left(self.TURTLE_ANGLE)
                if command == "turn_right":
                    self.turtles[player_id].right(self.TURTLE_ANGLE)
                

        # self.screen.ontimer(self.handle_server_command)

    def start(self):
        # Initialize screen and turtle
        self.screen.title("Turtle Keyboard Control")
        self.t.speed(10)
        # Keyboard bindings
        # keyboard.on_press_key("w", self.move_forward)
        self.screen.onkey(self.move_forward, "w")
        self.screen.onkey(self.move_backward, "s")
        self.screen.onkey(self.turn_left, "a")
        self.screen.onkey(self.turn_right, "d")
        self.screen.onkey(self.clear, "c")
        self.screen.onkey(self.reset, "r")
        self.screen.listen()
        # self.handle_server_command()
        threading.Thread(target=self.handle_server_command,
                         daemon=True).start()

        self.screen.mainloop()

    def recieve_commands(self):
        while 1:
            self.commands.append()


g = Game()
g.start()
