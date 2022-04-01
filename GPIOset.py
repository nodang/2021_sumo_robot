import RPi.GPIO as GPIO
import time

swU = 18
swD = 27
swR = 23
swL = 17
push = 22

def set():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(26, GPIO.OUT)
    GPIO.output(26, False)

    GPIO.setup(swU, GPIO.IN)
    GPIO.setup(swD, GPIO.IN)
    GPIO.setup(swR, GPIO.IN)
    GPIO.setup(swL, GPIO.IN)
    GPIO.setup(push, GPIO.IN)
    

def interrupt(pin,time):
    GPIO.add_event_detect(pin,
                GPIO.RISING,
                bouncetime=time)

def rm_interrupt(pin):
    GPIO.remove_event_detect(pin)

def rm_interrupt_all():
    GPIO.remove_event_detect(swU)
    GPIO.remove_event_detect(swD)
    GPIO.remove_event_detect(swR)
    GPIO.remove_event_detect(swL)
    GPIO.remove_event_detect(push)

def sw_interrupt(time):
    GPIO.add_event_detect(swU,
                GPIO.RISING,
                bouncetime=time)
    GPIO.add_event_detect(swD,
                GPIO.RISING,
                bouncetime=time)
    GPIO.add_event_detect(swR,
                GPIO.RISING,
                bouncetime=time)
    GPIO.add_event_detect(swL,
                GPIO.RISING,
                bouncetime=time)
    GPIO.add_event_detect(push,
                GPIO.RISING,
                bouncetime=time)

def event_bottom(pin):
    if GPIO.event_detected(pin):
        rm_interrupt(pin)
        return 0
    else:
        return 1

def event_top(pin, time, func):
    if GPIO.event_detected(pin):
        rm_interrupt(pin)
        func()
        interrupt(pin, time)

