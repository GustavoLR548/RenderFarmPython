from threading import Thread

class ClientThread(Thread):

    def __init__(self, conn = None, server = None) -> None:
        Thread.__init__(self)
        self.running = True
        self.conn = conn
        self.server = server

    def run(self) -> None:
        
        while self.running:

            data = str(self.conn.recv(1024),"utf-8")
            if not data:
                self.running = False 

            else:
                self.server.process_message(data,self.conn)
