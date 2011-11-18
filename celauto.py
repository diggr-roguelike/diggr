import libtcodpy as libtcod

#
# Swamp gas: 
#  lose small amount of thirst/hunger
#  lights all squares, even not in LOS
#  explodes via chain reaction
#
# the black rot:
#  like Ebola, but less permanent
#
# black mold:
#  monster that doesn't move, but spawns and occasionally releases black rot
#


class CelAuto:
    def __init__(self, color=libtcod.light_blue,
                 rule="345/26/5", featuretoggle=None,
                 watertoggle=None,
                 pic=None, anchor=(0,0)):
        self.color = color
        self.featuretoggle = featuretoggle
        self.watertoggle = watertoggle
        self.pic = pic
        self.anchor = anchor

        rule = rule.split('/')
        self.rule = (set(int(x) for x in rule[0]), 
                     set(int(x) for x in rule[1]),
                     int(rule[2]))


class CelAutoStock:
    def __init__(self):

        self.ebola = CelAuto(rule="345/26/5", color=None, featuretoggle='e',
                             pic=["..",".."])

        self.smokecloud = CelAuto(rule="0345/26/6", color=None,
                                  featuretoggle='f',
                                  pic=["..",".."])

        self.trapmaker = CelAuto(rule="13458/38/6", color=None,
                                 featuretoggle='^',
                                 pic=[" . ",
                                      "...",
                                      " . "])

        self.swampgas = CelAuto(rule="23/24/32", color=None,
                                featuretoggle='&',
                                pic=["..",".."])

        self.bmold = CelAuto(rule="3456/2/6", color=None,
                             featuretoggle='g', pic=["."])


    def paste(self, camap, x, y, w, h, ca):

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

                camap[(x1, y1)] = (ca, 0)


    def celauto_step(self, camap, w, h, funcon, funcoff):

        # See:
        # http://www.mirekw.com/ca/rullex_gene.html

        ret = {}

        que = {}
        dead = {}

        def find_n(x, y, ca, f=None):
            n = 0

            for xi in xrange(-1, 2):
                for yi in xrange(-1, 2):
                    if xi == 0 and yi == 0:
                        continue

                    ki = (x+xi, y+yi)

                    if ki[0] < 0 or ki[0] >= w or ki[1] < 0 or ki[1] >= h:
                        continue

                    if ki in camap and camap[ki][0] == ca and camap[ki][1] == 0:
                        n += 1

                    if f:
                        f(ki, ca)

            return n

        def fque(ki, ca):
            if ki not in camap:
                que[ki] = ca


        for k,v in sorted(camap.iteritems()):

            x,y = k
            ca,state = v

            # check if we are dead
            if state > 0:
                if state < ca.rule[2] - 1:
                    ret[k] = (ca, state + 1)
                else:
                    dead[k] = ca

            else:
                # check if we survive
                n = find_n(x, y, ca, f=fque)

                if n not in ca.rule[0]:
                    ret[k] = (ca, state + 1)
                else:
                    ret[k] = v

        # check for newborn cells
        for k,ca in sorted(que.iteritems()):
            x,y = k
            n = find_n(x, y, ca)

            if n in ca.rule[1]:
                ret[k] = (ca, 0)
                funcon(x, y, ca)

        # leave remains of dead cells
        for k,ca in sorted(dead.iteritems()):
            x,y = k
            funcoff(x, y, ca)

        return ret
