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

    t_huemin = 42
    # t_saturationmin = 125
    t_saturationmin=42 # s-min
    t_valuemin = 213

    t_huemax = 101
    t_saturationmax = 255
    t_valuemax = 255
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

        # Averages out surrounding pixels, simplifying matching entire regions
        # Removes noise by blurring
        # (5, 5) indicates the guassian kernel size 5x5
        # the third value indicateds standard deviation in the x direciton(none)
        img = cv2.GaussianBlur(img, (5, 5), 0)

        # Create thresh values from silder
        THRESH_MIN = np.array([self.t_huemin, self.t_saturationmin, self.t_valuemin], np.uint8)
        THRESH_MAX = np.array([self.t_huemax, self.t_saturationmax, self.t_valuemax], np.uint8)

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
                pass
                #print cv2.boundingRect(sides)

            if len(sides) == 4 and cv2.contourArea(sides) > 1000 and cv2.isContourConvex(sides):
                squares.append(sides)
                hull.append(cv2.convexHull(contour))

                mu=cv2.moments(contour)
                mc.append((int(mu['m10']/mu['m00']), int(mu['m01']/mu['m00'])) )
                #self.bounding_box=cv2.boundingRect(cont 
                # should I use a bounding rect or try to de-skew rectangles?

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


    def get_aspect_ratio( contour, ratio):
        """
        parameters: 
            contour: a single contour
            ratio: the desired ratio in decimal value width/hight
        """
        pass


    def huemin(self, x):
        self.t_huemin = x

    def saturationmin(self, x):
        self.t_saturationmin = x

    def valuemin(self, x):
        self.t_valuemin = x

    def huemax(self, x):
        self.t_huemax = x

    def saturationmax(self, x):
        self.t_saturationmax = x

    def valuemax(self, x):
        self.t_valuemax = x

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
