import socket
import threading
import Utilities as U

class Client:

    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))

        self.running = True
        self.new_text = ""
        self.nickname = "Not Logged in"
        self.new_messages = ""

        self.from_database = ""

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()


    def write(self,contents):
        contents = str(contents)
        if contents != "":
            self.sock.send(contents.encode('utf-8'))
            
    def stop(self):
        self.running = False
        print("closed")
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message.startswith("GFDB"):
                    self.from_database = message
                elif message.startswith("*"):
                    message = message.removeprefix("*")
                    self.new_text += message
                elif message.startswith("FM"):
                    self.new_messages = message
                
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break
    def fetch_text(self):
        if len(self.new_text)>0:
            text = self.new_text
            self.new_text = ""
        else:
            text = ""
        return text