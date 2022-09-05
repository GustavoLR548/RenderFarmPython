from threading import Thread
from image_utils import read_image_from_bytes

class ClientThread(Thread):

    def __init__(self, conn = None, server = None) -> None:
        Thread.__init__(self)
        self.running = True
        self.conn = conn
        self.server = server

    def run(self) -> None:
        
        while self.running:

            data = None
            m = str(self.conn.recv(4096),"utf-8")
            
            if "SENDING_IMAGE" in m:
                num_of_bytes = int(m.split("|")[1])
                data = self.capture_image(data,num_of_bytes)
                

            image = read_image_from_bytes(data)

            image.save("conseguimos.jpg")
            """
            if not data:
                self.running = False 

            else:
                self.server.process_message(data,self.conn)
            """

    def capture_image(self,data,num_of_bytes):
        m = self.conn.recv(4096)
        data = m
        i = 4096
        while i < num_of_bytes:
            m = self.conn.recv(4096)
            i += len(m)

            data += m

        return data