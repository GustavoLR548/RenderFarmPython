from threading import Thread

from socket import socket, AF_INET, SOCK_STREAM
from image_utils import open_image_as_byte_array, read_image_from_bytes

import constants as consts

from conversion_utils import to_bytes

class Client(Thread):


    def __init__(self,name, address = consts.LOCAL_CONNECTION) -> None:
        
        Thread.__init__(self)
        self.running  = True
        self.username = name
        self.address = address
        self.socket = socket(AF_INET, SOCK_STREAM)


    def run(self) -> None: 

        self.socket.connect(self.address)
        self.socket.sendall(to_bytes(self.username))
        print("Connected to server!")

        while self.running:
            
            data = self.socket.recv(consts.MSG_BUFFER_SIZE)


    def send_image(self, text: str) -> None:
        
        image = open_image_as_byte_array(text)
        image_size = len(image)

        msg = f"{consts.SENDING_IMAGE}|{image_size}"

        self.socket.sendall(to_bytes(msg))
        self.socket.sendall(image)


def main() -> None:

    name = input("Enter your name: ")

    client = Client(name)
    client.start()

    running = True

    while running:
        text = input()

        if text in consts.RESERVED_MESSAGES: 
            client.socket.sendall(to_bytes(text))

            if text == consts.QUIT_PROGRAM:
                client.running = False
                running = False 

        else:
            client.send_image(text)

    client.join()

if __name__ == "__main__":

    main()
    