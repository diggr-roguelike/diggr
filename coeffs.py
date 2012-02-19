
class Coeffs:
    def __init__(self):
        self.movetired = 0.01
        self.movesleep = 0.005
        self.movethirst = 0.005
        self.movehunger = 0.0005

        self.resttired = 0.03
        self.restsleep = 0.005
        self.restthirst = 0.005
        self.resthunger = 0.0005

        self.sleeptired = 0.06
        self.sleepsleep = 0.01
        self.sleepthirst = 0.005
        self.sleephunger = 0.0005

        self.sleeptime = (350, 50)
        self.quicksleeptime = (50, 10)
        self.waterpois = 0.425
        self.watercold = 0.03

        self.colddamage = 0.03
        self.thirstdamage = 0.02
        self.hungerdamage = 0.01
        self.healingsleep = 0.02

        self.unarmedattack = 0.1
        self.unarmeddefence = 0.0

        self.nummonsters = (8, 1)
        self.monlevel = 0.75
        self.numitems = (3, 1.5)
        self.itemlevel = 0.75

        self.boozestrength = (2, 0.5)
        self.coolingduration = (50, 5)

        self.glueduration = (10,1)
        self.gluedefencepenalty = 3

        self.shivadecstat = 3.5
        self.s_graceduration = 1000
        self.v_graceduration = 500
        self.b_graceduration = 1500

        self.s_praytimeout = 300
        self.v_praytimeout = 150

        self.raddamage = 3.0

        self.regeneration = 0.01
        self.green_attack = 12.0
        self.yellow_lightradius = 18
        self.purple_telerange = 12
        self.purple_camorange = 3

        self.moldchance = (1, 0)

        self.burnduration = 8
        self.burndamage = 0.76

        self.numfounts = (3, 1)

        self.resource_timeouts = {'r': 300,
                                  'g': 400,
                                  'y': 600,
                                  'b': 400,
                                  'p': 500}
