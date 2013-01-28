#!/usr/bin/env python2

import numpy as np
import cv2
from contourfeatures import Contour 
import math

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
    distance = 0;

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
            print cv2.boundingRect(sides)

            if len(sides) == 4 and cv2.contourArea(sides) > 1000 and cv2.isContourConvex(sides):
                squares.append(sides)
                hull.append(cv2.convexHull(contour))

                mu=cv2.moments(contour)
                mc.append((int(mu['m10']/mu['m00']), int(mu['m01']/mu['m00'])) )






        # Draw all the squares
        print "num of centroids: %d" % len(mc)
        for mci in mc:
            cv2.circle(img, mci, 5, (255, 255, 0), -1)
            cv2.circle(img, (320/2, mci[1]), 5, (255, 255, 0), -1)
            # xpoints = np.array([mci[0], 320/2], np.uint32)
            # ypoints = np.array([0, 0], np.uint32)
            # mag = cv2.magnitude(xpoints, ypoints)
            # print "mag %r" % mag

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

    def distance(self, x):
        self.distance = 0;

if __name__ == '__main__':
    processor = Processor()

    cap = cv2.VideoCapture("http://10.29.45.11/mjpg/video.mjpg")

    while True:
        # Get the current camera image
        ret, img = cap.read()

        processed_img, num = processor.find_squares(img)

        cv2.imshow("Processed", processed_img)
        cv2.waitKey(30)
