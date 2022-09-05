from socket import socket, AF_INET, SOCK_STREAM, gethostname
from threading import Thread
from image_utils import open_image_as_byte_array, read_image_from_bytes

HOST = "127.0.0.1"
PORT = 5000

class Client(Thread):

    def __init__(self,name) -> None:
        Thread.__init__(self)
        self.running  = True
        self.username = name
        self.socket   = socket(AF_INET, SOCK_STREAM)

    def run(self) -> None: 

        self.socket.connect((HOST, PORT))
        self.socket.sendall(bytes(self.username,"utf-8"))
        print("Connected to server!")

        while self.running:
            data = self.socket.recv(1024)

            image = read_image_from_bytes(data)
            if not data:
                self.running = False 

            else:
                print(image)

def main() -> None:

    name = input("Enter your name: ")

    client = Client(name)
    client.start()

    running = True

    while running:
        text = input()

        if text == "!quit":
            client.socket.sendall(bytes(f"!quit","utf-8"))
            client.running = False
            running = False 

        else:
            image = open_image_as_byte_array(text)
            print(len(image))

            client.socket.sendall(bytes(f"SENDING_IMAGE|{len(image)}","utf-8"))
            client.socket.sendall(image)

    client.join()

if __name__ == "__main__":
    main()
    