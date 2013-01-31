#!/usr/bin/env python2

import cv2
from processor import Processor
from processor import FPS
from processor import VideoHandler

if __name__ == '__main__':

    # Flags
    debug = True
    graphical = True

    # Create a processor object
    processor = Processor()

    cv2.namedWindow("Processed")

    if debug:
        cv2.createTrackbar("H-Min", "Processed", processor.tmin1, 255, processor.min1 )
        cv2.createTrackbar("S-Min", "Processed", processor.tmin2, 255, processor.min2 )
        cv2.createTrackbar("V-Min", "Processed", processor.tmin3, 255, processor.min3 )

        cv2.createTrackbar("H-Max", "Processed", processor.tmax1, 255, processor.max1 )
        cv2.createTrackbar("S-Max", "Processed", processor.tmax2, 255, processor.max2 )
        cv2.createTrackbar("V-Max", "Processed", processor.tmax3, 255, processor.max3 )

    # cap = cv2.VideoCapture("http://10.29.45.11/mjpg/video.mjpg")

    videohandler = VideoHandler() 
    fps = FPS()

    while True:

        if videohandler.goalcaptureenabled:
            goalimg = videohandler.get_goal_img()
            processedgoalimg, goalnum = processor.find_squares(goalimg, debug = True, graphical = True)
            if graphical:
                cv2.imshow("Processed", processedgoalimg)

        if videohandler.pyramidcaptureenabled:
            pyramidimg = videohandler.get_pyramid_img()
            processedpyramidimg, pyramidnum = processor.find_squares(pyramidimg, debug = True, graphical = True)
            if graphical:
                cv2.imshow("Processed", processedpyramid)


        if debug:
            print fps.determineFPS()

        cv2.waitKey(1)
