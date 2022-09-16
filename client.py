from threading import Thread

from socket import socket, AF_INET, SOCK_STREAM
from image_utils import open_image_as_byte_array, read_image_from_bytes, apply_blur

import constants as consts

from byte_utils import to_bytes
import network_utils as NetworkUtils

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
            #print(f"Data was received! {data}")

            instructions, data = NetworkUtils.separate_instructions_from_bytes(data)
            #print(f"Image data retrieved! {data}")

            if consts.SENDING_IMAGE in instructions:
                
                #print("Getting instruction data")
                num_of_bytes, image_id = NetworkUtils.get_instruction_data(instructions)
                #print(f"Num of bytes = {num_of_bytes} \t image_id = {image_id}")

                data = NetworkUtils.capture_image(self.socket,data,num_of_bytes)

                #print("reading and applying blur to image")
                image = read_image_from_bytes(data)
                image = apply_blur(image,5)
                print("processing complete! now sending the images back to the server")
                img_bytes  = open_image_as_byte_array(image)
                image_size = len(img_bytes) 

                msg = f"{consts.SENDING_IMAGE}|{image_id}|{image_size}"
                msg = NetworkUtils.to_image_instruction_msg(msg)

                print("Sending images back!")
                self.socket.sendall(msg + img_bytes)

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
    