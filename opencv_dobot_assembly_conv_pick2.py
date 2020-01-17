##################################################################################
############# mini assembly second conveyor cam is blue jig #####################
############# x1, y1 camera origin positions are strongly dependant on camera####
##################################################################################


import cv2
import numpy as np
import imutils
import dobot
import serial
from serial.tools import list_ports

port=list_ports.comports()[0].device
d1 = dobot.Dobot(port=port, verbose=True)

d1.motor(50)

d1.movel(205, 0, 160, 0)
d1.delay(3)
t=0
i=0
def dobot(X,Y,t,r,x,y):
	#d1.movel(250, 0, 50, 0)
	#d1.delay(2)
	d1.movel(X+30, Y, 40, 0)
	d1.delay(0.5)
	d1.movel(X+30, Y, -7, 0)
	d1.delay(2)
	d1.suck(True)
	d1.delay(0.5)
	#d1.movel(X+30, Y, 40, 0)
	#d1.delay(0.5)
	d1.jump(x, y, -65+t, r)
	d1.delay(3) 
	d1.suck(False)
	d1.delay(0.5)
	d1.movel(250, 0, 160, 0)
	d1.delay(3)
	d1.movel(205, 0, 160, 0)
	d1.motor(50)

cap = cv2.VideoCapture(1)

X1 = 187
Y1 = -103.4
ke = 0
while(1):

	# Take each frame
	_, frame = cap.read()

	def make_480p():
		cap.set(3, 640)
		cap.set(4, 480)
		
	make_480p()

	# Convert BGR to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# define range of blue color in HSV
	lower_blue = np.array([99,50,120])
	upper_blue = np.array([130,255,255])

	# Threshold the HSV image to get only blue colors
	mask = cv2.inRange(hsv, lower_blue, upper_blue)

	# Bitwise-AND mask and original image

	cv2.imshow('frame',frame)
	#cv2.imshow('mask',mask)

	cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)


	for c in cnts:
		area = cv2.contourArea(c)
		
		if area > 5000:
			
			d1.delay(0.5)
			d1.motor(0)
			cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
			
			M = cv2.moments(c)
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			print(cX,cY)
			
			cv2.circle(frame, (cX,cY), 7, (255, 255, 255), -1)
			cv2.putText(frame, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
			cv2.imshow("frame",frame)
			
			X = X1 + (cY * 0.3125)
			Y = Y1 + (cX * 0.3125)
			
			print(X,Y)
            
            
			if ke >= 3:
				i=i+1
				t=t+5.5
				if i%2 == 0:
					r=180
					x=75
					y=231
				else:
					r=0
					x=100
					y=233
				#cv2.imshow("frame",frame)
				dobot(X,Y,t,r,x,y)
				ke = 0
			ke = ke+1
			
			 
			
			
	k = cv2.waitKey(5) 
	if k == 27:
		break
            
d1.close()        
cv2.destroyAllWindows()
