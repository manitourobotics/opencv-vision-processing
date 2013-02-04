#!/usr/bin/env python2.7


import cv2

# Tests to see if any video's input can be capture.

cap = cv2.VideoCapture(0)
while True:
    ret, img = cap.read()
    cv2.imshow("test", img)
    cv2.waitKey(30)
