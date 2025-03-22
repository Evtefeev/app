import threading
import time
from turtleserver import TurtleClient
import turtleserver


def receive_updates():
    try:
        while 1:
            data = client.get_command()
            print(data)
    except ConnectionResetError:
        print("Disconnected from server.")
    finally:
        client.close()


client = TurtleClient(turtleserver.HOST, turtleserver.PORT)
client.connect()
threading.Thread(target=receive_updates, daemon=True).start()


client2 = TurtleClient(turtleserver.HOST, turtleserver.PORT)
client2.connect()
client2.send_command("HEllo")
time.sleep(1)
client2.close()
time.sleep(3)
