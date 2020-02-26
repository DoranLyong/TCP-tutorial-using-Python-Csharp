import socket 
import cv2 
import numpy as np 



HOST, PORT = socket.gethostname(), 8080


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock: 

    # _Connect to server and send data     
    client_sock.connect((HOST, PORT))
    
    while True:

        try: 
            message = input("Enter Message: ") 
            client_sock.sendall(message.encode('utf-8'))

            recvData = client_sock.recv(1024)
            print("상대방: ",recvData.decode('utf-8'))


        except KeyboardInterrupt as e: 
            break         
        


