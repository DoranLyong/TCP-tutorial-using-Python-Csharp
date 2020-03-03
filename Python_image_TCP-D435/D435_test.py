'''
Reference 
* https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python/examples

'''


import pyrealsense2 as d435
import numpy as np
import cv2

# Configure depth and color streams
pipeline = d435.pipeline()
config = d435.config()
config.enable_stream(d435.stream.depth, 640, 480, d435.format.z16, 30)
config.enable_stream(d435.stream.color, 640, 480, d435.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert any array to <numpy.ndarray>
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap1 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        depth_colormap2 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_BONE)
        
        depth_colormap3 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_RAINBOW)
        depth_colormap4 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_HSV)
        depth_colormap5 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_HOT)


        # _Stack both images horizontally        
        images_h1 = np.hstack((color_image, depth_colormap1, depth_colormap2))
        images_h2 = np.hstack((depth_colormap3, depth_colormap4, depth_colormap5))

        # _Stack both images vertically
        image_h3 = np.vstack((images_h1, images_h2))
        


        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', image_h3 )

        cv2.imwrite("Origina2l.png", image_h3  )
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop()
