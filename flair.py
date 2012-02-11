
import libtcodpy as libtcod
import libdiggrpy as dg
import dgsys

from xy import *

_kbdmap = {
    libtcod.KEY_LEFT: 'h',
    libtcod.KEY_RIGHT: 'l',
    libtcod.KEY_UP: 'k',
    libtcod.KEY_DOWN: 'j',
    libtcod.KEY_HOME: 'y',
    libtcod.KEY_PAGEUP: 'u',
    libtcod.KEY_END: 'b',
    libtcod.KEY_PAGEDOWN: 'n',
    libtcod.KEY_KP4: 'h',
    libtcod.KEY_KP6: 'l',
    libtcod.KEY_KP8: 'k',
    libtcod.KEY_KP2: 'j',
    libtcod.KEY_KP7: 'y',
    libtcod.KEY_KP9: 'u',
    libtcod.KEY_KP1: 'b',
    libtcod.KEY_KP3: 'n'
}

def draw_window(msg, do_mapping=False):

    vk,c = dg.render_draw_window(msg)

    if do_mapping:
        if vk in _kbdmap: return _kbdmap[vk]

    return c


def draw_blast(xy, w, h, r, func):
    x, y = xy

    x0 = min(x - r, 0)
    y0 = min(y - r, 0)
    x1 = max(x + r + 1, w)
    y1 = max(y + r + 1, h)
    c = []
    for xi in xrange(x0, x1):
        for yi in xrange(y0, y1):
            d = xy_dist(xy, (xi, yi))
            if d <= r and xi >= 0 and xi < w and yi >= 0 and yi < h:
                c.append((xi, yi))

    def dr():
        for c0 in c:
            libtcod.console_put_char_ex(None, c0[0], c0[1], '*', fore, back)
        libtcod.console_flush()
        libtcod.sys_sleep_milli(100)

    back = libtcod.darkest_red
    fore = libtcod.yellow
    dr()
    fore = libtcod.color_lerp(fore, back, 0.5)
    dr()
    fore = libtcod.color_lerp(fore, back, 0.5)
    dr()
    for c0 in c:
        func(c0)


def draw_blast2(xy, w, h, r, func1, func2, color=libtcod.light_azure):
    x,y = xy

    x0 = min(x - r, 0)
    y0 = min(y - r, 0)
    x1 = max(x + r + 1, w)
    y1 = max(y + r + 1, h)
    c = []
    for xi in xrange(x0, x1):
        for yi in xrange(y0, y1):
            d = xy_dist(xy, (xi, yi))
            if d <= r and xi >= 0 and xi < w and yi >= 0 and yi < h:
                if func1((xi, yi)):
                    c.append((xi, yi))

    def dr():
        for c0 in c:
            libtcod.console_put_char_ex(None, c0[0], c0[1], '*', fore, back)
        libtcod.console_flush()
        libtcod.sys_sleep_milli(100)

    if color is not None:
        back = libtcod.darkest_blue
        fore = color
        dr()
        fore = libtcod.color_lerp(fore, back, 0.5)
        dr()
        fore = libtcod.color_lerp(fore, back, 0.5)
        dr()

    for c0 in c:
        func2(c0)


def draw_floodfill(xy, w, h, func):

    procd = set()

    toproc = set()
    toproc.add(xy)

    while 1:
        x_, y_ = toproc.pop()

        for xi in xrange(x_-1, x_+2):
            for yi in xrange(y_-1, y_+2):

                if xi < 0 or yi < 0 or xi >= w or yi >= h:
                    continue

                xyi = (xi, yi)

                if xyi in procd:
                    continue

                procd.add(xyi)

                if func(xyi):
                    toproc.add(xyi)

        if len(toproc) == 0:
            break

    def dr():
        for c0 in procd:
            libtcod.console_put_char_ex(None, c0[0], c0[1], '*', fore, back)
        libtcod.console_flush()
        libtcod.sys_sleep_milli(100)

    back = libtcod.darkest_red
    fore = libtcod.yellow
    dr()
    fore = libtcod.color_lerp(fore, back, 0.5)
    dr()
    fore = libtcod.color_lerp(fore, back, 0.5)
    dr()
