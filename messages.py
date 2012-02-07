
import libtcodpy as libtcod
from flair import *


class Messages:
    def __init__(self):
        self.strings = []

    def draw(self, x, y, w, turn):
        l = []
        for v,m,z in self.strings[:3]:
            if z[0] is None or z[0] >= turn:
                l.append('%c%s' % (v or libtcod.COLCTRL_1, m))
                z[0] = turn
            else:
                l.append('%c%s' % (libtcod.COLCTRL_5, m))

        libtcod.console_print_rect(None, x, y, w, 3, '\n'.join(l))

    def m(self, s, bold = None):
        if len(self.strings) > 0 and s == self.strings[0][1]:
            self.strings[0][2][0] = None
            return

        if bold:
            self.strings.insert(0, (libtcod.COLCTRL_3, s, [None]))
        else:
            self.strings.insert(0, (None, s, [None]))
        if len(self.strings) > 25:
            self.strings.pop()

    def show_all(self):
        l = []
        for v,m,z in self.strings[:24]:
            if v:
                l.append('%c%s' % (v,m))
            elif len(l) == 0:
                l.append('%c%s' % (libtcod.COLCTRL_1, m))
            else:
                l.append('%c%s' % (libtcod.COLCTRL_5, m))
        draw_window(l)

