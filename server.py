from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from typing import Dict

from client_thread import ClientThread
from constants import MSG_BUFFER_SIZE, LOCAL_CONNECTION, SENDING_IMAGE

from conversion_utils import string_from_bytes, to_bytes
import image_utils as ImageUtils

USERNAME_KEY = "username"
ADDRESS_KEY  = "address"
BLUR_RADIUS = 5

class Server(Thread):

    _clients: Dict = {}
    _num_clients: int = 0
    _final_slabs = None

    def __init__(self,address=LOCAL_CONNECTION) -> None:

        Thread.__init__(self)
        
        self.running = True
        self.address = address
        self.socket = socket(AF_INET, SOCK_STREAM)
        
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


    def run(self) -> None:

        self.socket.bind(self.address)
        self.socket.listen()

        while self.running:

            print("Waiting for a connection...")
            conn, addr = self.socket.accept()

            username = string_from_bytes(conn.recv(MSG_BUFFER_SIZE))
            print(f"New connection detected!\nAddress: {addr} \nUsername: {username}")

            self.__add_new_connection(conn,addr,username)


    def process_client_message(self, msg, conn) -> None:
        
        self.__broadcast_message(msg,conn)


    def __add_new_connection(self,conn,addr,username) -> None:
        
        self._clients[conn] = {
            USERNAME_KEY : username,
            ADDRESS_KEY  : addr
        }
        self._num_clients += 1

        new_client = ClientThread(conn,self)
        new_client.start()


    def __broadcast_message(self, msg, conn) -> None:

        print("broadcasting message...")
        client: socket
        for client in self._clients.keys():

            if client != conn: 

                try: 
                    client.sendall(msg)

                except: 
                    client.close()
                    self._clients.pop(client)


    def receive_image_from_clients(self,img) -> None:
        pass #TODO: logic to get the images from clients and send to final step

    
    def process_final_image(self) -> None:
        reconstructed_img = ImageUtils.merge_img_slabs(self._final_slabs, 
                                                        self._num_clients, 
                                                        BLUR_RADIUS)

        reconstructed_img.save("conseguimos_rada.jpg")

    def send_image_to_clients_process(self,img_path: str) -> None:

        img = ImageUtils.open_image_as_numpy_array(img_path)
        img_slabs = ImageUtils.split_img(img, self._num_clients, BLUR_RADIUS)

        client: socket 
        i = 0
        for client in self._clients.keys():

            img_bytes = ImageUtils.open_image_as_byte_array(img_slabs[i])
            image_size = len(img_bytes)

            msg = f"{SENDING_IMAGE}|{image_size}"

            try:
                client.sendall(to_bytes(msg))
                client.sendall(img_bytes)
            except: 
                client.close()
                self._clients.pop(client)

            i += 1

def main() -> None:

    server = Server()
    server.start()

    running = True

    while running:
        text = input()

        server.send_image_to_clients_process(text)


if __name__ == "__main__":

    main()


