from threading import Thread

from socket import socket, AF_INET, SOCK_STREAM
from image_utils import open_image_as_byte_array, read_image_from_bytes, apply_blur

import constants as consts

from byte_utils import to_bytes
import network_utils as NetworkUtils

"""
Thread do cliente
"""
class Client(Thread):

    def __init__(self,name, address = consts.LOCAL_CONNECTION) -> None:
        
        Thread.__init__(self)
        self.running  = True
        self.username = name
        self.address = address

        # Iniciar socket do cliente
        self.socket = socket(AF_INET, SOCK_STREAM)

    # Funcao que sera chamada com o inicio da Thread
    def run(self) -> None: 

        # Conectar ao servidor e mandar nome de usuario
        self.socket.connect(self.address)
        self.socket.sendall(to_bytes(self.username))
        print("Connected to server!")

        while self.running:
            
            # Receber dados do servidor e separar bytes das instrucoes da imagem
            data = self.socket.recv(consts.MSG_BUFFER_SIZE)
            instructions, data = NetworkUtils.separate_instructions_from_bytes(data)

            if consts.SENDING_IMAGE in instructions:
                
                # Pegar informacoes da imagem e capturar ela
                num_of_bytes, image_id = NetworkUtils.get_instruction_data(instructions)
                data = NetworkUtils.capture_image(self.socket,data,num_of_bytes)

                # Ler a imagem dos bytes e aplicar a operacao
                image = read_image_from_bytes(data)
                image = apply_blur(image,5)
               
                # Transformar a imagem de volta para byte array
                img_bytes  = open_image_as_byte_array(image)
                image_size = len(img_bytes) 

                # Fazer mensagem para voltar para o servidor
                msg = f"{consts.SENDING_IMAGE}|{image_id}|{image_size}"
                msg = NetworkUtils.to_image_instruction_msg(msg)


                # Mandar a imagem de volta para o servidor
                print("Sending images back!")
                self.socket.sendall(msg + img_bytes)

def main() -> None:

    name = input("Enter your name: ")

    client = Client(name)
    client.start()

    running = True

    while running:
        text = input()

    client.join()

if __name__ == "__main__":
    main()
    