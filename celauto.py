import libtcodpy as libtcod

#


class CelAuto:
    def __init__(self, color=libtcod.light_blue,
                 rule="345/26/5", featuretoggle=None,
                 watertoggle=None, floorfeaturetoggle=None,
                 pic=None, anchor=(0,0)):
        self.color = color
        self.featuretoggle = featuretoggle
        self.watertoggle = watertoggle
        self.floorfeaturetoggle = floorfeaturetoggle
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


        self.ffern = CelAuto(rule="23/24/72", color=None,
                             floorfeaturetoggle='!f',
                             pic=["..",".."])

        self.nbors = None



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

    def seed(self, camap, x, y, ca):
        camap[(x,y)] = (ca, 0)

    def clear(self, camap, x, y, funcoff):
        if (x,y) in camap:
            funcoff(x, y, camap[(x,y)][0])
            del camap[(x,y)]

    def celauto_step(self, camap, neighbors, w, h, funcon, funcoff):

        # See:
        # http://www.mirekw.com/ca/rullex_gene.html

        ret = {}

        que = {}
        dead = {}

        def find_n(x, y, ca, fque=None):
            n = 0

            for ki in neighbors[(x,y)]:

                if ki in camap:
                    if camap[ki][0] == ca and camap[ki][1] == 0:
                        n += 1

                elif fque is not None:
                    fque[ki] = ca

            return n


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
                n = find_n(x, y, ca, fque=que)

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
