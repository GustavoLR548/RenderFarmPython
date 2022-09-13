from threading import Thread

from socket import socket, AF_INET, SOCK_STREAM
from image_utils import open_image_as_byte_array, read_image_from_bytes, apply_blur

import constants as consts

from conversion_utils import to_bytes, string_from_bytes
from network_utils import capture_image

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
            
            data        = None
            instruction = string_from_bytes(self.conn.recv(consts.MSG_BUFFER_SIZE))
            
            if consts.SENDING_IMAGE in instruction:
                num_of_bytes = int(instruction.split("|")[1])
                data = capture_image(self.conn,data,num_of_bytes)

            image = read_image_from_bytes(data)
            image = apply_blur(image,5)

            img_bytes = open_image_as_byte_array(image)

            self.socket.sendall(img_bytes)

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
    