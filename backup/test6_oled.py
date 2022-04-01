from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=32, rotate=0)

with canvas(device) as draw:
    #draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((0, 0), "Hello World!", fill="white")
while 1:
    time.sleep(1)
