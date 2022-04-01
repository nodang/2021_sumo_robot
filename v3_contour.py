import cv2
import numpy as np
import math
import RPi.GPIO as GPIO
import GPIOset as GS

cap = cv2.VideoCapture(0)

lower_blue = np.array([85,100,100])
upper_blue = np.array([130,255,255])

lower_green = np.array([50,80,80])
upper_green = np.array([80,255,255])

lower_red = np.array([150,80,100])#np.array([153,100,100])
upper_red = np.array([180,255,255])#np.array([173,255,255])

RM = (320, 480)
red = (0, 0, 255)
blue = (255, 0 ,0)
green = (0, 255, 0)

def dist(p, q):
    return int(math.sqrt(sum((px - qx) ** 2 for px, qx in zip(p, q))))

def used_blue_ToComposeDistance(APPROX, LeftOrRight):
    if len(APPROX) == 3:    #640
        b1 = dist(APPROX[0][0], APPROX[1][0])
        b2 = dist(APPROX[1][0], APPROX[2][0])
        b3 = dist(APPROX[2][0], APPROX[0][0])
        b_max = max(b1, b2, b3)
        if b_max == b1:
            aB = tuple(APPROX[2][0])
        elif b_max == b2:
            aB = tuple(APPROX[0][0])
        elif b_max == b3:
            aB = tuple(APPROX[1][0])
        b11 = APPROX[0][0][1]
        b22 = APPROX[1][0][1]
        b33 = APPROX[2][0][1]
        b_min = max(b11, b22, b33)
        if b_min == b11:
            aBB = tuple(APPROX[0][0])
        elif b_min == b22:
            aBB = tuple(APPROX[1][0])
        elif b_min == b33:
            aBB = tuple(APPROX[2][0])

        #need to show on screen
        '''cv2.circle(res, aB, 2, (0, 0, 255), 3)
        cv2.circle(res, aBB, 2, (0, 0, 255), 3)
        yB = (aB[1] - aBB[1])/(aB[0] - aBB[0])*(LeftOrRight - aBB[0]) + aBB[1]
        xB = (aB[0] - aBB[0])/(aB[1] - aBB[1])*(480 - aBB[1]) + aBB[0]
        if 0 < yB < 480:
            yB = int(yB)
            cv2.circle(res, (LeftOrRight, yB), 2, (0, 0, 255), 3)
        elif 0 < xB < 640:
            xB = int(xB)
            cv2.circle(res, (xB, 480), 2, (0, 0, 255), 3)
        '''

        return aB, aBB
    else:
        return None, None

def pinout_con(pin):
    GS.interrupt(pin, 100)

    try:
        while True:
            if GPIO.event_detected(pin):
                GS.rm_interrupt(pin)
                break
            contour()

    finally:
        #cap.release()
        cv2.destroyAllWindows()
        GPIO.cleanup()
        GS.set()

def contour():
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

        realX = None

        if contours:	#blue
            area = 0
            cntrB = contours[0]
            for cntr in contours:
                areaP = area
                area = cv2.contourArea(cntr)
                if area >= areaP:
                    cntrB_ = cntrB
                    cntrB = cntr
            epsilon = 0.07 * cv2.arcLength(cntrB, True)
            approx = cv2.approxPolyDP(cntrB, epsilon, True)         #right
            cv2.drawContours(res, [approx], -1, blue, 3)                
            epsilon_ = 0.07 * cv2.arcLength(cntrB_, True)       
            approx_ = cv2.approxPolyDP(cntrB_, epsilon_, True)      #left     
            cv2.drawContours(res, [approx_], -1, blue, 3)
          
            aB, aBB = used_blue_ToComposeDistance(approx, 0)
            aB_, aBB_ = used_blue_ToComposeDistance(approx_, 640)

            #Two half circle on the front
            if all([len(approx) == 3, len(approx_) == 3]):
                Cxy = np.array([[aBB[1]-aB[1], aB[0]-aBB[0]], [aBB_[1]-aB_[1], aB_[0]-aBB_[0]]])
                Cv = np.array([aBB[1]*(aB[0]-aBB[0])-aBB[0]*(aB[1]-aBB[1]), \
                        aBB_[1]*(aB_[0]-aBB_[0])-aBB_[0]*(aB_[1]-aBB_[1])])
                #print(Cxy[0], Cxy[1],Cv)
                if all([Cxy[0][1]/Cxy[0][0] != Cxy[1][1]/Cxy[1][0], \
                        not np.array_equal(Cxy[0], [0, 0]), \
                        not np.array_equal(Cxy[1], [0, 0])]):       #vanishing point
                    Cpoint = np.linalg.solve(Cxy, Cv)
                    #print(Cpoint)

                    #need to show on screen
                    '''if all([0 < Cpoint[0] < 640, 0 < Cpoint[1] < 480]): 
                        Cpoint = int(Cpoint[0]), int(Cpoint[1])
                        Cpoint = tuple(Cpoint)
                        cv2.circle(res, Cpoint, 2, (0, 0, 255), 10)
                    '''
                    Mxy = np.array([[aB_[1]-aB[1], aB[0]-aB_[0]],[Cpoint[1]-RM[1], RM[0]-Cpoint[0]]])
                    Mv = np.array([aB_[1]*(aB[0]-aB_[0])-aB_[0]*(aB[1]-aB_[1]), \
                            Cpoint[1]*(RM[0]-Cpoint[0])-Cpoint[0]*(RM[1]-Cpoint[1])])
                    #print(Mxy[0], Mxy[1], Mv)
                    if all([Mxy[0][1]/Mxy[0][0] != Mxy[1][1]/Mxy[1][0], \
                            not np.array_equal(Mxy[0], [0, 0]), \
                            not np.array_equal(Mxy[1], [0, 0])]): #point of robot between vanishing point
                        Mpoint = np.linalg.solve(Mxy, Mv)
                        #print(Mpoint)
                        aBMdiv2 = dist(aB, aB_)/2
                        n = dist(aB, tuple(Mpoint))
                        m = dist(aB_, tuple(Mpoint))
                        realdist = abs(1200 - 2400*(n/(n+m)))
                        l = dist(tuple(Mpoint), (320, 480))
                        if aBMdiv2 == n:
                            realX = l*2400/n
                        else:
                            realX = (l*realdist)/abs(aBMdiv2-n)
                        #print(realX)

                        #need to show on screen
                        '''if all([0 < Mpoint[0] < 640, 0 < Mpoint[1] < 480]):
                            Mpoint = int(Mpoint[0]), int(Mpoint[1])
                            Mpoint = tuple(Mpoint)
                            cv2.circle(res, Mpoint, 2, (0, 0, 255), 10)
                        '''
            #One half circle on the front
            #if approx_  

        if contours1:	#green
            area1 = 0
            for cntr1 in contours1:
                areaP1 = area1
                area1 = cv2.contourArea(cntr1)
                if area1 >= areaP1:
                    cntrB1 = cntr1
            epsilon1 = 0.07 * cv2.arcLength(cntrB1, True)               #
            approx1 = cv2.approxPolyDP(cntrB1, epsilon1, True)          #
            green_mean = cv2.moments(cntrB1)
            cv2.drawContours(res1, [approx1], -1, green, 3)       #
            if green_mean:
                cx = int(green_mean['m10']/green_mean['m00'])
                cy = int(green_mean['m01']/green_mean['m00'])           #
                cv2.circle(res1, (cx, cy), 2, green, 3)           #
        if contours2:	#red
            area2 = 0
            for cntr2 in contours2:
                areaP2 = area2
                area2 = cv2.contourArea(cntr2)
                if area2 >= areaP2:
                    cntrB2 = cntr2
            epsilon2 = 0.07 * cv2.arcLength(cntrB2, True)
            approx2 = cv2.approxPolyDP(cntrB2, epsilon2, True)
            cv2.drawContours(res2, [approx2], -1, red, 3)

        cv2.imshow('Blue', res)
        cv2.imshow('Green', res1)
        cv2.imshow('Red', res2)
        '''if contour:
            print("============================")
            #print(yB)
            #print(aBB)
        '''
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            cap.release()
            cv2.destroyAllWindows()

        return realX

if __name__ == '__main__':
    while True:
        contour()

