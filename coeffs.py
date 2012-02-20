
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

        ### The alignment bonus matrix.

        # Ex., for lg:
        # 
        #     l    n    c
        #  g   -- | -  | 0 
        #    -----+----+----  
        #  n   -  | 0  | +     
        #    -----+----+----
        #  e   0  | +  | ++ 
        # 

        # ng:
        #
        #     l    n    c
        #  g   -  | -- | - 
        #    -----+----+----  
        #  n   0  | 0  | 0     
        #    -----+----+----
        #  e   +  | ++ | +  

        # ln:
        #
        #     l    n    c
        #  g   -  | 0  | + 
        #    -----+----+----  
        #  n   -- | 0  | ++    
        #    -----+----+----
        #  e   -  | 0  | +  

        # nn:
        #
        #     l    n    c
        #  g   +  | -  | + 
        #    -----+----+----  
        #  n   -  | -- | -     
        #    -----+----+----
        #  e   +  | -  | +  



        self.alignbonus = {
            'lg': { 'lg': -0.5, 
                    'ng': -0.1,
                    'cg': 0,
                    'ln': -0.05,
                    'nn': 0,
                    'cn': +0.1,
                    'le': 0,
                    'ne': +0.2,
                    'ce': +0.35 },
            'ng': { 'lg': -0.05,
                    'ng': -0.5,
                    'cg': -0.05,
                    'ln': 0,
                    'nn': 0,
                    'cn': 0,
                    'le': +0.1,
                    'ne': +0.35,
                    'ce': +0.1 },
            'cg': { 'lg': 0,
                    'ng': -0.1,
                    'cg': -0.5,
                    'ln': +0.1,
                    'nn': 0,
                    'cn': -0.05,
                    'le': +0.35,
                    'ne': +0.2,
                    'ce': 0 },
            'ln': { 'lg': -0.05,
                    'ng': 0,
                    'cg': +0.1,
                    'ln': -0.5,
                    'nn': 0,
                    'cn': +0.35,
                    'le': -0.05,
                    'ne': 0,
                    'ce': +0.1 },
            'nn': { 'lg': +0.04,
                    'ng': -0.04,
                    'cg': +0.04,
                    'ln': -0.04,
                    'nn': -0.5,
                    'cn': -0.04,
                    'le': +0.04,
                    'ne': -0.04,
                    'ce': +0.04 },
            'cn': { 'lg': +0.1,
                    'ng': 0,
                    'cg': -0.05,
                    'ln': +0.35,
                    'nn': 0,
                    'cn': -0.5,
                    'le': +0.1,
                    'ne': 0,
                    'ce': -0.05 },
            'le': { 'lg': 0,
                    'ng': +0.2,
                    'cg': +0.35,
                    'ln': -0.05,
                    'nn': 0,
                    'cn': +0.1,
                    'le': -0.5,
                    'ne': -0.1,
                    'ce': 0 },
            'ne': { 'lg': +0.1,
                    'ng': +0.35,
                    'cg': +0.1,
                    'ln': 0,
                    'nn': 0,
                    'cn': 0,
                    'le': -0.05,
                    'ne': -0.5,
                    'ce': -0.05 },
            'ce': { 'lg': +0.35, 
                    'ng': +0.2,
                    'cg': 0,
                    'ln': +0.1,
                    'nn': 0,
                    'cn': -0.05,
                    'le': 0,
                    'ne': -0.1,
                    'ce': -0.5 }
            }


     
