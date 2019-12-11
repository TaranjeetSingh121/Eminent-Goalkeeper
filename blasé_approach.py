# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 13:58:32 2019

@author: singh Dhillon
"""

# USAGE
# python object_movement.py --video object_tracking_example.mp4
# python object_movement.py

# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import math
import requests
import serial

# choose distance between ball and goalpost(m)
distance=2
#distance car needs to move(m)
distance2=0
# direction variable declaration(F-car moves forward in right direction, B-car moves backward in left direction)
direction1='F'
# brake variable
brake='S'
# time for which the car moves
tiktok=0
# origionally measured Forward and backward speed of car(m/sec), calibrate if not working
speedF=2.28904
speedB=1.96714

counter=0

qq = 0
count= 0
xx=0
xx1=0
yy1=0
yy=0
var = 0
url = "http://192.168.43.1:8080/shot.jpg"
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()

# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(2.0)


count = 0
angle = 0
# keep looping

pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""
while True:
    temp=0
    url_response = requests.get(url)
    img_array = np.array(bytearray(url_response.content)	, dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)
	# grab the current frame
    frame = img
	#added
	# count =count+1
	# if count == 1000:
	# 	count = 0
	# 	gg=1
	# else:
	# 	continue

	#till here
	# handle the frame from VideoCapture or VideoStream
	#frame = frame[1] if args.get("video", False) else frame

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
    if frame is None:
        break

	# resize the frame, blur it, and convert it to the HSV
	# color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

	# only proceed if at least one contour was found
    if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
        c= max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        xx1 = xx
        yy1  = yy
        xx = int(M["m10"]/M["m00"])
        yy = int(M["m01"] / M["m00"])
        var = var+1
		# only proceed if the radius meets a minimum size
        if radius > 10:
            temp=1
            counter+=1
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)
        if var > 5:
            distance2=distance*math.tan(math.radians(abs(90-(180-(math.degrees((math.atan2((yy1-yy),(xx1-xx)))))))))
            print(distance2)
            if ((180-(math.degrees((math.atan2((yy1-yy),(xx1-xx))))))) >90:	
                print("backward")
                direction1='B'
                tiktok=distance2/speedB
            else:
                print("forward")
                direction1='F'
                tiktok=distance2/speedF
    if temp==0 and counter>1:
        break
    # loop over the set of tracked points
    for i in np.arange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
        if pts[i - 1] is None or pts[i] is None:
            continue

		# check to see if enough points have been accumulated in
		# the buffer
        if counter >= 10 and i == 1 and pts[-10] is not None:
			# compute the difference between the x and y
			# coordinates and re-initialize the direction
			# text variables
            dX = pts[-10][0] - pts[i][0]
            dY = pts[-10][1] - pts[i][1]
            (dirX, dirY) = ("", "")

			# ensure there is significant movement in the
			# x-direction
            if np.abs(dX) > 20:
                dirX = "East" if np.sign(dX) == 1 else "West"

			# ensure there is significant movement in the
			# y-direction
            if np.abs(dY) > 20:	
                dirY = "North" if np.sign(dY) == 1 else "South"

			# handle when both directions are non-empty
            if dirX != "" and dirY != "":
                direction = "{}-{}".format(dirY, dirX)

			# otherwise, only one direction is non-empty
            else:
                direction = dirX if dirX != "" else dirY
			#addded
            try:
                vvv=1
            except:
                gg=1
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# show the movement deltas and the direction of movement on
	# the frame
    cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 0, 255), 3)
    cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)

	# show the frame to our screen and increment the frame counter
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1

	# if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()

# otherwise, release the camera
else:
	vs.release()

# commands for serial port
# define the serial port and baud rate.
# ensure the 'COM#' corresponds to what was seen in the Windows Device Manager
ser = serial.Serial('COM5', 9600)

def movement():
    
    if direction1.upper()=='F':
        print("car moving right")
        time.sleep(0.1)
        ser.write(b'F')
        time.sleep(tiktok)
        print("Brake...........")
        ser.write(b'S')
    
    if direction.upper()=='B':
        print("car moving left")
        time.sleep(0.1)
        ser.write(b'B')
        time.sleep(tiktok)
        print("Brake..........")
        ser.write(b'S')
    
    else:
        print("something is wrong LOL")
    
    print("Program Exiting")
    ser.close()
    return
time.sleep(2) # wait for the serial connection to initialize

movement() #calling function to control car

# close all windows
cv2.destroyAllWindows()
