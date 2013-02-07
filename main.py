#!/usr/bin/env python2

import sys
import cv2
from processor import Processor
from processor import FPS
from processor import VideoHandler

if __name__ == '__main__':

    # -- Flags --
    # Second argument is always debug, third graphical if applicable
    if len(sys.argv) == 3:
        debug = sys.argv[1]
        graphical = sys.argv[2]
    else:
        debug = True
        graphical = True


    goalwinname = "NetCam"
    pyramidwinname = "UsbCam"
    if graphical:
        cv2.namedWindow(goalwinname)
        cv2.namedWindow(pyramidwinname)

    processor = Processor()
    frisbeecamera = VideoHandler("http://10.29.45.11/mjpg/video.mjpg") 
    climbingcamera = VideoHandler(0)
    fps = FPS()

    # Trackbars to find best hsv min/max values
    if debug and graphical:
        cv2.createTrackbar("H-Min", goalwinname, processor.tmin1, 255, processor.min1 )
        cv2.createTrackbar("S-Min", goalwinname, processor.tmin2, 255, processor.min2 )
        cv2.createTrackbar("V-Min", goalwinname, processor.tmin3, 255, processor.min3 )

        cv2.createTrackbar("H-Max", goalwinname, processor.tmax1, 255, processor.max1 )
        cv2.createTrackbar("S-Max", goalwinname, processor.tmax2, 255, processor.max2 )
        cv2.createTrackbar("V-Max", goalwinname, processor.tmax3, 255, processor.max3 )


    while True:

        if frisbeecamera.captureenabled:
            goalimg = frisbeecamera.get_img()
            processedgoalimg, goalnum = processor.find_squares(goalimg, debug = True, graphical = True)
            if graphical:
                cv2.imshow(winname, processedgoalimg)

        if climbingcamera.captureenabled:
            pyramidimg = climbingcamera.get_img()
            processedpyramidimg, pyramidnum = processor.find_squares(pyramidimg, debug, graphical)
            if graphical:
                cv2.imshow(winname, processedpyramid)


        if debug:
            print fps.determineFPS()

        cv2.waitKey(30)
