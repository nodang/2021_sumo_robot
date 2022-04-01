import cv2
import numpy as np
import math

import v3_contour as ctr
import map_matrix as mp
from map_matrix import map_sumo

origin_map = map_sumo

def mapping():
    d = ctr.contour()
    if d == None:
        d = None
    else:
        dist = d
        print("dist : %d mm" %dist)
    print(map_sumo)


if __name__ == '__main__':
    while True:
        mapping()


