from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from typing import Dict

from client_thread import ClientThread
from constants import MSG_BUFFER_SIZE, LOCAL_CONNECTION

from byte_utils import string_from_bytes

USERNAME_KEY = "username"
ADDRESS_KEY  = "address"

class Server(Thread):

    _clients: Dict = {}

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


    def process_message(self, msg, conn) -> None:
        
        self.__broadcast_message(msg,conn)


    def __add_new_connection(self,conn,addr,username) -> None:
        
        self._clients[conn] = {
            USERNAME_KEY : username,
            ADDRESS_KEY  : addr
        }

        new_client = ClientThread(conn,self)
        new_client.start()


    def __broadcast_message(self, msg, conn) -> None:

        print("broadcasting message...")
        client : socket
        for client in self._clients.keys():

            if client != conn: 

                try: 
                    client.sendall(msg)

                except: 
                    client.close()
                    self._clients.pop(client)

def main() -> None:

    server = Server()
    server.start()

    running = True

    while running:
        text = input()


if __name__ == "__main__":

    main()


