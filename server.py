from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from typing import Dict

from client_thread import ClientThread

HOST = "127.0.0.1"
PORT = 5000

USERNAME_KEY = "username"
ADDRESS_KEY  = "address"

class Server(Thread):

    _clients: Dict = {}

    def __init__(self) -> None:
        Thread.__init__(self)
        self.running = True
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


    def run(self) -> None:

        self.socket.bind((HOST,PORT))
        self.socket.listen()

        while self.running:

            print("Waiting for a connection...")
            conn, addr = self.socket.accept()

            username = conn.recv(1024)
            print("New connection detected!\nAddress: ", addr, "Username: ", username)
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

if __name__ == "__main__":

    server = Server()
    server.start()

