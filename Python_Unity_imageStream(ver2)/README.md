# Python TCP server ↔ Unity TCP client for image streaming

## Usage sample
* Start \'D435_PyServer_TCP.py\' first  <br/>
* This example is tested using the [Intel D435](https://www.intelrealsense.com/depth-camera-d435/) for depth image streaming.<br/>
    * if you want more example codes for Intel cameras using python, go to the github link below. 

<br/>

This project is fixed from the first version. <br/>
* python server code had been fixed for TCP client in C#. 

You can control the spent image quality in python server code. <br/>
*  ```encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),80]```  
* ``` 80 → 100 ``` makes images in 100% quality, but it can overflow the buffer size.

## Test 
It's not perfect yet. <br/>

<img src="./Python_unity.gif" width=650>


***

### Reference 
* [Sample Code for Intel RealSense Python Wrapper, Github](https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python/examples)
* [Visual Analytics using OpenCV and RealSense Camera](http://blog.cogitomethods.com/visual-analytics-using-opencv-and-realsense-camera/)
* [How to save a texture2d into a PNG?, unity forums](https://answers.unity.com/questions/1331297/how-to-save-a-texture2d-into-a-png.html)
* [While loop not working?, unity forums](https://forum.unity.com/threads/while-loop-not-working.429208/)
* [TCP socket communication for image streaming and Texture2D error, stack overflow](https://stackoverflow.com/questions/60576364/tcp-socket-communication-for-image-streaming-and-texture2d-error)
* [Avoiding Update() in Unity, using profiling and making your monobehaviours more efficient.](https://medium.com/@LJackso/avoiding-update-in-unity-using-profiling-and-making-your-monobehaviours-more-efficient-5b4517be72b4)
* [How can I send image or texture and text through TCP to send data from mobile to PC, unity forums](https://answers.unity.com/questions/1671977/how-can-i-send-image-or-texture-and-text-through-t.html)
* [FM Exhibition Tool Pack, unity forums](https://forum.unity.com/threads/release-fmetp-stream-all-in-one-gameview-audio-stream-udp-tcp-websockets-html.670270/?_ga=2.165395007.1437209308.1583660169-1192047143.1583289634)

