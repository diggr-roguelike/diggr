
import math
import os
import libtcodpy as libtcod
import random
import copy


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
        self.waterpois = 1.5
        self.watercold = 0.03

        self.colddamage = 0.03
        self.thirstdamage = 0.02
        self.hungerdamage = 0.01

        self.unarmedattack = 0.1
        self.unarmeddefence = 0.0

        self.nummonsters = (5, 1)
        self.monlevel = 0.75
        self.numitems = (3, 1.5)
        self.itemlevel = 0.75

        self.boozestrength = (2, 0.5)
        self.coolingduration = (50, 5)


class Stat:
    def __init__(self):
        self.x = 3.0

    def dec(self, dx):
        self.x -= dx
        if self.x < -3.0: self.x = -3.0

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

        self.black = libtcod.Color(0, 0, 0)
        self.red = libtcod.Color(255, 0, 0)
        self.yellow = libtcod.Color(255, 255, 0)
        self.green = libtcod.Color(0, 128, 0)
        self.white = libtcod.Color(255, 255, 255)
        self.gray = libtcod.Color(128, 128, 128)
        libtcod.console_set_color_control(libtcod.COLCTRL_1, self.white, self.black)
        libtcod.console_set_color_control(libtcod.COLCTRL_2, self.green, self.black)
        libtcod.console_set_color_control(libtcod.COLCTRL_3, self.yellow, self.black)
        libtcod.console_set_color_control(libtcod.COLCTRL_4, self.red, self.black)
        libtcod.console_set_color_control(libtcod.COLCTRL_5, self.gray, self.black)

    def draw(self, x, y):
        s = "%cHealth: %c%s\n" \
            "%cWarmth: %c%s\n" \
            "%c Tired: %c%s\n" \
            "%c Sleep: %c%s\n" \
            "%cThirst: %c%s\n" \
            "%cHunger: %c%s\n"

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






def draw_window(msg, w, h, do_mapping=False):
    maxl = 0
    for x in msg:
        maxl = max(len(x), maxl)

    l = len(msg)
    s = '\n'.join(msg)
    s = ('%c' % libtcod.COLCTRL_1) + s

    x0 = max(w - maxl - 4, 0)
    y0 = min(l + 2, h)
    libtcod.console_set_default_background(None, libtcod.darkest_blue)
    libtcod.console_rect(None, x0, 0, w - x0, y0, True, libtcod.BKGND_SET)
    libtcod.console_print_rect(None, x0 + 2, 1, w - x0 - 2, y0 - 1, s)
    libtcod.console_set_default_background(None, libtcod.black)

    libtcod.console_flush()
    k = libtcod.console_wait_for_keypress(False)
    libtcod.console_rect(None, x0, 0, w - x0, y0, True)
    libtcod.console_flush()

    if do_mapping:
        if k.vk == libtcod.KEY_LEFT: return 'h'
        elif k.vk == libtcod.KEY_RIGHT: return 'l'
        elif k.vk == libtcod.KEY_UP: return 'k'
        elif k.vk == libtcod.KEY_DOWN: return 'j'

    return chr(k.c)

def draw_blast(x, y, w, h, r, func):
    x0 = min(x - r, 0)
    y0 = min(y - r, 0)
    x1 = max(x + r + 1, w)
    y1 = max(y + r + 1, h)
    c = []
    for xi in xrange(x0, x1):
        for yi in xrange(y0, y1):
            d = math.sqrt(math.pow(abs(yi - y),2) + math.pow(abs(xi - x),2))
            if d <= r:
                c.append((xi, yi))

    def dr():
        for c0 in c:
            libtcod.console_put_char_ex(None, c0[0], c0[1], '*', fore, back)
        libtcod.console_flush()
        libtcod.sys_sleep_milli(100)

    back = libtcod.Color(60, 0, 0)
    fore = libtcod.Color(255, 255, 0)
    dr()
    fore = libtcod.color_lerp(fore, back, 0.5)
    dr()
    fore = libtcod.color_lerp(fore, back, 0.5)
    dr()
    for c0 in c:
        func(c0[0], c0[1])



class Messages:
    def __init__(self):
        self.strings = []

    def draw(self, x, y, w):
        l = []
        for v,m in self.strings[:3]:
            if v:
                l.append('%c%s' % (v,m))
            elif len(l) == 0:
                l.append('%c%s' % (libtcod.COLCTRL_1, m))
            else:
                l.append('%c%s' % (libtcod.COLCTRL_5, m))

        libtcod.console_print_rect(None, x, y, w, 3, '\n'.join(l))

    def m(self, s, bold = None):
        if bold:
            self.strings.insert(0, (libtcod.COLCTRL_3, s))
        else:
            self.strings.insert(0, (None, s))
        if len(self.strings) > 25:
            self.strings.pop()

    def show_all(self, w, h):
        l = []
        for v,m in self.strings[:24]:
            if v:
                l.append('%c%s' % (v,m))
            elif len(l) == 0:
                l.append('%c%s' % (libtcod.COLCTRL_1, m))
            else:
                l.append('%c%s' % (libtcod.COLCTRL_5, m))
        draw_window(l, w, h)


class Inventory:
    def __init__(self):
        self.head = None
        self.neck = None
        self.trunk = None
        self.left = None
        self.right = None
        self.legs = None
        self.feet = None
        self.backpack1 = None
        self.backpack2 = None

    def draw(self, w, h, dlev, plev):
        s = [
            ("a)       Head: %c%s", self.head),
            ("b)       Neck: %c%s", self.neck),
            ("c)      Trunk: %c%s", self.trunk),
            ("d)  Left hand: %c%s", self.left),
            ("e) Right hand: %c%s", self.right),
            ("f)       Legs: %c%s", self.legs),
            ("g)       Feet: %c%s", self.feet),
            ("h) Backpack 1: %c%s", self.backpack1),
            ("i) Backpack 2: %c%s", self.backpack2),
            "",
            "Character level: %d" % plev,
            "  Dungeon level: %d" % dlev]

        def pr(x):
            if not x:
                return ' -'
            return str(x)

        for x in xrange(len(s)):
            if type(s[x]) == type((0,)):
                s[x] = ("%c" % libtcod.COLCTRL_5) + \
                       s[x][0] % (libtcod.COLCTRL_1, pr(s[x][1]))

        return draw_window(s, w, h)

    def take(self, i):
        if   i.slot == 'a' and not self.head: self.head = i
        elif i.slot == 'b' and not self.neck: self.neck = i
        elif i.slot == 'c' and not self.trunk: self.trunk = i
        elif i.slot == 'd' and not self.left: self.left = i
        elif i.slot == 'e' and not self.right: self.right = i
        elif i.slot == 'f' and not self.legs: self.legs = i
        elif i.slot == 'g' and not self.feet: self.feet = i
        elif not self.backpack1: self.backpack1 = i
        elif not self.backpack2: self.backpack2 = i
        else: return False
        return True

    def drop(self, i):
        if i == 'a':
            i, self.head = self.head, None
            return i
        elif i == 'b':
            i, self.neck = self.neck, None
            return i
        elif i == 'c':
            i, self.trunk = self.trunk, None
            return i
        elif i == 'd':
            i, self.left = self.left, None
            return i
        elif i == 'e':
            i, self.right = self.right, None
            return i
        elif i == 'f':
            i, self.legs = self.legs, None
            return i
        elif i == 'g':
            i, self.feet = self.feet, None
            return i
        elif i == 'h':
            i, self.backpack1 = self.backpack1, None
            return i
        elif i == 'i':
            i, self.backpack2 = self.backpack2, None
            return i
        else:
            return None

    class _iter:
        def __init__(self, i):
            self.inv = i
            self.slot = 0
        def __iter__(self):
            return self
        def next(self):
            self.slot += 1
            if self.slot == 1: return self.inv.head
            elif self.slot == 2: return self.inv.neck
            elif self.slot == 3: return self.inv.trunk
            elif self.slot == 4: return self.inv.left
            elif self.slot == 5: return self.inv.right
            elif self.slot == 6: return self.inv.legs
            elif self.slot == 7: return self.inv.feet
            elif self.slot == 8: return self.inv.backpack1
            elif self.slot == 9: return self.inv.backpack2
            else: raise StopIteration()

    def __iter__(self):
        return self._iter(self)

    def purge(self, item):
        if self.head == item: self.head = None
        elif self.neck == item: self.neck = None
        elif self.trunk == item: self.trunk = None
        elif self.left == item: self.left = None
        elif self.right == item: self.right = None
        elif self.legs == item: self.legs = None
        elif self.feet == item: self.feet = None
        elif self.backback1 == item: self.backpack1 = None
        elif self.backpack2 == item: self.backpack2 = None

    def get_lightradius(self):
        return getattr(self.head,  'lightradius', 0) + \
               getattr(self.neck,  'lightradius', 0) + \
               getattr(self.left,  'lightradius', 0) + \
               getattr(self.right, 'lightradius', 0)

    def get_attack(self):
        return getattr(self.right, 'attack', 0) + \
               getattr(self.left, 'attack', 0) + \
               getattr(self.feet, 'attack', 0)

    def get_defence(self):
        return getattr(self.head, 'defence', 0) + \
               getattr(self.neck, 'defence', 0) + \
               getattr(self.trunk, 'defence', 0) + \
               getattr(self.legs, 'defence', 0) + \
               getattr(self.feet, 'defence', 0)

    def get_confattack(self):
        return getattr(self.right, 'confattack', None)


class Item:
    def __init__(self, name, slot='', bonus=0, count=None, ident=False,
                 skin=('~', libtcod.yellow), lightradius=0, explodes=0,
                 applies=False, liveexplode=None, radius=0, attack=0,
                 defence=0, desc=None, throwable=False, throwrange=8, booze=False,
                 cursedchance=0, range=None, ammochance=None, rangeattack=0,
                 straightline=False, confattack=None, rarity=None, healing=None,
                 homing=False, cooling=False, digging=False):
        self.slot = slot
        self.bonus = bonus
        self.name = name
        self.count = count
        self.ident = ident
        self.skin = skin
        self.lightradius = lightradius
        self.explodes = explodes
        self.applies = applies
        self.liveexplode = liveexplode
        self.radius = radius
        self.attack = attack
        self.defence = defence
        self.desc = desc
        self.throwable = throwable
        self.throwrange = throwrange
        self.booze = booze
        self.cursedchance = cursedchance
        self.range = range
        self.ammochance = ammochance
        self.ammo = None
        self.rangeattack = rangeattack
        self.straightline = straightline
        self.confattack = confattack
        self.rarity = rarity
        self.healing = healing
        self.homing = homing
        self.cooling = cooling
        self.digging = digging


    def __str__(self):
        s = ''
        if self.ident:
            if self.bonus > 0:
                s += 'blessed '
            elif self.bonus < 0:
                s += 'cursed '
        s += self.name
        if self.count != None:
            if self.count != 0:
                s = str(self.count) + " " + s
        elif len(s) > 0:
            if s[0] in 'aeiouAEIOU':
                s = 'an ' + s
            else:
                s = 'a ' + s
        if self.ammo:
            s = s + ' [%d]' % self.ammo
        return s

    def postprocess(self):
        if self.cursedchance:
            if random.randint(0, self.cursedchance) == 0:
                self.bonus = -1
        if self.ammochance:
            self.ammo = random.randint(self.ammochance[0], self.ammochance[1])


class ItemStock:
    def __init__(self):
        self.necklamp = Item("miner's lamp", slot='b', lightradius=8,
                             desc=['A lamp that provides light while you are cave-crawling.'])

        self.helmet = Item("miner's hardhat", slot='a',
                           skin=('[', libtcod.sepia), defence=0.25,
                           desc=['A simple plastic item of protective headgear.'])

        self.boots = Item('boots', slot='g', count=0,
                          skin=('[', libtcod.sepia), defence=0.1,
                          desc=['Steel-toed boots made of genuine leather.'])

        self.dynamite = Item('sticks of dynamite', count=3,
                             skin=('!', libtcod.red), applies=True, explodes=True,
                             radius=4, rarity=5,
                             desc=['Sticks of dynamite can be lit to create an explosive device.'])

        self.litdynamite = Item('burning stick of dynamite',
                                skin=('!', libtcod.yellow), explodes=True,
                                liveexplode=7, slot='d', radius=4, throwable=True,
                                desc=['Watch out!!'])

        self.pickaxe = Item("miner's pickaxe", slot='e', skin=('(', libtcod.gray),
                            attack=2.0, rarity=4, applies=True, digging=True,
                            desc=['Ostensibly to be used as an aid in traversing the caves,',
                                  'this sporting item is a good makeshift weapon.'])

        self.booze = Item("potion of booze", slot='d', skin=('!', libtcod.green),
                          booze=True, cursedchance=10, applies=True,
                          desc=['Sweet, sweet aqua vitae.',
                                'It helps keep one warm in these horrible caves.'])

        self.homing = Item("dowsing rod", slot='d', skin=(')', libtcod.cyan),
                           applies=True, rarity=4, homing=True,
                           desc=["A low-tech device for finding holes."])

        self.medpack = Item("magic pill", slot='d', skin=('%', libtcod.white),
                            rarity=3, applies=True, healing=(3, 0.5),
                            cursedchance=7,
                            desc=['A big white pill with a large red cross drawn on one side.'])


        self.mauser = Item("Mauser C96", slot='e', skin=('(', libtcod.blue),
                           rangeattack=7.0, range=(0,15), ammochance=(0, 10),
                           straightline=True, applies=True, rarity=5,
                           desc=['This antique beauty is a powerful handgun, ',
                                 'though a bit rusty for some reason.'])

        self.tazer = Item("tazer", slot='e', skin=('(', libtcod.gray),
                          attack=1.0, confattack=(10, 1), rarity=4,
                          desc=['Very useful for subduing enemies.'])

        self.coolpack = Item("some cold mud", slot='d', skin=('%', libtcod.light_blue),
                             applies=True, cooling=True, rarity=6, count=0,
                             desc=['A bluish lump of mud. ',
                                   'Useful for tricking predators with infrared vision.'])

        self._randpool = {}
        for x in dir(self):
            i = getattr(self, x)
            if type(i) == type(self.booze) and i.rarity:

                for x in xrange(i.rarity-3, i.rarity+1):
                    if x <= 0:
                        continue
                    if x not in self._randpool:
                        self._randpool[x] = [i]
                    else:
                        self._randpool[x].append(i)

        for k,v in self._randpool.iteritems():
            print k, [x.name for x in v]


    def get(self, item):
        i = getattr(self, item, None)
        if i:
            r = copy.copy(i)
            r.postprocess()
            return r
        return None

    def generate(self, level):
        if level not in self._randpool:
            return None

        x = self._randpool[level]
        r = copy.copy(x[random.randint(0, len(x)-1)])
        r.postprocess()
        print level, r.name
        return r


class Monster:
    def __init__(self, name, skin=('x', libtcod.cyan), unique=False, level=1,
                 attack=0.5, defence=0.5, explodeimmune=False, range=11,
                 itemdrop=None, heatseeking=False, desc=[]):
        self.name = name
        self.skin = skin
        self.unique = unique
        self.level = level
        self.attack = attack
        self.defence = defence
        self.explodeimmune = explodeimmune
        self.range = range
        self.itemdrop = itemdrop
        self.heatseeking = True
        self.desc = desc

        self.x = 0
        self.y = 0
        self.known_px = None
        self.known_py = None
        self.did_move = False
        self.do_move = None
        self.hp = 3.0
        self.items = []
        self.confused = 0

    def __str__(self):
        s = self.name
        if not self.unique:
            if s[0] in 'aeiouAEIOU':
                s = 'an ' + s
            else:
                s = 'a ' + s
        return s


class MonsterStock:
    def __init__(self):
        self.monsters = {}

        self.add(Monster('inebriated bum', skin=('h', libtcod.sepia),
                         attack=0.1, defence=0.2, range=3,
                         itemdrop='booze',
                         desc=['A drunken homeless humanoid.']))

        self.add(Monster('hobbit', skin=('h', libtcod.purple),
                         attack=1.5, defence=0.2, range=8, level=2,
                         desc=['A nasty, brutish humanoid creature endemic to these caves.']))

        self.add(Monster('laminaria', skin=('p', libtcod.light_blue),
                         attack=2.0, defence=0.1, range=10, level=3,
                         heatseeking=True,
                         desc=['Not a delicious condiment, but rather a gigantic pale-blue cave slug.',
                               'Being a cave creature, it seems to lack eyes of any sort.']))


    def add(self, mon):
        if mon.level not in self.monsters:
            self.monsters[mon.level] = [mon]
        else:
            self.monsters[mon.level].append(mon)

    def generate(self, level, itemstock):
        if level not in self.monsters:
            return None
        m = self.monsters[level]
        m = copy.copy(m[random.randint(0, len(m)-1)])

        if m.itemdrop:
            i = itemstock.get(m.itemdrop)
            if i:
                m.items = [i]

        return m


class World:

    def __init__(self):
        self.grid = None

        self.walkmap = None
        self.watermap = None
        self.featmap = None
        self.exit = None
        self.itemap = {}
        self.monmap = {}

        self.px = None
        self.py = None
        self.w = None
        self.h = None
        self.tcodmap = None
        self.done = False
        self.dead = False
        self.ckeys = None
        self.vkeys = None

        self.stats = Stats()
        self.msg = Messages()
        self.coef = Coeffs()
        self.inv = Inventory()
        self.itemstock = ItemStock()
        self.monsterstock = MonsterStock()

        self.dlev = 1
        self.plev = 1
        self.t = 0
        self.sleeping = 0
        self.resting = False
        self.cooling = 0
        self.digging = None

        self.floorpath = None

        self.monsters_in_view = []


    def makegrid(self, w_, h_):
        self.w = w_
        self.h = h_
        self.grid = [[10 for x in xrange(self.w)] for y in xrange(self.h)]

    def randgen(self, a, b, c, d, mid):
        x = ((c - a) / 2) + a
        y = ((d - b) / 2) + b
        if (a == x or c == x) and (b == y or d == y): return

        s = max((c-a), (d-b))
        step = 0 #max(n, 1)
        s = 1 #max(step / 3, 1)

        if not mid:
            mid = self.grid[b][a] + self.grid[b][c] + self.grid[d][a] + self.grid[d][c]
            mid = int(mid / 4.0) - step + random.randint(-s, s)

        self.grid[y][x] = mid

        top = ((self.grid[b][a] + self.grid[b][c] + mid) / 3) - step + random.randint(-s, s)
        self.grid[b][x] = top

        bot = ((self.grid[d][a] + self.grid[d][c] + mid) / 3) - step + random.randint(-s, s)
        self.grid[d][x] = bot

        lef = ((self.grid[b][a] + self.grid[d][a] + mid) / 3) - step + random.randint(-s, s)
        self.grid[y][a] = lef

        rig = ((self.grid[b][c] + self.grid[d][c] + mid) / 3) - step + random.randint(-s, s)
        self.grid[y][c] = rig

        self.randgen(a, b, x, y, None)
        self.randgen(x, b, c, y, None)
        self.randgen(a, y, x, d, None)
        self.randgen(x, y, c, d, None)

    def normalize(self, ):
        avg = 0.0
        min = 2000
        max = -2000
        for row in self.grid:
            for v in row:
                avg += v

        avg = avg / (self.w * self.h)

        for x in xrange(self.w):
            for y in xrange(self.h):
                self.grid[y][x] -= avg
                v = self.grid[y][x]
                if v > max: max = v
                elif v < min: min = v

        scale = (max - min) / 20

        for x in xrange(self.w):
            for y in xrange(self.h):
                self.grid[y][x] = int(self.grid[y][x] / scale)
                if self.grid[y][x] > 10: self.grid[y][x] = 10
                elif self.grid[y][x] < -10: self.grid[y][x] = -10


    def terra(self):
        self.randgen(0, 0, self.w - 1, self.h - 1, -10)
        self.normalize()
        return self.grid


    def flow(self, x, y, out, n, q):
        if n < 1e-5: return

        v0 = self.grid[y][x]
        l = []
        if (x,y) in out: return
        out.add((x, y))

        for ix in xrange(-1, 2):
            for iy in xrange(-1, 2):
                zx = x + ix
                zy = y + iy
                if zx < 0 or zy < 0 or zx >= self.w or zy >= self.h:
                    continue
                v = self.grid[zy][zx]

                if (zx,zy) not in out and v <= v0:
                    l.append((v, zx, zy))

        if len(l) == 0: return

        l.sort()
        l = l[:2]
        qq = n / (len(l) + 1)

        for v,ix,iy in l:
            self.flow(ix, iy, out, qq, q)


    def makeflow(self, gout, watr, n, q):

        x = random.randint(0, self.w-1)
        y = random.randint(0, self.h-1)
        out = set()
        self.flow(x, y, out, n, q)

        for ix,iy in out:

            if (ix,iy) not in watr:
                watr[(ix,iy)] = 1
            else:
                watr[(ix,iy)] += 1

            self.grid[iy][ix] -= q
            if self.grid[iy][ix] < -10:
                self.grid[iy][ix] = -10

        gout.update(out)


    def makerivers(self):
        gout = set()
        watr = {}
        for x in xrange(50):
            self.makeflow(gout, watr, 100.0, 1)

        self.walkmap = set()
        for x,y in gout:
            if self.grid[y][x] <= 0:
                self.walkmap.add((x,y))

        watr = [(v,k) for (k,v) in watr.iteritems()]
        watr.sort()
        watr.reverse()

        pctwater = random.gauss(5, 1)
        if pctwater <= 1: pctwater = 1
        watr = watr[:int(len(watr)/pctwater)]

        self.watermap = set()
        for n,v in watr:
            self.watermap.add(v)

        return self.grid, self.walkmap

    def make_map(self):
        self.tcodmap = libtcod.map_new(self.w, self.h)
        for x in xrange(self.w):
            for y in xrange(self.h):
                if (x,y) in self.walkmap:
                    v = True
                else:
                    v = False
                libtcod.map_set_properties(self.tcodmap, x, y, v, v)

    def make_feats(self):
        m = list(self.walkmap - self.watermap)

        if len(m) == 0: return

        d = m[random.randint(0, len(m)-1)]

        self.featmap = {}
        self.featmap[d] = '>'
        self.exit = d

    def make_paths(self):
        if self.floorpath:
            libtcod.path_delete(self.floorpath)

        def floor_callback(xfrom, yfrom, xto, yto, world):
            if (xto, yto) in world.monmap:
                return 0.0
            elif (xto, yto) in world.walkmap:
                return 1.0
            return 0.0

        self.floorpath = libtcod.path_new_using_function(self.w, self.h, floor_callback, self, 1.0)

    def make_monsters(self):

        self.monmap = {}
        n = int(max(random.gauss(*self.coef.nummonsters), 1))
        ll = list(self.walkmap)

        for i in xrange(n):
            lev = self.dlev + random.gauss(0, self.coef.monlevel)
            lev = max(int(round(lev)), 1)

            while 1:
                x, y = ll[random.randint(0, len(ll)-1)]
                if (x, y) not in self.monmap: break

            m = self.monsterstock.generate(lev, self.itemstock)
            if not m:
                print lev
            else:
                print m.name
                m.x = x
                m.y = y
                self.monmap[(x, y)] = m

    def make_items(self):

        self.itemap = {}
        n = int(max(random.gauss(self.coef.numitems[0] + self.dlev, self.coef.numitems[1]), 1))
        ll = list(self.walkmap)

        for i in xrange(n):
            lev = self.dlev + random.gauss(0, self.coef.itemlevel)
            lev = max(int(round(lev)), 1)
            x, y = ll[random.randint(0, len(ll)-1)]
            item = self.itemstock.generate(lev)
            if item:
                print item.name
                if (x, y) not in self.itemap:
                    self.itemap[(x, y)] = [item]
                else:
                    self.itemap[(x, y)].append(item)


    def regen(self, w_, h_):
        self.makegrid(w_, h_)
        self.terra()
        self.makerivers()
        self.make_map()
        self.make_feats()
        self.make_paths()
        self.make_monsters()
        self.make_items()

    def place(self):
        while 1:
            x = random.randint(0, self.w-1)
            y = random.randint(0, self.h-1)
            if (x,y) in self.walkmap:
                self.px = x
                self.py = y
                return

        self.stats = Stats()

    def generate_inv(self):
        self.inv.take(self.itemstock.get('necklamp'))
        self.inv.take(self.itemstock.get('helmet'))
        self.inv.take(self.itemstock.get('boots'))

        self.itemap[(self.px, self.py)] = [
                    self.itemstock.get('dynamite'),
                    self.itemstock.get('mauser'),
                    self.itemstock.get('pickaxe'),
                    self.itemstock.get('tazer')]


    def move(self, dx, dy):
        dx = dx + self.px
        dy = dy + self.py
        if (dx,dy) in self.walkmap and dx >= 0 and dx < self.w and dy < self.h:

            if (dx, dy) in self.monmap:
                self.fight(self.monmap[(dx, dy)], True)
            else:
                self.px = dx
                self.py = dy

                if (self.px, self.py) in self.itemap:
                    if len(self.itemap[(self.px, self.py)]) > 1:
                        self.msg.m("You see several items here.")
                    else:
                        self.msg.m("You see " + str(self.itemap[(self.px, self.py)][0]) + '.')

        else:
            return
        self.tick()

    def tick(self):
        self.stats.tired.dec(self.coef.movetired)
        self.stats.sleep.dec(self.coef.movesleep)
        self.stats.thirst.dec(self.coef.movethirst)
        self.stats.hunger.dec(self.coef.movehunger)
        if (self.px, self.py) in self.watermap or self.cooling:
            self.stats.warmth.dec(self.coef.watercold)
        self.tick_checkstats()

    def tick_checkstats(self):

        for i in self.inv:
            if i and i.liveexplode > 0:
                i.liveexplode -= 1
                if i.liveexplode == 0:
                    self.explode(self.px, self.py, i.radius)
                    self.inv.purge(i)

        if self.cooling > 0:
            self.cooling -= 1
            if self.cooling == 0:
                self.msg.m("Your layer of cold mud dries up.")

        if self.dead: return

        if self.stats.warmth.x <= -3.0:
            self.msg.m("Being so cold makes you sick!", True)
            self.stats.health.dec(self.coef.colddamage)

        if self.stats.thirst.x <= -3.0:
            self.msg.m('You desperately need something to drink!', True)
            self.stats.health.dec(self.coef.thirstdamage)

        if self.stats.hunger.x <= -3.0:
            self.msg.m('You desperately need something to eat!', True)
            self.stats.health.dec(self.coef.hungerdamage)

        if self.stats.health.x <= -3.0:
            self.msg.m('You die.', True)
            self.dead = True
            return

        if self.stats.tired.x <= -3.0:
            self.msg.m('You pass out from exhaustion!', True)
            self.start_sleep(force=True, quick=True)
            return

        if self.stats.sleep.x <= -3.0:
            self.msg.m('You pass out from lack of sleep!', True)
            self.start_sleep(force=True)
            return



    def rest(self):
        self.stats.tired.inc(self.coef.resttired)
        self.stats.sleep.dec(self.coef.restsleep)
        self.stats.thirst.dec(self.coef.restthirst)
        self.stats.hunger.dec(self.coef.resthunger)
        if (self.px, self.py) in self.watermap or self.cooling:
            self.stats.warmth.dec(self.coef.watercold)
        self.tick_checkstats()

    def sleep(self):
        self.stats.tired.inc(self.coef.sleeptired)
        self.stats.sleep.inc(self.coef.sleepsleep)
        self.stats.thirst.dec(self.coef.sleepthirst)
        self.stats.hunger.dec(self.coef.sleephunger)
        if (self.px, self.py) in self.watermap or self.cooling:
            self.stats.warmth.dec(self.coef.watercold)
        self.tick_checkstats()

        if self.sleeping > 0:
            self.sleeping -= 1

    def start_sleep(self, force = False, quick = False):
        if not force and self.stats.sleep.x > -2.0:
            self.msg.m('You don\'t feel like sleeping yet.')
            return

        if quick:
            self.sleeping = int(random.gauss(*self.coef.quicksleeptime))
        else:
            self.msg.m('You fall asleep.')
            self.sleeping = int(random.gauss(*self.coef.sleeptime))
        if self.sleep <= 10:
            self.sleep = 10

    def start_rest(self):
        self.msg.m('You start resting.')
        self.resting = True

    def drink(self):
        if (self.px,self.py) not in self.watermap:
            self.msg.m('There is no water here you could drink.')
            return

        self.stats.thirst.inc(6)

        x = abs(random.gauss(0, 1))
        if x > self.coef.waterpois:
            self.stats.health.dec(x-self.coef.waterpois)
            self.msg.m('This water has a bad smell.')
        else:
            self.msg.m('You drink from the puddle.')

        self.tick()

    def showinv(self):
        return self.inv.draw(self.w, self.h, self.dlev, self.plev)

    def showinv_apply(self):
        slot = self.inv.draw(self.w, self.h, self.dlev, self.plev)
        i = self.inv.drop(slot)
        if not i:
            if slot in 'abcdefghi':
                self.msg.m('You have no item in that slot.')
            return

        si = str(i)
        si = si[0].upper() + si[1:]
        s = [si + ':', '']
        if i.applies:
            s.append('a) use it')
        if not self.inv.backpack1 or not self.inv.backpack2:
            s.append('b) move it to a backpack slot')
        if i.desc:
            s.append('c) examine this item')
        s.append('d) drop this item')
        if i.throwable:
            s.append('f) throw this item')

        s.append('')
        s.append('any other key to equip it')
        cc = draw_window(s, self.w, self.h)

        if cc == 'a' and i.applies:
            i = self.apply(i)
            if i:
                self.inv.take(i)
            self.tick()

        elif cc == 'b':
            if not self.inv.backpack1:
                self.inv.backpack1 = i
                self.tick()
            elif not self.inv.backpack2:
                self.inv.backpack2 = i
                self.tick()

        elif cc == 'c' and i.desc:
            draw_window(i.desc, self.w, self.h)
            self.inv.take(i)
            self.tick()

        elif cc == 'd':
            if (self.px, self.py) in self.itemap:
                self.itemap[(self.px, self.py)].append(i)
            else:
                self.itemap[(self.px, self.py)] = [i]
            self.tick()

        elif cc == 'f':
            while 1:
                nx, ny = self.target(i.throwrange)
                if nx is not None:
                    break

            if nx >= 0:
                self.msg.m('You throw ' + str(i) + '.')

                if (nx, ny) in self.itemap:
                    self.itemap[(nx, ny)].append(i)
                else:
                    self.itemap[(nx, ny)] = [i]
            else:
                self.inv.take(i)
            self.tick()


        else:
            self.inv.take(i)
            self.tick()

    def apply(self, item):
        if not item.applies:
            return

        if item.explodes and item.count > 0:
            if self.inv.left or self.inv.right:
                self.msg.m('Both your right and left hands need to be free to light a stick of dynamite.')
                return item
            self.msg.m('You light a stick a dynamite. It is now in your left hand!', True)
            item.count -= 1
            self.inv.take(self.itemstock.get('litdynamite'))

            if item.count <= 0:
                return None

        elif item.digging:
            k = draw_window(['Dig in which direction?'], self.w, self.h, True)

            self.digging = None
            if k == 'h': self.digging = (self.px - 1, self.py)
            elif k == 'j': self.digging = (self.px, self.py + 1)
            elif k == 'k': self.digging = (self.px, self.py - 1)
            elif k == 'l': self.digging = (self.px + 1, self.py)
            else:
                return item

            if self.digging[0] < 0 or self.digging[0] >= self.w:
                self.digging = None
            if self.digging[1] < 0 or self.digging[1] >= self.h:
                self.digging = None

            if not self.digging:
                return item

            if self.digging in self.walkmap:
                self.msg.m('There is nothing to dig there.')
                self.digging = None
            else:
                self.msg.m("You start hacking at the wall.")

        elif item.healing:
            if item.bonus < 0:
                self.msg.m('This pill makes your eyes pop out of their sockets!')
                self.stats.tired.dec(max(random.gauss(*item.healing), 0))
                self.stats.sleep.dec(max(random.gauss(*item.healing), 0))
            else:
                self.msg.m('Eating this pill makes you dizzy.')
                self.stats.health.inc(max(random.gauss(*item.healing), 0))
                self.stats.hunger.dec(max(random.gauss(*item.healing), 0))
                self.stats.sleep.dec(max(random.gauss(*item.healing), 0))

        elif item.booze:
            if item.bonus < 0:
                self.msg.m("This stuff is contaminated! You fear you're going blind!", True)
                self.blind = True
            else:
                self.msg.m('Aaahh.')
                self.stats.sleep.dec(max(random.gauss(*self.coef.boozestrength), 0))
                self.stats.warmth.inc(max(random.gauss(*self.coef.boozestrength), 0))
            return None

        elif item.homing:
            d = math.sqrt(math.pow(abs(self.px - self.exit[0]), 2) +
                          math.pow(abs(self.py - self.exit[1]), 2))
            if d > 30:
                self.msg.m('Cold as ice!')
            elif d > 20:
                self.msg.m('Very cold!')
            elif d > 15:
                self.msg.m('Cold!')
            elif d > 10:
                self.msg.m('Getting warmer...')
            elif d > 5:
                self.msg.m('Warm and getting warmer!')
            elif d > 3:
                self.msg.m("This thing is buring!")

        elif item.cooling:
            self.cooling = max(int(random.gauss(*self.coef.coolingduration)), 1)
            self.msg.m("You cover yourself in cold mud.")
            return None

        elif item.rangeattack:
            if item.ammo <= 0:
                self.msg.m("It's out of ammo!")
                return item

            while 1:
                nx, ny = self.target(item.range[1],
                                     minrange=item.range[0],
                                     monstop=item.straightline)
                if nx is not None:
                    break
            if nx < 0:
                return item

            item.ammo -= 1
            if (nx, ny) in self.monmap:
                self.fight(self.monmap[(nx, ny)], True, item=item)


        return item


    def descend(self):
        if self.featmap.get((self.px,self.py), '') != '>':
            self.msg.m('You can\'t descend, there is no hole here.')
            return

        self.msg.m('You climb down the hole.')
        self.dlev += 1
        self.regen(self.w, self.h)
        self.place()
        self.tick()

    def debug_descend(self):
        self.dlev += 1
        self.regen(self.w, self.h)
        self.place()
        self.tick()

    def drop(self):
        slot = self.showinv()
        i = self.inv.drop(slot)
        if not i:
            if slot in 'abcdefghi':
                self.msg.m('There is no item in that slot.')
            return

        self.msg.m('You drop ' + str(i) +'.')
        if (self.px, self.py) in self.itemap:
            self.itemap[(self.px, self.py)].append(i)
        else:
            self.itemap[(self.px, self.py)] = [i]
        self.tick()

    def take_scavenge(self, item):
        if item.ammo > 0:
            for i in self.inv:
                if i.name == item.name:
                    i.ammo += item.ammo
                    item.ammo = 0
                    self.msg.m("You find some ammo for your " + str(i))
                    return

        self.msg.m('You have no free inventory slot for ' + str(item) + '!')


    def take(self):
        if (self.px, self.py) not in self.itemap:
            self.msg.m('You see no item here to take.')
            return

        items = self.itemap[(self.px, self.py)]

        if len(items) == 1:
            ok = self.inv.take(items[0])
            if ok:
                self.msg.m('You take ' + str(items[0]) + '.')
                del self.itemap[(self.px, self.py)]
            else:
                self.take_scavenge(items[0])
            return

        s = []
        for i in xrange(len(items)):
            if i == 0:
                s.append('%c' % libtcod.COLCTRL_1)
                s[-1] += '%c) %s' % (chr(97 + i), str(items[i]))
            elif i > 5:
                s.append('(There are other items here; clear away the pile to see more)')
                break
            else:
                s.append('%c) %s' % (chr(97 + i), str(items[i])))

        c = draw_window(s, self.w, self.h)
        c = ord(c) - 97

        if c < 0 or c >= len(items):
            return

        ok = self.inv.take(items[c])
        if ok:
            self.msg.m('You take ' + str(items[c]) + '.')
            del self.itemap[(self.px, self.py)][c]
        else:
            self.take_scavenge(items[c])
        self.tick()


    def handle_mondeath(self, mon, do_drop=True):
        if mon.level > self.plev:
            self.msg.m('You just gained level ' + str(mon.level) + '!', True)
            self.plev = mon.level

        if do_drop:
            if len(mon.items) > 0:
                if (mon.x, mon.y) in self.itemap:
                    self.itemap[(mon.x, mon.y)].extend(mon.items)
                else:
                    self.itemap[(mon.x, mon.y)] = mon.items



    def explode(self, x0, y0, rad):
        chains = set()
        def func(x, y):
            if random.randint(0, 5) == 0:
                libtcod.map_set_properties(self.tcodmap, x, y, False, True)
                if (x, y) not in self.featmap:
                    self.featmap[(x, y)] = '*'
            else:
                libtcod.map_set_properties(self.tcodmap, x, y, True, True)
            self.walkmap.add((x, y))

            if x == self.px and y == self.py:
                self.stats.health.dec(6.0)
                self.tick_checkstats()

            if (x, y) in self.itemap:
                for i in self.itemap[(x, y)]:
                    if i.explodes:
                        chains.add((x, y, i.radius))
                        break
                del self.itemap[(x, y)]

            if (x, y) in self.monmap:
                if not self.monmap[(x, y)].explodeimmune:
                    self.handle_mondeath(self.monmap[(x, y)], False)
                    del self.monmap[(x, y)]

        draw_blast(x0, y0, self.w, self.h, rad, func)

        for x, y, r in chains:
            self.explode(x, y, r)


    def fight(self, mon, player_move, item=None):

        sm = str(mon)
        smu = sm[0].upper() + sm[1:]

        d = math.sqrt(math.pow(abs(mon.x - self.px), 2) +
                      math.pow(abs(mon.y - self.py), 2))
        d = int(round(d))

        if d > 1.0 or item:
            plev = min(max(self.plev - item.range[1] + d, 1), self.plev)
            attack = item.rangeattack
        else:
            plev = self.plev
            attack = max(self.inv.get_attack(), self.coef.unarmedattack)


        def roll(attack, leva, defence, levd):
            a = 0
            for x in xrange(leva):
                a += random.uniform(0, attack)
            d = 0
            for x in xrange(levd):
                d += random.uniform(0, defence)

            ret = max(a - d, 0)
            return ret

        if player_move:

            defence = mon.defence
            dmg = roll(attack, plev, defence, mon.level)

            mon.hp -= dmg

            if dmg > 2:
                self.msg.m('You seriously wound ' + sm + '!')
            elif dmg > 0:
                self.msg.m('You hit ' + sm + '.')
            else:
                self.msg.m('You miss ' + sm + '.')

            if mon.hp <= -3.0:
                self.msg.m('You killed ' + sm + '!')
                self.handle_mondeath(mon)
                del self.monmap[(mon.x, mon.y)]
            else:
                if item:
                    ca = item.confattack
                else:
                    ca = self.inv.get_confattack()

                if ca and dmg > 0:
                    self.msg.m(smu + ' looks totally dazed!')
                    mon.confused += int(max(random.gauss(*ca), 1))

            if dmg > 0:
                mon.known_px = self.px
                mon.known_py = self.py


        else:
            defence = max(self.inv.get_defence(), self.coef.unarmeddefence)
            dmg = roll(mon.attack, mon.level, defence, plev)

            if dmg > 0:
                self.msg.m(smu + ' hits!')
            else:
                self.msg.m(smu + ' misses.')
            self.stats.health.dec(dmg)

            if self.resting:
                self.msg.m('You stop resting.')
                self.resting = False

            if self.digging:
                self.msg.m('You stop digging.')
                self.digging = None

            if self.sleeping:
                self.sleeping = 0

            self.tick_checkstats()


    def look(self):
        tx = self.px
        ty = self.py

        while 1:
            seen = self.draw(False, tx, ty)

            s = []

            if tx == self.px and ty == self.py:
                s.append('This is you.')
                s.append('')

            if not seen:
                s.append('You see nothing.')

            else:
                if (tx, ty) in self.monmap:
                    m = self.monmap[(tx, ty)]
                    s.append('You see ' + str(m) + ':')
                    s.extend(m.desc)
                    s.append('')

                if (tx, ty) in self.itemap:
                    i = self.itemap[(tx, ty)]
                    s.append('You see the following items:')
                    for ix in xrange(len(i)):
                        if ix >= 5:
                            s.append('(And some other items)')
                            break
                        s.append(str(i[ix]))
                    s.append('')

                if (tx, ty) in self.featmap:
                    f = self.featmap[(tx, ty)]
                    if f == '>':
                        s.append('You see a hole in the floor.')
                    elif f == '*':
                        s.append('You see rubble.')

                elif (tx, ty) in self.walkmap:
                    if (tx, ty) in self.watermap:
                        s.append('You see a water-covered floor.')
                    else:
                        s.append('You see a cave floor.')

                else:
                        s.append('You see a cave wall. ' + str(self.grid[ty][tx]))

            k = draw_window(s, self.w, self.h, True)

            if   k == 'h': tx -= 1
            elif k == 'j': ty += 1
            elif k == 'k': ty -= 1
            elif k == 'l': tx += 1
            elif k == 'y':
                tx -= 1
                ty -= 1
            elif k == 'u':
                tx += 1
                ty -= 1
            elif k == 'b':
                tx -= 1
                ty += 1
            elif k == 'n':
                tx += 1
                ty += 1
            else:
                break

            if tx < 0: tx = 0
            elif tx >= self.w: tx = self.w - 1

            if ty < 0: ty = 0
            elif ty >= self.h: ty = self.h - 1


    def target(self, range, minrange=None, monstop=False):

        monx = None
        mony = None
        for i in xrange(len(self.monsters_in_view)):
            mon = self.monsters_in_view[i]
            d = math.sqrt(math.pow(abs(self.px - mon.x), 2) +
                          math.pow(abs(self.py - mon.y), 2))
            if d > range:
                continue
            if minrange and d < minrange:
                continue

            monx = mon.x
            mony = mon.y
            del self.monsters_in_view[i]
            self.monsters_in_view.append(mon)
            break

        if monx is not None:
            self.draw(False, monx, mony)

        k = draw_window(['Pick a target. '
                         "HJKL YUBN for directions, "
                         "<space> and '.' to target a monster."],
                         self.w, self.h, True)

        if k == 'h':
            dx = max(self.px - range, 0)
            dy = self.py
        elif k == 'j':
            dx = self.px
            dy = min(self.py + range, self.h - 1)
        elif k == 'k':
            dx = self.px
            dy = max(self.py - range, 0)
        elif k == 'l':
            dx = min(self.px + range, self.w - 1)
            dy = self.py
        elif k == 'y':
            dx = max(self.px - int(range * 0.71), 0)
            dy = max(self.py - int(range * 0.71), 0)
        elif k == 'u':
            dx = min(self.px + int(range * 0.71), self.w - 1)
            dy = max(self.py - int(range * 0.71), 0)
        elif k == 'b':
            dx = max(self.px - int(range * 0.71), 0)
            dy = min(self.py + int(range * 0.71), self.h - 1)
        elif k == 'n':
            dx = min(self.px + int(range * 0.71), self.w - 1)
            dy = min(self.py + int(range * 0.71), self.h - 1)
        elif k == '.':
            if monx is not None:
                dx = monx
                dy = mony
            else:
                return (None, None)
        elif k == ' ':
            return (None, None)
        else:
            return -1, -1

        libtcod.line_init(self.px, self.py, dx, dy)
        xx = None
        yy = None
        while 1:
            tmpx, tmpy = libtcod.line_step()
            if not tmpx:
                return (xx, yy)

            if minrange:
                d = math.sqrt(math.pow(abs(tmpx - self.px), 2) +
                              math.pow(abs(tmpy - self.py), 2))
                if d < minrange:
                    continue

            if monstop and (tmpx, tmpy) in self.monmap:
                return (tmpx, tmpy)

            if (tmpx, tmpy) in self.walkmap:
                xx = tmpx
                yy = tmpy
            else:
                return (xx, yy)


    def show_messages(self):
        self.msg.show_all(self.w, self.h)


    def move_down(self): self.move(0, 1)
    def move_up(self): self.move(0, -1)
    def move_left(self): self.move(-1, 0)
    def move_right(self): self.move(1, 0)
    def move_upleft(self): self.move(-1, -1)
    def move_upright(self): self.move(1, -1)
    def move_downleft(self): self.move(-1, 1)
    def move_downright(self): self.move(1, 1)

    def quit(self): self.done = True

    def restart(self):
        self.regen(self.w, self.h)
        self.place()



    def make_keymap(self):
        self.ckeys = {
            'h': self.move_left,
            'j': self.move_down,
            'k': self.move_up,
            'l': self.move_right,
            'y': self.move_upleft,
            'u': self.move_upright,
            'b': self.move_downleft,
            'n': self.move_downright,
            '.': self.rest,
            's': self.start_sleep,
            'r': self.start_rest,
            'q': self.drink,
            'i': self.showinv_apply,
            '>': self.descend,
            'x': self.debug_descend,
            'd': self.drop,
            ',': self.take,
            '/': self.look,
            'P': self.show_messages,
            'Q': self.quit
            }
        self.vkeys = {
            libtcod.KEY_ESCAPE: self.quit,
            libtcod.KEY_ENTER: self.restart,
            libtcod.KEY_LEFT: self.move_left,
            libtcod.KEY_RIGHT: self.move_right,
            libtcod.KEY_UP: self.move_up,
            libtcod.KEY_DOWN: self.move_down
            }


    def walk_monster(self, mon, dist, x, y):

        if dist > mon.range or mon.confused:
            mdx = x + random.randint(-1, 1)
            mdy = y + random.randint(-1, 1)
            if (mdx, mdy) not in self.walkmap:
                mdx = None
                mdy = None
            if mon.confused:
                mon.confused -= 1

        else:

            if mon.known_px is None or mon.known_py is None:
                mon.known_px = self.px
                mon.known_py = self.py

            elif mon.heatseeking and \
                 ((self.px, self.py) in self.watermap or self.cooling):
                pass
            else:
                mon.known_px = self.px
                mon.known_py = self.py

            if mon.heatseeking:
                print '|', mon.known_px, mon.known_py, self.px, self.py

            libtcod.path_compute(self.floorpath, x, y, mon.known_px, mon.known_py)
            mdx, mdy = libtcod.path_walk(self.floorpath, True)

        return mdx, mdy


    def draw(self, withtime=True, _hlx=None, _hly=None):
        back = libtcod.Color(0,0,0)

        lightradius = min(max(self.inv.get_lightradius(), 2), 8)
        libtcod.map_compute_fov(self.tcodmap, self.px, self.py, lightradius,
                                True, libtcod.FOV_RESTRICTIVE)

        explodes = set()
        mons = []

        monsters_in_view = []
        did_highlight = False

        for x in xrange(self.w):
            for y in xrange(self.h):

                if withtime and (x, y) in self.itemap:
                    for i in self.itemap[(x, y)]:
                        if i.liveexplode > 0:
                            i.liveexplode -= 1
                            if i.liveexplode == 0:
                                explodes.add((x, y, i.radius))
                                del self.itemap[(x, y)]
                                break

                if withtime and (x, y) in self.monmap and not self.monmap[(x, y)].did_move:

                    dist = math.sqrt(math.pow(abs(self.px - x), 2) + math.pow(abs(self.py - y), 2))
                    mon = self.monmap[(x, y)]

                    mdx, mdy = self.walk_monster(mon, dist, x, y)

                    if mdx is not None:
                        if mdx == self.px and mdy == self.py:
                            self.fight(mon, False)
                        else:
                            mon.do_move = (mdx, mdy)

                        mon.did_move = True
                        mons.append(mon)


                fore = libtcod.Color(200, 255, 200)

                if not libtcod.map_is_in_fov(self.tcodmap, x, y):
                    c = ' '
                    fore = libtcod.Color(0, 0, 0)
                else:
                    if x == self.px and y == self.py:
                        c = '@'
                        if self.sleeping > 1 and (self.t & 1) == 1:
                            c = '*'
                        elif self.resting and (self.t & 1) == 1:
                            c = '.'
                        elif self.digging and (self.t & 1) == 1:
                            c = '('

                    elif (x, y) in self.monmap:
                        mon = self.monmap[(x, y)]
                        c, fore = mon.skin
                        monsters_in_view.append(mon)

                    elif (x, y) in self.itemap:
                        c, fore = self.itemap[(x, y)][0].skin

                    elif (x, y) in self.featmap:
                        f = self.featmap[(x, y)]
                        c = f

                    elif (x, y) in self.walkmap:
                        if (x,y) in self.watermap:
                            c = '-'
                            fore = libtcod.Color(80, 80, 255)
                        else:
                            c = 250
                    else:
                        if (x,y) in self.watermap:
                            fore = libtcod.Color(100, 128, 255)
                        c = '#'

                    d = math.sqrt(math.pow(abs(y - self.py),2) + math.pow(abs(x - self.px),2))

                    fore = libtcod.color_lerp(fore, back, min(d/lightradius, 1.0))

                if x == _hlx and y == _hly:
                    # hack
                    if c != ' ':
                        did_highlight = True

                    libtcod.console_put_char_ex(None, x, y, c, fore, libtcod.white)
                else:
                    libtcod.console_put_char_ex(None, x, y, c, fore, back)

        if self.px > self.w / 2:
            self.stats.draw(0, 0)
        else:
            self.stats.draw(self.w - 14, 0)

        if self.py > self.h / 2:
            self.msg.draw(15, 0, self.w - 30)
        else:
            self.msg.draw(15, self.h - 3, self.w - 30)


        for mon in mons:
            if mon.do_move:
                mon.old_pos = (mon.x, mon.y)
                del self.monmap[(mon.x, mon.y)]

        for mon in mons:
            if mon.do_move:
                if mon.do_move in self.monmap:
                    mon.do_move = mon.old_pos

                mon.x = mon.do_move[0]
                mon.y = mon.do_move[1]
                self.monmap[mon.do_move] = mon
                mon.do_move = None

            mon.did_move = False

        for x, y, r in explodes:
            self.explode(x, y, r)
            #hack
            self.draw(False)

        # hack
        if withtime:
            self.monsters_in_view = []
            for mon in monsters_in_view:
                if (mon.x, mon.y) in self.monmap:
                    self.monsters_in_view.append(mon)

        if withtime:
            self.t += 1

        return did_highlight



def main():
    w = 80
    h = 25

    #libtcod.sys_set_renderer(libtcod.RENDERER_SDL)

    font = 'terminal10x16_gs_ro.png'
    libtcod.console_set_custom_font(font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(w, h, 'Diggr', False, libtcod.RENDERER_SDL)
    libtcod.sys_set_fps(30)
    #cons = libtcod.console_new(w, h)
    #cons = None

    world = World()
    world.regen(w, h)
    world.place()
    world.make_keymap()

    world.generate_inv()

    while not libtcod.console_is_window_closed():

        if world.done or world.dead: break

        world.draw()
        libtcod.console_flush()

        if world.sleeping > 0:
            if world.stats.sleep.x >= 3.0:
                world.msg.m('You wake up.')
                world.sleeping = 0
                world.draw(False)
                libtcod.console_flush()
            else:
                world.sleep()
                continue

        if world.resting:
            if world.stats.tired.x >= 3.0:
                world.msg.m('You stop resting.')
                world.resting = False
                world.draw(False)
                libtcod.console_flush()
            else:
                world.rest()
                continue

        if world.digging:
            if world.grid[world.digging[1]][world.digging[0]] <= -10:
                world.walkmap.add(world.digging)
                world.digging = None
                world.draw(False)
                libtcod.console_flush()
            else:
                world.grid[world.digging[1]][world.digging[0]] -= 0.1
                world.tick()
                continue

        if world.dead: break

        key = libtcod.console_wait_for_keypress(True)

        if chr(key.c) in world.ckeys:
            world.ckeys[chr(key.c)]()

        elif key.vk in world.vkeys:
            world.vkeys[key.vk]()

    world.msg.m('*** Press any key ***', True)
    world.draw(False)
    libtcod.console_flush()
    libtcod.console_wait_for_keypress(False)

#import cProfile
#cProfile.run('main()')

main()
