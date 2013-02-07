#!/usr/bin/env python2

import numpy as np
import cv2
from contourfeatures import Contour 
import math
import socket
import time
import traceback


class TCPserver:
    TCP_IP = '' # needs to be blank to bind to any ip
    TCP_PORT = 1180
    BUFFER_SIZE = 1024
    message = ""

    tocrio = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)

    def __init__(self):
        self.initilize_connection()

    def initilize_connection(self):
        try:
            self.tocrio.bind( (self.TCP_IP, self.TCP_PORT) )
            self.tocrio.listen(1)
            self.connection, addr = self.tocrio.accept() # This is blocking
        except:
            traceback.print_exc()
            self.tocrio = None 

    def sendmessage(self, message):
        self.message = message
        try: 
            self.tocrio.send(self.message)
        except:
            self.connection.close()
            self.initilize_connection()
            traceback.print_exc()

    def recieveMessage(self):
        data = tocrio.recv(BUFFER_SIZE)

    def __del__(self):
        self.connection.close()

class FPS:
    """
    This class counts the number of times the loop is called

    determineFPS() should be only called exactly once per loop
    """
    frames = 0;
    start = time.time()
    last_time = 0.0

    def determineFPS(self):
        elapsed = time.time()  - self.start
        self.fps = self.frames / elapsed
        self.frames += 1
        return self.fps


class VideoHandler:

    capturefeed = ""
    captureenabled = False


    def __init__(self, capturefeed):
        self.capturefeed = capturefeed
        self.start_capture()



    def start_capture(self):
        self.capture = cv2.VideoCapture(self.capturefeed)
        if self.capture == None or not self.capture.isOpened():
            self.captureenabled = False
        elif self.capture.isOpened(): 
            self.captureenabled = True

    def get_img(self):
        if not self.captureenabled:
            print "retrying to capture feed"
            self.start_capture()

        # Retval is useless because of bad documentation
        retval, self.img = self.capture.read()

        return self.img


class Processor:
    """
    Processor: Used to process images
    """

    tmin1 = 67
    # tmin2 = 125
    tmin2=42 # s-min
    tmin3 = 213

    tmax1 = 101
    tmax2 = 255
    tmax3 = 255
    distance = 0
    #datatocrio = TCPserver()

    def  find_squares(self, img, debug = True, graphical = True):
        """
        find_squares: used to find squares in an image

        params:
            img: image to process

        return:
            An image of the same size with drawn outlines and 
            The number of squares found
        """

        # Blur the image
        img = cv2.GaussianBlur(img, (5, 5), 0)

        # Create thresh values from silder
        THRESH_MIN = np.array([self.tmin1, self.tmin2, self.tmin3], np.uint8)
        THRESH_MAX = np.array([self.tmax1, self.tmax2, self.tmax3], np.uint8)

        # Convert image to hsv
        hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

        # Do in range
        thresh = cv2.inRange(hsv_img, THRESH_MIN, THRESH_MAX)

        # Show the threshed image
        if debug and graphical:
            cv2.imshow('thresh', thresh)

        # Storage for squares
        squares = []

        # Storage for all convex hull operations
        hull = []

        mu = []
        mc = []

        # Get all contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Check if the contours have 4 sides and store it if it does
        for contour in contours:
            contour_length = cv2.arcLength(contour, True) * 0.02
            sides = cv2.approxPolyDP(contour, contour_length, True)
            if debug:
                print cv2.boundingRect(sides)

            if len(sides) == 4 and cv2.contourArea(sides) > 1000 and cv2.isContourConvex(sides):
                squares.append(sides)
                hull.append(cv2.convexHull(contour))

                mu=cv2.moments(contour)
                mc.append((int(mu['m10']/mu['m00']), int(mu['m01']/mu['m00'])) )






        # Draw all the squares
        if debug:
            print "num of centroids: %d" % len(mc)
        for mci in mc:
            if graphical:
                cv2.circle(img, mci, 5, (255, 255, 0), -1)
                cv2.circle(img, (320/2, mci[1]), 5, (255, 255, 0), -1)
            distance = (320/2) - mci[0] # Distance from centroid to center  of screen
            self.distance = distance
            if debug:
                print "dist %d" % distance
                if distance > 5: 
                    print "left"
                elif distance < -5:
                    print "right"
                else:
                    print "centered"
            message = "distance:%s" % str(distance)
            # xpoints = np.array([mci[0], 320/2], np.uint32)
            # ypoints = np.array([0, 0], np.uint32)
            # mag = cv2.magnitude(xpoints, ypoints)
            # print "mag %r" % mag

        if graphical:
            cv2.drawContours( img, squares, -1, (0, 255, 0), 3 )
            cv2.drawContours( img, hull, -1, (0, 255, 255), 3 )

        # Return the image we drew on the number of squares found
        return img, len(squares)


    def min1(self, x):
        self.tmin1 = x

    def min2(self, x):
        self.tmin2 = x

    def min3(self, x):
        self.tmin3 = x

    def max1(self, x):
        self.tmax1 = x

    def max2(self, x):
        self.tmax2 = x

    def max3(self, x):
        self.tmax3 = x

# Test code
if __name__ == '__main__':
    processor = Processor()

    cap = cv2.VideoCapture("http://10.29.45.11/mjpg/video.mjpg")

    while True:
        # Get the current camera image
        ret, img = cap.read()

        processed_img, num = processor.find_squares(img)

        cv2.imshow("Processed", processed_img)
        cv2.waitKey(30)
