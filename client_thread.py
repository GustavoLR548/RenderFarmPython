from threading import Thread
from image_utils import read_image_from_bytes
from network_utils import capture_image

from constants import MSG_BUFFER_SIZE, RECEIVING_IMAGE

from conversion_utils import string_from_bytes

class ClientThread(Thread):


    def __init__(self, conn = None, server = None) -> None:

        Thread.__init__(self)
        self.running = True
        self.conn = conn
        self.server = server


    def run(self) -> None:
        
        while self.running:

            data        = None
            instruction = string_from_bytes(self.conn.recv(MSG_BUFFER_SIZE))
            
            if RECEIVING_IMAGE in instruction:
                num_of_bytes = int(instruction.split("|")[1])
                data = capture_image(self.conn,data,num_of_bytes)

            image = read_image_from_bytes(data)
            

