
import math

def xy_dist(xy1, xy2):
    return math.sqrt(math.pow(abs(xy1[0] - xy2[0]), 2) + 
                     math.pow(abs(xy1[1] - xy2[1]), 2))

def xy_add(xy1, xy2):
    return (xy1[0] + xy2[0],
            xy1[1] + xy2[1])

def xy_sub(xy1, xy2):
    return (xy1[0] - xy2[0],
            xy1[1] - xy2[1])

def xy_none(xy):
    return xy[0] is None or xy[1] is None

def xy_outside(xy, xy0, a, b, c, d):
    return xy[0] < a or xy[1] < b or xy[0] + xy0[0] >= c or xy[1] + xy0[1] >= d

def xy_out_wh(xy, w, h):
    return xy[0] < 0 or xy[1] < 0 or xy[0] >= w or xy[1] >= h
