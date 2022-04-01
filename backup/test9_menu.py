import RPi.GPIO as GPIO
import time
import test7_led as tl
import GPIOset as GS
from GPIOset import swU, swD, swL, swR, push

import oled as le
from oled import device

import v3_contour as ct
from v3_contour import pinout_con

def setting():
    GS.set()

    global ow, oh, isr, mp, max_mp, mm
    ow = 63	#oled width #mid : 64
    oh = 16	#oled height
    isr = 100

    mp = [0,0]	#menu position [x, y]
    max_mp = [1,1]

    mm = [  [led, con],
            [led, con]  ]

    GS.sw_interrupt(isr)


def menu(sw):
    if sw == swU:
        if mp[0] < max_mp[0]:
            mp[0] += 1
    elif sw == swD:
        if mp[0] > 0:
            mp[0] -= 1
    elif sw == swL:
        if mp[1] > 0:
            mp[1] -= 1
    elif sw == swR:
        if mp[1] < max_mp[1]:
            mp[1] += 1
    elif sw == push:
        mm[mp[0]][mp[1]](swU)

    le.text("%s" %mm[mp[0]][mp[1]].__name__,ow,oh)


def led(pin):
    GS.rm_interrupt(swU)
    tl.led_on(swU)
    GS.sw_interrupt(isr)

def con(pin):
        GS.rm_interrupt(swU)
        ct.pinout_con(swU)
        GS.sw_interrupt(isr)

def main():
    try:
        while 1:
            if GPIO.event_detected(swU):
                print("up")
                menu(swU)
                print(mp)
            elif GPIO.event_detected(swD):
                print("down")
                menu(swD)
                print(mp)
            elif GPIO.event_detected(swR):
                print("right")
                menu(swR)
                print(mp)
            elif GPIO.event_detected(swL):
                print("left")
                menu(swL)
                print(mp)
            elif GPIO.event_detected(push):
                print("push")
                menu(push)

            print("TOP MENU")
            time.sleep(1)

    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    setting()
    main()

