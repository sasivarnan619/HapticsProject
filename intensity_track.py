# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from scipy.spatial import distance
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
        help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (10, 10, 10)
greenUpper = (255, 255, 255)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
        camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
        camera = cv2.VideoCapture(args["video"])
count = 0
frame_count = 0
# keep looping
label = [["A", (0, 0),0,0], ["B", (0, 0),0,0], ["C", (0, 0),0,0]]
while True:
        # grab the current frame
        (grabbed, frame) = camera.read()

        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if args.get("video") and not grabbed:
                break

        if frame_count < 1:
            frame_count = 1 + frame_count
            continue
        frame = imutils.resize(frame, width=600)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        ret,mask = cv2.threshold(gray,20,255,cv2.THRESH_BINARY)
        ret,maskh = cv2.threshold(gray,105,255,cv2.THRESH_BINARY)
        ret,masklt = cv2.threshold(gray,100,255,cv2.THRESH_TOZERO_INV)
        ret,maskl = cv2.threshold(masklt,10,255,cv2.THRESH_BINARY)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        maskh = cv2.erode(maskh, None, iterations=2)
        maskh = cv2.dilate(maskh, None, iterations=2)
        maskl = cv2.erode(maskl, None, iterations=2)
        maskl = cv2.dilate(maskl, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
        cntsh = cv2.findContours(maskh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
        cntsl = cv2.findContours(maskl.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
        print len(cntsl)
        center = None
        centerh = None
        centerl = None
        
        
        if len(cnts) > 0:
               
                for i in range(len(cnts)):
                        c = cnts[i]
                        ((x, y), radius) = cv2.minEnclosingCircle(c)
                        M = cv2.moments(c)
                        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                        #print center
                        # only proceed if the radius meets a minimum size
                        if frame_count == 2:
                                label[i][1] = center
                        else:
                                for j in range (3):
                                        dst = distance.euclidean(label[j][1],center)
                                        if dst<10:
                                                label[j][1] = center
                        if len(cntsh) > 0:
                                for j in range(len(cntsh)):
                                        ch = cntsh[j]
                                        ((x, y), radius) = cv2.minEnclosingCircle(ch)
                                        M = cv2.moments(ch)
                                        centerh = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                                        if centerh == center:
                                                label[i][2] = label[i][2] + 1
                        if len(cntsl) > 0:
                                for j in range(len(cntsl)):
                                        cl = cntsl[j]
                                        ((x, y), radius) = cv2.minEnclosingCircle(cl)
                                        M = cv2.moments(cl)
                                        centerl = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                                        if centerl == center:
                                                label[i][3] = label[i][3] + 1
                       
        if frame_count % 15 == 0:
                print label
                for i in range(len(label)):
                        if label[i][2] >= 3 and label[i][2] <= 7:
                                label[i][0] = "B"
                        elif label[i][2] < 2:
                                label[i][0] = "A"
                        elif label[i][2] >= 8 and label[i][2] <= 12:
                                label[i][0] = "C"
                        #elif label[i][2] > 13:
                                #label[i][0] = "D"
        frame_count = frame_count + 1
                #print str(count) +"at"+ str(frame_count)
       
        # loop over the set of tracked points
##        for i in xrange(1, len(pts)):
##                # if either of the tracked points are None, ignore
##                # them
##                if pts[i - 1] is None or pts[i] is None:
##                        continue
##
##                # otherwise, compute the thickness of the line and
##                # draw the connecting lines
##                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
##                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        # show the frame to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
                break
        
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
