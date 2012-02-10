
import libtcodpy as libtcod

class Stat:
    def __init__(self):
        self.x = 3.0
        self.reason = None

    def dec(self, dx, reason=None, sound=None):
        if reason and self.x > -3.0:
            self.reason = reason
        self.x -= dx
        if self.x <= -3.0: self.x = -3.0

        if sound:
            sound.play("windnoise", dur=max(dx, 0.1))

    def inc(self, dx):
        self.x += dx
        if self.x > 3.0: self.x = 3.0

class Stats:
    def __init__(self):
        self.health = Stat()
        self.sleep = Stat()
        self.tired = Stat()
        self.hunger = Stat()
        self.thirst = Stat()
        self.warmth = Stat()

    def draw(self, x, y, grace=None, resource=None, luck=None):
        s = "%cHealth: %c%s\n" \
            "%cWarmth: %c%s\n" \
            "%c Tired: %c%s\n" \
            "%c Sleep: %c%s\n" \
            "%cThirst: %c%s\n" \
            "%cHunger: %c%s\n"

        if grace:
            s += "%c%cGrace: %c%s\n" % \
                (libtcod.COLCTRL_1, grace[0],
                 libtcod.COLCTRL_4 if grace[2] else libtcod.COLCTRL_3,
                 chr(175) * min(grace[1], 6))

        if resource:
            rdefs = {'r': ("   Red", libtcod.red),
                     'g': (" Green", libtcod.dark_green),
                     'y': ("Yellow", libtcod.yellow),
                     'b': ("  Blue", libtcod.blue),
                     'p': ("Purple", libtcod.purple) }

            ss, col = rdefs[resource[0]]
            col2 = (col if resource[2] else libtcod.white) 
            col = (max(col.r,1),max(col.g,1),max(col.b,1))
            col2 = (max(col2.r,1),max(col2.g,1),max(col2.b,1))
            s += "%c%c%c%c%s: %c%c%c%c%s\n" % \
                (libtcod.COLCTRL_FORE_RGB, col[0], col[1], col[2], ss,
                 libtcod.COLCTRL_FORE_RGB, col2[0], col2[1], col2[2],
                 chr(175) * min(resource[1], 6))

        if luck:
            luck = max(-3, min(3, luck))
            if luck < 0:
                l = abs(luck)
                s += "%c  Luck: %c%s%s\n" % \
                    (libtcod.COLCTRL_1, libtcod.COLCTRL_4, (3 - l) * ' ', l * chr(18))
            else:
                s += "%c  Luck: %c   %s\n" % \
                    (libtcod.COLCTRL_1, libtcod.COLCTRL_3, luck * chr(17))


        def pr(x):
            if x >= 2.0: return    '   +++'
            elif x >= 1.0: return  '   ++'
            elif x >= 0.0: return  '   +'
            elif x >= -1.0: return '  -'
            elif x >= -2.0: return ' --'
            else: return           '---'

        def cl(x):
            if x >= 1.5: return libtcod.COLCTRL_2
            elif x >= -0.5: return libtcod.COLCTRL_3
            else: return libtcod.COLCTRL_4

        h = self.health.x
        d = self.warmth.x
        t = self.tired.x
        e = self.sleep.x
        i = self.thirst.x
        u = self.hunger.x

        q = (libtcod.COLCTRL_1, cl(h), pr(h),
             libtcod.COLCTRL_1, cl(d), pr(d),
             libtcod.COLCTRL_1, cl(t), pr(t),
             libtcod.COLCTRL_1, cl(e), pr(e),
             libtcod.COLCTRL_1, cl(i), pr(i),
             libtcod.COLCTRL_1, cl(u), pr(u))

        libtcod.console_print(None, x, y, s % q)

