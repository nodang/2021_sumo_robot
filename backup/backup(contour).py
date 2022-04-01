import cv2
import numpy as np

cap = cv2.VideoCapture(0)

lower_blue = np.array([85,100,100])
upper_blue = np.array([105,255,255])

lower_green = np.array([50,80,80])
upper_green = np.array([80,255,255])

lower_red = np.array([153,100,100])
upper_red = np.array([173,255,255])

while(1):
    ret, frame = cap.read()

    hsv = cv2. cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask1 = cv2.inRange(hsv, lower_green, upper_green)
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    res = cv2.bitwise_and(frame, frame, mask=mask)
    res1 = cv2.bitwise_and(frame, frame, mask=mask1)
    res2 = cv2.bitwise_and(frame, frame, mask=mask2)

    #cv2.imshow('frame', frame)

    con = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(con, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN,  cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    contours, hierachy = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    con1 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
    ret, binary1 = cv2.threshold(con1, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    opening1 = cv2.morphologyEx(binary1, cv2.MORPH_OPEN,  cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    contours1, hierachy = cv2.findContours(opening1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    con2 = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)
    ret, binary2 = cv2.threshold(con2, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    opening2 = cv2.morphologyEx(binary2, cv2.MORPH_OPEN,  cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    contours2, hierachy = cv2.findContours(opening2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
	area = 0
	for cntr in contours:
	#cntr = contours[0]
	    #print(approx)
	    areaP = area
	    area = cv2.contourArea(cntr)
	    if area >= areaP:
		cntrB = cntr
	epsilon = 0.07 * cv2.arcLength(cntrB, True)
	approx = cv2.approxPolyDP(cntrB, epsilon, True)
	cv2.drawContours(res, [approx], -1, (255, 0, 0), 3)
    if contours1:
	area1 = 0
	for cntr1 in contours1:
	#cntr = contours[0]
	    #print(approx)
	    areaP1 = area1
	    area1 = cv2.contourArea(cntr1)
	    if area1 >= areaP1:
		cntrB1 = cntr1
	epsilon1 = 0.07 * cv2.arcLength(cntrB1, True)
	approx1 = cv2.approxPolyDP(cntrB1, epsilon1, True)
	cv2.drawContours(res1, [approx1], -1, (0, 255, 0), 3)
    if contours2:
	area2 = 0
	for cntr2 in contours2:
	#cntr = contours[0]
	    #print(approx)
	    areaP2 = area2
	    area2 = cv2.contourArea(cntr2)
	    if area2 >= areaP2:
		cntrB2 = cntr2
	epsilon2 = 0.07 * cv2.arcLength(cntrB2, True)
	approx2 = cv2.approxPolyDP(cntrB2, epsilon2, True)
	cv2.drawContours(res2, [approx2], -1, (0, 0, 255), 3)

    cv2.imshow('Blue', res)
    cv2.imshow('Green', res1)
    cv2.imshow('Red', res2)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
	break

cv2.destroyAllWindows()
