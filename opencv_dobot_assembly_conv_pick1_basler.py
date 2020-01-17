##################################################################################
############# mini assembly first conveyor cam is yellow jig #####################
##################################################################################

import cv2
import numpy as np
import imutils
import dobot
import serial
from serial.tools import list_ports
from pypylon import pylon

port=list_ports.comports()[0].device
d1 = dobot.Dobot(port=port, verbose=True)

d1.motor(50)

d1.movel(205, 0, 160, 0)
d1.delay(3)
placex=180
placey=-203
yv=0
o=0
def dobot(X,Y,xp,yp):
	#d1.movel(250, 0, 50, 0)
	#d1.delay(2)
	d1.movel(X, Y, 40, 0)
	d1.delay(0.5)
	d1.movel(X, Y, -6, 0)
	d1.delay(2)
	d1.suck(True)
	d1.delay(0.5)
	d1.movel(X, Y, 40, 0)
	d1.delay(0.5)
	d1.movel(xp, yp, -10, 0)
	d1.delay(2) 
	d1.suck(False)
	d1.delay(0.5)
	d1.jump(xp-30,yp,-20)
	d1.delay(0.5)
	d1.suck(True)
	d1.jump(122,-281,7)
	d1.delay(2)
	d1.suck(False)
	d1.delay(0.5)
	d1.movel(250, 0, 50, 0)
	d1.delay(1)
	d1.movel(205, 0, 160, 0)
	d1.delay(1)
	d1.motor(50)
	d1.delay(1)
	
# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

X1 = 182
Y1 = -93.4
ke = 0
while camera.IsGrabbing():

	grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

	if grabResult.GrabSucceeded():
		# Access the image data
		image = converter.Convert(grabResult)
		img = image.GetArray()

	'''def make_480p():
		cap.set(3, 640)
		cap.set(4, 480)
		
	make_480p()'''

	# Convert BGR to HSV
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# define range of blue color in HSV
	lower_blue = np.array([95,50,120])
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
        
		if area > 6000:

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
            
			'''#print(X,Y)
			if ke >= 3:
				for i in range(4):
					xv=0
					for j in range(2):
						dobot(X,Y,placex+xv,placey+yv)
						xv=xv+64
						continue
					yv=yv+32
				ke = 0
			ke = ke+1'''
			if ke >= 3:
				o=o+1
				if o<5:
					dobot(X,Y,placex,placey+yv)
				elif o==5:
					yv=0
					dobot(X,Y,placex+64,placey+yv)
				else:
					dobot(X,Y,placex+64,placey+yv)
				yv=yv+34
				
				ke = 0
			ke = ke+1			

             
            
            
	k = cv2.waitKey(5) 
	if k == 27:
		break
            
d1.close()        
cv2.destroyAllWindows()

'''
			if ke >= 3:
				c=c+1
				if c<5:
					dobot(X,Y,placex,placey+yv)
				elif c=5:
					yv=0
					dobot(X,Y,placex+64,placey+yv)
				else:
					dobot(X,Y,placex+64,placey+yv)
				yv=yv+32
				
				ke = 0
			ke = ke+1
'''