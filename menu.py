import RPi.GPIO as GPIO
import time
import os
import socket
import numpy as np

import test7_led as tl

import GPIOset as GS
from GPIOset import swU, swD, swL, swR, push

import oled as le
from oled import device

#import v3_contour as ct
#from v3_contour import pinout_con

import Contour as contour

def setting():
    GS.set()

    global ow, oh, isr, mp, max_mp, mm
    ow = 63	#oled width #mid : 64
    oh = 16	#oled height
    isr = 100

    mp = [0,0]	#menu position [x, y]
    max_mp = [1,1]

    mm = [  [race, config],
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
        GS.interrupt(push,isr)
        while True:
            if GPIO.event_detected(push):
                time.sleep(1)
                GS.rm_interrupt(push)
                GS.sw_interrupt(isr)
                break
    le.text("%s" %mm[mp[0]][mp[1]].__name__,ow,oh)

def led(pin):
    GS.rm_interrupt_all()
    tl.led_on(swU)
    le.text("led out",ow,oh)

def con(pin):
    GS.rm_interrupt_all()
    contour.contours.pinout_con(swU)
    le.text("contour out",ow,oh)

def config(pin):
    try:
        IP_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        IP_sock.connect(("8.8.8.8",80))
        IP = IP_sock.getsockname()[0]
        le.text(IP,ow,oh)
        print(IP)
    except OSError:
        le.text("Wifi Not Connect\\Reconnect : PUSH",ow,oh)
        while True:
            if GPIO.event_detected(push):
                os.system('sudo rfkill unblock wifi')
                os.system('wpa_cli -i wlan0 reconfigure')
                T = True
                break
            if GPIO.event_detected(pin):
                T = False
                break
        while T:
            for i in range(1,15):
                time.sleep(1)
                le.text("Waiting 15sec\\%d" %i,ow,oh)
                ping = os.system("ping -c 1 "+'8.8.8.8')
                if GPIO.event_detected(pin):
                    le.text("Wifi Connect Cancel",ow,oh)
                    T = False
                    break
                if ping == 0:            
                    IP_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                    IP_sock.connect(("8.8.8.8",80))
                    IP = IP_sock.getsockname()[0]
                    le.text("Wifi Connect Success\\"+IP,ow,oh)
                    print(IP)
                    T = False
                    break

    except:
        le.text("Unknown Error",ow,oh)
        while True:
            if GPIO.event_detected(swU):
                break
    finally:
        GS.rm_interrupt_all()

def race(pin):
    GS.rm_interrupt_all()
    GS.interrupt(pin, 100)
    
    while True:
        if GPIO.event_detected(pin):
            break
        contour.compose()

    GS.rm_interrupt(pin)
    le.text("race out",ow,oh)


def main():
    for i in range(0,5):
        le.text("SUMO menu -ON-\\%d" %(5-i),ow,oh)
        time.sleep(1)   
    le.text("%s" %mm[mp[0]][mp[1]].__name__,ow,oh)
    try:
        while True:
            if GPIO.event_detected(swU):
                print("up")
                menu(swU)
                #print(mp)
            elif GPIO.event_detected(swD):
                print("down")
                menu(swD)
                #print(mp)
            elif GPIO.event_detected(swR):
                print("right")
                menu(swR)
                #print(mp)
            elif GPIO.event_detected(swL):
                print("left")
                menu(swL)
                #print(mp)
            elif GPIO.event_detected(push):
                print("push")
                menu(push)
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    setting()
    main()

