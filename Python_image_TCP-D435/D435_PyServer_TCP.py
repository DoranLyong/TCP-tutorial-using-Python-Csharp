""" 
Code author : DoranLyong 

Reference : 
* https://docs.python.org/3.7/library/socketserver.html
* https://webnautes.tistory.com/1382
* https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python/examples
* http://blog.cogitomethods.com/visual-analytics-using-opencv-and-realsense-camera/
"""
import pyrealsense2 as d435
import socketserver
import socket
import cv2 
import numpy as np 
from queue import Queue
from _thread import *


# _Set queue 
enclosure_queue = Queue() 


# _Configures of depth and color streams 
pipeline = d435.pipeline()
config = d435.config()
config.enable_stream(d435.stream.depth, 640, 480, d435.format.z16, 30)
config.enable_stream(d435.stream.color, 640, 480, d435.format.bgr8, 30)



# _ D435 process 
def D435(queue):
    
    
    print("D435 processing", end="\n ")
    pipeline.start(config) # _Start streaming

    try:
        while True: 
            # _Wait for a coherent pair of frames: depth and color 
            frames = pipeline.wait_for_frames()            
            depth_frame, color_frame = (frames.get_depth_frame(), frames.get_color_frame())

            if not (depth_frame and color_frame): 
                print("Missing frame...", end="\n")
                continue

            # _Convert <pyrealsense2 frame> to <ndarray>
            depth_image = np.asanyarray(depth_frame.get_data()) # convert any array to <ndarray>
            color_image = np.asanyarray(color_frame.get_data())


            # _Apply colormap on depth image 
            #  (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.05), cv2.COLORMAP_BONE)

            #print("Depth map shape = ", depth_colormap.shape)   


            # _Encoding 
            target_frame = depth_colormap 

            #print(target_frame.shape)

            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]

            result, imgencode = cv2.imencode('.jpg', target_frame, encode_param)  # Encode numpy into '.jpg'
            data = np.array(imgencode)

            stringData = data.tostring()   # Convert numpy to string
            queue.put(stringData)          # Put the encode in the queue stack


            # __ Image show             
            images = np.hstack((color_image, depth_colormap)) # stack both images horizontally             
            cv2.namedWindow('RealSense_server', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense_server', images)
            cv2.waitKey(1)        

        

    finally: 
        cv2.destroyAllWindows()

        # _Stop streaming 
        pipeline.stop()

    





class MyTCPHandler(socketserver.BaseRequestHandler):

    queue  = enclosure_queue 
    stringData = str()

    def handle(self):
       
        # 'self.request' is the TCP socket connected to the client     
        print("A client connected by: ", self.client_address[0], ":", self.client_address[1] )


        while True:
            try:
                # _server <- client 
                self.data = self.request.recv(1024).strip()   # 1024 byte for header 

                if not self.data: 
                    print("The client disconnected by: ", self.client_address[0], ":", self.client_address[1] )     
                    break                

                # _Get data from Queue stack 
                MyTCPHandler.stringData = MyTCPHandler.queue.get()     

                # _server -> client 
                #print(str(len(MyTCPHandler.stringData)).ljust(16).encode())  # <str>.ljust(16) and encode <str> to <bytearray>
                self.request.sendall(str(len(MyTCPHandler.stringData)).ljust(16).encode())
                self.request.sendall(MyTCPHandler.stringData)             

                
            except ConnectionResetError as e: 
                print("The client disconnected by: ", self.client_address[0], ":", self.client_address[1] )     
                break


if __name__ == "__main__":

    # _Webcam process is loaded onto subthread
    start_new_thread(D435, (enclosure_queue,))  
    
    # _Server on
    HOST, PORT = socket.gethostname(), 8080 
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:    
        
        print("****** Server started ****** ", end="\n \n")     
        
        try: 
            server.serve_forever()
        
        except KeyboardInterrupt as e:
            print("******  Server closed ****** ", end="\n \n" )  