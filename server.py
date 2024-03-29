from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread, enumerate
from typing import Dict

from client_thread import ClientThread
from constants import MSG_BUFFER_SIZE, LOCAL_CONNECTION, SENDING_IMAGE

from byte_utils import string_from_bytes
import image_utils as ImageUtils
from network_utils import to_image_instruction_msg

USERNAME_KEY = "username"
ADDRESS_KEY  = "address"
BLUR_RADIUS = 20

"""
Thread para o cliente
"""
class Server(Thread):

    # Informacao dos clientes conectados ao servidor
    _clients: Dict = {}
    _num_clients: int = 0

    def __init__(self,address=LOCAL_CONNECTION) -> None:

        Thread.__init__(self)

        self.num_images_received = 0
        self.running = True
        self.address = address

        # Iniciando um socket para servidor tcp
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


    def run(self) -> None:

        # Inicializar de vez o servidor
        self.socket.bind(self.address)
        self.socket.listen()

        while self.running:

            # Esperando por conexoes de clientes
            print("Waiting for a connection...")
            conn, addr = self.socket.accept()

            # Receber primeiro pacote, que sera o nome do cliente
            username = string_from_bytes(conn.recv(MSG_BUFFER_SIZE))
            print(f"New connection detected!\nAddress: {addr} \nUsername: {username}")

            self.__add_new_connection(conn,addr,username)


    # Salvar a nova conexao e suas informacoes, e inicializar a thread
    # do cliente
    def __add_new_connection(self,conn,addr,username) -> None:
        
        self._clients[conn] = {
            USERNAME_KEY : username,
            ADDRESS_KEY  : addr
        }
        self._num_clients += 1

        new_client = ClientThread(conn,self)
        new_client.start()

    # Abrir a imagem a ser processada, separar elas e 
    # mandar para os clientes processarem
    def send_image_to_clients_process(self,img_path: str) -> None:

        print("splitting the image in slabs")

        img = ImageUtils.open_image_as_numpy_array(img_path)
        img_slabs = ImageUtils.split_img(img, self._num_clients, BLUR_RADIUS)

        print("starting the sending process")
        ClientThread.start_client_processing(len(img_slabs))
        print("Success! Now sending to the clients")

        client: socket 
        i = 0
        for client in self._clients.keys():

            img_bytes = ImageUtils.open_image_as_byte_array(img_slabs[i])
            image_size = len(img_bytes)

            msg = f"{SENDING_IMAGE}|{i}|{image_size}"
            msg = to_image_instruction_msg(msg)

            try:
                client.sendall(msg + img_bytes)
            
            except: 
                client.close()
                self._clients.pop(client)

            i += 1
        print("Success! The slabs were sent")

def main() -> None:

    server = Server()
    server.start()

    running = True

    while running:
        text = input()

        # enumerar as threads que foram criadas ate entao (server side)
        if text == "!enumerate":
            print(enumerate())
        
        else:
            server.send_image_to_clients_process(text)


if __name__ == "__main__":
    main()