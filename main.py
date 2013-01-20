import cv2
from processor import Processor

if __name__ == '__main__':

    #Debug?
    debug = True

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

    cap = cv2.VideoCapture("http://10.29.45.11/mjpg/video.mjpg")

    while True:

        ret, img = cap.read()

        img, num = processor.find_squares(img, debug = True)

        cv2.imshow("Processed", img)

        cv2.waitKey(30)
    
