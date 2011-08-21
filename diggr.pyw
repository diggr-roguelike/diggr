
import math
import os
import random
import copy
import time

import cPickle

import libtcodpy as libtcod

#
# - versioning in replays!
#

global _version
_version = '11.08.21'

global _inputs
global _inputqueue
_inputqueue = None
class fakekey:
    def __init__(self, c, vk):
        self.c = c
        self.vk = vk


def console_wait_for_keypress():
    global _inputqueue
    if _inputqueue is not None:

        if len(_inputqueue) == 0:
            raise Exception('Malformed replay file.')

        c, vk = _inputqueue[0]
        _inputqueue = _inputqueue[1:]
        #libtcod.console_wait_for_keypress(False)
        libtcod.console_check_for_keypress()
        libtcod.sys_sleep_milli(100)
        return fakekey(c, vk)

    k = libtcod.console_wait_for_keypress(False)
    _inputs.append((k.c, k.vk))
    return k


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

        self.glueduration = (10,1)
        self.gluedefencepenalty = 3


class Stat:
    def __init__(self):
        self.x = 3.0
        self.reason = None

    def dec(self, dx, reason=None):
        self.x -= dx
        if self.x < -3.0: self.x = -3.0
        if reason:
            self.reason = reason

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

        libtcod.console_set_color_control(libtcod.COLCTRL_1, libtcod.white, libtcod.black)
        libtcod.console_set_color_control(libtcod.COLCTRL_2, libtcod.darker_green, libtcod.black)
        libtcod.console_set_color_control(libtcod.COLCTRL_3, libtcod.yellow, libtcod.black)
        libtcod.console_set_color_control(libtcod.COLCTRL_4, libtcod.red, libtcod.black)
        libtcod.console_set_color_control(libtcod.COLCTRL_5, libtcod.gray, libtcod.black)

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
    #k = libtcod.console_wait_for_keypress(False)
    #_inputs.append((k.c, k.vk))
    k = console_wait_for_keypress()

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

    back = libtcod.darkest_red
    fore = libtcod.yellow
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
        if len(self.strings) > 0 and s == self.strings[0][1]:
            return

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

    def take(self, i, slot=None):
        if not slot:
            slot = i.slot
        if   slot == 'a' and not self.head: self.head = i
        elif slot == 'b' and not self.neck: self.neck = i
        elif slot == 'c' and not self.trunk: self.trunk = i
        elif slot == 'd' and not self.left: self.left = i
        elif slot == 'e' and not self.right: self.right = i
        elif slot == 'f' and not self.legs: self.legs = i
        elif slot == 'g' and not self.feet: self.feet = i
        elif slot == 'h' and not self.backpack1: self.backpack1 = i
        elif slot == 'i' and not self.backpack2: self.backpack2 = i
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

    def check(self, slot):
        if   slot == 'a': return self.head
        elif slot == 'b': return self.neck
        elif slot == 'c': return self.trunk
        elif slot == 'd': return self.left
        elif slot == 'e': return self.right
        elif slot == 'f': return self.legs
        elif slot == 'g': return self.feet
        elif slot == 'h': return self.backpack1
        elif slot == 'i': return self.backpack2
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
        elif self.backpack1 == item: self.backpack1 = None
        elif self.backpack2 == item: self.backpack2 = None

    def get_lightradius(self):
        return getattr(self.head,  'lightradius', 0) + \
               getattr(self.neck,  'lightradius', 0) + \
               getattr(self.legs,  'lightradius', 0) + \
               getattr(self.trunk, 'lightradius', 0)

    def get_attack(self):
        return getattr(self.right, 'attack', 0) + \
               getattr(self.left, 'attack', 0) + \
               getattr(self.feet, 'attack', 0)

    def get_defence(self):
        return getattr(self.head, 'defence', 0) + \
               getattr(self.left, 'defence', 0) + \
               getattr(self.trunk, 'defence', 0) + \
               getattr(self.legs, 'defence', 0) + \
               getattr(self.feet, 'defence', 0)

    def get_heatbonus(self):
        return getattr(self.trunk, 'heatbonus', 0) + \
               getattr(self.legs, 'heatbonus', 0)

    def get_confattack(self):
        return getattr(self.right, 'confattack', None)

    def get_psyimmune(self):
        return getattr(self.head, 'psyimmune', None) or \
               getattr(self.right, 'psyimmune', None) or \
               getattr(self.left, 'psyimmune', None)


class Item:
    def __init__(self, name, slot='', bonus=0, count=None, ident=False,
                 skin=('~', libtcod.yellow), lightradius=0, explodes=0,
                 applies=False, liveexplode=None, radius=0, attack=0,
                 defence=0, desc=None, throwable=False, throwrange=8, booze=False,
                 cursedchance=0, range=None, ammochance=None, rangeattack=0,
                 straightline=False, confattack=None, rarity=None, healing=None,
                 homing=False, cooling=False, digging=False, psyimmune=False,
                 rangeexplode=False, springy=False, detector=False,
                 detect_monsters=False, detect_items=False, food=None,
                 tracker=False, wishing=False, repelrange=None, selfdestruct=None,
                 digray=None, jinni=False, heatbonus=0, use_an=False,
                 stackrange=None, mapper=None, converts=None, jumprange=None,
                 explodeimmune=False, telepathyrange=None, makestrap=False,
                 summon=None):
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
        self.rangeattack = rangeattack
        self.straightline = straightline
        self.confattack = confattack
        self.rarity = rarity
        self.healing = healing
        self.homing = homing
        self.cooling = cooling
        self.digging = digging
        self.psyimmune = psyimmune
        self.rangeexplode = rangeexplode
        self.springy = springy
        self.detector = detector
        self.detect_monsters = detect_monsters
        self.detect_items = detect_items
        self.food = food
        self.tracker = tracker
        self.wishing = wishing
        self.repelrange = repelrange
        self.selfdestruct = selfdestruct
        self.digray = digray
        self.jinni = jinni
        self.heatbonus = heatbonus
        self.use_an = use_an
        self.stackrange = stackrange
        self.mapper = mapper
        self.converts = converts
        self.jumprange = jumprange
        self.explodeimmune = explodeimmune
        self.telepathyrange = telepathyrange
        self.makestrap = makestrap
        self.summon = summon

        self.ammo = None
        self.gencount = 0


    def __str__(self):
        s = ''
        if self.ident:
            if self.bonus > 0:
                s += 'blessed '
            elif self.bonus < 0:
                s += 'cursed '
        s += self.name
        if self.count > 1:
            s = str(self.count) + " " + s.replace('$s', 's')
        elif self.count != 0 and len(s) > 0:
            if self.count == 1:
                s = s.replace('$s', '')

            if self.use_an or s[0] in 'aeiouAEIOU':
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

        if self.selfdestruct:
            self.selfdestruct = int(max(random.gauss(*self.selfdestruct), 1))


class ItemStock:
    def __init__(self):
        self.necklamp = Item("miner's lamp", slot='b', lightradius=8, rarity=8,
                             desc=['A lamp that provides light while you are cave-crawling.'])

        self.helmet = Item("miner's hardhat", slot='a', rarity=8,
                           skin=('[', libtcod.sepia), defence=0.25,
                           desc=['A simple plastic item of protective headgear.'])

        self.boots = Item('boots', slot='g', count=0, rarity=8,
                          skin=('[', libtcod.sepia), defence=0.1,
                          desc=['Steel-toed boots made of genuine leather.'])

        self.dynamite = Item('stick$s of dynamite', count=3,
                             skin=('!', libtcod.red), applies=True, explodes=True,
                             radius=4, rarity=8, converts='litdynamite',
                             desc=['Sticks of dynamite can be lit to create an explosive device.'])

        self.minibomb = Item('minibomb$s', count=3, skin=('(', libtcod.pink),
                             applies=True, explodes=True, radius=1, rarity=8,
                             converts='litminibomb',
                             desc=['Tiny hand-held grenades.'])

        self.litdynamite = Item('burning stick of dynamite',
                                skin=('!', libtcod.yellow), explodes=True,
                                liveexplode=7, slot='d', radius=4, throwable=True,
                                desc=['Watch out!!'])

        self.litminibomb = Item('armed minibomb', skin=('!', libtcod.yellow),
                                explodes=True, liveexplode=2, slot='d', radius=1,
                                throwable=True,
                                desc=['Watch out!!'])

        self.bomb = Item('exploding spore', skin=('!', libtcod.yellow), explodes=True,
                         liveexplode=4, slot='d', radius=3, throwable=True,
                         desc=['Uh-oh.'])

        self.pickaxe = Item("miner's pickaxe", slot='e', skin=('(', libtcod.gray),
                            attack=2.0, rarity=8, applies=True, digging=True,
                            desc=['Ostensibly to be used as an aid in traversing the caves,',
                                  'this sporting item is a good makeshift weapon.'])

        self.longsword = Item('longsword', slot='e', skin=('(', libtcod.silver),
                              attack=6.0, rarity=8,
                              desc=['Ye olde assault weapon.'])

        self.excalibur = Item('Excalibur', slot='e', skin=('(', libtcod.silver),
                              attack=7.5, count=0,
                              desc=['A larger-than-life sword.'])

        self.booze = Item("potion$s of booze", slot='d', skin=('!', libtcod.green),
                          booze=True, cursedchance=10, applies=True, stackrange=2,
                          count=1, rarity=10,
                          desc=['Sweet, sweet aqua vitae.',
                                'It helps keep one warm in these horrible caves.'])

        self.homing = Item("dowsing rod", slot='d', skin=(')', libtcod.cyan),
                           applies=True, rarity=8, homing=True,
                           desc=["A low-tech device for finding holes."])

        self.medpack = Item("magic pill$s", slot='d', skin=('%', libtcod.white),
                            rarity=20, applies=True, healing=(3, 0.5),
                            cursedchance=7, stackrange=5, count=1,
                            desc=['A big white pill with a large red cross drawn on one side.'])

        self.mushrooms = Item("mushroom$s", slot='d', skin=('%', libtcod.light_orange),
                              rarity=20, applies=True, food=(3, 0.5),
                              cursedchance=7, stackrange=3, count=1,
                              desc=['A mushroom growing on the cave floor.'])

        self.rpg = Item('RPG launcher', slot='e', skin=('(', libtcod.red),
                        rarity=15, applies=True, rangeexplode=True, range=(4, 15),
                        explodes=True, radius=3, attack=0, ammochance=(1,1),
                        use_an=True,
                        desc=['A metal tube that holds a single explosive rocket.'])

        self.killerwand = Item('killer wand', slot='e', skin=('/', libtcod.red),
                               rarity=5, applies=True, rangeexplode=True, range=(1, 3),
                               explodes=True, radius=0, attack=0, ammochance=(1,1),
                               desc=['A metallic wand with a skull-and-crossbones embossed on it.',
                                     'There is an annoying blinking LED light mounted in the handle.'])

        self.mauser = Item("Mauser C96", slot='e', skin=('(', libtcod.blue),
                           rangeattack=7.0, range=(0,15), ammochance=(0, 10),
                           straightline=True, applies=True, rarity=15,
                           desc=['This antique beauty is a powerful handgun, ',
                                 'though a bit rusty for some reason.'])

        self.ak47 = Item('AK-47', slot='e', skin=('(', libtcod.desaturated_blue),
                         rangeattack=3.5, range=(0, 7), ammochance=(0, 30),
                         straightline=True, applies=True, rarity=15,
                         desc=['A semi-automatic rifle.'])

        self.shotgun = Item('shotgun', slot='e', skin=('(', libtcod.turquoise),
                            rangeattack=14.0, range=(2,5), ammochance=(1,4),
                            straightline=True, applies=True, rarity=15,
                            desc=['A powerful, killer weapon.',
                                  'You learned that much from playing videogames.'])

        self.tazer = Item("tazer", slot='e', skin=('(', libtcod.gray),
                          attack=1.0, confattack=(10, 1), rarity=5,
                          desc=['Very useful for subduing enemies.'])

        self.dartgun = Item('dart gun', slot='e', skin=('(', libtcod.light_crimson),
                            attack=0.5, confattack=(30, 5), rarity=5, range=(0,5),
                            rangeattack=0.5, ammochance=(10,30), straightline=True,
                            applies=True,
                            desc=['A small plastic gun loaded with suspicious-looking darts.'])

        self.tinfoilhat = Item('tin foil hat', slot='a', skin=('[', libtcod.gray),
                               psyimmune=True, rarity=6,
                               selfdestruct=(3000,500),
                               desc=['A metallic hat that protects against attempts of ',
                                     'mind control by various crazies.'])

        self.tinfoilcrystal = Item('crystal of tin', slot='d', skin=('+', libtcod.gray),
                                   psyimmune=True, rarity=6,
                                   selfdestruct=(3000,500),
                                   desc=['A magical crystal of tin.',
                                         'It acts much the same as a tin foil hat.'])

        self.tinstaff = Item('eldritch staff', slot='e', skin=('/', libtcod.gray),
                             psyimmune=True, rarity=5, attack=0.01,
                             desc=['A staff covered with ornate carvings of lovecraftian horrors.',
                                   'It seems to be a powerful psyonic artefact, albeit a useless weapon.'])

        self.coolpack = Item("some cold mud", slot='d', skin=('%', libtcod.light_blue),
                             applies=True, cooling=True, rarity=12, count=0,
                             desc=['A bluish lump of mud. ',
                                   'Useful for tricking predators with infrared vision.'])

        self.tinfoil = Item("tin foil", slot='a', skin=('[', libtcod.lightest_sepia), count=0,
                            psyimmune=True, rarity=12, selfdestruct=(450, 100),
                            desc=['Not as good as a real tin foil hat, but will still help in emergencies.'])

        self.springboots = Item("springy boots", slot='g', count=0,
                                skin=('[', libtcod.pink), defence=0.01, rarity=3,
                                springy=True,
                                desc=['Strange boots with giant springs attached to the soles.'])

        self.spikeboots = Item('spiked boots', slot='g', count=0,
                               skin=('[', libtcod.darkest_gray), attack=1.0, defence=0.05,
                               rarity=5,
                               desc=['These boots have giant spikes attached to them.',
                                   'Very heavy metal.'])

        self.shinypants = Item('shiny pants', slot='f', count=0,
                               skin=('[', libtcod.lightest_yellow), defence=0.01,
                               lightradius=3, rarity=5,
                               desc=["These pants a completely covered in spiffy sparkles and shiny LED's.",
                                     "Here in the caves there is nothing to be ashamed of, really."])

        self.furpants = Item('fur pants', slot='f', count=0,
                             skin=('[', libtcod.gray), defence=0.15, heatbonus=0.005, rarity=5,
                             desc=['Shaggy pants made of fur. You would look like a true barbarian in them.'])

        self.furcoat = Item('fur coat', slot='c',
                             skin=('[', libtcod.gray), defence=0.15, heatbonus=0.005, rarity=5,
                             desc=['A shaggy coat made of fur. You would look like a true barbarian in it.'])

        self.halolamp = Item("halogen lamp", slot='b', lightradius=12, rarity=3,
                             selfdestruct=(1000,100),
                             desc=['A lamp that is somewhat brighter than a generic lamp.'])

        self.helmetlamp = Item("flashlight helmet", slot='a',
                               skin=('[', libtcod.orange), defence=0.15, rarity=8, lightradius=4,
                               desc=['A plastic helmet with a lamp mounted on it.'])

        self.pelorusm = Item('pelorus', slot='b', skin=('"', libtcod.gray),
                            applies=True, detector=True, rarity=3, detect_monsters=True,
                            desc=['A device that looks somewhat like an old cellphone.',
                                  'It comes with a necklace strap, a display and a large antenna.'])

        self.pelorusi = Item('pelorus', slot='b', skin=('"', libtcod.gray),
                            applies=True, detector=True, rarity=3, detect_items=True,
                            desc=['A device that looks somewhat like an old cellphone.',
                                  'It comes with a necklace strap, a display and a large antenna.'])

        self.pelorusim = Item('pelorus', slot='b', skin=('"', libtcod.gray),
                            applies=True, detector=True, rarity=2, detect_monsters=True, detect_items=True,
                            desc=['A device that looks somewhat like an old cellphone.',
                                  'It comes with a necklace strap, a display and a large antenna.'])

        self.gps = Item('GPS tracker', slot='b', skin=('"', libtcod.green),
                        tracker=True, rarity=6, applies=True,
                        desc=["A device that tracks and remembers where you've already been."])

        self.wishing = Item('wand of wishes', slot='e', skin=('/', libtcod.gray),
                            applies=True, wishing=True, rarity=2,
                            desc=['A magic wand.'])

        self.digwandh = Item('wand of digging', slot='e', skin=('/', libtcod.azure),
                             applies=True, digray=(1,0), rarity=4,
                             desc=['A magic wand.'])

        self.digwandv = Item('wand of digging', slot='e', skin=('/', libtcod.azure),
                             applies=True, digray=(0,1), rarity=4,
                             desc=['A magic wand.'])

        self.repellerarmor = Item('repeller armor', slot='c', skin=('[', libtcod.white),
                                  repelrange=3, rarity=3, defence=0.01,
                                  selfdestruct=(1000, 100),
                                  desc=['A vest that proves a portable force-field shileld.'])

        self.vikinghelmet = Item('viking helmet', slot='a', skin=('[', libtcod.green),
                                 rarity=5, defence=0.5,
                                 desc=['An iron helmet with large horns, for extra protection.'])

        self.shield = Item('shield', slot='d', skin=('[', libtcod.dark_green),
                           rarity=5, defence=1.0,
                           desc=['A sturdy wooden shield.'])

        self.metalboots = Item('metal boots', slot='g', skin=('[', libtcod.brass),
                               count=0, rarity=5, defence=0.5,
                               desc=['Heavy boots made out of a single piece of sheet metal.'])

        self.legarmor = Item('leg armor', slot='f', skin=('[', libtcod.copper),
                             count=0, rarity=5, defence=0.5,
                             desc=['Protective iron plates that go on your thighs and shins.'])

        self.ringmail = Item('ring mail', slot='c', skin=('[', libtcod.gold),
                             rarity=5, defence=2.0,
                             desc=['Ye olde body protection armor.'])

        self.magiclamp = Item('magic lamp', slot='d', skin=('(', libtcod.gold),
                              rarity=4, jinni=True, applies=True,
                              desc=['Rub me for a surprise!'])

        self.magicmapper = Item('magic mapper', slot='e', skin=('"', libtcod.light_yellow),
                                rarity=6, applies=True, mapper=4,
                                desc=['A strange device that looks something like a large fishing sonar.'])


        self.portablehole = Item('portable hole$s', slot='d', skin=('`', libtcod.sepia),
                                 rarity=6, applies=True, jumprange=3, stackrange=5,
                                 count=2,
                                 desc=['A portable hole. Used as an escape device.'])

        self.bombsuit = Item('bomb suit', slot='c', skin=('[', libtcod.lightest_yellow),
                             explodeimmune=True, rarity=3, defence=0.1,
                             selfdestruct=(300, 50),
                             desc=['The standard protective suit for bomb squads.'])

        self.psyhelmet = Item('crystal helmet', slot='a', skin=('[', libtcod.white),
                               telepathyrange=6, rarity=6,
                               desc=['An ornate helmet made of crystal.',
                                     'It is a powerful artifact of psyonic magic.'])

        self.stickyglue = Item('sticky glue$s', slot='d', skin=('+', libtcod.light_yellow),
                               applies=True, makestrap=True, rarity=8, count=1,
                               stackrange=4,
                               desc=['A tube of very sticky glue. It can be used to make traps.'])


        self.cclarva = Item('carrion crawler larva', slot='', skin=(',', libtcod.white),
                            rarity=0, summon=('carrion crawler', 2),
                            throwable=True, liveexplode=4,
                            desc=['A tiny larva of the carrion crawler species.'])

        self.regenpool()

    def regenpool(self):
        self._randpool = []
        for x in dir(self):
            i = getattr(self, x)
            if type(i) == type(self.booze) and i.rarity:
                for n in xrange(i.rarity):
                    self._randpool.append(i)


    def get(self, item):
        i = getattr(self, item, None)
        if i:
            r = copy.copy(i)
            r.postprocess()
            return r
        return None

    def find(self, item):
        if len(item) < 3:
            return None

        l = []
        for x in xrange(len(self._randpool)):
            if self._randpool[x].name.replace('$s','').lower().find(item) >= 0:
                l.append((x, self._randpool[x]))

        if len(l) == 0:
            return None

        x = int(random.randint(0, len(l)-1))
        item = l[x][1]
        r = copy.copy(item)
        r.postprocess()
        del self._randpool[l[x][0]]
        return r

    def generate(self, level):
        if len(self._randpool) == 0:
            self.regenpool()

        i = int(random.randint(0, len(self._randpool)-1))
        item = self._randpool[i]

        item.gencount += 1
        r = copy.copy(item)
        r.postprocess()

        del self._randpool[i]

        return r



class Monster:
    def __init__(self, name, skin=('x', libtcod.cyan), count=10, level=1,
                 attack=0.5, defence=0.5, explodeimmune=False, range=11,
                 itemdrop=None, heatseeking=False, desc=[], psyattack=0,
                 psyrange=0, confimmune=False, slow=False, selfdestruct=False,
                 straightline=False, stoneeating=False, sleepattack=False,
                 hungerattack=False, flying=False):
        self.name = name
        self.skin = skin
        self.count = count
        self.level = level
        self.attack = attack
        self.defence = defence
        self.explodeimmune = explodeimmune
        self.range = range
        self.itemdrop = itemdrop
        self.heatseeking = heatseeking
        self.desc = desc
        self.psyattack = psyattack
        self.psyrange = psyrange
        self.confimmune = confimmune
        self.slow = slow
        self.selfdestruct = selfdestruct
        self.straightline = straightline
        self.stoneeating = stoneeating
        self.sleepattack = sleepattack
        self.hungerattack = hungerattack
        self.flying = flying

        self.x = 0
        self.y = 0
        self.known_px = None
        self.known_py = None
        self.did_move = False
        self.do_move = None
        self.do_die = False
        self.hp = 3.0
        self.items = []
        self.confused = 0
        self.glued = 0

    def __str__(self):
        s = self.name
        if self.count > 1:
            if s[0] in 'aeiouAEIOU':
                s = 'an ' + s
            else:
                s = 'a ' + s
        return s


class MonsterStock:
    def __init__(self):
        self.monsters = {}

        self.add(Monster('inebriated bum', skin=('h', libtcod.sepia),
                         attack=0.1, defence=0.2, range=3, level=1,
                         itemdrop='booze', count=9,
                         desc=['A drunken homeless humanoid.']))

        self.add(Monster('lichen', skin=('F', libtcod.light_purple),
                         attack=0.3, defence=0.2, range=1, level=1,
                         itemdrop='mushrooms', confimmune=True, count=9,
                         desc=['Looks yummy.']))

        self.add(Monster('hobbit', skin=('h', libtcod.purple),
                         attack=1.5, defence=0.2, range=8, level=2, count=5,
                         desc=['A nasty, brutish humanoid creature endemic to these caves.']))

        self.add(Monster('gnobold', skin=('k', libtcod.green),
                         attack=1.0, defence=0.7, range=6, level=2, count=5,
                         desc=['A gnome-kobold hybrid.']))

        self.add(Monster('laminaria', skin=('p', libtcod.light_blue),
                         attack=2.0, defence=0.1, range=10, level=3, count=7,
                         heatseeking=True,
                         desc=['Not a delicious condiment, but rather a gigantic pale-blue cave slug.',
                               'Being a cave creature, it seems to lack eyes of any sort.']))

        self.add(Monster('dromedary', skin=('q', libtcod.dark_sepia),
                         attack=0.7, psyattack=0.5, defence=0.6, range=5, psyrange=3, level=3,
                         count=5,
                         desc=['A giant cave lizard with two hemisperical humps.']))

        self.add(Monster('spore plant', skin=('x', libtcod.dark_yellow),
                         attack=0.3, defence=0.2, range=7, level=3,
                         itemdrop='bomb', confimmune=True, count=7,
                         desc=['A large plantlike carnivorous creature.',
                               'It has large bulbous appendages growing out of its stalk.',
                               'It looks like it is radiating heat from the inside.']))

        self.add(Monster('cannibal', skin=('h', libtcod.light_red),
                         attack=7.0, defence=0.01, range=5, level=4,
                         count=4,
                         desc=["A degenerate inhabitant of the caves who feeds on",
                               "other people's flesh for sustenance."]))

        self.add(Monster('nematode', skin=('w', libtcod.yellow),
                         attack=0, psyattack=2.0, defence=0.1, range=30, psyrange=4,
                         level=4, count=5,
                         desc=['A gigantic (5 meter long) yellow worm.',
                               'It has no visible eyes, but instead has a ',
                               'giant, bulging, pulsating brain.']))

        self.add(Monster('spore', skin=('x', libtcod.pink),
                         attack=0, defence=0.2, range=30, level=4,
                         itemdrop='bomb', heatseeking=True, selfdestruct=True,
                         confimmune=True, count=7, flying=True,
                         desc=['A pulsating pink spherical spore, about 1 meter in diameter.',
                               'It is levitating.',
                               'It looks like it is radiating heat from the inside.']))

        self.add(Monster('cthulhumon', skin=('v', libtcod.gray),
                         attack=3.0, psyattack=2.0, defence=1.0, range=8, psyrange=8,
                         level=5, confimmune=True, count=4,
                         desc=['The other Pokemon nobody told you about.']))

        self.add(Monster('giant turtle', skin=('O', libtcod.green),
                         attack=1.0, defence=24.0, explodeimmune=True, range=30,
                         confimmune=True, slow=True, level=5, count=4,
                         desc=['A giant, the size of a small house, turtle!']))

        self.add(Monster('shaihulud', skin=('W', libtcod.gray),
                         attack=2.0, defence=4.5, explodeimmune=True, range=30,
                         level=6, count=4, straightline=True, stoneeating=True,
                         heatseeking=True,
                         desc=['A giant worm. It is gray in color and has a skin made of something like granite.',
                               'It is about 15 meters in length.']))

        self.add(Monster('sleep faerie', skin=('f', libtcod.light_pink),
                         attack=1.0, defence=1.0, range=9, level=6, count=5,
                         sleepattack=True, flying=True,
                         desc=["A tiny fay creature dressed in pink ballet clothes.",
                               "It looks adorable."]))

        self.add(Monster('leipreachan', skin=('f', libtcod.azure),
                         attack=2.5, defence=1.5, range=9, level=7, count=5,
                         hungerattack=True,
                         desc=['A fay creature in the form of a dirty, lecherous old man.']))

        self.add(Monster('black knight', skin=('k', libtcod.darker_grey),
                         attack=6.0, defence=4.5, range=8, level=7, count=5,
                         desc=['An evil humanoid in black cast-iron armor.',
                               'He is armed with a longsword.']))

        self.add(Monster('juggernaut', skin=('k', libtcod.darkest_grey),
                         attack=6.0, defence=4.5, range=8, level=8, count=5,
                         desc=['A larger, comically deformed version of the black knight.',
                               'He has ridiculously bulging muscles and a tiny head.']))

        self.add(Monster('carrion crawler', skin=('w', libtcod.white),
                         attack=2.0, defence=2.0, range=5, level=8, count=16,
                         itemdrop='cclarva',
                         desc=['A creature that looks like a maggot,',
                               'only a thousand times bigger.']))

        self.add(Monster('Oberon', skin=('F', libtcod.purple),
                         attack=3.0, defence=3.0, range=10, level=9, count=1,
                         flying=True, explodeimmune=True, confimmune=True,
                         psyrange=8, psyattack=2.0,
                         desc=['A faerie king.',
                               'He takes on the appearance of a 2 meter tall',
                               'handsome man, wearing a delicate crown.']))

        self.add(Monster('Conan', skin=('K', libtcod.sepia),
                         attack=7.5, defence=5.5, range=8, level=10, count=1,
                         confimmune=True, itemdrop='excalibur',
                         desc=['A well-muscled adventurer,',
                               'he looks like he just stepped off a movie poster.',
                               "He hates competition."]))


    def add(self, mon):
        if mon.level not in self.monsters:
            self.monsters[mon.level] = [mon]
        else:
            self.monsters[mon.level].append(mon)

    def find(self, name, n, itemstock):
        for v in self.monsters.itervalues():
            for m in v:
                if m.name == name:
                    l = []
                    for x in xrange(n):
                        mm = copy.copy(m)
                        if mm.itemdrop:
                            item = itemstock.get(mm.itemdrop)
                            mm.items = [item]
                        l.append(mm)
                    return l

        return []

    def generate(self, level, itemstock):
        while level > 0 and level not in self.monsters:
            level -= 1

        m = self.monsters[level]
        m = copy.copy(m[random.randint(0, len(m)-1)])

        if m.itemdrop:
            i = itemstock.get(m.itemdrop)
            if i:
                m.items = [i]

        return m

    def death(self, mon):
        if mon.level not in self.monsters:
            return (len(self.monsters) == 0)

        m = self.monsters[mon.level]

        for x in range(len(m)):
            if mon.name == m[x].name:
                if m[x].count == 1:
                    del m[x]
                else:
                    m[x].count -= 1
                break

        if len(m) == 0:
            del self.monsters[mon.level]

        return (len(self.monsters) == 0)



class World:

    def __init__(self):
        self.grid = None

        self.walkmap = None
        self.watermap = None
        self.featmap = {}
        self.exit = None
        self.itemap = {}
        self.monmap = {}
        self.visitedmap = {}

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
        self.forcedsleep = False
        self.resting = False
        self.cooling = 0
        self.digging = None
        self.blind = False
        self.mapping = 0
        self.glued = 0

        self.floorpath = None

        self.monsters_in_view = []

        self.killed_monsters = []

        self._seed = None
        self._inputs = []




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

        self.visitedmap = {}

        return self.grid, self.walkmap

    def make_map(self):
        self.tcodmap = libtcod.map_new(self.w, self.h)
        for x in xrange(self.w):
            for y in xrange(self.h):
                if (x,y) in self.walkmap:
                    v = True
                    w = True
                else:
                    v = False
                    w = False

                if (x,y) in self.featmap and self.featmap[(x, y)] == '*':
                    v = False

                libtcod.map_set_properties(self.tcodmap, x, y, v, w)

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
            if m:
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
                if (x, y) not in self.itemap:
                    self.itemap[(x, y)] = [item]
                else:
                    self.itemap[(x, y)].append(item)

        for pl,dl,itm in self.bones:
            if dl == self.dlev and len(itm) > 0:
                itm2 = [copy.copy(i) for i in itm]

                x, y = ll[random.randint(0, len(ll)-1)]

                if (x, y) not in self.itemap:
                    self.itemap[(x,y)] = itm2
                else:
                    self.itemap[(x,y)].extend(itm2)


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
            if (x,y) in self.walkmap and (x,y) not in self.monmap:
                self.px = x
                self.py = y
                return

        self.stats = Stats()

    def generate_inv(self):
        self.inv.take(self.itemstock.find('lamp'))
        l = [self.itemstock.get('pickaxe')]
        for x in range(3):
            l.append(self.itemstock.generate(1))
        if (self.px, self.py) not in self.itemap:
            self.itemap[(self.px, self.py)] = l
        else:
            self.itemap[(self.px, self.py)].extend(l)

        #self.inv.take(self.itemstock.get('necklamp'))
        #self.inv.take(self.itemstock.get('helmet'))
        #self.inv.take(self.itemstock.get('boots'))

        #self.itemap[(self.px, self.py)] = [
        #            self.itemstock.get('dynamite'),
        #            self.itemstock.get('mauser'),
        #            self.itemstock.get('pickaxe'),
        #            self.itemstock.get('tazer')]


    def move(self, _dx, _dy, do_spring=True):

        if self.glued > 0:
            self.glued -= 1
            if self.glued == 0:
                self.msg.m('You dislodge yourself from the glue.')
                del self.featmap[(self.px, self.py)]
            else:
                self.msg.m('You are stuck in the glue!')
                self.tick()
                return

        dx = _dx + self.px
        dy = _dy + self.py
        if (dx,dy) in self.walkmap and dx >= 0 and dx < self.w and dy < self.h:

            if (dx, dy) in self.monmap:
                self.fight(self.monmap[(dx, dy)], True)
                self.tick()
                return
            else:
                self.px = dx
                self.py = dy

                if (dx, dy) not in self.visitedmap:
                    self.visitedmap[(dx, dy)] = 0

                if (self.px, self.py) in self.itemap:
                    if len(self.itemap[(self.px, self.py)]) > 1:
                        self.msg.m("You see several items here.")
                    else:
                        self.msg.m("You see " + str(self.itemap[(self.px, self.py)][0]) + '.')

                if (self.px, self.py) in self.featmap and \
                    self.featmap[(self.px, self.py)] == '^':
                        self.msg.m('You just stepped in some glue!', True)
                        self.glued = max(int(random.gauss(*self.coef.glueduration)), 1)


        else:
            return

        if do_spring and self.inv.feet and self.inv.feet.springy:
            self.move(_dx, _dy, do_spring=False)
            return

        self.tick()

    def tick(self):
        self.stats.tired.dec(self.coef.movetired)
        self.stats.sleep.dec(self.coef.movesleep)
        self.stats.thirst.dec(self.coef.movethirst)
        self.stats.hunger.dec(self.coef.movehunger)
        if (self.px, self.py) in self.watermap or self.cooling:
            self.stats.warmth.dec(self.coef.watercold)
        else:
            self.stats.warmth.inc(self.inv.get_heatbonus())
        self.tick_checkstats()

    def tick_checkstats(self):

        for i in self.inv:
            if i and i.liveexplode > 0:
                i.liveexplode -= 1
                if i.liveexplode == 0:
                    if i.summon:
                        self.summon(self.px, self.py, i.summon[0], i.summon[1])
                    else:
                        self.explode(self.px, self.py, i.radius)
                    self.inv.purge(i)

            elif i and i.selfdestruct > 0:
                i.selfdestruct -= 1
                #print '-', i.selfdestruct, i.name
                if i.selfdestruct == 0:
                    self.msg.m('Your ' + i.name + ' falls apart!', True)
                    self.inv.purge(i)

        if self.cooling > 0:
            self.cooling -= 1
            if self.cooling == 0:
                self.msg.m("Your layer of cold mud dries up.")

        if self.dead: return

        if self.stats.warmth.x <= -3.0:
            self.msg.m("Being so cold makes you sick!", True)
            self.stats.health.dec(self.coef.colddamage, "cold")
            if self.resting: self.resting = False
            if self.digging: self.digging = None

        if self.stats.thirst.x <= -3.0:
            self.msg.m('You desperately need something to drink!', True)
            self.stats.health.dec(self.coef.thirstdamage, "thirst")
            if self.resting: self.resting = False
            if self.digging: self.digging = None

        if self.stats.hunger.x <= -3.0:
            self.msg.m('You desperately need something to eat!', True)
            self.stats.health.dec(self.coef.hungerdamage, "hunger")
            if self.resting: self.resting = False
            if self.digging: self.digging = None

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
        else:
            self.stats.warmth.inc(self.inv.get_heatbonus())
        self.tick_checkstats()

    def sleep(self):
        self.stats.tired.inc(self.coef.sleeptired)
        self.stats.sleep.inc(self.coef.sleepsleep)
        self.stats.thirst.dec(self.coef.sleepthirst)
        self.stats.hunger.dec(self.coef.sleephunger)
        if (self.px, self.py) in self.watermap or self.cooling:
            self.stats.warmth.dec(self.coef.watercold)
        else:
            self.stats.warmth.inc(self.inv.get_heatbonus())
        self.tick_checkstats()

        if self.sleeping > 0:
            self.sleeping -= 1
        else:
            self.forcedsleep = False

    def start_sleep(self, force = False, quick = False, realforced = False):
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
        self.digging = None
        self.resting = False

        if realforced:
            self.forcedsleep = True

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
            self.stats.health.dec(x-self.coef.waterpois, "unclean water")
            self.msg.m('This water has a bad smell.')
        else:
            self.msg.m('You drink from the puddle.')

        self.tick()

    def convert_to_floor(self, x, y, rubble=0):
        self.walkmap.add((x,y))
        if rubble == 0:
            if (x,y) in self.featmap and self.featmap[(x,y)] == '*':
                del self.featmap[(x,y)]
        elif rubble == 1:
            if (x, y) not in self.featmap:
                self.featmap[(x,y)] = '*'

        libtcod.map_set_properties(self.tcodmap, x, y, True, True)


    def showinv(self):
        return self.inv.draw(self.w, self.h, self.dlev, self.plev)


    def showinv_apply(self):
        slot = self.inv.draw(self.w, self.h, self.dlev, self.plev)
        i = self.inv.drop(slot)
        if not i:
            if slot in 'abcdefghi':
                self.msg.m('You have no item in that slot.')
            return

        if not i.applies:
            self.msg.m('This item cannot be applied.')
            self.inv.take(i, slot)
            return

        i2 = self.apply(i)
        if i2:
            self.inv.take(i2)
        else:
            if i.count > 0:
                i.count -= 1
            if i.count > 0:
                self.inv.take(i)

        self.tick()


    def slot_to_name(self, slot):
        if slot == 'a': return 'head'
        elif slot == 'b': return 'neck'
        elif slot == 'c': return 'trunk'
        elif slot == 'd': return 'left hand'
        elif slot == 'e': return 'right hand'
        elif slot == 'f': return 'legs'
        elif slot == 'g': return 'feet'
        else: return 'backpack'


    def showinv_interact(self):
        slot = self.inv.draw(self.w, self.h, self.dlev, self.plev)
        i = self.inv.drop(slot)
        if not i:
            if slot in 'abcdefghi':
                self.msg.m('You have no item in that slot.')
            return

        si = str(i)
        si = si[0].upper() + si[1:]
        s = [si + ':', '']
        choices = 'd'


        if i.applies:
            s.append('a) use it')
            choices += 'a'

        if not self.inv.backpack1 or not self.inv.backpack2:
            s.append('b) move it to a backpack slot')
            choices += 'b'

        if i.desc:
            s.append('c) examine this item')
            choices += 'c'

        s.append('d) drop this item')
        if i.throwable:
            s.append('f) throw this item')
            choices += 'f'

        if i.slot in 'abcdefg' and slot in 'hi':
            s.append('x) swap this item with item in equipment')
            choices += 'x'

        s.append('')
        s.append('any other key to equip it')
        cc = draw_window(s, self.w, self.h)

        if cc not in choices:
            self.inv.take(i)
            self.tick()
            return

        if cc == 'a' and i.applies:
            i2 = self.apply(i)
            if i2:
                self.inv.take(i2)
            else:
                if i.count > 0:
                    i.count -= 1
                if i.count > 0:
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
            ss = i.desc[:]
            ss.append('')
            ss.append('Slot: ' + self.slot_to_name(i.slot))
            draw_window(ss, self.w, self.h)
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

        elif cc == 'x':
            item2 = self.inv.drop(i.slot)
            self.inv.take(i)
            if item2:
                self.inv.take(item2)

        else:
            self.inv.take(i)
            self.tick()

    def apply(self, item):
        if not item.applies:
            return item

        if item.converts:
            inew = self.itemstock.get(item.converts)

            if self.inv.check(inew.slot) is not None:
                self.msg.m('Your ' + self.slot_to_name(inew.slot) + ' slot needs to be free to use this.')
                return item

            self.inv.take(inew)
            s = str(inew)
            s = s[0].upper() + s[1:]
            self.msg.m(s + ' is now in your ' + self.slot_to_name(inew.slot) + ' slot!', True)

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
                self.msg.m('This pill makes your eyes pop out of their sockets!', True)
                self.stats.tired.dec(max(random.gauss(*item.healing), 0))
                self.stats.sleep.dec(max(random.gauss(*item.healing), 0))
            else:
                self.msg.m('Eating this pill makes you dizzy.')
                self.stats.health.inc(max(random.gauss(*item.healing), 0))
                self.stats.hunger.dec(max(random.gauss(*item.healing), 0))
                self.stats.sleep.dec(max(random.gauss(*item.healing), 0))
            return None

        elif item.food:
            if item.bonus < 0:
                self.msg.m('Yuck, eating this makes you vomit!', True)
                self.stats.hunger.dec(max(random.gauss(*item.food), 0))
            else:
                self.msg.m('Mm, yummy.')
                self.stats.hunger.inc(max(random.gauss(*item.food), 0))
            return None

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
            else:
                self.msg.m('You are at the spot. Look around.')

        elif item.tracker:
            self.visitedmap[(self.px, self.py)] = 1
            self.msg.m("You mark this spot in your tracker's memory.")

        elif item.detector:
            s = []
            if item.detect_monsters:
                s.append('You detect the following monsters:')
                for v in self.monmap.itervalues():
                    s.append('  '+str(v))
                s.append('')

            if item.detect_items:
                s.append('You detect the following items:')
                for v in self.itemap.itervalues():
                    for vv in v:
                        s.append('  '+str(vv))
                s.append('')

            if len(s) > 19:
                s = s[:19]
                s.append('(There is more information, but it does not fit on the screen)')

            draw_window(s, self.w, self.h)


        elif item.cooling:
            self.cooling = max(int(random.gauss(*self.coef.coolingduration)), 1)
            self.msg.m("You cover yourself in cold mud.")
            return None

        elif item.wishing:
            self.wish()
            return None

        elif item.mapper:
            self.mapping = item.mapper
            return None

        elif item.jinni:
            l = []
            for x in xrange(-1, 2):
                for y in xrange(-1, 2):
                    if x != 0 or y != 0:
                        q = (self.px + x, self.py + y)
                        if q in self.walkmap and q not in self.monmap:
                            l.append(q)

            if len(l) == 0:
                self.msg.m('Nothing happened.')
                return None

            jinni = Monster('Jinni', level=self.plev+1,
                            attack=max(self.inv.get_attack(), 0.5),
                            defence=self.inv.get_defence(),
                            range=self.inv.get_lightradius(),
                            skin=('&', libtcod.yellow),
                            desc=['A supernatural fire fiend.'])

            self.msg.m('A malevolent spirit appears!')
            q = l[random.randint(0, len(l)-1)]
            jinni.x = q[0]
            jinni.y = q[1]
            jinni.items = [self.itemstock.get('wishing')]
            self.monmap[q] = jinni
            return None

        elif item.digray:
            if item.digray[0] == 1:
                for x in xrange(0, self.w):
                    self.convert_to_floor(x, self.py)
            if item.digray[1] == 1:
                for y in xrange(0, self.h):
                    self.convert_to_floor(self.px, y)
            self.msg.m('The wand explodes in a brilliant white flash!')
            return None

        elif item.jumprange:
            l = []
            for x in xrange(self.px - item.jumprange, self.px + item.jumprange + 1):
                for y in [self.py - item.jumprange, self.px + item.jumprange]:
                    if (x,y) in self.walkmap:
                        l.append((x,y))

            for y in xrange(self.py - item.jumprange - 1, self.py + item.jumprange):
                for x in [self.px - item.jumprange, self.px + item.jumprange]:
                    if (x,y) in self.walkmap:
                        l.append((x,y))

            l = l[random.randint(0, len(l)-1)]
            self.px = l[0]
            self.py = l[1]
            return None

        elif item.makestrap:
            if (self.px,self.py) in self.featmap:
                self.msg.m('Nothing happens.')
                return item

            if (self.px,self.py) in self.watermap:
                self.msg.m("That won't work while you're standing on water.")
                return item

            self.featmap[(self.px, self.py)] = '^'
            self.msg.m('You spread the glue liberally on the floor.')
            return None

        elif item.rangeattack or item.rangeexplode:
            if item.ammo <= 0:
                self.msg.m("It's out of ammo!")
                return item

            while 1:
                nx, ny = self.target(item.range[1],
                                     minrange=item.range[0],
                                     monstop=item.straightline)
                if nx is not None:
                    break
            #print '//', nx, ny
            if nx < 0:
                return item

            item.ammo -= 1

            if item.rangeexplode:
                self.explode(nx, ny, item.radius)
            else:
                if (nx, ny) in self.monmap:
                    self.fight(self.monmap[(nx, ny)], True, item=item)

            if item.ammo <= 0:
                return None


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



    def take(self):
        if (self.px, self.py) not in self.itemap:
            self.msg.m('You see no item here to take.')
            return

        items = self.itemap[(self.px, self.py)]

        c = 0
        if len(items) > 1:
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

        i = items[c]

        did_scavenge = False

        for ii in self.inv:
            if ii and ii.name == i.name:
                if ii.stackrange and ii.count < ii.stackrange:
                    n = min(ii.stackrange - ii.count, i.count)
                    ii.count += n
                    i.count -= n

                    self.msg.m('You now have ' + str(ii))
                    did_scavenge = True

                    if i.count == 0:
                        del items[c]
                        if len(items) == 0:
                            del self.itemap[(self.px, self.py)]
                            break

                elif i.ammo > 0 and ii.ammo and ii.ammo < ii.ammochance[1]:
                    n = min(ii.ammochance[1] - ii.ammo, i.ammo)
                    ii.ammo += n
                    i.ammo -= n
                    self.msg.m("You find some ammo for your " + ii.name)
                    did_scavenge = True

        if did_scavenge:
            self.tick()
            return

        ok = self.inv.take(i)
        if ok:
            self.msg.m('You take ' + str(i) + '.')
            del items[c]
            if len(items) == 0:
                del self.itemap[(self.px, self.py)]
        else:
            self.msg.m('You have no free inventory slot for ' + str(i) + '!')

        self.tick()


    def handle_mondeath(self, mon, do_drop=True, do_gain=True):
        if do_gain and mon.level > self.plev:
            self.msg.m('You just gained level ' + str(mon.level) + '!', True)
            self.plev = mon.level

        if do_drop:
            if len(mon.items) > 0:
                if (mon.x, mon.y) in self.itemap:
                    self.itemap[(mon.x, mon.y)].extend(mon.items)
                else:
                    self.itemap[(mon.x, mon.y)] = mon.items

        if do_gain:
            self.killed_monsters.append((mon.level, self.plev, self.dlev, mon.name))

        if self.monsterstock.death(mon):
            while 1:
                c = draw_window(['Congratulations! You have won the game.', '', 'Press space to exit.'], self.w, self.h)
                if c == ' ': break

            self.stats.health.reason = 'winning'
            self.dead = True


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

            if x == self.px and y == self.py and \
                not (self.inv.trunk and self.inv.trunk.explodeimmune):
                self.stats.health.dec(6.0, "explosion")
                self.tick_checkstats()

            if (x, y) in self.itemap:
                for i in self.itemap[(x, y)]:
                    if i.explodes:
                        chains.add((x, y, i.radius))
                        break
                del self.itemap[(x, y)]

            if (x, y) in self.monmap:
                mon = self.monmap[(x, y)]
                if not mon.explodeimmune:
                    self.handle_mondeath(mon, do_drop=False)

                    for i in mon.items:
                        if i.explodes:
                            chains.add((x, y, i.radius))
                            break

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

        if player_move and item:
            plev = min(max(self.plev - d + 1, 1), self.plev)
            attack = item.rangeattack
            #print '+', d, plev, attack
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
            #print ' ->', ret, ':', attack, leva, '/', defence, levd
            return ret

        if player_move:

            defence = mon.defence
            if mon.glued:
                defence /= self.coef.gluedefencepenalty

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

                if ca and dmg > 0 and not mon.confimmune:
                    self.msg.m(smu + ' looks totally dazed!')
                    mon.confused += int(max(random.gauss(*ca), 1))

            if dmg > 0:
                mon.known_px = self.px
                mon.known_py = self.py


        else:

            attack = None
            defence = None
            psy = False

            if d > 1 and mon.psyattack > 0:
                if self.inv.get_psyimmune():
                    return
                attack = mon.psyattack
                defence = self.coef.unarmeddefence
                psy = True
            else:
                attack = mon.attack
                defence = max(self.inv.get_defence(), self.coef.unarmeddefence)
                if self.glued:
                    defence /= self.coef.gluedefencepenalty


            if attack == 0:
                return

            dmg = roll(attack, mon.level, defence, plev)

            if psy:
                if dmg > 0:
                    self.msg.m(smu + ' is attacking your brain!')
            else:
                if dmg > 0:
                    self.msg.m(smu + ' hits!')
                else:
                    self.msg.m(smu + ' misses.')

            if mon.sleepattack:
                self.msg.m('You fall asleep!')
                self.start_sleep(force=True, quick=True, realforced=True)
                self.tick_checkstats()
                return

            if mon.hungerattack:
                self.stats.hunger.dec(dmg)
            else:
                self.stats.health.dec(dmg, sm)

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
                    elif f == '^':
                        s.append('You see a cave floor covered with glue.')
                    elif f == '*':
                        s.append('You see rubble.')

                elif (tx, ty) in self.walkmap:
                    if (tx, ty) in self.watermap:
                        s.append('You see a water-covered floor.')
                    else:
                        s.append('You see a cave floor.')

                else:
                        s.append('You see a cave wall.')

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

        self.draw(False)

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

            if tmpx is None:
                return (xx, yy)

            if (tmpx, tmpy) in self.walkmap:
                if minrange:
                    d = math.sqrt(math.pow(abs(tmpx - self.px), 2) +
                                  math.pow(abs(tmpy - self.py), 2))
                    if d < minrange:
                        continue

                xx = tmpx
                yy = tmpy

                if monstop and (tmpx, tmpy) in self.monmap:
                    return (xx, yy)

            else:
                return (xx, yy)


    def show_messages(self):
        self.msg.show_all(self.w, self.h)


    def wish(self):
        s = ''
        while 1:
            k = draw_window(['Whish for what? : ' + s], self.w, self.h)
            k = k.lower()
            if k in "abcdefghijklmnopqrstuvwxyz' ":
                s = s + k
            elif ord(k) == 8 or ord(k) == 127:
                if len(s) > 0:
                    s = s[:-1]
            elif k in '\r\n':
                break

        i = self.itemstock.find(s)

        if not i:
            self.msg.m('Nothing happened!')
        else:
            self.msg.m('Suddenly, ' + str(i) + ' appears at your feet!')
            if (self.px, self.py) in self.itemap:
                self.itemap[(self.px, self.py)].append(i)
            else:
                self.itemap[(self.px, self.py)] = [i]


    def move_down(self): self.move(0, 1)
    def move_up(self): self.move(0, -1)
    def move_left(self): self.move(-1, 0)
    def move_right(self): self.move(1, 0)
    def move_upleft(self): self.move(-1, -1)
    def move_upright(self): self.move(1, -1)
    def move_downleft(self): self.move(-1, 1)
    def move_downright(self): self.move(1, 1)

    def quit(self):
        k = draw_window(["Really quit? Press 'y' if you are truly sure."], self.w, self.h)
        if k == 'y':
            self.stats.health.reason = 'quitting'
            self.done = True
            self.dead = True


    def show_help(self):
        s = ['',
             "Movement keys: roguelike 'hjkl' 'yubn' or the arrow keys.",
             "               NOTE! To move diagonally, use 'yubn'.",
             " . : Stand on one place for one turn.",
             " s : Start sleeping.",
             " r : Start resting.",
             " q : Drink from the floor.",
             " > : Descend down to the next level.",
             " a : Apply (use) an item from your inventory.",
             " i : Manipulate your inventory.",
             " d : Drop an item from your inventory.",
             " , : Pick up an item from the floor.",
             " / : Look around at the terrain, items and monsters.",
             " P : Show a log of previous messages.",
             " Q : Quit the game by committing suicide.",
             " S : Save the game and quit.",
             " ? : Show this help."
        ]
        draw_window(s, self.w, self.h)


    def gainlev(self):
        self.plev += 1

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
            'a': self.showinv_apply,
            'i': self.showinv_interact,
            '>': self.descend,
            'd': self.drop,
            ',': self.take,
            '/': self.look,
            'P': self.show_messages,
            'Q': self.quit,
            '?': self.show_help,
            'S': self.save

            #'z': self.gainlev,
            #'x': self.debug_descend,
            #'w': self.wish
            }
        self.vkeys = {
            libtcod.KEY_LEFT: self.move_left,
            libtcod.KEY_RIGHT: self.move_right,
            libtcod.KEY_UP: self.move_up,
            libtcod.KEY_DOWN: self.move_down
            }


    def walk_monster(self, mon, dist, x, y):

        if mon.slow and (self.t & 1) == 0:
            return None, None

        if mon.glued > 0:
            mon.glued -= 1
            if mon.glued == 0:
                del self.featmap[(mon.x, mon.y)]
            else:
                return None, None

        if dist > mon.range or mon.confused or (mon.sleepattack and self.sleeping):
            mdx = x + random.randint(-1, 1)
            mdy = y + random.randint(-1, 1)
            if (mdx, mdy) not in self.walkmap:
                mdx = None
                mdy = None
            if mon.confused:
                mon.confused -= 1

        else:

            if mon.psyrange > 0 and dist <= mon.psyrange:
                self.fight(mon, False)

            if mon.known_px is None or mon.known_py is None:
                mon.known_px = self.px
                mon.known_py = self.py

            elif self.inv.trunk and self.inv.trunk.repelrange and \
                 dist <= self.inv.trunk.repelrange and dist > 1:
                 return None, None

            elif mon.heatseeking and \
                 ((self.px, self.py) in self.watermap or self.cooling):
                pass
            else:
                mon.known_px = self.px
                mon.known_py = self.py

            if mon.straightline:
                libtcod.line_init(x, y, mon.known_px, mon.known_py)
                mdx, mdy = libtcod.line_step()
            else:
                libtcod.path_compute(self.floorpath, x, y, mon.known_px, mon.known_py)
                mdx, mdy = libtcod.path_walk(self.floorpath, True)

        if mon.stoneeating:
            if mdx is not None:
                if (mdx, mdy) not in self.walkmap:
                    self.convert_to_floor(mdx, mdy, rubble=1)

        return mdx, mdy

    def process_monstep(self, mon):
        mdx = mon.x
        mdy = mon.y

        if (mdx, mdy) in self.featmap and self.featmap[(mdx, mdy)] == '^' and not mon.flying:
            mn = str(mon)
            mn = mn[0].upper() + mn[1:]
            self.msg.m(mn + ' gets stuck in some glue!')
            mon.glued = max(int(random.gauss(*self.coef.glueduration)), 1)


    def summon(self, x, y, monname, n):
        m = self.monsterstock.find(monname, n, self.itemstock)
        if len(m) == 0:
            return

        l = []
        for xx in xrange(x-1,x+2):
            for yy in xrange(y-1,y+2):
                if (xx,yy) in self.walkmap and \
                   (xx,yy) not in self.monmap and \
                   (xx != self.px or yy != self.py):
                    l.append((xx,yy))

        for i in xrange(len(m)):
            if len(l) == 0:
                return
            j = random.randint(0, len(l)-1)
            xx,yy = l[j]
            del l[j]

            m[i].x = xx
            m[i].y = yy
            self.monmap[(xx, yy)] = m[i]

    def process_world(self):

        explodes = set()
        mons = []
        delitems = []

        for k,v in self.itemap.iteritems():
            for i in v:
                if i.liveexplode > 0:
                    i.liveexplode -= 1
                    if i.liveexplode == 0:
                        if i.summon:
                            self.summon(k[0], k[1], i.summon[0], i.summon[1])
                            delitems.append(k)
                        else:
                            explodes.add((k[0], k[1], i.radius))

        for ix,iy in delitems:
            for i in xrange(len(self.itemap[(ix,iy)])):
                if self.itemap[(ix,iy)][i].liveexplode == 0:
                    del self.itemap[(ix,iy)][i]
                    if len(self.itemap[(ix,iy)]) == 0:
                        del self.itemap[(ix,iy)]

        for k,mon in self.monmap.iteritems():
            if not mon.did_move:
                x, y = k
                dist = math.sqrt(math.pow(abs(self.px - x), 2) + math.pow(abs(self.py - y), 2))

                mdx, mdy = self.walk_monster(mon, dist, x, y)

                if mdx is not None:
                    if mdx == self.px and mdy == self.py:
                        if mon.selfdestruct:
                            smu = str(mon)
                            smu = smu[0].upper() + smu[1:]
                            self.msg.m(smu + ' suddenly self-destructs!')
                            self.handle_mondeath(mon, do_gain=False)
                            mon.do_die = True
                        else:
                            self.fight(mon, False)
                    else:
                        mon.do_move = (mdx, mdy)

                    mon.did_move = True
                    mons.append(mon)

        for mon in mons:
            if mon.do_move:
                mon.old_pos = (mon.x, mon.y)
                del self.monmap[(mon.x, mon.y)]
            elif mon.do_die:
                del self.monmap[(mon.x, mon.y)]

        for mon in mons:
            if mon.do_move:
                if mon.do_move in self.monmap:
                    mon.do_move = mon.old_pos

                mon.x = mon.do_move[0]
                mon.y = mon.do_move[1]
                self.monmap[mon.do_move] = mon
                mon.do_move = None

                self.process_monstep(mon)

            mon.did_move = False

        for x, y, r in explodes:
            del self.itemap[(x, y)]
            self.explode(x, y, r)



    def draw(self, withtime=True, _hlx=None, _hly=None):
        back = libtcod.black

        lightradius = min(max(self.inv.get_lightradius(), 2), 15)

        if self.blind:
            lightradius /= 2

        if self.mapping > 0:
            if withtime:
                self.mapping -= 1
            if self.mapping > 0:
                lightradius = 25


        libtcod.map_compute_fov(self.tcodmap, self.px, self.py, lightradius,
                                True, libtcod.FOV_RESTRICTIVE)

        monsters_in_view = []
        did_highlight = False

        if withtime:
            self.process_world()


        for x in xrange(self.w):
            for y in xrange(self.h):

                fore = libtcod.lightest_green

                if self.inv.neck and self.inv.neck.tracker:
                    if (x, y) in self.visitedmap:
                        if self.visitedmap[(x, y)]:
                            back = libtcod.red
                        else:
                            back = libtcod.darkest_gray
                    else:
                        back = libtcod.black

                if self.mapping:
                    in_fov = True
                else:
                    in_fov = libtcod.map_is_in_fov(self.tcodmap, x, y)

                is_lit = False

                if self.inv.head and self.inv.head.telepathyrange:
                    if (x, y) in self.monmap:
                        d = math.sqrt(math.pow(abs(y - self.py),2) + math.pow(abs(x - self.px),2))
                        if d <= self.inv.head.telepathyrange:
                            in_fov = True
                            is_lit = True


                if not in_fov:
                    c = ' '
                    fore = libtcod.black

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
                        if f == '^':
                            c = 250
                            fore = libtcod.red
                        else:
                            c = f

                    elif (x, y) in self.walkmap:
                        if (x,y) in self.watermap:
                            c = '-'
                            fore = libtcod.dark_azure #libtcod.Color(80, 80, 255)
                        else:
                            c = 250
                    else:
                        if (x,y) in self.watermap:
                            fore = libtcod.desaturated_blue #libtcod.Color(100, 128, 255)
                        c = '#'

                    if not is_lit:
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


        # hack
        if withtime:
            self.monsters_in_view = []
            for mon in monsters_in_view:
                if (mon.x, mon.y) in self.monmap:
                    self.monsters_in_view.append(mon)

        if withtime:
            self.t += 1

        return did_highlight


    def save(self):
        f = None
        atts = [
          'grid', 'walkmap', 'watermap', 'exit', 'itemap', 'monmap', 'visitedmap',
          'featmap', 'px', 'py', 'w', 'h',
          'done', 'dead', 'stats', 'msg', 'coef', 'inv', 'itemstock', 'monsterstock',
          'dlev', 'plev', 't', 'sleeping', 'resting', 'cooling', 'digging', 'blind',
          'mapping', 'glued',
          'killed_monsters', '_seed', '_inputs'
          ]
        state = {}

        for x in atts:
            state[x] = getattr(self, x)

        if 1: #try:
            f = open('savefile', 'w')
            cPickle.dump(state, f)
        #except:
        #    return
        self.msg.m('Saved!')
        self.done = True


    def load_bones(self):
        self.bones = []
        try:
            bf = open('bones', 'r')
            self.bones = cPickle.load(bf)
        except:
            pass


    def load(self):
        f = None
        state = None

        try:
            f = open('savefile', 'r')
            state = cPickle.load(f)
        except:
            return False
        #print 'LOADING!'

        for k,v in state.iteritems():
            setattr(self, k, v)

        random.seed(self._seed)
        global _inputs
        _inputs = self._inputs

        self.make_map()
        self.make_paths()
        return True


    def form_highscore(self):

        hs = {'plev': self.plev,
              'dlev': self.dlev,
              'kills': self.killed_monsters,
              'reason': self.stats.health.reason,
              'seed': self._seed,
              'inputs': self._inputs,
              'bones': self.bones,
              'version': _version}

        # Clobber the savefile.
        try:
            open('savefile', 'w').truncate(0)
        except:
            pass

        # Append to highscore.
        hss = []
        try:
            hsf = open('highscore', 'r')
            hss = cPickle.load(hsf)
        except:
            pass

        hss.append(hs)

        try:
            hsf = open('highscore', 'w')
            cPickle.dump(hss, hsf)
        except:
            pass


        # Form bones.
        bones = []
        try:
            bf = open('bones', 'r')
            bones = cPickle.load(bf)
        except:
            pass

        bones.append((self.plev, self.dlev, [i for i in self.inv if i is not None]))
        bones = bones[-3:]

        try:
            bf = open('bones', 'w')
            cPickle.dump(bones, bf)
        except:
            pass

        # Show some info.

        s = ['']
        s.append('%c%d total games logged.' % (libtcod.COLCTRL_1, len(hss)))

        sortd = {}
        for x in hss:
            total = (x['plev'] * 5) + (x['dlev'] * 5) + len(x['kills'])
            x['score'] = total
            x['kills'] = len(x['kills'])

            for k,v in x.iteritems():
                if k not in sortd:
                    sortd[k] = []
                sortd[k].append(v)

            if x == hs and len(s) == 0:
                s.append('%d points: Level %d character, killed by %s on dlev '
                         '%d, and scored %d kills.' % \
                         (total, x['plev'], x['reason'], x['dlev'], x['kills']))

        def count(ll, x):
            less = 0
            more = 0
            place = None
            inn = 0
            for i in ll:
                inn += 1
                if i == x and place is None:
                    place = inn
                if i < x:
                    less += 1
                elif i > x:
                    more += 1
            return less,more,place

        sortd2 = {}
        for k,v in sortd.iteritems():
            sortd2[k] = count(list(reversed(sorted(v))), hs[k])

        s.append('')
        s.append('Scored %d points. That is #%d out of %d, with %d scoring lower and %d higher.' % \
                 (hs['score'], sortd2['score'][2], len(hss), sortd2['score'][0], sortd2['score'][1]))

        s.append('')
        s.append('Reached dungeon level %d. %d games reached a lower level and %d a higher one.' % \
                 (hs['dlev'], sortd2['dlev'][1], sortd2['dlev'][0]))

        s.append('')
        s.append('Reached player level %d. %d games reached a higher level and %d a lower one.' % \
                 (hs['plev'], sortd2['plev'][1], sortd2['plev'][0]))

        s.append('')
        s.append('Killed %d monsters. %d games had more kills, %d less.' % \
                 (hs['kills'], sortd2['kills'][1], sortd2['kills'][0]))

        s.append('')
        s.append('Killed by %s. %d games ended for the same reason.'% \
                 (hs['reason'], len(hss) - sortd2['reason'][0] - sortd2['reason'][1]))

        s.append('')
        s.append('Press space.')

        while 1:
            if draw_window(s, self.w, self.h) == ' ':
                break

        s = ['']
        sortd = {}
        for x in hss:
            if x['reason'] not in sortd:
                sortd[x['reason']] = 1
            else:
                sortd[x['reason']] += 1

        sortd = list(reversed(sorted((n,r) for (r,n) in sortd.iteritems())))
        sortd = sortd[:10]
        s.append('Top 10 reasons for death:')
        s.append('')
        for n,r in sortd:
            s.append('%5d: %s' % (n,r))
        s.append('')
        s.append('Press space to exit.')

        while 1:
            if draw_window(s, self.w, self.h) == ' ':
                break



def start_game(world, w, h, oldseed=None, oldbones=None):

    if oldbones is not None:
        world.bones = oldbones
    else:
        world.load_bones()

    if oldseed or not world.load():
        if oldseed:
            world._seed = oldseed
        else:
            world._seed = int(time.time())

        #print 'SEEDING!: ', world._seed
        random.seed(world._seed)
        global _inputs
        _inputs = world._inputs

        world.regen(w, h)
        world.place()
        world.generate_inv()
        world.msg.m("Kill all the monsters in the dungeon to win the game.")
        world.msg.m("Please press '?' to see help.")

def check_autoplay(world):

    if world.sleeping > 0:
        if world.stats.sleep.x >= 3.0 and not world.forcedsleep:
            world.msg.m('You wake up.')
            world.sleeping = 0
            return 1
        else:
            world.sleep()
            return -1

    if world.resting:
        if world.stats.tired.x >= 3.0:
            world.msg.m('You stop resting.')
            world.resting = False
            return 1
        else:
            world.rest()
            return -1

    if world.digging:
        if world.grid[world.digging[1]][world.digging[0]] <= -10:
            world.convert_to_floor(world.digging[0], world.digging[1])
            world.digging = None
            return 1
        else:
            world.grid[world.digging[1]][world.digging[0]] -= 0.1
            world.tick()
            return -1

    return 0


def main(replay=None, highscorefilename='highscore'):

    oldseed = None
    oldbones = None

    if replay is not None:
        hss = []
        hsf = open(highscorefilename, 'r')
        hss = cPickle.load(hsf)

        oldseed = hss[replay]['seed']
        oldinputs = hss[replay]['inputs']
        oldbones = hss[replay]['bones']

        global _inputqueue
        _inputqueue = oldinputs

        if _version != hss[replay]['version']:
            return False

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
    world.make_keymap()

    start_game(world, w, h, oldseed=oldseed, oldbones=oldbones)

    while 1:

        if libtcod.console_is_window_closed():
            if replay is None:
                world.save()
            break

        if world.done or world.dead: break

        world.draw()
        libtcod.console_flush()

        r = check_autoplay(world)
        if r == -1:
            libtcod.console_check_for_keypress()
            continue
        elif r == 1:
            world.draw(False)
            libtcod.console_flush()


        if world.dead: break

        #key = libtcod.console_wait_for_keypress(True)
        #world._inputs.append((key.c, key.vk))
        key = console_wait_for_keypress()

        if chr(key.c) in world.ckeys:
            world.ckeys[chr(key.c)]()

        elif key.vk in world.vkeys:
            world.vkeys[key.vk]()

    world.msg.m('*** Press any key ***', True)
    world.draw(False)
    libtcod.console_flush()
    libtcod.console_wait_for_keypress(False)

    if replay is None and world.dead:
        world.form_highscore()

    return True


#import cProfile
#cProfile.run('main()')

if __name__=='__main__':
    main()
