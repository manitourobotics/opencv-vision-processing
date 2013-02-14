#!/usr/bin/env python2.7

import socket
import time
import traceback
import sys

import cv2
from processor import Processor
from processor import FPS
from processor import VideoHandler
if __name__ == '__main__':
    # -- Flags --
    # Second argument is always debug, third graphical if applicable
    if len(sys.argv) == 3:
        debug = argv[1]
        graphical = argv[2]
    else:
        debug = True
        graphical = True


    winname = "Processed"
    cv2.namedWindow(winname)

    processor = Processor()
    frisbeecamera = VideoHandler("http://10.29.45.11/mjpg/video.mjpg") 
    climbingcamera = VideoHandler(0)
    fps = FPS()

    # Trackbars to find best hsv min/max values
    if debug:
        cv2.createTrackbar("H-Min", winname, processor.t_huemin, 255, processor.huemin )
        cv2.createTrackbar("S-Min", winname, processor.tmin2, 255, processor.min2 )
        cv2.createTrackbar("V-Min", winname, processor.tmin3, 255, processor.min3 )

        cv2.createTrackbar("H-Max", winname, processor.tmax1, 255, processor.max1 )
        cv2.createTrackbar("S-Max", winname, processor.tmax2, 255, processor.max2 )
        cv2.createTrackbar("V-Max", winname, processor.tmax3, 255, processor.max3 )

    # Do not use bind with localhost as the address -- The port will
    #   not be opened to outside IPs
    TCP_IP = ''
    TCP_PORT  = 1180

    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind((TCP_IP, TCP_PORT)) # still needs to be a tupple
    # s.listen(1) # Only l isten for one connection max

    while True:
        # conn, addr = s.accept() # Accept any connections. 
        # Reaccept if connection lost



        while True:
            if frisbeecamera.captureenabled:
                goalimg = frisbeecamera.get_img()
                processedgoalimg, goalnum = processor.find_squares(goalimg, debug = True, graphical = True)
                if graphical:
                    cv2.imshow(winname, processedgoalimg)

            if climbingcamera.captureenabled:
                pyramidimg = climbingcamera.get_img()
                processedpyramidimg, pyramidnum = processor.find_squares(pyramidimg, debug = True, graphical = True)
                if graphical:
                    cv2.imshow(winname, processedpyramid)


            if debug:
                print fps.determineFPS()

            # print 'Connection address:', addr
            # try:
            #     conn.send("distance:" + str(processor.distance) + "\n")
            # except: 
            #     # If the client closes the connection, don't quit and
            #     #   look for a new one
            #     traceback.print_exc()
            #     conn.close()
            #     break
            # time.sleep(1) # Do I need a wait? -- rapid sucession of sends else
            cv2.waitKey(30)

        #conn.close()
