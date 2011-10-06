import libtcodpy as libtcod

class Feature:
    def __init__(self, walkable=False, visible=False, skin=('=', libtcod.white),
                 name="something strange", stairs=False, sticky=False, water=None,
                 s_shrine=False, b_shrine=False, v_shrine=False, height=-10,
                 shootable=False, warm=False, branch=None, healingfountain=False,
                 nofeature=False, poison=None, confuse=False, back=None):
        self.walkable = walkable
        self.visible = visible
        self.water = water
        self.skin = skin
        self.stairs = stairs
        self.name = name
        self.sticky = sticky
        self.s_shrine = s_shrine
        self.b_shrine = b_shrine
        self.v_shrine = v_shrine
        self.height = height
        self.shootable = shootable
        self.warm = warm
        self.branch = branch
        self.healingfountain = healingfountain
        self.nofeature = nofeature
        self.poison = poison
        self.confuse = confuse
        self.back = back


class FeatureStock:
    def __init__(self):
        self.f = {}

        self.f['>'] = Feature(walkable=True, visible=True, skin=('>', libtcod.white),
                              stairs=1, name='a hole in the floor')

        self.f['1'] = Feature(walkable=True, visible=True, skin=('>', libtcod.lime),
                              stairs=1, name='a hole in the floor', branch='a')

        self.f['2'] = Feature(walkable=True, visible=True, skin=('>', libtcod.crimson),
                              stairs=1, name='a hole in the floor', branch='b')

        self.f['3'] = Feature(walkable=True, visible=True, skin=('>', libtcod.sky),
                              stairs=1, name='a hole in the floor', branch='c')

        self.f['4'] = Feature(walkable=True, visible=True, skin=('>', libtcod.dark_gray),
                              stairs=1, name='a hole in the floor', branch='d')

        self.f['5'] = Feature(walkable=True, visible=True, skin=('>', libtcod.light_gray),
                              stairs=1, name='a hole in the floor', branch='e')

        self.f['*'] = Feature(walkable=True, visible=False, skin=('*', libtcod.lightest_green),
                              name='rubble')

        self.f['^'] = Feature(walkable=True, visible=True, skin=(250, libtcod.red),
                              sticky=True, name='a cave floor covered with glue')

        self.f['s'] = Feature(walkable=True, visible=True, skin=(234,  libtcod.darker_grey),
                              s_shrine=True, name='a shrine to Shiva')

        self.f['b'] = Feature(walkable=True, visible=True, skin=(127, libtcod.white),
                              b_shrine=True, name='a shrine to Brahma')

        self.f['v'] = Feature(walkable=True, visible=True, skin=(233, libtcod.azure),
                              v_shrine=True, name='a shrine to Vishnu')

        self.f[':'] = Feature(walkable=False, visible=False, skin=(9, libtcod.white),
                              name='a column', height=0)

        self.f['h'] = Feature(walkable=True, visible=True, skin=(242, libtcod.white),
                              stairs=6, name='a dropchute')

        self.f['a'] = Feature(walkable=True, visible=True, skin=(254, libtcod.green),
                              name='an abandoned altar stone')

        self.f['@'] = Feature(walkable=True, visible=True, skin=(15, libtcod.yellow),
                              name='a hearth', warm=True)

        self.f['$'] = Feature(walkable=True, visible=True, skin=(20, libtcod.light_sky),
                              name='a Fountain of Youth', healingfountain=True)


        self.f['='] = Feature(walkable=False, visible=True, skin=(196, libtcod.gray),
                              name='barricades', shootable=True)
        self.f['l'] = Feature(walkable=False, visible=True, skin=(179, libtcod.gray),
                              name='barricades', shootable=True)
        self.f['r'] = Feature(walkable=False, visible=True, skin=(218, libtcod.gray),
                              name='barricades', shootable=True)
        self.f['q'] = Feature(walkable=False, visible=True, skin=(191, libtcod.gray),
                              name='barricades', shootable=True)
        self.f['p'] = Feature(walkable=False, visible=True, skin=(192, libtcod.gray),
                              name='barricades', shootable=True)
        self.f['d'] = Feature(walkable=False, visible=True, skin=(217, libtcod.gray),
                              name='barricades', shootable=True)


        self.f['|'] = Feature(walkable=False, visible=False, skin=(186, libtcod.white),
                              name='a smooth stone wall', height=0)
        self.f['-'] = Feature(walkable=False, visible=False, skin=(205, libtcod.white),
                              name='a smooth stone wall', height=0)
        self.f['+'] = Feature(walkable=False, visible=False, skin=(206, libtcod.white),
                              name='a smooth stone wall', height=0)
        self.f['R'] = Feature(walkable=False, visible=False, skin=(201, libtcod.white),
                              name='a smooth stone wall', height=0)
        self.f['L'] = Feature(walkable=False, visible=False, skin=(200, libtcod.white),
                              name='a smooth stone wall', height=0)
        self.f['T'] = Feature(walkable=False, visible=False, skin=(203, libtcod.white),
                              name='a smooth stone wall', height=0)
        self.f['F'] = Feature(walkable=False, visible=False, skin=(204, libtcod.white),
                              name='a smooth stone wall', height=0)
        self.f['J'] = Feature(walkable=False, visible=False, skin=(202, libtcod.white),
                              name='a smooth stone wall', height=0)
        self.f['7'] = Feature(walkable=False, visible=False, skin=(187, libtcod.white),
                              name='a smooth stone wall', height=0)
        self.f['/'] = Feature(walkable=False, visible=False, skin=(188, libtcod.white),
                              name='a smooth stone wall', height=0)
        self.f['Z'] = Feature(walkable=False, visible=False, skin=(185, libtcod.white),
                              name='a smooth stone wall', height=0)

        self.f['Y'] = Feature(walkable=False, visible=False, skin=(157, libtcod.green),
                              name='a tree', height=5)
        self.f['!'] = Feature(walkable=True, visible=False, skin=(173, libtcod.dark_green),
                              name='a giant fern')

        self.f['w'] = Feature(walkable=True, visible=True, skin=('-', libtcod.sky),
                              water=True, name='a pool of water')

        self.f['W'] = Feature(walkable=True, visible=True, nofeature=True, 
                              water=True)

        self.f['.'] = Feature(walkable=True, visible=True, nofeature=True, 
                              water=False)

        self.f['e'] = Feature(walkable=True, visible=True, skin=None, back=libtcod.darkest_green,
                              poison=0.5, name='a cloud of Ebola virus')

        self.f['f'] = Feature(walkable=True, visible=True, skin=None, back=libtcod.dark_gray,
                              confuse=True, name='confusing smoke')
