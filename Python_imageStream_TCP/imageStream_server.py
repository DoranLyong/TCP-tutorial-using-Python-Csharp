""" 
Code author : DoranLyong 

Reference : 
* https://docs.python.org/3.7/library/socketserver.html
* https://webnautes.tistory.com/1382

"""

import socketserver
import socket
import cv2
import numpy as np 
from queue import Queue 
from _thread import *


enclosure_queue = Queue() 


# _ Webcam-image process 
def webcam(queue):

    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()

        if ret == False:
            continue

        # _Encoding 
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

        result, imgencode = cv2.imencode('.jpg', frame, encode_param)  # Encode numpy into '.jpg'
        data = np.array(imgencode)

        stringData = data.tostring()   # Convert numpy to string
        queue.put(stringData)          # Put the encode in the queue stack

        # _Image show
        cv2.imshow('image on Server', frame)
        
        key = cv2.waitKey(1)
        if key == 27:
            break




class MyTCPHandler(socketserver.BaseRequestHandler):

    queue  = enclosure_queue 
    stringData = str()

    def handle(self):
       
        # 'self.request' is the TCP socket connected to the client     
        print("A client connected by: ", self.client_address[0], ":", self.client_address[1] )



        while True:
            try:
                self.data = self.request.recv(1024).strip()  

                if not self.data: 
                    print("The client disconnected by: ", self.client_address[0], ":", self.client_address[1] )     
                    break
                

                MyTCPHandler.stringData = MyTCPHandler.queue.get()                  

                self.request.sendall(str(len(MyTCPHandler.stringData)).ljust(16).encode())
                self.request.sendall(MyTCPHandler.stringData)             

                
            except ConnectionResetError as e: 
                print("The client disconnected by: ", self.client_address[0], ":", self.client_address[1] )     
                break





if __name__ == "__main__": 
    
    # _Webcam process is loaded onto subthread
    start_new_thread(webcam, (enclosure_queue,))  
    
    # _Server on
    HOST, PORT = socket.gethostname(), 8080 
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:    
        
        print("****** Server started ****** ", end="\n \n")     
        
        try: 
            server.serve_forever()
        
        except KeyboardInterrupt as e:
            print("******  Server closed ****** ", end="\n \n" )
            