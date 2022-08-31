from socket import socket, AF_INET, SOCK_STREAM, gethostname
from threading import Thread
from typing import List

from client_thread import ClientThread

HOST = "127.0.0.1"
PORT = 5000

class Server(Thread):

    _clients: List = []

    def __init__(self) -> None:
        Thread.__init__(self)
        self.running = True
        self.socket = socket(AF_INET, SOCK_STREAM)


    def run(self) -> None:

        self.socket.bind((HOST,PORT))
        self.socket.listen()

        while self.running:

            print("Waiting for a connection...")
            conn, addr = self.socket.accept()

            print("New connection detected: ", addr)
            self._clients.append(conn)
            new_client = ClientThread(conn,self)
            new_client.start()

    def process_message(self, msg, conn) -> None:
        
        if "!" in msg:

            if "quit" in msg:
                self.__broadcast_message("Client disconnected!",conn)
        else: 
            self.__broadcast_message(msg,conn)

    def __broadcast_message(self, msg, conn) -> None:

        print("broadcasting message...")
        for client in self._clients:

            if client != conn: 

                try: 
                    client.sendall(bytes(msg,"utf-8"))

                except: 
                    client.close()
                    self._clients.remove(client)

if __name__ == "__main__":

    server = Server()
    server.start()

