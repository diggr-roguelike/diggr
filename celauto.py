import libtcodpy as libtcod

import libdiggrpy as dg

#


class CelAuto:
    def __init__(self, color=libtcod.light_blue,
                 rule="345/26/5", featuretoggle=None,
                 watertoggle=None, floorfeaturetoggle=None, littoggle=None,
                 pic=None, anchor=(0,0)):
        self.color = color
        self.featuretoggle = featuretoggle
        self.watertoggle = watertoggle
        self.floorfeaturetoggle = floorfeaturetoggle
        self.pic = pic
        self.anchor = anchor
        self.littoggle = littoggle

        rule = rule.split('/')
        self.rule = (rule[0], rule[1], int(rule[2]))


class CelAutoStock:

    EBOLA     = 1
    SMOKE     = 2
    TRAPMAKER = 3
    SWAMPGAS  = 4
    MOLD      = 5
    FERN      = 6
    FIRE      = 7

    def __init__(self):

        self.stock = {
            self.EBOLA: CelAuto(rule="345/26/5", color=None, featuretoggle='e',
                                pic=["..",".."]),

            self.SMOKE: CelAuto(rule="0345/26/6", color=None,
                                featuretoggle='f',
                                pic=["..",".."]),

            self.TRAPMAKER: CelAuto(rule="13458/38/6", color=None,
                                    featuretoggle='^',
                                    pic=[" . ",
                                         "...",
                                         " . "]),

            self.SWAMPGAS: CelAuto(rule="23/24/32", color=None,
                                   featuretoggle='&', littoggle=True,
                                   pic=["..",".."]),

            self.MOLD: CelAuto(rule="3456/2/6", color=None,
                               featuretoggle='g', pic=["."]),

            self.FERN: CelAuto(rule="23/24/72", color=None,
                               floorfeaturetoggle='!f',
                               pic=["..",".."]),

            self.FIRE: CelAuto(rule="012/3/2", color=None,
                               featuretoggle='"', pic=["."])
            }

        for k,v in self.stock.iteritems():
            dg.celauto_make_rule(k, v.rule[0], v.rule[1], v.rule[2])


    def paste(self, xy, w, h, _ca):
        x, y = xy

        ca = self.stock[_ca]

        x -= ca.anchor[0]
        y -= ca.anchor[1]

        for yi in xrange(len(ca.pic)):
            for xi in xrange(len(ca.pic[yi])):
                if ca.pic[yi][xi] != '.':
                    continue
                
                x1 = x + xi
                y1 = y + yi

                if x1 < 0 or x1 >= w or y1 < 0 or y1 >= h:
                    continue

                dg.celauto_seed(x1, y1, _ca)

    def seed(self, x, y, ca):
        dg.celauto_seed(x, y, ca)

    def clear(self, x, y, funcoff):
        dg.celauto_clear(x, y, funcoff)

    def celauto_step(self, funcon, funcoff):
        dg.celauto_step(funcon, funcoff)
