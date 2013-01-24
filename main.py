#!/usr/bin/env python2

import cv2
from processor import Processor
import time

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
        cv2.createTrackbar("Direction From Target", "Processed", 0,  320, processor.distance)

    cap = cv2.VideoCapture("http://10.29.45.11/mjpg/video.mjpg")

    start = time.time()

    frames = 0

    while True:

        ret, img = cap.read()

        img, num = processor.find_squares(img, debug = True, graphical = True)

        if graphical:
            cv2.imshow("Processed", img)

        if debug:
            if frames != 0:
                elapsed =  time.time() - start
                fps= frames / elapsed
                print fps # Really shows loops per second, but serves as a way for me to see how well the image is being computed

        frames += 1
        cv2.waitKey(1)
