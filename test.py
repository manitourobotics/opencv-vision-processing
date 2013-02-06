#!/usr/bin/env python2.7


import cv2
import sys

# Tests to see if any video's input can be captured.

# if first argument is 'usb'(and it's available) use the first camera in the usb index, else, test 
#   the axis 206 network feed

cv2.namedWindow("test")

if len(sys.argv) == 2 and sys.argv[1] == "usb":
    cap = cv2.VideoCapture(0)
else:
    cap = cv2.VideoCapture("http://10.29.45.11/mjpg/video.mjpg")

while True:
    ret, img = cap.read()
    cv2.imshow("test", img)
    cv2.waitKey(30)
