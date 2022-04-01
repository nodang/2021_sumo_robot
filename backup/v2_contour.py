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

lower_red = np.array([153,100,100])
upper_red = np.array([173,255,255])

RM = (320, 480)

def dist(p, q):
    return int(math.sqrt(sum((px - qx) ** 2 for px, qx in zip(p, q))))

def used_blue_ToComposeDistance(APPROX, LeftOrRight):
    a=0

def pinout_con(pin):
    GS.interrupt(pin, 100)

    try:
        while True:
            if GPIO.event_detected(pin):
                GS.rm_interrupt(pin)
                break
            contour()

            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
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
            cv2.drawContours(res, [approx], -1, (255, 0, 0), 3)                
            approx_ = cv2.approxPolyDP(cntrB_, epsilon_, True)      #left      
            epsilon_ = 0.07 * cv2.arcLength(cntrB_, True)
            cv2.drawContours(res, [approx_], -1, (255, 0, 0), 3)
            
            if len(approx) == 3:    #640
                b1 = dist(approx[0][0], approx[1][0])
                b2 = dist(approx[1][0], approx[2][0])
                b3 = dist(approx[2][0], approx[0][0])
                b_max = max(b1, b2, b3)
                if b_max == b1:
                    aB = tuple(approx[2][0])
                elif b_max == b2:
                    aB = tuple(approx[0][0])
                elif b_max == b3:
                    aB = tuple(approx[1][0])
                b11 = approx[0][0][1]
                b22 = approx[1][0][1]
                b33 = approx[2][0][1]
                b_min = max(b11, b22, b33)
                if b_min == b11:
                    aBB = tuple(approx[0][0])
                elif b_min == b22:
                    aBB = tuple(approx[1][0])
                elif b_min == b33:
                    aBB = tuple(approx[2][0])

                #need to show on screen
                '''cv2.circle(res, aB, 2, (0, 0, 255), 3)
                cv2.circle(res, aBB, 2, (0, 0, 255), 3)
                yB = (aB[1] - aBB[1])/(aB[0] - aBB[0])*(0 - aBB[0]) + aBB[1]
                xB = (aB[0] - aBB[0])/(aB[1] - aBB[1])*(480 - aBB[1]) + aBB[0]
                if 0 < yB < 480:
                    yB = int(yB)
                    cv2.circle(res, (0, yB), 2, (0, 0, 255), 3)
                elif 0 < xB < 640:
                    xB = int(xB)
                    cv2.circle(res, (xB, 480), 2, (0, 0, 255), 3)
                '''
            if len(approx_) == 3:   #0
                b1_ = dist(approx_[0][0], approx_[1][0])
                b2_ = dist(approx_[1][0], approx_[2][0])
                b3_ = dist(approx_[2][0], approx_[0][0])
                b_max_ = max(b1_, b2_, b3_)
                if b_max_ == b1_:
                    aB_ = tuple(approx_[2][0])
                elif b_max_ == b2_:
                    aB_ = tuple(approx_[0][0])
                elif b_max_ == b3_:
                    aB_ = tuple(approx_[1][0])
                b11_ = approx_[0][0][1]
                b22_ = approx_[1][0][1]
                b33_ = approx_[2][0][1]
                b_min_ = max(b11_, b22_, b33_)
                if b_min_ == b11_:
                    aBB_ = tuple(approx_[0][0])
                elif b_min_ == b22_:
                    aBB_ = tuple(approx_[1][0])
                elif b_min_ == b33_:
                    aBB_ = tuple(approx_[2][0])
                
                #need to show on screen
                '''cv2.circle(res, aB_, 2, (0, 0, 255), 3)
                cv2.circle(res, aBB_, 2, (0, 0, 255), 3)
                yB_ = (aB_[1] - aBB_[1])/(aB_[0] - aBB_[0])*(640 - aBB_[0]) + aBB_[1]
                xB_ = (aB_[0] - aBB_[0])/(aB_[1] - aBB_[1])*(480 - aBB_[1]) + aBB_[0]
                if 0 < yB_ < 480:
                    yB_ = int(yB_)
                    cv2.circle(res, (640, yB_), 2, (0, 255, 0), 3)
                elif 0 < xB_ < 640:
                    xB_ = int(xB_)
                    cv2.circle(res, (xB_, 480), 2, (0, 255, 0), 3)
                '''
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
                        print(realX)

                        #need to show on screen
                        '''if all([0 < Mpoint[0] < 640, 0 < Mpoint[1] < 480]):
                            Mpoint = int(Mpoint[0]), int(Mpoint[1])
                            Mpoint = tuple(Mpoint)
                            cv2.circle(res, Mpoint, 2, (0, 0, 255), 10)
                        '''
            #One half circle on the front
            if approx_  

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
            cv2.drawContours(res1, [approx1], -1, (0, 255, 0), 3)       #
            if green_mean:
                cx = int(green_mean['m10']/green_mean['m00'])
                cy = int(green_mean['m01']/green_mean['m00'])           #
                cv2.circle(res1, (cx, cy), 2, (0, 255, 0), 3)           #
        if contours2:	#red
            area2 = 0
            for cntr2 in contours2:
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
        if contour:
            print("============================")
            #print(yB)
            #print(aBB)

if __name__ == '__main__':
    while True:
        contour()
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cap.release() 
    cv2.destroyAllWindows()

