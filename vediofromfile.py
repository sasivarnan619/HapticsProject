import numpy 
import cv2
import time
from PIL import Image
frame_count = 0
cap = cv2.VideoCapture('hi.mp4')
while(cap.isOpened()):
    ret, frame = cap.read()
    frame_count = frame_count + 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,230,255,cv2.THRESH_BINARY)
    print ret
    cv2.imshow('frame',thresh)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break
    if frame_count == 10:
        break
cap.release()
cv2.destroyAllWindows()
 
