from threading import Thread, Lock
from image_utils import read_image_from_bytes
from network_utils import separate_instructions_from_bytes, get_instruction_data

import image_utils as ImageUtils
import time

from constants import MSG_BUFFER_SIZE, SENDING_IMAGE, FILE_BUFFER_SIZE

class ClientThread(Thread):

    processed_image_slabs = []
    num_images_received: int = 0
    num_slabs_to_process: int = 0

    def __init__(self, conn = None, server = None) -> None:

        Thread.__init__(self)

        self.thread_lock = Lock()
        self.running = True
        self.conn = conn
        self.server = server

    @classmethod
    def start_client_processing(cls,num_slabs) -> None:
        cls.num_slabs_to_process  = num_slabs
        cls.processed_image_slabs = [None] * num_slabs

    def run(self) -> None:
        
        while self.running:

            data = self.conn.recv(MSG_BUFFER_SIZE)
            #print(f"ClientThread {self.name}: New data received! {data}")
            instruction, data = separate_instructions_from_bytes(data)

            if not instruction:
                print("Error! Invalid instruction")
                continue

            if SENDING_IMAGE in instruction:
                print(f"ClientThread {self.name}: Get instruction set")
                num_of_bytes, image_id = get_instruction_data(instruction)
                print(f"Thread status: {self.thread_lock.locked()}")
                print(f"ClientThread {self.name}: Num of bytes = {num_of_bytes} \t image_id = {image_id}")
                self.thread_lock.acquire(True, 5)
                data = self.capture_image(data,num_of_bytes)
                
                print(f"ClientThread {self.name}: Reading image")
                image = read_image_from_bytes(data)
                
                print(f"ClientThread {self.name}: Sending received image")
                self.receive_image_from_clients(image,image_id)
                self.thread_lock.release()


    def capture_image(self,data,num_of_bytes):
        
        if not data:
            data = b''

        temp_data = self.conn.recv(FILE_BUFFER_SIZE)
        data      += temp_data 

        i = FILE_BUFFER_SIZE
        while i < num_of_bytes:
            temp_data  = self.conn.recv(FILE_BUFFER_SIZE)
            data      += temp_data 

            i += FILE_BUFFER_SIZE

        return data


    def receive_image_from_clients(self,img,id) -> None:

        print(f"ClientThread {self.name}: adding new slab")
        self.processed_image_slabs[id] = img
        self.server.num_images_received += 1

        print(self.processed_image_slabs)
        

        print(f"ClientThread {self.name}: releasing lock")
        #self.thread_lock.release()

        print(f"Recebi {self.server.num_images_received} slabs")
        print(f"Tenho que receber {self.num_slabs_to_process}")

        if self.server.num_images_received == self.num_slabs_to_process:
            self.process_final_image()


    
    def process_final_image(self) -> None:
        
        #print(f"ClientThread {self.name}: Processing final image!")
        reconstructed_img = ImageUtils.merge_img_slabs(self.processed_image_slabs, 
                                                        self.num_slabs_to_process, 
                                                        21)

        reconstructed_img.save("conseguimos_rada.jpg")

        self.processed_image_slabs = []
        self.num_images_received   = 0
        self.num_slabs_to_process  = 0
            