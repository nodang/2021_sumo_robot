from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=32, rotate=0)

def text(word,width,height):
    with canvas(device) as draw:
        c = word.count('\\')
        #draw.rectangle(device.bounding_box, outline="white", fill="black")
        if c == 0:
            pos = len(word)
            draw.text((width-pos*3, height), word, fill="white")
        elif c == 1:
            s = word.find('\\')
            w1 = word[:s]
            w2 = word[s+c:]
            pos1 = len(w1)
            pos2 = len(w2)
            draw.text((width-pos1*3, 0), w1, fill="white")
            draw.text((width-pos2*3, height), w2, fill="white")     
        else:
            draw.text((width-len('Word Error')*3, height), 'Word Error', fill="white")
