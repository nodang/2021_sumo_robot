#!/usr/bin/env python

import RPi.GPIO as GPIO
import GPIOset as GS
import v5_contour as contours
import sci

def compose():
    #WAY, BLUE, RED = contours.contour(1000.0)
    WAY = contours.contour(0.0, test=False)
    '''
    WAY = None, M, R, L + E
    BLUE = None, O, T
    RED = None, O

    PASS =  RT  RIGHT TURN
            RG  GO RIGHT
            LT  LEFT TURN
            LG  GO LEFT
            S   STAIGHT
            B   BACK
    '''
    
    '''
    if WAY == None:                     # No enemy
        if RED == 'O':                      # Red circle is showing on cam
            PASS = ''
        else:                               # no red circle
            if BLUE == 'O':                     # one blue half circle is showing on cam 
                PASS = 'RT'
            elif BLUE == 'T':                   # two blue half circle is showing on cam
                PASS = ''
            else:                               # no blue half circle
                PASS = '' 
    else:                               # Find enemy
        if WAY == WAY.find('E'):            # enemy is closing 
            PASS = ''
        elif WAY == WAY.find('R'):          # enemy is right
            PASS = ''
        elif WAY == WAY.find('L'):          # enemy is left
            PASS = ''
        else:                               # enemy is middle
            PASS = ''

    sci.write('fuck')
    print(WAY, BLUE, RED)
    '''
    if WAY == None:
        sci.write('N,N,N', test=False)
    else:
        sci.write(WAY, test=False)
    print(WAY)


if __name__ == '__main__':
    sci.write('N,N,N', test=False, START='N')
    while True:
        S = input('\nSTART(Y or N) :')
        if S == 'Y' or S == 'y':
            print('START now')
            break
        elif S == 'N' or S =='N':
            print('START yet')
        else:
            print('Worng Command')
    while True:
        compose()
