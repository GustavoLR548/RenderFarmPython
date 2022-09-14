from threading import Thread
from image_utils import read_image_from_bytes
from network_utils import capture_image, extract_instruction_from_bytes

from constants import MSG_BUFFER_SIZE, SENDING_IMAGE

class ClientThread(Thread):


    def __init__(self, conn = None, server = None) -> None:

        Thread.__init__(self)
        self.running = True
        self.conn = conn
        self.server = server


    def run(self) -> None:
        
        while self.running:

            data = self.conn.recv(MSG_BUFFER_SIZE)
            instruction, data = extract_instruction_from_bytes(data)

            if not instruction:
                print("Error! Invalid instruction")
                continue

            if SENDING_IMAGE in instruction:
                num_of_bytes = int(instruction.split("|")[1])
                data = capture_image(self.conn,data,num_of_bytes)

            image = read_image_from_bytes(data)
            image.save("conseguimos.jpg")
            
            

