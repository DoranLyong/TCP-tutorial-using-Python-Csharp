""" 
Code author : DoranLyong 

Reference : 
* https://docs.python.org/3.7/library/socketserver.html
"""

import socketserver
import socket
import cv2
import numpy as np 
from queue import Queue 
from _thread import *


class MyTCPHandler(socketserver.BaseRequestHandler):
    
    sendData = str() 

    def handle(self):
        # 'self.request' is the TCP socket connected to the client   
        print("A client connected by: ", self.client_address[0], ":", self.client_address[1] )

        while True: 
            try:
                #self.data = self.request.recv(1024).strip()  # .strip() is .decode()
                self.data = self.request.recv(1024)
                
                if not self.data: 
                    print("The client disconnected by: ", self.client_address[0], ":", self.client_address[1] )     
                    break

                print("Received from ", self.client_address[0], ":", self.client_address[1],">>> ", self.data.decode() )


                MyTCPHandler.sendData = input("serverResponse:   ") 
                
                self.request.sendall(MyTCPHandler.sendData.encode('utf-8')) 

                 

            except ConnectionResetError as e:
                print("The client disconnected by: ", self.client_address[0], ":", self.client_address[1] )     
                break                 



if __name__ == "__main__": 
    
    # _Server on
    HOST, PORT = socket.gethostname(), 8080 
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:    
        
        print("****** Server started ****** ", end="\n \n")     
        
        try: 
            server.serve_forever()
        
        except KeyboardInterrupt as e:
            print("******  Server closed ****** ", end="\n \n" )
            