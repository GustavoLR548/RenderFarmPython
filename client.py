from socket import socket, AF_INET, SOCK_STREAM, gethostname
from threading import Thread

HOST = "127.0.0.1"
PORT = 5000

class Client(Thread):

    def __init__(self) -> None:
        Thread.__init__(self)
        self.running = True
        self.socket = socket(AF_INET, SOCK_STREAM)

    def run(self) -> None: 

        self.socket.connect((HOST, PORT))
        print("Connected to server!")

        while self.running:
            data = str(self.socket.recv(1024), "utf-8")
            if not data:
                self.running = False 

            else:
                print(data)

def main() -> None:

    name = input("Enter your name: ")

    client = Client()
    client.start()

    running = True

    while running:
        text = input()

        if text == "!quit":
            client.socket.sendall(bytes(f"!quit","utf-8"))
            client.running = False
            running = False 

        else:
            print(f"[{name}]: {text}")
            client.socket.sendall(bytes(f"[{name}]: {text}","utf-8"))

    client.join()

if __name__ == "__main__":
    main()
    