""" 
Code author : DoranLyong 

Reference : 
* https://docs.python.org/3.7/library/socketserver.html
* https://webnautes.tistory.com/1382


Please, start 'imageStream_server.py' first. 
"""

import socket 
import cv2 
import numpy as np 


# _ receive all 
def recvall(sock, count):
    buf = b''
    while count: 
        newbuf = sock.recv(count)   
        #print("sock data:", newbuf, end="\n")
        #print("Count: ", count, end="\n")
        #print("buff: ", buf, end="\n")
        if not newbuf: 
            return None 
        
        buf += newbuf 
        count -= len(newbuf)
    return buf


# _client host , server port 
HOST, PORT = socket.gethostname(), 8080 
client_send = "1"



# Creat a socket (SOCk_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock: 

    # _Connect to server and send data    
    client_sock.connect((HOST, PORT))
    
    while True:

        try:            
            # _client -> server  
            client_sock.sendall(client_send.encode())  

            # _client <- server  
            length = recvall( client_sock, 16)
            stringData = recvall(client_sock, int(length))
            data = np.frombuffer(stringData, dtype= 'uint8') 


            # _Image show 
            decodeImg = cv2.imdecode(data, 1) 
            cv2.imshow("image on Client", decodeImg)  

            cv2.waitKey(1)

        except KeyboardInterrupt as e: 
            print("***** Client closed ***** ", end="\n \n")
            cv2.destroyAllWindows()
            break         
        


