""" 
Code author : DoranLyong 

Reference : 
* https://docs.python.org/3.7/library/socketserver.html


Please, start 'chatStream_server.py' first. 
"""


import socket 
import cv2 
import numpy as np 


HOST, PORT = socket.gethostname(), 8080


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock: 

    # _Connect to server and send data     
    client_sock.connect((HOST, PORT))
    
    while True:

        try: 

            # _client -> server 
            message = input("Enter Message: ") 
            client_sock.sendall(message.encode('utf-8'))

            # _client <- server 
            recvData = client_sock.recv(1024)
            print("상대방: ",recvData.decode('utf-8'))


        except KeyboardInterrupt as e: 
            print("***** Client closed *****", end="\n \n")
            break         
        


