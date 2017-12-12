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
# label, co-cordinate, on frame count, off frame count
label = [["A", (0, 0),0,0], ["B", (0, 0),0,0], ["C", (0, 0),0,0], ["D", (0, 0),0,0]]
upd=0
# keep looping
while True:
        # grab the current frame
        (grabbed, frame) = camera.read()

        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if args.get("video") and not grabbed:
            
                break
        if frame_count == 0:
            frame_count = 1
            continue
            
        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #ret,hsv = cv2.threshold(gray,230,255,cv2.THRESH_BINARY)
        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        #mask = cv2.inRange(hsv, greenLower, greenUpper)
        #mask = cv2.erode(mask, None, iterations=2)
        #mask = cv2.dilate(mask, None, iterations=2)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #gray = cv2.GaussianBlur(gray, (7,7), 1.5)
        #gray = cv2.GaussianBlur(gray, (7,7), 1.5)
        ret,mask = cv2.threshold(gray,10,255,cv2.THRESH_BINARY)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        frame_count = frame_count + 1
        check = [[0,0], [1,0], [2,0], [3,0]]
        # only proceed if at least one contour was found
        print len(cnts)
        
        if len(cnts) == 1:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                #c = max(cnts, key=cv2.contourArea)
                
            c = cnts[0]
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            for i in range (4):
                if label[i][0] == "D":
                    label[i][1] = center
                    label[i][2] = label[3][2] + 1
                else:
                    label[i][3] = label[i][3] + 1
            
                        #print center
                        # only proceed if the radius meets a minimum size
            if radius > 0:
                                # draw the circle and centroid on the frame,
                                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 0), 2)
                cv2.circle(frame, center, 1, (0, 0, 255), -1)
            else:
                count = count
                                #print str(count) +"at"+ str(frame_count)
                         # update the points queue
                        #pts.appendleft(center)
        elif len(cnts) == 4:
            if upd == 0:
                upd = upd+1
                for i in range(len(cnts)):
                        c = cnts[i]
                        ((x, y), radius) = cv2.minEnclosingCircle(c)
                        M = cv2.moments(c)
                        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                        label[i][1] = center
                        label[i][2] = label[i][2] + 1
                        #print center
                        # only proceed if the radius meets a minimum size
                        if radius > 0:
                                # draw the circle and centroid on the frame,
                                # then update the list of tracked points
                                cv2.circle(frame, (int(x), int(y)), int(radius),
                                        (0, 0, 0), 2)
                                cv2.circle(frame, center, 1, (0, 0, 255), -1)
                        else:
                                count = count
            else:
                for i in range(len(cnts)):
                        c = cnts[i]
                        ((x, y), radius) = cv2.minEnclosingCircle(c)
                        M = cv2.moments(c)
                        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                        for j in range (4):
                            dst = distance.euclidean(label[j][1],center)
                            if dst<10:
                                label[j][1] = center
                                label[j][2] = label[j][2] + 1
                        #print center
                        # only proceed if the radius meets a minimum size
                        if radius > 0:
                                # draw the circle and centroid on the frame,
                                # then update the list of tracked points
                                cv2.circle(frame, (int(x), int(y)), int(radius),
                                        (0, 0, 0), 2)
                                cv2.circle(frame, center, 1, (0, 0, 255), -1)
                        else:
                                count = count
        elif len(cnts) == 3 or len(cnts) == 2:
            for i in range(len(cnts)):
                        c = cnts[i]
                        ((x, y), radius) = cv2.minEnclosingCircle(c)
                        M = cv2.moments(c)
                        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                        for j in range (4):
                            dst = distance.euclidean(label[j][1],center)
                            if dst<10:
                                label[j][1] = center
                                label[j][2] = label[j][2] + 1
                                check[j][1] = 1
                        #print center
                        # only proceed if the radius meets a minimum size
                        if radius > 0:
                                # draw the circle and centroid on the frame,
                                # then update the list of tracked points
                                cv2.circle(frame, (int(x), int(y)), int(radius),
                                        (0, 0, 0), 2)
                                cv2.circle(frame, center, 1, (0, 0, 255), -1)
                        else:
                                count = count
            for i in range (4):
                if check[i][1] == 0:
                    label[i][3] = label[i][3] + 1
                
        else:
                count = count + 1
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
