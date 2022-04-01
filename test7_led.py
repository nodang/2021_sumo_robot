import RPi.GPIO as GPIO
import time
import GPIOset as GS

def led_on(pin):
    GS.interrupt(pin, 50)

    try:
        while 1:
            if GPIO.event_detected(pin):
                GS.rm_interrupt(pin)
                return 0
            GPIO.output(26, False)
            time.sleep(1)
            GPIO.output(26, True)
            time.sleep(1)
    finally:
        GPIO.cleanup()
        GS.set()
        print("LED OUT")

if __name__ == '__main__':
    GS.set()
    led_on(17)
