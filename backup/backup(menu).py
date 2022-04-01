import RPi.GPIO as GPIO
import time
import test7_led as tl
import GPIOset as GS
from GPIOset import swU, swD, swL, swR, push

GS.set()
GS.sw_interrupt(50)

try:
    while 1:
	if GPIO.event_detected(swU):
	    print("up")
	elif GPIO.event_detected(swD):
	    print("down")
	elif GPIO.event_detected(swR):
	    print("right")
	elif GPIO.event_detected(swL):
	    print("left")
	elif GPIO.event_detected(push):
	    print("push")
	    GS.rm_interrupt(swU)
	    tl.led_on(swU)
	    GS.sw_interrupt(50)

	print("TOP MENU")
	time.sleep(1)

finally:
     GPIO.cleanup()

