#!/usr/bin/env python

import math
import os
#import random
import copy
import time

import cPickle

import libtcodpy as libtcod

import sqlite3

import sounds
import moon

import libdiggrpy as dg


class Logger:
    def __init__(self):
        self.f = None

    def log(self, *x):
        if self.f:
            print >> self.f, ' '.join(str(i) for i in x)
        else:
            print ' '.join(str(i) for i in x)

# log = Logger()

# random__ = random

# class random(object):
#     @staticmethod
#     def randint(*a):
#         log.log('randint', a)
#         return random__.randint(*a)
#     @staticmethod
#     def seed(*a):
#         log.log('seed', a)
#         return random__.seed(*a)
#     @staticmethod
#     def gauss(*a):
#         log.log('gauss', a)
#         return random__.gauss(*a)
#     @staticmethod
#     def uniform(*a):
#         log.log('uniform', a)
#         return random__.uniform(*a)
#     @staticmethod
#     def choice(*a):
#         log.log('choice', a)
#         return random__.choice(*a)


# B: large bird
# d: small dinosaur
# D: dinosaur
# f: faerie
# F: powerful faerie
# G: Japanese giant reptile
# h: humanoid
# H: powerful human
# k: knight, warrior or soldier
# K: epic hero, demigod or deity
# o: turtle, armadillo or porcupine
# O: large turtle
# q: quadruped mammal
# Q: huge quadriped mammal
# R: large reptile
# S: large snake
# u: urthian being
# U: urthian megatherian
# v: apparition, illusion or digital construct
# V: powerful digital construct
# w: worm
# W: giant worm
# x: insect, fungus or plant
# X: huge insect or insectoid
# y: undead
# Y: elder undead
# z: robot
# Z: large robot


# a: find the monolith
# b: circle of cthulhu: sacrifice 5 monsters and craft the call of cthulhu
# c: the graphite vault/maze, with root password inside (crystalline graphite, carbonized graphite)
# d: none, but add vaults with colored fountains
# e: eye of kali (from Conan), with statue of kali


global _version
_version = '12.02.05'

global _inputs
global _inputqueue
_inputqueue = None

global _inputdelay
_inputdelay = 100


class fakekey:
    def __init__(self, c, vk):
        self.c = c
        self.vk = vk

class Config:
    def __init__(self, sound_enabled=True):
        self.fullscreen = False
        self.sound_enabled = True
        self.music_enabled = True

        self.sound = sounds.Engine(sound_enabled)
        self.music_n = None

        self.cfgfile = {}
        self.load()
    
    def load(self):
        try:
            self.cfgfile = eval(open('diggr.cfg').read())
        except:
            pass

        if 'fullscreen' in self.cfgfile:
            self.fullscreen = bool(self.cfgfile['fullscreen'])

        if 'sound' in self.cfgfile:
            self.sound_enabled = bool(self.cfgfile['sound'])

        if 'music' in self.cfgfile:
            self.music_enabled = bool(self.cfgfile['music'])



def console_wait_for_keypress():
    global _inputqueue
    global _inputdelay

    if _inputqueue is not None:

        if len(_inputqueue) == 0:
            raise Exception('Malformed replay file.')

        c, vk = _inputqueue[0]
        _inputqueue = _inputqueue[1:]

        if _inputdelay < 1000:
            tmp = libtcod.console_check_for_keypress()
        else:
            tmp = libtcod.console_wait_for_keypress(False)

        if tmp.vk == libtcod.KEY_RIGHT and _inputdelay > 20:
            _inputdelay -= (20 if _inputdelay <= 200 else 200)
        elif tmp.vk == libtcod.KEY_LEFT and _inputdelay < 1000:
            _inputdelay += (20 if _inputdelay < 200 else 200)
        elif tmp.c == 32: # space
            _inputdelay = 1000

        if _inputdelay < 1000:
            libtcod.sys_sleep_milli(_inputdelay)

        #log.log('  key:', (chr(c) if c > 31 else ''), c, vk)
        return fakekey(c, vk)

    k = libtcod.console_wait_for_keypress(False)
    _inputs.append((k.c, k.vk))
    #log.log('  key:', (chr(k.c) if k.c > 31 else ''), k.c, k.vk)
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
        self.waterpois = 0.85
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

        self.moldchance = 2

        self.burnduration = 8
        self.burndamage = 0.76

        self.resource_timeouts = {'r': 300,
                                  'g': 400,
                                  'y': 600,
                                  'b': 400,
                                  'p': 500}


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

        libtcod.console_set_color_control(libtcod.COLCTRL_1, libtcod.white, libtcod.black)
        libtcod.console_set_color_control(libtcod.COLCTRL_2, libtcod.darker_green, libtcod.black)
        libtcod.console_set_color_control(libtcod.COLCTRL_3, libtcod.yellow, libtcod.black)
        libtcod.console_set_color_control(libtcod.COLCTRL_4, libtcod.red, libtcod.black)
        libtcod.console_set_color_control(libtcod.COLCTRL_5, libtcod.gray, libtcod.black)

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




_kbdmap = {
    libtcod.KEY_LEFT: 'h',
    libtcod.KEY_RIGHT: 'l',
    libtcod.KEY_UP: 'k',
    libtcod.KEY_DOWN: 'j',
    libtcod.KEY_HOME: 'y',
    libtcod.KEY_PAGEUP: 'u',
    libtcod.KEY_END: 'b',
    libtcod.KEY_PAGEDOWN: 'n',
    libtcod.KEY_KP4: 'h',
    libtcod.KEY_KP6: 'l',
    libtcod.KEY_KP8: 'k',
    libtcod.KEY_KP2: 'j',
    libtcod.KEY_KP7: 'y',
    libtcod.KEY_KP9: 'u',
    libtcod.KEY_KP1: 'b',
    libtcod.KEY_KP3: 'n'
}

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
    k = console_wait_for_keypress()

    libtcod.console_rect(None, x0, 0, w - x0, y0, True)
    libtcod.console_flush()

    if do_mapping:
        if k.vk in _kbdmap: return _kbdmap[k.vk]

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
            if d <= r and xi >= 0 and xi < w and yi >= 0 and yi < h:
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


def draw_blast2(x, y, w, h, r, func1, func2, color=libtcod.light_azure):
    x0 = min(x - r, 0)
    y0 = min(y - r, 0)
    x1 = max(x + r + 1, w)
    y1 = max(y + r + 1, h)
    c = []
    for xi in xrange(x0, x1):
        for yi in xrange(y0, y1):
            d = math.sqrt(math.pow(abs(yi - y),2) + math.pow(abs(xi - x),2))
            if d <= r and xi >= 0 and xi < w and yi >= 0 and yi < h:
                if func1(xi, yi):
                    c.append((xi, yi))

    def dr():
        for c0 in c:
            libtcod.console_put_char_ex(None, c0[0], c0[1], '*', fore, back)
        libtcod.console_flush()
        libtcod.sys_sleep_milli(100)

    if color is not None:
        back = libtcod.darkest_blue
        fore = color
        dr()
        fore = libtcod.color_lerp(fore, back, 0.5)
        dr()
        fore = libtcod.color_lerp(fore, back, 0.5)
        dr()

    for c0 in c:
        func2(c0[0], c0[1])


def draw_floodfill(x, y, w, h, func):

    procd = set()

    toproc = set()
    toproc.add((x,y))

    while 1:
        x_, y_ = toproc.pop()

        for xi in xrange(x_-1, x_+2):
            for yi in xrange(y_-1, y_+2):

                if xi < 0 or yi < 0 or xi >= w or yi >= h:
                    continue

                if (xi, yi) in procd:
                    continue

                procd.add((xi, yi))

                if func(xi, yi):
                    toproc.add((xi, yi))

        if len(toproc) == 0:
            break

    def dr():
        for c0 in procd:
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

    def show_all(self, w, h):
        l = []
        for v,m,z in self.strings[:24]:
            if v:
                l.append('%c%s' % (v,m))
            elif len(l) == 0:
                l.append('%c%s' % (libtcod.COLCTRL_1, m))
            else:
                l.append('%c%s' % (libtcod.COLCTRL_5, m))
        draw_window(l, w, h)


class Inventory:
    def __init__(self):
        self._items = {
            'a': None,
            'b': None,
            'c': None,
            'd': None,
            'e': None,
            'f': None,
            'g': None,
            'h': None,
            'i': None }
        self._slotnames = {
            'a': 'head',
            'b': 'neck',
            'c': 'trunk',
            'd': 'left hand',
            'e': 'right hand',
            'f': 'legs',
            'g': 'feet',
            'h': 'backpack 1',
            'i': 'backpack 2'}
        self._slotnums = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

    def draw(self, w, h, dlev, plev, floor=None):

        def fmt(slot):
            nm = self._slotnames[slot]
            nm = nm[0].upper() + nm[1:]
            pad = ' '*(10-len(nm))
            itm = ' -'
            tmp = self._items[slot]
            if tmp:
                itm = str(tmp)
            return "%c%c)%s %s:%c%s" % (libtcod.COLCTRL_5, 
                                        slot, pad, nm,
                                        libtcod.COLCTRL_1,
                                        itm)

        s = [fmt(slot) for slot in self._slotnums]

        if floor:
            s.extend(floor)

        s.extend(["",
                  "Character level: %d" % plev,
                  "  Dungeon level: %d" % dlev])

        return draw_window(s, w, h)

    def take(self, i, slot=None):
        if not slot:
            slot = i.slot

        if not self._items[slot]:
            self._items[slot] = i
            return True

        elif not self._items['h']:
            self._items['h'] = i
            return True

        elif not self._items['i']:
            self._items['i'] = i
            return True

        return False

    def get_tagged(self):
        i = []
        for slot in self._slotnums:
            j = self._items[slot]
            if j and j.tag:
                i.append((j.tag, slot, j))

        i.sort()
        return i

    def drop(self, slot):
        if slot in self._items:
            ret = self._items[slot]
            self._items[slot] = None
            return ret
        return None

    def check(self, slot):
        if slot in self._items:
            return self._items[slot]
        return None

    class _iter:
        def __init__(self, i):
            self.inv = i
            self.slot = -1
        def __iter__(self):
            return self
        def next(self):
            self.slot += 1
            if self.slot >= len(self.inv._slotnums):
                raise StopIteration()
            s = self.inv._slotnums[self.slot]
            i = self.inv._items[s]
            return (i, s)

    def __iter__(self):
        return self._iter(self)

    def purge(self, item):
        for k,v in self._items:
            if v == item:
                self._items[k] = None


##################################################
##################################################

from items import *
from monsters import *
from features import *
from vaults import *
from celauto import *






class Achieve:
    def __init__(self, tag=None, desc=None, weight=0):
        self.tag = tag
        self.desc = desc
        self.weight = weight


class Achievements:
    def __init__(self):
        self.achs = []
        self.killed_monsters = []
        self.prayed = 0
        self.shrines = set()
        self.used = 0
        self.wishes = 0
        self.rangeattacks = 0
        self.branches = set()
        self.onlyonce = set()
        self.extinguished = 0
        self.healing = 0
        self.booze = 0
        self.food = 0
        self.nodoz = 0
        self.dowsing = 0
        self.radkilled = 0
        self.explodekilled = 0
        self.digged = 0
        self.crafted = 0
        self.a_craft = 0
        self.ebola = 0
        self.killed_molds = 0
        self.colors = 0
        self.bonus_colors = 0

    def finish(self, plev, dlev, moon, reason):
        self.add('plev%d' % plev, 'Reached player level %d' % plev)
        self.add('dlev%d' % dlev, 'Reached dungeon level %d' % dlev)

        moonstr = moon.phase_string(moon)
        self.add('moon_%s' % moonstr, 'Played on a %s moon' % moonstr)

        if len(self.killed_monsters) == 0:
            self.add('loser', 'Scored *no* kills')
        else:
            killbucket = ((len(self.killed_monsters) / 5) * 5)
            if killbucket > 0:
                self.add('%dkills' % killbucket, 'Killed at least %d monsters' % killbucket, weight=10*killbucket)

        self.add('dead_%s' % reason, 'Killed by %s' % reason)

        if len(self.shrines) >= 3:
            self.add('3gods', 'Worshipped 3 gods', weight=60)
        elif len(self.shrines) >= 2:
            self.add('2gods', 'Worshipped 2 gods', weight=50)
        elif len(self.shrines) >= 1:
            self.add('religion', 'Worshipped a god')

        praybucket = ((self.prayed / 3) * 3)
        if praybucket > 0:
            self.add('%dprayers' % praybucket, 'Prayed at least %d times' % praybucket, weight=10*praybucket)

        usebucket = ((self.used / 20) * 20)
        if usebucket > 0:
            self.add('%duses' % usebucket, 'Used an item at least %d times' % usebucket, weight=10)

        if self.wishes == 0:
            self.add('nowish', 'Never wished for an item', weight=20)
        else:
            self.add('%dwish' % self.wishes, 'Wished for an item %d times' % self.wishes, weight=20)

        if self.rangeattacks == 0:
            self.add('nogun', 'Never used a firearm', weight=20)
        else:
            firebucket = ((self.rangeattacks / 10) * 10)
            if firebucket > 0:
                self.add('%dfires' % firebucket, 'Used a firearm at least %d times' % firebucket, weight=20)

        nbranches = len(self.branches)

        if 'q' in self.branches:
            self.add('thunderdome', 'Visited the Rehabilitation Thunderdome', weight=26)
            nbranches -= 1

        if 'qk' in self.branches:
            self.add('kalitemple', 'Visited the temple of Kali', weight=98)
            nbranches -= 1

        if nbranches <= 1:
            self.add('onebranch', 'Visited only one dungeon branch', weight=15)
        else:
            self.add('%dbranch' % nbranches, 'Visited %d dungeon branches' % nbranches, weight=25)

        if self.extinguished > 0:
            self.add('%dxting' % self.extinguished, 'Extinguished %d monster species' % self.extinguished, weight=97)

        if self.radkilled > 0:
            radbucket = ((self.radkilled / 5) * 5)
            if radbucket > 0:
                self.add('%dnuked' % radbucket, 'Killed at least %d monsters with radiation' % radbucket, weight=45)
            else:
                self.add('nuked', 'Killed a monster with radiation', weight=35)

        if self.explodekilled > 0:
            explbucket = ((self.explodekilled / 5) * 5)
            if explbucket > 0:
                self.add('%dexploded' % explbucket, 'Exploded at least %d monsters' % explbucket, weight=33)

        if self.ebola > 0:
            ebolabucket = ((self.ebola / 5) * 5)
            if ebolabucket > 0:
                self.add('%debola' % ebolabucket, 'Killed at least %d monsters via Ebolavirus' % ebolabucket, weight=77)
            else:
                self.add('ebola', 'Killed a monster via Ebolavirus', weight=77)

        if self.killed_molds > 0:
            moldbucket = ((self.killed_molds / 10) * 10)
            if moldbucket > 0:
                self.add('%dmolds' % moldbucket, 'Cleaned up black mold over %d times' % moldbucket, weight=34)
            else:
                self.add('molds', 'Cleaned up black mold', weight=32)

        if self.digged == 0:
            self.add('nodig', 'Never used a pickaxe', weight=23)

        if self.dowsing == 0:
            self.add('norod', 'Never used a dowsing rod', weight=15)

        foodbucket = ((self.food / 5) * 5)
        boozebucket = ((self.booze / 5) * 5)
        pillbucket = ((self.healing / 5) * 5)
        nodozbucket = ((self.nodoz / 5) * 5)

        if self.food == 0 and self.booze == 0 and self.healing == 0 and self.nodoz == 0:
            self.add('teetotal', 'Never ate food, drank alcohol or used medicine', weight=9)
        else:
            if self.food == 0:
                self.add('nofood', 'Never ate a mushroom', weight=7)
            elif foodbucket > 0:
                self.add('%dfood' % foodbucket, 'Dined on mushrooms at least %d times' % foodbucket, weight=5)

            if self.booze == 0:
                self.add('nobooze', 'Never drank alcohol', weight=7)
            elif boozebucket > 0:
                self.add('%dbooze' % boozebucket, 'Drank booze at least %d times' % boozebucket, weight=5)

            if self.healing == 0:
                self.add('nopill', 'Never used medicine', weight=7)
            elif pillbucket > 0:
                self.add('%dpill' % pillbucket, 'Swallowed a pill at least %d times' % pillbucket, weight=5)

            if self.nodoz == 0:
                self.add('nopep', 'Never used No-Doz pills', weight=7)
            elif nodozbucket > 0:
                self.add('%dpep' % nodozbucket, 'Used No-Doz pills at least %d times' % nodozbucket, weight=5)

        if self.crafted > 0:
            self.add('%dcraft' % self.crafted, 'Tried crafting %d times' % self.crafted, weight=15)

        if self.a_craft > 0:
            if self.a_craft == 1:
                self.add('artifact', 'Crafted a powerful artifact', weight=88)
            else:
                self.add('%dafacts', 'Crafted %d powerful artifacts', weight=89)

        if self.bonus_colors > 0:
            if self.bonus_colors == 1:
                self.add('colorwow', 'Used colored liquid for great success', weight=88)
            else:
                self.add('%dcolorwow' % self.bonus_colors, 'Used colored liquid for great success %d times' % self.bonus_colors, weight=89)

        if self.colors < 6:
            self.add('%dcolor' % self.colors, 'Drank colored liquid %d times' % self.colors, weight=4)
        else:
            self.add('6color', 'Drank colored liquid 6 times or more', weight=44)


    def descend(self, plev, dlev, branch):
        if dlev >= plev+5:
            self.add('tourist', 'Dived to a very deep dungeon', weight=50, once=True)

        elif dlev >= plev+2:
            self.add('small_tourist', 'Dived to a deep dungeon', weight=15, once=True)

        self.branches.add(branch)

    def questdone(self, branch):
        if branch == 'q':
            self.add('thunderdome_win', 'Became a Thunderdome champion', weight=78)

    def winner(self, msg=None):
        if msg:
            self.add(msg[0], msg[1], weight=99)

        self.add('winner', ' =*= Won the game =*= ', weight=100)

    def mondone(self):
        self.extinguished += 1

    def mondeath(self, plev, dlev, mon, is_rad=False, is_explode=False, is_poison=False):
        if mon.inanimate:
            return

        if mon.is_mold:
            self.killed_molds += 1
            return

        if mon.level >= plev+5:
            self.add('stealth', 'Killed a monster massively out of depth', weight=50)
        elif mon.level >= plev+2:
            self.add('small_stealth', 'Killed a monster out of depth', weight=10)

        if is_poison:
            self.ebola += 1
        else:
            self.killed_monsters.append((mon.level * mon.pointsfac, mon.branch, mon.name, dlev, plev))

        if is_rad:
            self.radkilled += 1

        if is_explode:
            self.explodekilled += 1


    def pray(self, shrine):
        self.shrines.add(shrine)
        self.prayed += 1

    def craft_use(self, item):
        self.crafted += 1
        if not item.craft:
            self.a_craft += 1

    def resource_use(self, resource, bonus):
        self.colors += 1
        if bonus:
            self.bonus_colors += 1

    def use(self, item):
        self.used += 1

        if item.rangeattack or item.rangeexplode:
            self.rangeattacks += 1

        elif item.food:
            self.food += 1
        elif item.booze:
            self.booze += 1
        elif item.healing or item.healingsleep:
            self.healing += 1
        elif item.nodoz:
            self.nodoz += 1
        elif item.homing:
            self.dowsing += 1
        elif item.digging:
            self.digged += 1

        if item.switch_moon:
            if item.switch_moon == moon.FULL:
                self.add('full_m_prism', 'Used a prism of the Full Moon', weight=41)
            elif item.switch_moon == moon.NEW:
                self.add('new_m_prism', 'Used a prism of the New Moon', weight=41)


    def wish(self):
        self.wishes += 1

    def __iter__(self):
        return iter(self.achs)

    def add(self, tag, desc, weight=0, once=False):
        if once:
            if tag in self.onlyonce:
                return
            else:
                self.onlyonce.add(tag)

        self.achs.append(Achieve(tag=tag, desc=desc, weight=weight))


class QuestInfo:
    def __init__(self, moncounts={}, monlevels=(1,12),
                 itemcounts={}, dlevels=(1,12),
                 messages={}, gifts=None):
        self.moncounts = moncounts
        self.monlevels = monlevels
        self.itemcounts = itemcounts
        self.dlevels = dlevels
        self.messages = messages
        self.gifts = gifts


class Player:
    def __init__(self):

        self.stats = Stats()
        self.inv = Inventory()
        self.achievements = Achievements()

        self.done = False
        self.dead = False

        self.plev = 1

        self.sleeping = 0
        self.forcedsleep = False
        self.forced2sleep = False
        self.healingsleep = False
        self.resting = False
        self.cooling = 0
        self.digging = None
        self.blind = False
        self.mapping = 0
        self.glued = 0
        self.onfire = 0

        self.s_grace = 0
        self.b_grace = 0
        self.v_grace = 0

        self.resource = None
        self.resource_buildup = 0
        self.resource_timeout = 0

        self.tagorder = 1
        self.monsters_in_view = []
        self.new_visibles = False


class Dungeon:
    def __init__(self):

        self.w = None
        self.h = None

        self.featmap = {}
        self.itemap = {}
        self.monmap = {}
        self.exit = None

        self.dlev = 1

        self.px = None
        self.py = None

        self.tcodmap = None

        self.coef = Coeffs()
        self.itemstock = ItemStock()
        self.monsterstock = MonsterStock()
        self.featstock = FeatureStock()
        self.vaultstock = VaultStock()
        self.celautostock = CelAutoStock()

        self.branch = None
        self.moon = None

        self.doppelpoint = None
        self.doppeltime = 0

        self.floorpath = None



class World:

    def __init__(self, config):

        self.p = Player()
        self.d = Dungeon()

        self.ckeys = None
        self.vkeys = None

        self.msg = Messages()

        self.did_moon_message = False
        self.t = 0
        self.oldt = -1

        self._seed = None
        self._inputs = []

        self.save_disabled = False

        self.config = config
        self.last_played_themesound = 0

        ### 

        self.theme = { 'a': (libtcod.lime,),
                       'b': (libtcod.red,),
                       'c': (libtcod.sky,),
                       'd': (libtcod.darkest_grey,),
                       'e': (libtcod.lightest_yellow,),
                       's': (libtcod.darkest_blue,),
                       'q': (libtcod.white,),
                       'qk': (libtcod.grey,) }
        
        quest1 = QuestInfo(moncounts={3:1, 4:1, 5:2, 6:2, 7:3}, 
                           monlevels=(3,8),
                           itemcounts={3:1, 4:1, 5:1, 6:1, 7:1}, 
                           dlevels=(3,7),
                           messages={3: ['Victory! The Thunderdome grants you a gift!', 'An exit appears.'],
                                     4: ['Victory! The Thunderdome grants you a gift!', 'An exit appears.'],
                                     5: ['Victory! The Thunderdome grants you a gift!', 'An exit appears.'],
                                     6: ['Victory! The Thunderdome grants you a gift!', 'An exit appears.'],
                                     7: ['Total victory!', 'The Thunderdome grants you godlike powers!']}, 
                           gifts={3: [None, None, None],
                                  4: [None, None, None],
                                  5: [None, None, None],
                                  6: [None, None, None],
                                  7: ['deusex']})

        questkali = QuestInfo(moncounts={15:10},
                              monlevels=(8,11),
                              itemcounts={15:10},
                              dlevels=(15,15),
                              messages={15: []},
                              gifts={15: []})
        
        self.quests = {'q': quest1,
                       'qk': questkali}

        self.neighbors = None


    def health(self): return self.p.stats.health
    def sleep(self):  return self.p.stats.sleep
    def tired(self):  return self.p.stats.tired
    def hunger(self): return self.p.stats.hunger
    def thirst(self): return self.p.stats.thirst
    def warmth(self): return self.p.stats.warmth

    def generate_and_take_item(self, itemname):
        self.p.inv.take(self.d.itemstock.find(itemname))

    ##

    def try_feature(self, x, y, att, deflt=None):
        if (x,y) not in self.d.featmap:
            return deflt
        return getattr(self.d.featmap[(x, y)], att, deflt)


    ##

    def get_inv_attr(self, slots, attr, default=None):
        ix = [ getattr(self.p.inv, slot) for slot in slots ]
        return [ getattr(i, attr, default) for i in ix ]

    def get_fires(self):
        return self.get_inv_attr(['right'], 'fires')[0]

    def get_glueimmune(self):
        return self.get_inv_attr(['left'], 'glueimmune')[0]

    def get_digspeed(self):
        return self.get_inv_attr(['head'], 'digbonus')[0]

    def get_springy(self):
        return (self.get_inv_attr(['feet'], 'springy')[0] or 
                (self.p.resource_timeout and self.p.resource == 'y'))

    def get_heatbonus(self):
        return sum(self.get_inv_attr(['trunk', 'legs'], 'heatbonus', 0))

    def get_radimmune(self):
        return (self.get_inv_attr(['trunk'], 'radimmune')[0] or
                (self.p.resource_timeout and self.p.resource == 'b'))

    def get_explodeimmune(self):
        return (self.get_inv_attr(['trunk'], 'explodeimmune')[0] or
                (self.p.resource_timeout and self.p.resource == 'b'))

    def get_confattack(self):
        for tmp in self.get_inv_attr(['right', 'left'], 'confattack'):
            if tmp:
                return tmp
        return None

    def get_psyimmune(self):
        return any(self.get_inv_attr(['head', 'right', 'left'], 'psyimmune'))

    def get_repelrange(self):
        return max(self.get_inv_attr(['trunk', 'left'], 'repelrange', 0))

    def get_telepathyrange(self):
        tmp = max(self.get_inv_attr(['head'], 'telepathyrange', 0))

        if self.p.resource_timeout and self.p.resource == 'p':
            tmp = max(self.d.coef.purple_telerange, tmp)

        return tmp


    def get_camorange(self, monrange):
        tmp = min(self.get_inv_attr(['trunk', 'feet', 'neck'], 
                                    'camorange', monrange))

        if self.p.resource_timeout and self.p.resource == 'p':
            tmp = min(self.d.coef.purple_camorange, tmp)

        if self.p.b_grace:
            rang = 12 - int(9 * (float(self.p.b_grace) / 
                                 self.d.coef.b_graceduration))
            tmp = min(rang, tmp)

        return tmp

    def get_attack(self):
        if self.p.resource_timeout and self.p.resource == 'g':
            baseattack = self.d.coef.green_attack
        else:
            baseattack = self.d.coef.unarmedattack

        return max(sum(self.get_inv_attr(['right', 'left', 'feet'], 
                                         'attack', 0),
                       baseattack))

    def get_defence(self):
        tmp = max(sum(self.get_inv_attr(['head', 'left', 'trunk', 
                                         'legs', 'feet'], 'defence', 0)),
                  self.d.coef.unarmeddefence)

        if self.p.glued:
            tmp /= self.d.coef.gluedefencepenalty
        return tmp

    def get_lightradius(self, default):

        if self.p.resource_timeout and self.p.resource == 'y':
            ret = self.d.coef.yellow_lightradius
        else:
            tmp = sum(self.get_inv_attr(['head', 'neck', 'legs', 'right', 'trunk'],
                                        'lightradius', 0))
            ret = min(max(tmp + (default or 0), 2), 15)

        if self.p.blind:
            ret /= 2

        if self.p.b_grace:
            n = int(15 * (float(self.p.b_grace) / self.d.coef.b_graceduration))
            ret = max(ret, n)

        if self.d.moon == moon.NEW:
            ret += 1
        elif self.d.moon == moon.FULL:
            ret -= 2

        ret += self.try_feature(self.px, self.py, 'lightbonus', 0)

        return max(ret, 1)

    ### 

    def filter_inv(self, func1, func2):
        ret = False
        for i,slot in self.p.inv:
            if i:
                f1ret = func1(i, slot)
                if f1ret:
                    ret = True
                    done, purge = func2(i, f1ret)
                    if purge:
                        self.p.inv.drop(slot)
                    if done:
                        break
        return ret

    # XXX 


    def makegrid(self, w_, h_):

        self.d.w = w_
        self.h = h_

        dg.grid_init(w_, h_)

        self.featmap = {}

        self.neighbors = {}
        for x in xrange(0, w_):
            for y in xrange(0, h_):
                self.neighbors[(x,y)] = []
                for xi in xrange(-1, 2):
                    for yi in xrange(-1, 2):
                        if xi == 0 and yi == 0:
                            continue

                        ki = (x+xi, y+yi)

                        if ki[0] < 0 or ki[0] >= w_ or ki[1] < 0 or ki[1] >= h_:
                            continue

                        self.neighbors[(x,y)].append(ki)

        dg.neighbors_init(w_, h_)
        dg.render_init(w_, h_)
      

    def make_map(self):
        self.tcodmap = libtcod.map_new(self.d.w, self.h)
        libtcod.map_clear(self.tcodmap)

        for x in xrange(self.d.w):
            for y in xrange(self.h):
                if dg.grid_is_walk(x, y):
                    v = True
                    w = True
                else:
                    v = False
                    w = False

                if (x,y) in self.featmap:
                    f = self.featmap[(x, y)]
                    w = f.walkable
                    v = f.visible

                libtcod.map_set_properties(self.tcodmap, x, y, v, w)


    def set_renderprops(self, x, y):

        feat = None
        if (x,y) in self.featmap:
            feat = self.featmap[(x,y)]

        if feat and feat.lit:
            dg.render_set_is_lit(x, y, True)
        else:
            dg.render_set_is_lit(x, y, False)

        if feat and feat.back:
            dg.render_set_back(x, y, feat.back)
        else:
            dg.render_set_back(x, y, libtcod.black)

        fore = self.theme[self.branch][0]
        fore2 = fore
        fore_i = 0
        is_terrain = False
        c = ' '

        if feat and feat.skin:
            c, fore = feat.skin

        elif dg.grid_is_walk(x, y):
            if dg.grid_is_water(x, y):
                c = 251
                fore = libtcod.light_azure
                fore2 = libtcod.dark_azure
                fore_i = 1
            else:
                c = 250
                is_terrain = True

        else:
            if dg.grid_is_water(x,y):
                fore = libtcod.desaturated_blue
            c = 176
            is_terrain = True

        dg.render_set_skin(x, y, fore, c, fore2, fore_i, is_terrain)


    def unset_feature(self, x, y):
        if (x,y) in self.featmap:
            del self.featmap[(x,y)]
            self.set_renderprops(x,y)

    def set_feature(self, x, y, f_):
        if (x, y) in self.featmap and self.featmap[(x, y)].stairs:
            return

        if not f_:
            if (x, y) in self.featmap:
                del self.featmap[(x, y)]

            if f_ is None:
                dg.grid_set_walk(x, y, True)
                libtcod.map_set_properties(self.tcodmap, x, y, True, True)
                dg.grid_set_height(x, y, -10.0)

            else:
                dg.grid_set_walk(x, y, False)
                libtcod.map_set_properties(self.tcodmap, x, y, False, False)
                dg.grid_set_height(x, y, 0.0)

            self.set_renderprops(x, y)
            return

        f = self.featstock.f[f_]
        w = f.walkable
        v = f.visible

        libtcod.map_set_properties(self.tcodmap, x, y, v, w)

        if f.nofeature:
            if (x, y) in self.featmap:
                del self.featmap[(x, y)]
        else:
            self.featmap[(x, y)] = f

        if w:
            dg.grid_set_walk(x, y, True)
        else:
            dg.grid_set_walk(x, y, False)

        dg.grid_set_height(x, y, f.height)

        if f.water:
            dg.grid_set_water(x, y, True)
        elif f.water is not None:
            dg.grid_set_water(x, y, False)


        self.set_renderprops(x, y)



    def set_item(self, x, y, itms):
        while 1:
            if not self.try_feature(x, y, 'stairs'):

                if (x,y) not in self.itemap:
                    self.itemap[(x,y)] = []
                iis = self.itemap[(x,y)]

                while len(iis) < 5 and len(itms) > 0:
                    iis.append(itms.pop(0))

                if len(itms) == 0:
                    break

            d = [ k for k in self.neighbors[(x,y)] if dg.grid_is_walk(k[0], k[1]) ]
            if len(d) == 0:
                iis.extend(itms)
                return
            x,y = d[dg.random_n(len(d))]


    def paste_vault(self, v):
        x = None
        y = None

        if v.anywhere:
            x = dg.random_n(self.d.w - v.w)
            y = dg.random_n(self.h - v.h)

        else:
            for x in xrange(10):
                d = dg.grid_one_of_floor()

                x0 = d[0] - v.anchor[0]
                y0 = d[1] - v.anchor[1]

                if x0 < 0 or y0 < 0 or x0 + v.w >= self.d.w or y0 + v.h >= self.h:
                    continue

                x = x0
                y = y0
                break

        if x is None or y is None:
            return

        if v.message:
            for msg in reversed(v.message):
                self.msg.m(msg, True)

        for yi in xrange(v.h):
            for xi in xrange(v.w):
                z = v.pic[yi]
                if xi >= len(z):
                    continue
                z = z[xi]
                z = v.syms[z]
                if z is None:
                    continue

                xx = x + xi
                yy = y + yi
                self.set_feature(xx, yy, z[0])

                if len(z) >= 3:
                    if z[1] is True:
                        dg.grid_add_nogen(xx, yy)
                    else:
                        itm = self.itemstock.get(z[1])
                        if itm:
                            self.set_item(xx, yy, [itm])


    def make_feats(self):

        self.featmap = {}
        dg.celauto_init()

        # HACK!
        # This is done here, and not in make_items(),
        # so that vaults could generate items.
        self.itemap = {}

        oldvaults = set()
        while 1:
            vault = self.vaultstock.get(self.branch, self.dlev, oldvaults)

            if vault:
                self.paste_vault(vault)
                oldvaults.add(vault)

            if not vault or not vault.free:
                break

        # Quests
        if self.branch in self.quests:
            return

        d = dg.grid_one_of_floor()

        self.set_feature(d[0], d[1], '>')
        self.exit = d

        dg.grid_add_nogen(d[0], d[1])

        if self.moon == moon.NEW:
            d = dg.grid_one_of_floor()
            self.set_feature(d[0], d[1], 'bb')

        elif self.moon == moon.FULL:
            d = dg.grid_one_of_floor()
            self.set_feature(d[0], d[1], 'dd')
            self.paste_celauto(d[0], d[1], self.celautostock.FERN)

        else:
            a = dg.random_range(-1, 1)
            d = dg.grid_one_of_floor()
            if a == -1:
                self.set_feature(d[0], d[1], 's')
            elif a == 0:
                self.set_feature(d[0], d[1], 'b')
            elif a == 1:
                self.set_feature(d[0], d[1], 'v')

        nfounts = int(round(dg.random_gauss(3, 1)))

        for tmp in xrange(nfounts):
            d = dg.grid_one_of_water()
            self.set_feature(d[0], d[1], ['C','V','B','N','M'][dg.random_n(5)])



    def make_paths(self):
        #log.log('  making path')
        if self.floorpath:
            libtcod.path_delete(self.floorpath)

        def floor_callback(xfrom, yfrom, xto, yto, world):
            if (xto, yto) in world.monmap:
                return 0.0
            elif dg.grid_is_walk(xto, yto):
                return 1.0
            return 0.0

        self.floorpath = libtcod.path_new_using_function(self.d.w, self.h, floor_callback, self, 1.0)

    def make_monsters(self):

        self.monsterstock.clear_gencount()
        self.monmap = {}

        # Quests
        if self.branch in self.quests:
            n = self.quests[self.branch].moncounts.get(self.dlev, 0)

        else:
            n = int(max(dg.random_gauss(*self.coef.nummonsters), 1))

        i = 0
        while i < n:
            lev = self.dlev + dg.random_gauss(0, self.coef.monlevel)
            lev = max(int(round(lev)), 1)

            # Quests
            if self.branch in self.quests:
                lev = min(max(lev, self.quests[self.branch].monlevels[0]), 
                          self.quests[self.branch].monlevels[1])

            while 1:
                x, y = dg.grid_one_of_walk()
                if (x, y) not in self.monmap: break

            m = self.monsterstock.generate(self.branch, lev, self.itemstock, self.moon)
            if m:
                m.x = x
                m.y = y
                self.monmap[(x, y)] = m

                dg.grid_add_nogen(x, y)

                if m.inanimate:
                    continue

            i += 1


        # Generate some mold.
        if self.branch in self.quests:
            return

        if dg.random_range(1, self.coef.moldchance) == 1:
            x, y = dg.grid_one_of_floor()
            m = self.monsterstock.generate('x', self.dlev, self.itemstock, self.moon)
            if m:
                m.x = x
                m.y = y
                self.monmap[(x, y)] = m


    def make_items(self):

        ## Quests
        if self.branch in self.quests:
            n = self.quests[self.branch].itemcounts.get(self.dlev, 0)
        else:
            n = int(max(dg.random_gauss(self.coef.numitems[0] + self.dlev, self.coef.numitems[1]), 1))

        for i in xrange(n):
            lev = self.dlev + dg.random_gauss(0, self.coef.itemlevel)
            lev = max(int(round(lev)), 1)
            x, y = dg.grid_one_of_walk()
            item = self.itemstock.generate(lev)
            if item:
                self.set_item(x, y, [item])

        ## Quests
        if self.branch in self.quests:
            return

        for pl,dl,itm in self.bones:
            if dl == self.dlev and len(itm) > 0:
                itm2 = [copy.copy(i) for i in itm]

                x, y = dg.grid_one_of_walk()

                self.set_item(x, y, itm2)


    def place(self):

        # Do not place a player in an unfair position.
        # Otherwise, the monster will get a free move and might
        # kill the player.
        monn = set(k for k in self.monmap.iterkeys())

        for x in xrange(3):
            monn2 = set()
            for k in monn:
                for ki in self.neighbors[k]:
                    monn2.add(ki)
            monn.update(monn2)

        for k in monn:
            dg.grid_add_nogen(k[0], k[1])

        x, y = dg.grid_one_of_walk()
        self.px = x
        self.py = y

        
    def regen(self, w_, h_):
        if self.branch is None:
            self.branch = ['a', 'b', 'c', 'd', 'e'][dg.random_n(5)]

        if self.moon is None:
            m = moon.phase(self._seed)
            self.moon = m['phase']

        self.makegrid(w_, h_)

        # Quests
        if self.branch not in self.quests:
            gentype = 0

            if self.moon in (moon.NEW, moon.FULL):
                gentype = 1
            elif self.moon in (moon.FIRST_QUARTER, moon.LAST_QUARTER):
                gentype = -1

            dg.grid_generate(gentype)


        self.make_feats()
        self.make_paths()
        self.make_monsters()
        self.make_items()
        self.make_map()
        self.place()

        for x in xrange(w_):
            for y in xrange(h_):
                self.set_renderprops(x, y)

        if self.moon == moon.FULL:
            dg.render_set_env(libtcod.gray, 0.6)
        elif self.moon == moon.NEW:
            dg.render_set_env(libtcod.darkest_blue, 0.4)
        else:
            dg.render_set_env(libtcod.white, 0)



    def generate_inv(self):
        if self.moon == moon.FULL:
            self.generate_and_take_item("miner's lamp")
        else:
            self.generate_and_take_item('lamp')
            
        self.generate_and_take_item('pickaxe')


        pl = [k for k in self.neighbors[(self.px,self.py)] if dg.grid_is_walk(k[0], k[1])] + [(self.px,self.py)]

        for x in xrange(9):
            k = pl[dg.random_n(len(pl))]
            i = self.itemstock.generate(1)

            self.set_item(k[0], k[1], [i])



    def move(self, _dx, _dy, do_spring=True):

        if self.p.glued > 0:
            self.p.glued -= 1
            if self.p.glued == 0:
                self.msg.m('You dislodge yourself from the glue.')
                if (self.px, self.py) in self.featmap and \
                   self.featmap[(self.px, self.py)] == self.featstock.f['^']:
                    self.unset_feature(self.px, self.py)
            else:
                self.msg.m('You are stuck in the glue!')
                self.tick()
                return

        dx = _dx + self.px
        dy = _dy + self.py

        if dg.grid_is_walk(dx,dy) and dx >= 0 and dx < self.d.w and dy < self.h:

            if (dx, dy) in self.monmap:
                self.fight(self.monmap[(dx, dy)], True)
                self.tick()
                return
            else:
                self.px = dx
                self.py = dy

                if (self.px, self.py) in self.itemap:
                    if len(self.itemap[(self.px, self.py)]) > 1:
                        self.msg.m("You see several items here.")
                    else:
                        self.msg.m("You see " + str(self.itemap[(self.px, self.py)][0]) + '.')

                sign = self.try_feature(self.px, self.py, 'sign')
                if sign:
                    self.msg.m('You see an engraving: ' + sign)

                if self.p.onfire > 0:
                    self.seed_celauto(self.px, self.py, self.celautostock.FIRE)
                    self.set_feature(self.px, self.py, '"')

                if self.try_feature(self.px, self.py, 'sticky') and not self.get_glueimmune():
                    self.msg.m('You just stepped in some glue!', True)
                    self.p.glued = max(int(dg.random_gauss(*self.coef.glueduration)), 1)


        else:
            return

        is_springy = self.get_springy()

        if do_spring and is_springy:
            self.move(_dx, _dy, do_spring=False)
            return

        self.tick()


    def tick_checkstats(self):

        self.t += 1

        def is_destruct(i, slot): 
            if i.liveexplode > 0:
                return 1
            if i.selfdestruct > 0 and slot not in ('h','i'):
                return 2
            return False

        def do_destruct(i, n):
            if n == 1:
                i.liveexplode -= 1
                if i.liveexplode == 0:
                    if i.summon:
                        self.summon(self.px, self.py, i.summon[0], i.summon[1])
                    elif i.radexplode:
                        self.rayblast(self.px, self.py, i.radius)
                    elif i.swampgas:
                        self.paste_celauto(self.px, self.py, self.celautostock.SWAMPGAS)
                    else:
                        self.explode(self.px, self.py, i.radius)
                    return False, True

            elif n == 2:
                i.selfdestruct -= 1
                if i.selfdestruct == 0:
                    self.msg.m('Your ' + i.name + ' falls apart!', True)
                    return False, True
            return False, False

        self.filter_inv(is_destruct, do_destruct)


        fdmg = self.try_feature(self.px, self.py, 'fire')
        if fdmg > 0:
            self.health().dec(fdmg, "fire", self.config.sound)
            self.p.onfire = max(self.coef.burnduration, self.p.onfire)
        elif self.p.onfire > 0:
            if self.p.cooling == 0:
                self.health().dec(self.coef.burndamage, "fire", self.config.sound)
            self.p.onfire -= 1

        if self.p.cooling > 0:
            self.p.cooling -= 1
            if self.p.cooling == 0:
                self.msg.m("Your layer of cold mud dries up.")

        if self.doppeltime > 0:
            self.doppeltime -= 1

        if self.p.resource_timeout > 0: 
            if self.p.resource == 'r':
                self.health().inc(self.coef.regeneration)
                self.warmth().inc(self.coef.regeneration)
                self.hunger().inc(self.coef.regeneration)

            self.p.resource_timeout -= 1
            if self.p.resource_timeout == 0: self.p.resource = None

        if self.p.dead: return

        if self.try_feature(self.px, self.py, 'warm'):
            self.warmth().inc(self.coef.watercold)
        elif dg.grid_is_water(self.px, self.py):
            self.warmth().dec(self.coef.watercold)
        else:
            self.warmth().inc(self.get_heatbonus())

        p = self.try_feature(self.px, self.py, 'queasy')
        if p:
            self.msg.m('You feel queasy.', True)
            self.thirst().dec(p)
            self.hunger().dec(p)

        if self.warmth().x <= -3.0:
            self.msg.m("Being so cold makes you sick!", True)
            self.health().dec(self.coef.colddamage, "cold", self.config.sound)
            if self.p.resting: self.p.resting = False
            if self.p.digging: self.p.digging = None

        if self.thirst().x <= -3.0:
            self.msg.m('You desperately need something to drink!', True)
            self.health().dec(self.coef.thirstdamage, "thirst", self.config.sound)
            if self.p.resting: self.p.resting = False
            if self.p.digging: self.p.digging = None

        if self.hunger().x <= -3.0:
            self.msg.m('You desperately need something to eat!', True)
            self.health().dec(self.coef.hungerdamage, "hunger", self.config.sound)
            if self.p.resting: self.p.resting = False
            if self.p.digging: self.p.digging = None

        p = self.try_feature(self.px, self.py, 'poison')
        if p:
            self.msg.m('You feel very sick!', True)
            self.health().dec(p, 
                                  'black mold' if self.featmap[(self.px,self.py)].pois2 else 'Ebola infection', 
                                  self.config.sound)

        if self.health().x <= -3.0:
            self.p.dead = True
            return

        if self.tired().x <= -3.0:
            self.msg.m('You pass out from exhaustion!', True)
            self.start_sleep(force=True, quick=True)
            return

        if self.sleep().x <= -3.0:
            self.msg.m('You pass out from lack of sleep!', True)
            self.start_sleep(force=True)
            return


    def tick(self):
        self.tired().dec(self.coef.movetired)
        self.sleep().dec(self.coef.movesleep)
        self.thirst().dec(self.coef.movethirst)
        self.hunger().dec(self.coef.movehunger)

        if self.p.b_grace > 0: self.p.b_grace -= 1
        if self.p.v_grace > 0: self.p.v_grace -= 1
        if self.p.s_grace > 0: self.p.s_grace -= 1

        self.tick_checkstats()


    def do_rest(self):
        self.tired().inc(self.coef.resttired)
        self.sleep().dec(self.coef.restsleep)
        self.thirst().dec(self.coef.restthirst)
        self.hunger().dec(self.coef.resthunger)

        self.tick_checkstats()


    def do_sleep(self):
        self.tired().inc(self.coef.sleeptired)
        self.sleep().inc(self.coef.sleepsleep)
        self.thirst().dec(self.coef.sleepthirst)
        self.hunger().dec(self.coef.sleephunger)

        if self.p.healingsleep:
            self.health().inc(self.coef.healingsleep)

        if self.p.sleeping > 0:
            self.p.sleeping -= 1

            if self.p.sleeping == 0:
                self.p.forcedsleep = False
                self.p.forced2sleep = False
                self.p.healingsleep = False

        self.tick_checkstats()


    def start_sleep(self, force = False, quick = False,
                    realforced = False, realforced2 = False):
        if not force and self.sleep().x > -2.0:
            self.msg.m('You don\'t feel like sleeping yet.')
            return

        if quick:
            self.p.sleeping = int(dg.random_gauss(*self.coef.quicksleeptime))
        else:
            if not realforced2:
                self.msg.m('You fall asleep.')
            self.p.sleeping = int(dg.random_gauss(*self.coef.sleeptime))

        self.p.digging = None
        self.p.resting = False

        if realforced:
            self.p.forcedsleep = True
        elif realforced2:
            self.p.forced2sleep = True

    def start_rest(self):
        self.msg.m('You start resting.')
        self.p.resting = True

        
    def colordrink(self, fount):
        if self.p.resource and (self.p.resource != fount):
            self.msg.m('You feel confused.')
            self.p.resource = None
            self.p.resource_timeout = 0
            self.p.resource_buildup = 0
            return

        if fount == 'r': self.msg.m('You drink something red.')
        elif fount == 'g': self.msg.m('You drink something green.')
        elif fount == 'y': self.msg.m('You drink something yellow.')
        elif fount == 'b': self.msg.m('You drink something blue.')
        elif fount == 'p': self.msg.m('You drink something purple.')
        self.p.resource = fount

        bonus = False
        
        if self.p.resource_timeout:
            self.p.resource_timeout += (self.coef.resource_timeouts[fount]/6)
        else:
            self.p.resource_buildup += 1

            if self.p.resource_buildup >= 6:
                if self.p.resource == 'r':
                    self.msg.m('You gain superhuman regeneration power!', True)
                elif self.p.resource == 'g':
                    self.msg.m('Hulk Smash! You gain superhuman strength.', True)
                elif self.p.resource == 'y':
                    self.msg.m('You gain superhuman speed and vision!', True)
                elif self.p.resource == 'b':
                    self.msg.m('You are now immune to explosions and radiation!', True)
                elif self.p.resource == 'p':
                    self.msg.m('You gain telepathy and superhuman stealth!', True)

                bonus = True
                self.p.resource_buildup = 0
                self.p.resource_timeout = self.coef.resource_timeouts[fount]

        self.p.achievements.resource_use(fount, bonus)


    def drink(self):

        if self.try_feature(self.px, self.py, 'healingfountain'):
            nn = min(3.0 - self.health().x, self.hunger().x + 3.0)
            if nn <= 0:
                self.msg.m('Nothing happens.')
                return

            self.msg.m('You drink from the eternal fountain.')
            self.health().inc(nn)
            self.hunger().dec(nn)
            return

        fount = self.try_feature(self.px, self.py, 'resource')
        if fount:
            self.colordrink(fount)
            self.unset_feature(self.px, self.py)
            return
            
        if not dg.grid_is_water(self.px, self.py):
            self.msg.m('There is no water here you could drink.')
            return

        if self.p.v_grace:
            self.msg.m('Your religion prohibits drinking from the floor.')
            return

        self.thirst().inc(6)

        x = abs(dg.random_gauss(0, 0.7))
        tmp = x - self.coef.waterpois
        if tmp > 0:
            self.health().dec(tmp, "unclean water", self.config.sound)
            if tmp > 0.2:
                self.msg.m('This water has a bad smell.')
        else:
            self.msg.m('You drink from the puddle.')

        self.tick()

    def pray(self):
        if (self.px,self.py) not in self.featmap:
            self.msg.m('You need to be standing at a shrine to pray.')
            return

        a = self.featmap[(self.px, self.py)]

        if a.bb_shrine:

            def bb_shrine_func(i, n):
                self.msg.m("Ba'al-Zebub accepts your sacrifice!")

                i2 = self.itemstock.generate(self.dlev)
                if i2:
                    self.set_item(self.px, self.py, [i2])
                return False, True

            if self.filter_inv((lambda (i,slot): i.corpse), bb_shrine_func):
                return

            self.msg.m("Ba'al-Zebub needs to be sated with blood!!")
            return

        if a.s_shrine:
            if self.p.b_grace or self.p.v_grace:
                self.msg.m("You don't believe in Shiva.")
                return
            if self.p.s_grace > self.coef.s_graceduration - self.coef.s_praytimeout:
                self.msg.m('Nothing happens.')
                return

            ss = "hwp"
            decc = self.coef.shivadecstat
            ss = ss[dg.random_n(len(ss))]

            if ss == 'h': self.hunger().dec(decc)
            elif ss == 'w': self.warmth().dec(decc)
            elif ss == 'p': self.health().dec(decc, 'the grace of Shiva', self.config.sound)

            self.msg.m('You pray to Shiva.')
            self.wish('Shiva grants you a wish.')
            self.p.s_grace = self.coef.s_graceduration
            self.tick()
            self.p.achievements.pray('s')

        elif a.b_shrine:
            if self.p.s_grace or self.p.v_grace:
                self.msg.m("You don't believe in Brahma.")
                return
            self.msg.m('As a follower of Brahma, you are now forbidden hand-to-hand combat.')
            self.msg.m('You feel enlightened.')
            self.p.b_grace = self.coef.b_graceduration
            self.tick()
            self.p.achievements.pray('b')

        elif a.v_shrine:
            if self.p.s_grace or self.p.b_grace:
                self.msg.m("You don't believe in Vishnu.")
                return

            if self.p.v_grace > self.coef.v_graceduration - self.coef.v_praytimeout:
                self.msg.m('Nothing happens.')
                return

            self.msg.m('As a follower of Vishnu, you are now forbidden '
                       'medicine, alcohol and unclean food.')
            self.msg.m('You meditate on the virtues of Vishnu.')
            self.start_sleep(force=True, realforced2=True)

            self.health().inc(6.0)
            self.sleep().inc(6.0)
            self.tired().inc(6.0)
            self.hunger().inc(6.0)
            self.thirst().inc(6.0)
            self.warmth().inc(6.0)
            self.p.v_grace = self.coef.v_graceduration
            self.tick()
            self.p.achievements.pray('v')

        elif a.special == 'kali':

            def kalifunc(i, n):
                self.msg.m('You return the Eye to Kali.', True)
                self.victory(msg=('winkali', 'Returned the Eye of Kali'))
                return True, False

            if self.filter_inv((lambda (i,slot): i.special == 'kali'), kalifunc):
                return

            self.msg.m('Kali is silent. Perhaps she requires an offering?', True)

        elif a.special == 'monolith':
            self.victory(msg=('winmono', 'Rubbed the Monolith'))

        else:
            self.msg.m('You need to be standing at a shrine to pray.')
            return


    def convert_to_floor(self, x, y, rubble):
        if self.try_feature(x, y, 'permanent'):
            return

        if not rubble:
            self.set_feature(x, y, None)
        else:
            self.set_feature(x, y, '*')


    def find_blink_targ(self, _x, _y, range):
        l = []
        for x in xrange(_x - range, _x + range + 1):
            for y in [_y - range, _x + range]:
                if x >= 0 and y >= 0 and dg.grid_is_walk(x,y) and (x,y) not in self.monmap:
                    l.append((x,y))

        for y in xrange(_y - range - 1, _y + range):
            for x in [_x - range, _x + range]:
                if x >= 0 and y >= 0 and dg.grid_is_walk(x,y) and (x,y) not in self.monmap:
                    l.append((x,y))

        if len(l) == 0:
            return _x, _y

        l = l[dg.random_n(len(l))]
        return l[0], l[1]


    def showinv(self):
        return self.p.inv.draw(self.d.w, self.h, self.dlev, self.p.plev)


    def showinv_apply(self):
        slot = self.p.inv.draw(self.d.w, self.h, self.dlev, self.p.plev)
        i = self.p.inv.drop(slot)
        if not i:
            if slot in 'abcdefghi':
                self.msg.m('You have no item in that slot.')
            return

        if not i.applies:
            self.msg.m('This item cannot be applied.')
            self.p.inv.take(i, slot)
            return

        self.apply_from_inv_aux(i)


    def tagged_apply(self):

        iss = self.p.inv.get_tagged()

        if len(iss) == 0:
            self.msg.m("Tag an item from your inventory to use this command.")
            return

        items = [i[2] for i in iss]

        i,c = self.pick_one_item(items)
        if not i:
            return

        i = self.p.inv.drop(iss[c][1])

        self.apply_from_inv_aux(i)


    def slot_to_name(self, slot):
        if slot == 'a': return 'head'
        elif slot == 'b': return 'neck'
        elif slot == 'c': return 'trunk'
        elif slot == 'd': return 'left hand'
        elif slot == 'e': return 'right hand'
        elif slot == 'f': return 'legs'
        elif slot == 'g': return 'feet'
        else: return 'backpack'


    def delete_item(self, items, c, x, y):
        del items[c]
        if len(items) == 0:
            del self.itemap[(x,y)]
            return True
        return False


    def take_aux(self, items, c):

        i = items[c]
        did_scavenge = False

        def takepred(i, slot):
            if ii.stackrange and ii.count < ii.stackrange:
                return 1
            elif i.ammo > 0 and ii.ammo and ii.ammo < ii.ammochance[1]:
                return 2
            return False

        def takefunc(ii, whc):
            if whc == 1:
                n = min(ii.stackrange - ii.count, i.count)
                ii.count += n
                i.count -= n

                self.msg.m('You now have ' + str(ii) + '.')

                if i.count == 0:
                    if self.delete_item(items, c, self.px, self.py):
                        return True, False

            elif whc == 2:
                n = min(ii.ammochance[1] - ii.ammo, i.ammo)
                ii.ammo += n
                i.ammo -= n
                self.msg.m("You find some ammo for your " + ii.name + '.')
            return False, False

        if self.filter_inv(takepred, takefunc):
            self.tick()
            return

        ok = self.p.inv.take(i)
        if ok:
            self.msg.m('You take ' + str(i) + '.')
            self.delete_item(items, c, self.px, self.py)
        else:
            self.msg.m('You have no free inventory slot for ' + str(i) + '!')

        self.tick()


    def apply_from_inv_aux(self, i):
        i2 = self.apply(i)

        if i2 == -1:
            self.p.inv.take(i)
            return

        if i2:
            self.p.inv.take(i2)
        else:
            if i.count > 0:
                i.count -= 1
            if i.count > 0:
                self.p.inv.take(i)

        self.tick()

    def take(self):
        if (self.px, self.py) not in self.itemap:
            self.msg.m('You see no item here to take.')
            return

        self.showinv_interact(takestuff=True)

    def showinv_interact(self, takestuff=False):

        floorstuff = None
        flooritems = {}
        items = []

        if (self.px, self.py) in self.itemap:
            floorstuff = ['','Items on the floor:','']

            items = self.itemap[(self.px, self.py)]
            pad = ' ' * 12

            for i in xrange(len(items)):
                if i > 5:
                    floorstuff.append('(There are other items here; clear away the pile to see more)')
                    break
                else:
                    cc = chr(106 + i)
                    flooritems[cc] = i
                    floorstuff.append('%c%c) %s%c%s' % \
                        (libtcod.COLCTRL_5, cc, pad, libtcod.COLCTRL_1, str(items[i])))

        if takestuff and len(flooritems) == 1:
            slot = 'j'
        else:
            slot = self.p.inv.draw(self.d.w, self.h, self.dlev, self.p.plev, floor=floorstuff)

        i = None
        if slot in flooritems:
            i = items[flooritems[slot]]
        else:
            i = self.p.inv.check(slot)

        if not i:
            if slot in 'abcdefghi':
                self.msg.m('You have no item in that slot.')
            return

        if takestuff and slot in flooritems:
            self.take_aux(items, flooritems[slot])
            return

        si = str(i)
        si = si[0].upper() + si[1:]
        s = [si + ':', '']
        choices = ''


        if i.applies:
            s.append('a) use it')
            choices += 'a'

            if not i.tag:
                s.append('z) tag this item for quick access')
            else:
                s.append('z) remove tag from this item')
            choices += 'z'

        if i.desc:
            s.append('c) examine this item')
            choices += 'c'

        if i.throwable:
            s.append('f) throw this item')
            choices += 'f'

        if i.liveexplode is None:
            s.append('q) destroy this item')
            choices += 'q'

        if slot not in flooritems:

            s.append('d) drop this item')
            choices += 'd'

            do_x = False
            if i.slot in 'abcdefg' and slot in 'hi':
                do_x = True

            elif slot in 'abcdefg':
                backpk1 = self.p.inv.check('h')
                backpk2 = self.p.inv.check('i')
                if not backpk1 or backpk1.slot == slot or not backpk2 or backpk2.slot == slot:
                    do_x = True

            if do_x:
                s.append('x) swap this item with item in equipment')
                choices += 'x'

        else:
            s.append('t) take this item')
            choices += 't'

            s.append('x) swap this item with item in equipment')
            choices += 'x'

        self.draw()
        cc = draw_window(s, self.d.w, self.h)

        if cc not in choices:
            return

        if cc == 'a' and i.applies:
            if slot not in flooritems:
                i = self.p.inv.drop(slot)

            if slot in flooritems:
                px = self.px
                py = self.py
                self.apply_from_ground_aux(i, px, py)
            else:
                self.apply_from_inv_aux(i)

        elif cc == 'z':
            if not i.tag and i.applies:
                i.tag = self.tagorder
                self.tagorder += 1

            elif i.tag:
                i.tag = None

        elif cc == 'c' and i.desc:
            ss = i.desc[:]
            ss.append('')
            ss.append('Slot: ' + self.slot_to_name(i.slot))

            if i.converts:
                inew = self.itemstock.get(i.converts)
                if inew:
                    ss.append('Slot that needs to be free to use this item: ' + self.slot_to_name(inew.slot))

            self.draw()
            draw_window(ss, self.d.w, self.h)

        elif cc == 'd':
            i = self.p.inv.drop(slot)
            self.set_item(self.px, self.py, [i])
            self.tick()

        elif cc == 'q':

            if draw_window(['','Really destroy ' + str(i) +'? (Y/N)', ''], self.d.w, self.h) in ('y','Y'):
                if slot in flooritems:
                    self.delete_item(items, flooritems[slot], self.px, self.py)
                else:
                    self.p.inv.drop(slot)
                self.tick()

        elif cc == 'f':
            while 1:
                nx, ny = self.target(i.throwrange)
                if nx is not None:
                    break

            if nx >= 0:
                if slot not in flooritems:
                    i = self.p.inv.drop(slot)

                self.msg.m('You throw ' + str(i) + '.')

                self.set_item(nx, ny, [i])

                if slot in flooritems:
                    self.delete_item(items, flooritems[slot], self.px, self.py)

                self.tick()

        elif cc == 'x':
            if slot in flooritems:
                item2 = self.p.inv.drop(i.slot)
                ok = self.p.inv.take(i)
                if ok:
                    self.delete_item(items, flooritems[slot], self.px, self.py)

                    if item2:
                        if not self.p.inv.take(item2):
                            self.set_item(self.px, self.py, [item2])

                elif item2:
                    self.p.inv.take(item2)

            else:
                if slot != i.slot:
                    i = self.p.inv.drop(slot)
                    item2 = self.p.inv.drop(i.slot)
                    self.p.inv.take(i)
                    if item2:
                        self.p.inv.take(item2)

                else:
                    slt2 = None
                    if self.p.inv.backpack1 and self.p.inv.backpack1.slot == slot:
                        slt2 = 'h'
                    elif self.p.inv.backpack2 and self.p.inv.backpack2.slot == slot:
                        slt2 = 'i'

                    if slt2:
                        i = self.p.inv.drop(slot)
                        item2 = self.p.inv.drop(slt2)
                        self.p.inv.take(item2)
                        self.p.inv.take(i)
                    else:
                        if not self.p.inv.backpack1:
                            self.p.inv.backpack1 = self.p.inv.drop(slot)
                        elif not self.p.inv.backpack2:
                            self.p.inv.backpack2 = self.p.inv.drop(slot)

            self.tick()

        elif cc == 't':
            self.take_aux(items, flooritems[slot])



    def apply(self, item):
        if not item.applies:
            return item

        if item.applies_in_slot and self.p.inv.check(item.slot) is not None:
            self.msg.m("You can only use this item if it's in the " + self.slot_to_name(item.slot) + ' slot.', True)
            return item

        if item.converts:
            inew = self.itemstock.get(item.converts)

            if self.p.inv.check(inew.slot) is not None:
                self.msg.m('Your ' + self.slot_to_name(inew.slot) + ' slot needs to be free to use this.')
                return item

            self.p.inv.take(inew)
            s = str(inew)
            s = s[0].upper() + s[1:]
            self.msg.m(s + ' is now in your ' + self.slot_to_name(inew.slot) + ' slot!', True)

            self.p.achievements.use(item)
            return None

        elif item.craft:

            newi = None

            for i2 in self.p.inv:
                if i2 and i2.craft:
                    if item.craft[0] in i2.craft[1]:
                        newi = self.itemstock.get(i2.craft[1][item.craft[0]])
                        break

                    elif i2.craft[0] in item.craft[1]:
                        newi = self.itemstock.get(item.craft[1][i2.craft[0]])
                        break

            if not newi:
                self.msg.m('You have nothing you can combine with this item.')
                return item

            self.p.inv.purge(i2)
            self.p.achievements.craft_use(newi)
            self.msg.m('Using %s and %s you have crafted %s!' % (item, i2, newi))
            return newi

        elif item.digging:
            k = draw_window(['Dig in which direction?'], self.d.w, self.h, True)

            digspeed = self.get_digspeed() + 0.1

            self.p.digging = None
            if k == 'h': self.p.digging = (self.px - 1, self.py, digspeed)
            elif k == 'j': self.p.digging = (self.px, self.py + 1, digspeed)
            elif k == 'k': self.p.digging = (self.px, self.py - 1, digspeed)
            elif k == 'l': self.p.digging = (self.px + 1, self.py, digspeed)
            else:
                return -1 #item

            if self.p.digging[0] < 0 or self.p.digging[0] >= self.d.w:
                self.p.digging = None
                return item

            if self.p.digging[1] < 0 or self.p.digging[1] >= self.h:
                self.p.digging = None

            if not self.p.digging:
                return item

            if dg.grid_is_walk(self.p.digging[0], self.p.digging[1]):
                self.msg.m('There is nothing to dig there.')
                self.p.digging = None
            else:
                self.msg.m("You start hacking at the wall.")
                self.p.achievements.use(item)

        elif item.healing:

            if self.p.v_grace:
                self.msg.m('Your religion prohibits taking medicine.')
                return item

            if item.bonus < 0:
                self.msg.m('This pill makes your eyes pop out of their sockets!', True)
                self.tired().dec(max(dg.random_gauss(*item.healing), 0))
                self.sleep().dec(max(dg.random_gauss(*item.healing), 0))
            else:
                self.msg.m('Eating this pill makes you dizzy.')
                self.health().inc(max(dg.random_gauss(*item.healing), 0))
                self.hunger().dec(max(dg.random_gauss(*item.healing), 0))
                self.sleep().dec(max(dg.random_gauss(*item.healing), 0))

            self.p.achievements.use(item)
            return None


        elif item.healingsleep:

            if self.p.v_grace:
                self.msg.m('Your religion prohibits taking medicine.')
                return item

            if item.bonus < 0:
                self.msg.m('You drift into a restless sleep!', True)
                self.p.sleeping = max(dg.random_gauss(*item.healingsleep), 1)
                self.p.forced2sleep = True
            else:
                self.msg.m('You drift into a gentle sleep.')
                self.p.sleeping = max(dg.random_gauss(*item.healingsleep), 1)
                self.p.forced2sleep = True
                self.p.healingsleep = True

            self.p.achievements.use(item)

            if item.count == 0:
                return item
            return None

        elif item.food:

            if self.p.v_grace:
                self.msg.m('Your religion prohibits eating unclean food.')
                return item

            if item.bonus < 0:
                self.msg.m('Yuck, eating this makes you vomit!', True)
                self.hunger().dec(max(dg.random_gauss(*item.food), 0))
            else:
                self.msg.m('Mm, yummy.')
                self.hunger().inc(max(dg.random_gauss(*item.food), 0))

            self.p.achievements.use(item)
            return None

        elif item.booze:

            if self.p.v_grace:
                self.msg.m('Your religion prohibits alcohol.')
                return item

            if item.bonus < 0:
                self.msg.m("This stuff is contaminated! You fear you're going blind!", True)
                self.p.blind = True
            else:
                self.msg.m('Aaahh.')
                self.sleep().dec(max(dg.random_gauss(*self.coef.boozestrength), 0))
                self.warmth().inc(max(dg.random_gauss(*self.coef.boozestrength), 0))

            self.p.achievements.use(item)
            return None

        elif item.nodoz:
            
            if self.p.v_grace:
                self.msg.m('Your religion prohibits eating pills.')
                return item

            if item.bonus < 0:
                self.msg.m('Your heart starts palpitating!', True)
                self.tired().x = min(-2.9, self.tired().x)
            else:
                n = self.tired().x - (-2.9)

                if n <= 0:
                    self.msg.m('Nothing happens.')
                else:
                    self.msg.m('Wow, what a kick!')
                    self.sleep().inc(n)
                    self.tired().dec(n)

            self.p.achievements.use(item)
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

            self.p.achievements.use(item)

        elif item.sounding:
            k = draw_window(['Check in which direction?'], self.d.w, self.h, True)

            s = None
            if k == 'h': s = (-1, 0)
            elif k == 'j': s = (0, 1)
            elif k == 'k': s = (0, -1)
            elif k == 'l': s = (1, 0)
            else:
                return -1 #item

            n = 0
            x = self.px
            y = self.py
            while x >= 0 and y >= 0 and x < self.d.w and y < self.h:
                x += s[0]
                y += s[1]
                if dg.grid_is_walk(x,y):
                    break
                n += 1

            draw_window(['Rock depth: ' + str(n)], self.d.w, self.h)
            self.p.achievements.use(item)

        elif item.detector:
            s = []
            if item.detect_monsters:
                s.append('You detect the following monsters:')
                s.extend(sorted('  '+str(v) for v in self.monmap.itervalues()))
                s.append('')

            if item.detect_items:
                s.append('You detect the following items:')
                s.extend(sorted('  '+str(vv) for v in self.itemap.itervalues() for vv in v))
                s.append('')

            if len(s) > 19:
                s = s[:19]
                s.append('(There is more information, but it does not fit on the screen)')

            draw_window(s, self.d.w, self.h)
            self.p.achievements.use(item)

        elif item.cooling:
            self.p.cooling = max(int(dg.random_gauss(*self.coef.coolingduration)), 1)
            self.msg.m("You cover yourself in cold mud.")

            self.p.achievements.use(item)
            return None

        elif item.wishing:
            self.wish()

            self.p.achievements.use(item)
            return None

        elif item.mapper:
            self.p.mapping = item.mapper

            # HACK
            for x in xrange(self.d.w):
                for y in xrange(self.h):
                    dg.render_set_is_lit(x, y, True)

            self.p.achievements.use(item)
            return None

        elif item.jinni:
            l = []
            for ki in self.neighbors[(self.px,self.py)]:
                if dg.grid_is_walk(ki[0], ki[1]) and ki not in self.monmap:
                    l.append(ki)

            if len(l) == 0:
                self.msg.m('Nothing happened.')
                return None

            jinni = Monster('Jinni', level=self.p.plev+1,
                            attack=self.dlev*0.1,
                            defence=self.dlev*0.2,
                            range=max(self.dlev-1, 1),
                            skin=('&', libtcod.yellow),
                            desc=['A supernatural fire fiend.'])

            self.msg.m('A malevolent spirit appears!')
            q = l[dg.random_n(len(l))]
            jinni.x = q[0]
            jinni.y = q[1]
            jinni.items = [self.itemstock.get('wishing')]
            self.monmap[q] = jinni

            self.p.achievements.use(item)
            return None

        elif item.digray:
            if item.digray[0] == 1:
                for x in xrange(0, self.d.w):
                    self.convert_to_floor(x, self.py, False)
            if item.digray[1] == 1:
                for y in xrange(0, self.h):
                    self.convert_to_floor(self.px, y, False)
            self.msg.m('The wand explodes in a brilliant white flash!')

            self.p.achievements.use(item)
            return None

        elif item.jumprange:
            x, y = self.find_blink_targ(self.px, self.py, item.jumprange)
            self.px = x
            self.py = y

            self.p.achievements.use(item)

            if item.count is None:
                return item
            return None

        elif item.makestrap:
            if (self.px, self.py) in self.featmap:
                self.msg.m('Nothing happens.')
                return item

            if dg.grid_is_water(self.px, self.py):
                self.msg.m("That won't work while you're standing on water.")
                return item

            #self.featmap[(self.px, self.py)] = self.featstock.f['^']
            self.set_feature(self.px, self.py, '^')
            self.msg.m('You spread the glue liberally on the floor.')

            self.p.achievements.use(item)

            if item.count is None:
                return item
            return None

        elif item.ebola:
            self.msg.m('The Ebola virus is unleashed!')
            self.paste_celauto(self.px, self.py, self.celautostock.EBOLA)
            self.p.achievements.use(item)
            return None

        elif item.smoke:
            self.paste_celauto(self.px, self.py, self.celautostock.SMOKE)
            self.p.achievements.use(item)
            return item

        elif item.trapcloud:
            self.msg.m('You set the nanobots to work.')
            self.paste_celauto(self.px, self.py, self.celautostock.TRAPMAKER)

            self.p.achievements.use(item)

            if item.count is None:
                return item
            return None

        elif item.airfreshener:
            if item.ammo == 0:
                self.msg.m("It's out of ammo!")
                return item

            self.airfreshen(self.px, self.py, item.airfreshener)
            self.p.achievements.use(item)

            if item.ammo > 0:
                item.ammo -= 1

            if item.ammo == 0:
                return None
            return item

        elif item.resource:
            self.p.achievements.use(item)
            self.colordrink(item.resource)
            return None

        elif item.summon:
            self.summon(self.px, self.py, item.summon[0], item.summon[1])
            self.p.achievements.use(item)
            return None

        elif item.switch_moon:
            self.moon = item.switch_moon
            self.regen(self.d.w, self.h)
            self.p.achievements.use(item)
            self.msg.m('The local space-time continuum shifts slightly.', True)
            return None

        elif item.doppel:
            self.doppelpoint = (self.px, self.py)
            self.doppeltime = item.doppel
            self.p.achievements.use(item)
            self.msg.m('You activate the doppelganger.')
            return None

        elif item.winning:
            self.victory(msg=item.winning)
            return None
                    
        elif item.rangeattack or item.rangeexplode or item.fires:
            if item.ammo == 0:
                self.msg.m("It's out of ammo!")
                return item

            while 1:
                nx, ny = self.target(item.range[1],
                                     minrange=item.range[0],
                                     monstop=item.straightline,
                                     lightradius=item.lightradius)
                if nx is not None:
                    break
            if nx < 0:
                return -1 #item

            if not item.rangeexplode and not item.fires and (nx, ny) not in self.monmap:
                return -1 #item

            if item.ammo > 0:
                item.ammo -= 1

            if item.rangeexplode:
                self.explode(nx, ny, item.radius)
            elif item.fires:
                self.seed_celauto(nx, ny, self.celautostock.FIRE)
                self.set_feature(nx, ny, '"')
            else:
                self.fight(self.monmap[(nx, ny)], True, item=item)

            self.p.achievements.use(item)

            if item.ammo == 0:
                return None


        return item


    def descend(self):

        ss = self.try_feature(self.px, self.py, 'stairs')
        if not ss:
            self.msg.m('You can\'t descend, there is no hole here.')
            return

        self.msg.m('You climb down the hole.')
        self.dlev += ss

        b = self.try_feature(self.px, self.py, 'branch')
        if b:
            self.branch = b

        # Quests
        if b in self.quests:
            self.dlev = self.quests[b].dlevels[0]

        if self.dlev >= 26:
            self.victory()
            return

        self.regen(self.d.w, self.h)
        self.tick()
        self.p.achievements.descend(self.p.plev, self.d.dlev, self.d.branch)

        if self.config.music_n >= 0:
            self.config.sound.set(self.config.music_n, rate=min(10, 2.0+(0.5*self.dlev)))


    def drop(self):
        slot = self.showinv()
        i = self.p.inv.drop(slot)
        if not i:
            if slot in 'abcdefghi':
                self.msg.m('There is no item in that slot.')
            return

        self.msg.m('You drop ' + str(i) +'.')
        self.set_item(self.px, self.py, [i])
        self.tick()


    def apply_from_ground_aux(self, i, px, py):

        def _purge():
            # The item might be deleted already by the time we get here.
            if (px,py) not in self.itemap:
                return

            for ix in xrange(len(self.itemap[(px, py)])):
                if id(self.itemap[(px, py)][ix]) == id(i):

                    self.delete_item(self.itemap[(px, py)], ix, px, py)
                    break

        i2 = self.apply(i)

        if i2 == -1:
            return

        if not i2:
            if i.count > 1:
                i.count -= 1
                self.tick()
                return
            _purge()

        elif id(i2) != id(i):
            _purge()
            self.set_item(px, py, [i2])

        self.tick()

    def pick_one_item(self, items):

        if len(items) == 1:
            return items[0], 0

        c = 0
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

        c = draw_window(s, self.d.w, self.h)
        c = ord(c) - 97

        if c < 0 or c >= len(items):
            return None, None

        i = items[c]
        return i, c

    def ground_apply(self):
        px = self.px
        py = self.py

        if (px, py) not in self.itemap:
            self.msg.m('There is no item here to apply.')
            return

        items = self.itemap[(px, py)]
        items = [i for i in items if i.applies]

        if len(items) == 0:
            self.msg.m('There is no item here to apply.')
            return

        i,c = self.pick_one_item(items)
        if not i:
            return

        self.apply_from_ground_aux(i, px, py)


    def filter_items(self, x, y, func, ret):
        if (x,y) not in self.itemap:
            return

        i2 = []
        for i in self.itemap[(x,y)]:
            q1,q2 = func(i)
            if q1:
                if ret is not None:
                    ret.append((x,y,q2))
            else:
                i2.append(i)

        if len(i2) > 0:
            self.itemap[(x,y)] = i2
        else:
            del self.itemap[(x,y)]



    def victory(self, msg=None):
        while 1:
            c = draw_window(['Congratulations! You have won the game.', '', 'Press space to exit.'], self.d.w, self.h)
            if c == ' ': break

        self.health().reason = 'winning'
        self.p.done = True
        self.p.dead = True
        self.p.achievements.winner(msg)


    def handle_mondeath(self, mon, do_drop=True, do_gain=True,
                        is_rad=False, is_explode=False, is_poison=False):

        if mon.inanimate:
            do_gain = False

        if do_gain:
            self.p.achievements.mondeath(self.p.plev, self.d.dlev, mon, 
                                         is_rad=is_rad, is_explode=is_explode)
        elif is_poison:
            self.p.achievements.mondeath(self.p.plev, self.d.dlev, mon, 
                                         is_poison=True)

        if do_gain and mon.level > self.p.plev:
            self.msg.m('You just gained level ' + str(mon.level) + '!', True)
            self.p.plev = mon.level

        if do_drop:
            itemdrop = mon.items

            # HACK
            is_noncorpse = False
            if mon.flavor in ('digital', 'air', 'robot') or mon.boulder:
                is_noncorpse = True

            if self.try_feature(mon.x, mon.y, 'special') == 'cthulhu' and not is_noncorpse:
                # HACK HACK!
                itm = self.itemstock.get(['cthulhu_o1', 'cthulhu_o2', 'cthulhu_o3'][dg.random_n(3)])
                if itm:
                    itemdrop = [itm]

            elif self.moon == moon.NEW and not mon.itemdrop and not is_noncorpse:
                corpse = self.itemstock.get('corpse')
                corpse.corpse = mon
                itemdrop = itemdrop[:]
                itemdrop.append(corpse)

            if len(itemdrop) > 0:
                self.set_item(mon.x, mon.y, itemdrop)

        winner, exting = self.monsterstock.death(mon, self.moon)

        if exting:
            self.p.achievements.mondone()

        # Quests
        if self.branch in self.quests and sum(1 for m in self.monmap.itervalues() if not m.inanimate) == 1:
            quest = self.quests[self.branch]

            questdone = (quest.dlevels[1] == self.dlev)

            for msg in quest.messages[self.dlev]:
                self.msg.m(msg, True)

            if questdone:
                self.p.achievements.questdone(self.branch)
            else:
                self.set_feature(mon.x, mon.y, '>')

            qis = []
            for g in quest.gifts[self.dlev]:
                if g:
                    i = self.itemstock.get(g)
                else:
                    i = self.itemstock.generate(self.dlev)
                if i:
                    qis.append(i)

            self.set_item(mon.x, mon.y, qis)

            return

        if winner:
            self.victory()


    def rayblast(self, x0, y0, rad):

        libtcod.map_compute_fov(self.tcodmap, x0, y0, rad,
                                False, libtcod.FOV_SHADOW)

        def func1(x, y):
            return libtcod.map_is_in_fov(self.tcodmap, x, y)

        def func2(x, y):
            if x == self.px and y == self.py:
                if not self.get_radimmune():
                    self.health().dec(self.coef.raddamage, "radiation", self.config.sound)

            if (x, y) in self.monmap:
                mon = self.monmap[(x, y)]
                if not mon.radimmune:
                    mon.hp -= self.coef.raddamage
                    if mon.hp <= -3.0:
                        self.handle_mondeath(mon, is_rad=True)
                        del self.monmap[(x, y)]

        draw_blast2(x0, y0, self.d.w, self.h, rad, func1, func2)


    def explode(self, x0, y0, rad):

        chains = set()

        def f_explod(x, y):
            if x == self.px and y == self.py:
                if not self.get_explodeimmune():
                    self.health().dec(6.0, "explosion", self.config.sound)
                    self.p.dead = True

            if (x, y) in self.itemap:
                for i in self.itemap[(x, y)]:
                    if i.explodes:
                        chains.add((x, y, i.radius, True))
                        break
                del self.itemap[(x, y)]

            if (x, y) in self.monmap:
                mon = self.monmap[(x, y)]
                if not mon.explodeimmune:
                    self.handle_mondeath(mon, do_drop=False, is_explode=True)

                    for i in mon.items:
                        if i.explodes:
                            chains.add((x, y, i.radius, True))
                            break

                    del self.monmap[(x, y)]


        def func_ff(x, y):
            f_explod(x, y)

            is_gas = False
            if (x,y) in self.featmap and self.featmap[(x,y)].explode:
                is_gas = True

            self.set_feature(x, y, None)
            return is_gas


        def func_r(x, y):

            f_explod(x, y)

            if (x,y) in self.featmap and self.featmap[(x,y)].explode:
                draw_floodfill(x, y, self.d.w, self.h, func_ff)

            self.convert_to_floor(x, y, (dg.random_range(0, 5) == 0))


        draw_blast(x0, y0, self.d.w, self.h, rad, func_r)

        for x, y, r, d in sorted(chains):
            self.explode(x, y, r)



    def airfreshen(self, x0, y0, rad):

        libtcod.map_compute_fov(self.tcodmap, x0, y0, rad,
                                False, libtcod.FOV_SHADOW)

        def func1(x, y):
            return libtcod.map_is_in_fov(self.tcodmap, x, y)

        def func2(x, y):
            self.clear_celauto(x, y)

        draw_blast2(x0, y0, self.d.w, self.h, rad, func1, func2, color=libtcod.yellow)

    def raise_dead(self, x0, y0, rad):

        libtcod.map_compute_fov(self.tcodmap, x0, y0, rad,
                                False, libtcod.FOV_SHADOW)

        ret = []

        def func1(x, y):
            return libtcod.map_is_in_fov(self.tcodmap, x, y)

        def func2(x, y):
            self.filter_items(x, y, lambda i: (i.corpse, i.corpse), ret)

        draw_blast2(x0, y0, self.d.w, self.h, rad, func1, func2, color=None)
        return ret


    def fight(self, mon, player_move, item=None):

        sm = str(mon)
        smu = sm[0].upper() + sm[1:]

        ##

        if mon.boulder:
            if player_move:
                mon.bld_delta = (mon.x - self.px,
                                 mon.y - self.py)

                if mon.bld_delta[0] < -1: mon.bld_delta = (-1, mon.bld_delta[1])
                elif mon.bld_delta[0] > 1: mon.bld_delta = (1, mon.bld_delta[1])
                if mon.bld_delta[1] < -1: mon.bld_delta = (mon.bld_delta[0], -1)
                elif mon.bld_delta[1] > 1: mon.bld_delta = (mon.bld_delta[0], 1)

                self.msg.m('You push ' + sm)
                return
            else:
                self.health().dec(6, sm, self.config.sound)
                self.msg.m('You got squashed. What a silly way to die!')
                self.p.dead = True
                return

        ##

        d = math.sqrt(math.pow(abs(mon.x - self.px), 2) +
                      math.pow(abs(mon.y - self.py), 2))
        d = int(round(d))

        if player_move and item:
            plev = min(max(self.p.plev - d + 1, 1), self.p.plev)
            attack = item.rangeattack
            #log.log('+', d, plev, attack)

        else:
            if self.p.b_grace and player_move:
                self.msg.m('Your religion prohibits you from fighting.')
                return

            plev = self.p.plev
            attack = self.get_attack()

        def roll(attack, leva, defence, levd):
            a = 0
            for x in xrange(leva):
                a += dg.random_uniform(0, attack)
            d = 0
            for x in xrange(levd):
                d += dg.random_uniform(0, defence)

            ret = max(a - d, 0)
            #print ' ->', ret, ':', attack, leva, '/', defence, levd
            return ret

        if player_move:

            defence = mon.defence
            if mon.glued:
                defence /= self.coef.gluedefencepenalty

            dmg = roll(attack, plev, defence, mon.level)

            mon.hp -= dmg

            if dmg > 0:
                m = max(0.1, min(1.0, dmg/3))
                self.config.sound.play("klang1", mul=m)

            if mon.hp <= -3.0:
                if mon.visible or mon.visible_old:
                    self.msg.m('You killed ' + sm + '!')
                self.handle_mondeath(mon)
                del self.monmap[(mon.x, mon.y)]
            else:

                ca = None
                fires = None

                if item:
                    ca = item.confattack
                    fires = item.fires
                else:
                    ca = self.get_confattack()
                    fires = self.get_fires()

                if ca and dmg > 0 and not mon.confimmune:
                    if mon.visible or mon.visible_old:
                        self.msg.m(smu + ' looks totally dazed!')
                    mon.confused += int(max(dg.random_gauss(*ca), 1))

                if fires and dmg > 0 and not mon.fireimmune:
                    mon.onfire = max(self.coef.burnduration, mon.onfire)

                if not (mon.visible or mon.visible_old):
                    pass

                elif dmg > 4:
                    self.msg.m('You mortally wound ' + sm + '!')
                elif dmg > 2:
                    self.msg.m('You seriously wound ' + sm + '.')
                elif dmg > 0.5:
                    self.msg.m('You wound ' + sm + '.')
                elif dmg > 0:
                    self.msg.m('You barely wound ' + sm + '.')
                else:
                    self.msg.m('You miss ' + sm + '.')

            if dmg > 0 and (mon.visible or mon.visible_old):
                mon.known_px = self.px
                mon.known_py = self.py


        else:

            attack = None
            defence = None
            psy = False

            if d > 1 and mon.psyattack > 0:
                if self.get_psyimmune():
                    return
                attack = mon.psyattack
                defence = self.coef.unarmeddefence
                psy = True
            else:
                attack = mon.attack
                defence = self.get_defence()

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
                if dmg > 0:
                    self.msg.m('You fall asleep!')
                    self.start_sleep(force=True, quick=True, realforced=True)

            elif mon.bloodsucker:
                if dmg > 0:
                    self.msg.m('You feel weak!')
                    self.hunger().dec(mon.bloodsucker[0])
                    self.health().dec(mon.bloodsucker[0], sm, self.config.sound)
                    mon.fleetimeout = mon.bloodsucker[1]

            elif mon.hungerattack:
                self.hunger().dec(dmg)

            else:
                self.health().dec(dmg, sm, self.config.sound)

            if self.p.resting:
                self.msg.m('You stop resting.')
                self.p.resting = False

            if self.p.digging:
                self.msg.m('You stop digging.')
                self.p.digging = None

            if self.p.sleeping and not self.p.forced2sleep:
                self.p.sleeping = 0
                self.p.forcedsleep = False
                self.p.healingsleep = False

            if self.health().x <= -3.0:
                self.p.dead = True


    def look(self):
        tx = self.px
        ty = self.py

        while 1:
            seen = self.draw(tx, ty)

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
                    s.append('')
                    s.extend(m.desc)
                    s.append('')

                if (tx, ty) in self.itemap:
                    i = self.itemap[(tx, ty)]
                    s.append('You see the following items:')
                    for ix in xrange(len(i)):
                        if ix > 5:
                            s.append('(And some other items)')
                            break
                        s.append(str(i[ix]))
                    s.append('')

                if (tx, ty) in self.featmap:
                    f = self.featmap[(tx, ty)]
                    s.append('You see ' + f.name + '.')

                elif dg.grid_is_walk(tx, ty):
                    if dg.grid_is_water(tx, ty):
                        s.append('You see a water-covered floor.')
                    else:
                        s.append('You see a cave floor.')

                else:
                        s.append('You see a cave wall.')

            k = draw_window(s, self.d.w, self.h, True)

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
            elif tx >= self.d.w: tx = self.d.w - 1

            if ty < 0: ty = 0
            elif ty >= self.h: ty = self.h - 1


    def _target(self, point, range, minrange=0, monstop=False, lightradius=None):

        self.draw(range=(minrange, range), lightradius=lightradius)

        #monx = None
        #mony = None

        if point[0] is None:
            for i in xrange(len(self.monsters_in_view)):
                mon = self.monsters_in_view[i]
                d = math.sqrt(math.pow(abs(self.px - mon.x), 2) +
                              math.pow(abs(self.py - mon.y), 2))

                #log.log(" #", mon.x, mon.y, d, range, minrange)
                if d > range:
                    continue

                if d < minrange:
                    continue

                #log.log(" # ok")
                #monx = mon.x
                #mony = mon.y
                point = (mon.x, mon.y)

                del self.monsters_in_view[i]
                self.monsters_in_view.append(mon)
                break

        tmsg = ['Pick a target.  '
                "HJKL YUBN for directions, "
                "<space> to choose and '.' to fire."]

        if point[0] is not None:
            self.draw(point[0], point[1], range=(minrange, range), 
                      lightradius=lightradius)
            if point[1] <= 2:
                tmsg = []

        k = draw_window(tmsg,
                        self.d.w, self.h, True)

        poiok = (point[0] is not None)
        final_choice = False
                           

        if k == 'h':
            if poiok: point = (max(point[0]-1,0), point[1])
            else:     point = (max(self.px-range,0), self.py)
        elif k == 'j':
            if poiok: point = (point[0], min(point[1]+1,self.h-1))
            else:     point = (self.px, min(self.py+range, self.h-1))
        elif k == 'k':
            if poiok: point = (point[0], max(point[1]-1,0))
            else:     point = (self.px, max(self.py-range,0))
        elif k == 'l':
            if poiok: point = (min(point[0]+1,self.d.w-1), point[1])
            else:     point = (min(self.px+range,self.d.w-1), self.py)
        elif k == 'y':
            if poiok: point = (max(point[0]-1,0), max(point[1]-1,0))
            else:     point = (max(self.px - int(range * 0.71), 0),
                               max(self.py - int(range * 0.71), 0))
        elif k == 'u':
            if poiok: point = (min(point[0]+1,self.d.w-1), max(point[1]-1,0))
            else:     point = (min(self.px + int(range * 0.71), self.d.w - 1),
                               max(self.py - int(range * 0.71), 0))
        elif k == 'b':
            if poiok: point = (max(point[0]-1,0), min(point[1]+1,self.h-1))
            else:     point = (max(self.px - int(range * 0.71), 0),
                               min(self.py + int(range * 0.71), self.h - 1))
        elif k == 'n':
            if poiok:  point = (min(point[0]+1,self.d.w-1), min(point[1]+1,self.h-1))
            else:      point = (min(self.px + int(range * 0.71), self.d.w - 1),
                                min(self.py + int(range * 0.71), self.h - 1))
        elif k == '.':
            if poiok is None:
                return (None, None), False
            else:
                final_choice = True
        elif k == ' ':
            return (None, None), False
        else:
            return (-1, -1), True

        libtcod.line_init(self.px, self.py, point[0], point[1])
        xx = None
        yy = None
        while 1:
            tmpx, tmpy = libtcod.line_step()

            if tmpx is None:
                #return (xx, yy), True
                break

            if dg.grid_is_walk(tmpx, tmpy) or self.try_feature(tmpx, tmpy, 'shootable'):

                if minrange > 0:
                    d = math.sqrt(math.pow(abs(tmpx - self.px), 2) +
                                  math.pow(abs(tmpy - self.py), 2))
                    if d < minrange:
                        continue

                xx = tmpx
                yy = tmpy

                if monstop and (tmpx, tmpy) in self.monmap:
                    #return (xx, yy), True
                    break

            else:
                break
                #return (xx, yy), True

        if final_choice and xx == point[0] and yy == point[1]:
            return (xx, yy), True
        return (xx, yy), False



    def target(self, range, minrange=0, monstop=False, lightradius=None):

        point = (None, None)
        while 1:
            point, ok = self._target(point, range, 
                                     minrange=minrange, 
                                     monstop=monstop, 
                                     lightradius=lightradius)

            if ok:
                return point



    def show_messages(self):
        self.msg.show_all(self.d.w, self.h)


    def wish(self, msg=None):
        s = ''
        while 1:
            if msg:
                k = draw_window([msg, '', 'Wish for what? : ' + s],
                                self.d.w, self.h)
            else:
                k = draw_window(['Wish for what? : ' + s], self.d.w, self.h)

            k = k.lower()
            if k in "abcdefghijklmnopqrstuvwxyz' -":
                s = s + k
            elif ord(k) == 8 or ord(k) == 127:
                if len(s) > 0:
                    s = s[:-1]
            elif k in '\r\n':
                break

        i = self.itemstock.find(s)

        self.p.achievements.wish()

        if not i:
            self.msg.m('Nothing happened!')
        else:
            self.msg.m('Suddenly, ' + str(i) + ' appears at your feet!')
            self.set_item(self.px, self.py, [i])


    def move_down(self): self.move(0, 1)
    def move_up(self): self.move(0, -1)
    def move_left(self): self.move(-1, 0)
    def move_right(self): self.move(1, 0)
    def move_upleft(self): self.move(-1, -1)
    def move_upright(self): self.move(1, -1)
    def move_downleft(self): self.move(-1, 1)
    def move_downright(self): self.move(1, 1)



    def quit(self):
        k = draw_window(["Really quit? Press 'y' if you are truly sure."], self.d.w, self.h)
        if k == 'y':
            self.health().reason = 'quitting'
            self.p.dead = True


    def show_help(self):
        s = [('%c' % libtcod.COLCTRL_1) + \
             "Movement keys: roguelike 'hjkl' 'yubn' or the numpad/arrow keys.",
             "",
             " .   : Stand in place for one turn.",
             " s   : Start sleeping.",
             " r   : Start resting.",
             " q   : Drink from the floor.",
             " p   : Pray at a shrine.",
             " >   : Descend down to the next level.",
             "",
             " a   : Apply (use) an item from your inventory.",
             " A   : Apply (use) an item from the ground.",
             " z   : Apply (use) an item tagged for quick access.",
             " i   : Manipulate your inventory or items on the ground.",
             " d   : Drop an item from your inventory.",
             " ,   : Pick up an item from the ground.",
             "",
             " /   : Look around at the terrain, items and monsters.",
             " P   : Show a log of previous messages.",
             " Q   : Quit the game by committing suicide.",
             " S   : Save the game and quit.",
             " F11 : Toggle fullscreen mode.",
             " F10 : Toggle sound.",
             " F9  : Toggle music.",
             " ?   : Show this help."
        ]
        draw_window(s, self.d.w, self.h)


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
            'p': self.pray,
            'a': self.showinv_apply,
            'A': self.ground_apply,
            'z': self.tagged_apply,
            'i': self.showinv_interact,
            '>': self.descend,
            'd': self.drop,
            ',': self.take,
            '/': self.look,
            'P': self.show_messages,
            'Q': self.quit,
            '?': self.show_help,
            'S': self.save
            }
        self.vkeys = {
            libtcod.KEY_KP4: self.move_left,
            libtcod.KEY_KP6: self.move_right,
            libtcod.KEY_KP8: self.move_up,
            libtcod.KEY_KP2: self.move_down,
            libtcod.KEY_KP7: self.move_upleft,
            libtcod.KEY_KP9: self.move_upright,
            libtcod.KEY_KP1: self.move_downleft,
            libtcod.KEY_KP3: self.move_downright,

            libtcod.KEY_LEFT: self.move_left,
            libtcod.KEY_RIGHT: self.move_right,
            libtcod.KEY_UP: self.move_up,
            libtcod.KEY_DOWN: self.move_down,
            libtcod.KEY_HOME: self.move_upleft,
            libtcod.KEY_PAGEUP: self.move_upright,
            libtcod.KEY_END: self.move_downleft,
            libtcod.KEY_PAGEDOWN: self.move_downright,

            libtcod.KEY_F11: self.toggle_fullscreen,
            libtcod.KEY_F10: self.toggle_sound,
            libtcod.KEY_F9: self.toggle_music
            }


    def walk_monster(self, mon, dist, x, y):

        if mon.moldspew and (self.t % mon.moldspew[2]) == 0:
            for ki in self.neighbors[(x,y)]:
                if dg.random_range(1, mon.moldspew[1]) == 1:
                    self.seed_celauto(ki[0], ki[1], mon.moldspew[0])

        if mon.static:
            return None, None

        if mon.slow and (self.t & 1) == 0:
            return None, None

        if mon.glued > 0:
            mon.glued -= 1
            if mon.glued == 0:
                if (mon.x, mon.y) in self.featmap and \
                   self.featmap[(mon.x, mon.y)] == self.featstock.f['^']:
                    self.unset_feature(mon.x, mon.y)
            else:
                return None, None

        if mon.boulder:
            if mon.bld_delta:
                ret =  (mon.x + mon.bld_delta[0],
                        mon.y + mon.bld_delta[1])

                if not dg.grid_is_walk(ret[0], ret[1]):
                    mon.bld_delta = None
                    return None, None
                else:
                    return ret[0], ret[1]
            else:
                return None, None

        rang = self.get_camorange(mon.range)

        if self.try_feature(x, y, 'confuse'):
            rang = 1

        if dist > rang or mon.confused or (mon.sleepattack and self.p.sleeping):
            mdx = x + dg.random_range(-1, 1)
            mdy = y + dg.random_range(-1, 1)
            if not dg.grid_is_walk(mdx, mdy):
                mdx = None
                mdy = None
            if mon.confused:
                mon.confused -= 1

        else:

            if mon.psyrange > 0 and dist <= mon.psyrange:
                self.fight(mon, False)

            repelrange = self.get_repelrange()

            if repelrange and dist <= repelrange and dist > 1:
                 return None, None

            if mon.heatseeking:
                if (dg.grid_is_water(self.px, self.py) or self.p.cooling or mon.onfire):
                    if mon.known_px is None or mon.known_py is None:
                        mon.known_px = mon.x
                        mon.known_py = mon.y
                else:
                    mon.known_px = self.px
                    mon.known_py = self.py
            else:
                if self.doppeltime > 0:
                    mon.known_px = self.doppelpoint[0]
                    mon.known_py = self.doppelpoint[1]
                else:
                    mon.known_px = self.px
                    mon.known_py = self.py


            if mon.straightline:
                libtcod.line_init(x, y, mon.known_px, mon.known_py)
                mdx, mdy = libtcod.line_step()
            else:

                flee = False

                if mon.blink_away and dist < 2.0:
                    mdx, mdy = self.find_blink_targ(x, y, mon.blink_away)
                    return mdx, mdy

                elif mon.fleerange and dist <= mon.fleerange:
                    if math.fabs(dist - mon.fleerange) < 0.9:
                        return None, None
                    flee = True

                elif mon.fleetimeout > 0 and dist <= mon.range - 2:
                    flee = True
                    mon.fleetimeout -= 1

                if flee:
                    mdx, mdy = None, None
                    for _x,_y in self.neighbors[(x,y)]:
                        if dg.grid_is_walk(_x,_y) and \
                           ((mon.known_px >= x and _x < x) or \
                            (mon.known_px <= x and _x > x) or \
                            (mon.known_py <= y and _y > y) or \
                            (mon.known_py >= y and _y < y)):
                            mdx, mdy = _x, _y
                            break

                else:
                    libtcod.path_compute(self.floorpath, x, y, mon.known_px, mon.known_py, rang*2)
                    mdx, mdy = libtcod.path_walk(self.floorpath, True, rang*2)

                    if mon.fast:
                        mdx2, mdy2 = libtcod.path_walk(self.floorpath, True, rang*2)
                        if mdx2 is not None and mdy2 is not None:
                            mdx, mdy = mdx2, mdy2
                    
                    if mdx is None or mdy is None:
                        mdx = x + dg.random_range(-1, 1)
                        mdy = y + dg.random_range(-1, 1)
                        if not dg.grid_is_walk(mdx, mdy):
                            mdx = None
                            mdy = None



        if mon.stoneeating:
            if mdx is not None:
                if self.try_feature(mdx, mdy, 'permanent'):
                    return None, None

                if not dg.grid_is_walk(mdx, mdy):
                    self.convert_to_floor(mdx, mdy, True)

        return mdx, mdy

    def process_monstep(self, mon):
        mdx = mon.x
        mdy = mon.y

        if self.try_feature(mdx, mdy, 'sticky') and not mon.flying:
            if mon.visible or mon.visible_old:
                mn = str(mon)
                mn = mn[0].upper() + mn[1:]
                self.msg.m(mn + ' gets stuck in some glue!')
            mon.glued = max(int(dg.random_gauss(*self.coef.glueduration)), 1)


    def monster_conflict(self, mon_attack, mon_defend):
        if mon_attack.boulder:
            if mon_defend.large:
                mon_attack.bld_delta = None
            else:
                if mon_defend.visible or mon_defend.visible_old:
                    sm = str(mon_attack)
                    smu = sm[0].upper() + sm[1:]
                    self.msg.m(smu + ' squashes ' + str(mon_defend) + '!')
                return True

        return False

    def summon(self, x, y, monname, n):
        if monname is None:
            m = []
            for ii in xrange(n):
                mmi = self.monsterstock.generate(self.branch, self.dlev, self.itemstock, self.moon)
                if mmi and not mmi.inanimate:
                    m.append(mmi)

        else:
            m = self.monsterstock.find(monname, n, self.itemstock)
            if len(m) == 0:
                return []

        l = []
        for ki in self.neighbors[(x,y)]:
            if dg.grid_is_walk(ki[0], ki[1]) and \
               ki not in self.monmap and \
               (ki[0] != self.px or ki[1] != self.py):
                l.append(ki)

        ret = []
        for i in xrange(len(m)):
            if len(l) == 0:
                return ret
            j = dg.random_n(len(l))
            xx,yy = l[j]
            del l[j]

            m[i].x = xx
            m[i].y = yy
            self.monmap[(xx, yy)] = m[i]
            ret.append(m[i])

        return ret


    def moon_message(self):
        if self.did_moon_message:
            return

        if len(self.msg.strings) > 0 and self.msg.strings[0][2][0] and (self.t - self.msg.strings[0][2][0]) > 9:
            d = {moon.NEW:  'New moon tonight. A perfect night for evil and the dark arts.',
                 moon.FULL: 'Full moon tonight. The lunatics are out in droves.',
                 moon.FIRST_QUARTER: 'First quarter moon tonight. Watch out for the UFOs.',
                 moon.LAST_QUARTER: 'Last quarter moon tonight. Watch out for the UFOs.',
                 moon.WAXING_CRESCENT: "Tonight's moon is waxing crescent.",
                 moon.WAXING_GIBBOUS: "Tonight's moon is waxing gibbous.",
                 moon.WANING_CRESCENT: "Tonight's moon is waning crescent.",
                 moon.WANING_GIBBOUS: "Tonight's moon is waning gibbous."}

            self.msg.m(d[self.moon], True)
            self.did_moon_message = True


    def monster_flavor_message(self, mon, dist):
        def msg(flavor, dist):
            m = max(0.1, min(1.0, 1.0 - (dist/50)))

            if flavor == 'air':
                self.msg.m('You hear the hissing of air.')
                self.config.sound.play("air", mul=m)

            elif flavor == 'animal':
                self.msg.m('You hear the sounds of a restless animal.')
                self.config.sound.play("hooves", mul=m)

            elif flavor == 'carnivore':
                self.msg.m('You hear the roar of an animal.')
                self.config.sound.play("roar", mul=m)

            elif flavor == 'digital':
                self.msg.m('You hear the sounds of 8-bit music.')
                self.config.sound.play("nintendo", mul=m)

            elif flavor == 'earthshake':
                self.msg.m('You feel the earth shake.')
                self.config.sound.play("quake", mul=m)

            elif flavor == 'faerie':
                self.msg.m('You hear the tinkling of bells.')
                self.config.sound.play("bells", mul=m)

            elif flavor == 'flying':
                self.msg.m('You hear the flapping of wings.')
                self.config.sound.play("wings", mul=m)

            elif flavor == 'giant':
                self.msg.m('You hear a loud rumble.')
                self.config.sound.play("boom", mul=m)

            elif flavor == 'humanwarrior':
                self.msg.m('You hear the angry sounds of a foreign language.')
                self.config.sound.play("mutter", mul=m)

            elif flavor == 'humanweird':
                self.msg.m('You hear somebody wildly gibber.')
                self.config.sound.play("laugh", mul=m)

            elif flavor == 'robot':
                self.msg.m('You hear the clanking of metal.')
                self.config.sound.play("robot", mul=m)

            elif flavor == 'snake':
                self.msg.m('You hear something slither.')
                self.config.sound.play("slither", mul=m)

            elif flavor == 'weird':
                self.msg.m('You faintly sense eldritch chanting.')
                self.config.sound.play("cthulhu", mul=m)

            elif flavor == 'wizard':
                self.msg.m('You hear incantations of arcana.')
                self.config.sound.play("wizard", mul=m)


        d = (mon.level - self.p.plev)
        if d >= 2:
            ok = False
            if d == 2 and dg.random_range(0, 50) == 1:
                ok = True
            elif d == 3 and dg.random_range(0, 20) == 1:
                ok = True
            elif dg.random_range(0, 10) == 1:
                ok = True

            if ok:
                t = int(time.time())
                if t - self.last_played_themesound < 5:
                    return

                msg(mon.flavor, dist)
                self.last_played_themesound = t


    def paste_celauto(self, x, y, ca):
        self.celautostock.paste(x, y, self.d.w, self.h, ca)

    def seed_celauto(self, x, y, ca):
        self.celautostock.seed(x, y, ca)

    def clear_celauto(self, x, y):
        def cboff(x,y,ca):
            self.celauto_off(x,y,ca)
        self.celautostock.clear(x, y, cboff)
        


    def celauto_on(self, x, y, ca):
        ca = self.celautostock.stock[ca]

        if ca.watertoggle is not None:
            dg.grid_set_water(x, y, True)
        elif ca.featuretoggle:
            if (x, y) not in self.featmap and dg.grid_is_walk(x, y):
                self.set_feature(x, y, ca.featuretoggle)
        elif ca.floorfeaturetoggle:
            if (x, y) not in self.featmap and dg.grid_is_walk(x, y) and not dg.grid_is_water(x, y):
                self.set_feature(x, y, ca.floorfeaturetoggle)

        if ca.littoggle is not None and dg.grid_is_walk(x,y):
            dg.render_set_is_lit(x, y, True)

    def celauto_off(self, x, y, ca):
        ca = self.celautostock.stock[ca]

        if ca.watertoggle is not None:
            dg.grid_set_water(x, y, False)
        elif ca.featuretoggle and (x, y) in self.featmap and \
             self.featmap[(x, y)] == self.featstock.f[ca.featuretoggle]:
            self.unset_feature(x, y)

        if ca.littoggle is not None and dg.grid_is_walk(x,y):
            dg.render_set_is_lit(x, y, False)


    def process_world(self):

        def cbon(x,y,ca):
            self.celauto_on(x,y,ca)

        def cboff(x,y,ca):
            self.celauto_off(x,y,ca)

        self.celautostock.celauto_step(cbon, cboff)

        explodes = set()
        mons = []
        delitems = []
        rblasts = []

        for k,v in sorted(self.itemap.iteritems()):
            for i in v:
                if i.liveexplode > 0:
                    i.liveexplode -= 1
                    if i.liveexplode == 0:
                        if i.summon:
                            self.summon(k[0], k[1], i.summon[0], i.summon[1])
                        elif i.radexplode:
                            rblasts.append((k[0], k[1], i.radius))
                        elif i.swampgas:
                            self.paste_celauto(self.px, self.py, self.celautostock.SWAMPGAS)
                        else:
                            explodes.add((k[0], k[1], i.radius))

                        delitems.append(k)

        for x,y,r in rblasts:
            self.rayblast(x, y, r)

        for ix,iy in delitems:
            self.filter_items(ix, iy, lambda i: (i.liveexplode == 0, None), None)

        summons = []
        raise_dead = []

        for k,mon in sorted(self.monmap.iteritems()):
            #log.log('  tick:', k)

            x, y = k
            if mon.static:
                dist = 0
            else:
                dist = math.sqrt(math.pow(abs(self.px - x), 2) + math.pow(abs(self.py - y), 2))

            mon.do_move = None

            if mon.static:
                pass

            elif (mon.visible or mon.visible_old) and not (mon.was_seen) and not self.p.mapping:
                mon.was_seen = True
                self.msg.m('You see ' + str(mon) + '.')
                m = max(0.25, min(3, 0.5 * (mon.level - self.p.plev)))
                self.config.sound.play("wobble", dur=m)

            elif not mon.visible:
                self.monster_flavor_message(mon, dist)


            p = self.try_feature(x, y, 'poison')
            if p and not mon.poisimmune:
                mon.hp -= p
                if mon.hp <= -3.0:
                    if mon.visible:
                        smu = str(mon)
                        smu = smu[0].upper() + smu[1:]
                        self.msg.m(smu + ' falls over and dies!')

                    self.handle_mondeath(mon, do_gain=False, 
                                         is_poison=(False if self.featmap[(x,y)].pois2 else True))
                    mon.do_die = True
                    mons.append(mon)
                    continue

            p = self.try_feature(x, y, 'fire')
            if (p or mon.onfire) and not mon.fireimmune:
                mon.hp -= (p or self.coef.burndamage)
                if mon.hp <= -3.0:
                    if mon.visible:
                        smu = str(mon)
                        smu = smu[0].upper() + smu[1:]
                        self.msg.m(smu + ' burns ' + ('up.' if mon.boulder else 'to death!'))

                    self.handle_mondeath(mon, do_gain=True)
                    mon.do_die = True
                    mons.append(mon)
                    continue

                elif p:
                    mon.onfire = max(self.coef.burnduration, mon.onfire)

                else:
                    mon.onfire -= 1
                    self.seed_celauto(x, y, self.celautostock.FIRE)
                    self.set_feature(x, y, '"')



            msumm = (mon.summon or mon.summononce)

            if msumm and (mon.visible or mon.static) and (self.t % msumm[1]) == 0:
                summons.append((k, mon))
                continue

            if mon.raise_dead and (mon.visible or mon.static) and (self.t % mon.raise_dead[1]) == 0:
                raise_dead.extend(self.raise_dead(mon.x, mon.y, mon.raise_dead[0]))

            mon.visible_old = mon.visible
            mon.visible = False

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
                    
                    if mon.do_move in self.monmap:
                        mon2 = self.monmap[mon.do_move]
                        if self.monster_conflict(mon, mon2):
                            self.handle_mondeath(mon2)
                            mon2.do_die = True
                            mons.append(mon2)

                mons.append(mon)


        for k,mon in summons:
            smu = str(mon)
            smu = smu[0].upper() + smu[1:]

            if mon.summon:
                q = self.summon(k[0], k[1], mon.summon[0], 1)
                if len(q) > 0:
                    if not mon.static:
                        self.msg.m(smu + ' summons ' + str(q[0]) + '!')
                else:
                    mon.summon = None

            elif mon.summononce:
                q = self.summon(k[0], k[1], None, mon.summononce[0])
                if len(q) > 0:
                    self.msg.m(smu + ' summons monsters!')
                    mon.summononce = None



        for x,y,mon in raise_dead:
            if dg.grid_is_walk(x,y) and (x,y) not in self.monmap and not (x == self.px and y == self.py):
                smu = str(mon)
                smu = smu[0].upper() + smu[1:]
                self.msg.m(smu + ' rises from the dead!')
                mon.reset()
                mon.x = x
                mon.y = y
                self.monmap[(x,y)] = mon


        for mon in mons:
            if mon.do_die:
                if (mon.x, mon.y) in self.monmap:
                    del self.monmap[(mon.x, mon.y)]
            elif mon.do_move:
                mon.old_pos = (mon.x, mon.y)
                del self.monmap[(mon.x, mon.y)]

        for mon in mons:
            if mon.do_die:
                continue

            elif mon.do_move:
                if mon.do_move in self.monmap:
                    mon.do_move = mon.old_pos

                mon.x = mon.do_move[0]
                mon.y = mon.do_move[1]
                self.monmap[mon.do_move] = mon
                mon.do_move = None

                self.process_monstep(mon)

        for x, y, r in sorted(explodes):
            self.explode(x, y, r)



    def draw_hud(self):
        statsgrace = None
        if self.p.s_grace:
            statsgrace = (chr(234),
                          ((self.p.s_grace * 6) / self.coef.s_graceduration) + 1,
                          (self.p.s_grace > self.coef.s_graceduration - self.coef.s_praytimeout))

        elif self.p.v_grace:
            statsgrace = (chr(233),
                          ((self.p.v_grace * 6) / self.coef.v_graceduration) + 1,
                          (self.p.v_grace > self.coef.v_graceduration - self.coef.v_praytimeout))

        elif self.p.b_grace:
            statsgrace = (chr(127),
                          ((self.p.b_grace * 6) / self.coef.b_graceduration) + 1,
                          False)

        statsresource = None
        if self.p.resource:
            if self.p.resource_timeout:
                n = ((self.p.resource_timeout * 6) / self.coef.resource_timeouts[self.p.resource] + 1)
            else:
                n = self.p.resource_buildup

            statsresource = (self.p.resource, n,
                             True if self.p.resource_timeout else False)

        luck = -2

        if self.px > self.d.w / 2:
            self.stats.draw(0, 0, grace=statsgrace, resource=statsresource, luck=luck)
        else:
            self.stats.draw(self.d.w - 14, 0, grace=statsgrace, resource=statsresource, luck=luck)

        if self.py > self.h / 2:
            self.msg.draw(15, 0, self.d.w - 30, self.t)
        else:
            self.msg.draw(15, self.h - 3, self.d.w - 30, self.t)


    ### 

    def draw(self, _hlx=1000, _hly=1000, range=(0,1000), lightradius=None):

        withtime = False
        if self.oldt != self.t:
            withtime = True

        lightradius = self.get_lightradius(lightradius)

        did_mapping = False
        if self.p.mapping > 0:
            did_mapping = True
            if withtime:
                self.p.mapping -= 1

            if self.p.mapping > 0:
                lightradius = 25

            else:
                # HACK
                for x in xrange(self.d.w):
                    for y in xrange(self.h):
                        dg.render_set_is_lit(x, y, False)


        if withtime:
            self.process_world()
            self.monsters_in_view = []

        # hack, after process_world because confusing features may be created
        if self.try_feature(self.px, self.py, 'confuse'):
            lightradius = 1

        
        did_highlight = False

        telerange = self.get_telepathyrange()

        ###

        for k,v in sorted(self.itemap.iteritems()):
            itm = v[0]

            if itm.corpse:
                dg.render_push_skin(k[0], k[1], itm.corpse.skin[1], itm.skin[0], libtcod.black, 0, False)
            else:
                dg.render_push_skin(k[0], k[1], itm.skin[1], itm.skin[0], libtcod.black, 0, False)


        if self.doppeltime > 0:
            dg.render_push_skin(self.doppelpoint[0], self.doppelpoint[1],
                                libtcod.white, '@', libtcod.black, 0, False)

        lit_mons = set()

        for k,v in sorted(self.monmap.iteritems()):
            dg.render_push_skin(k[0], k[1], v.skin[1], v.skin[0], libtcod.black, 0, v.boulder)

            if telerange and not v.inanimate:
                d = math.sqrt(math.pow(abs(self.px - k[0]),2) + math.pow(abs(self.py - k[1]),2))

                if d <= telerange:
                    lit_mons.add(k)
                    dg.render_set_is_lit(k[0], k[1], True)


        pc = '@'
        if self.p.sleeping > 1 and (self.t & 1) == 1:
            pc = '*'
        elif self.p.resting and (self.t & 1) == 1:
            pc = '.'
        elif self.p.digging and (self.t & 1) == 1:
            pc = '('
        else:
            pc = '@'

        pccol = libtcod.white
        if self.p.onfire:
            pccol = libtcod.amber
        dg.render_push_skin(self.px, self.py, pccol, pc, libtcod.black, 0, False)

        ###

        did_highlight = dg.render_draw(self.tcodmap, self.t, self.px, self.py, 
                                       _hlx, _hly, range[0], range[1], lightradius)
        
        ###

        dg.render_pop_skin(self.px, self.py)

        self.new_visibles = False

        for k,v in sorted(self.monmap.iteritems()):
            dg.render_pop_skin(k[0], k[1])
            if k in lit_mons:
                dg.render_set_is_lit(k[0], k[1], False)

            if withtime and dg.render_is_in_fov(k[0], k[1]):
                self.monsters_in_view.append(v)
                v.visible = True

                # Hack
                if not v.visible_old:
                    self.new_visibles = True


        if self.doppeltime > 0:
            dg.render_pop_skin(self.doppelpoint[0], self.doppelpoint[1])

        for k,v in sorted(self.itemap.iteritems()):
            dg.render_pop_skin(k[0], k[1])

        ### 

        if not did_mapping:
            self.draw_hud()

        # hack
        if withtime:
            self.moon_message()
            self.oldt = self.t

        return did_highlight


    def save(self):
        # HACK! For supporting replays of games that have been saved and then loaded.
        if self.save_disabled:
            dg.random_init(self._seed)
            return


        f = None
        atts = [
          'exit', 'itemap', 'monmap', 
          'featmap', 'px', 'py', 'w', 'h',
          'done', 'dead', 'stats', 'msg', 'coef', 'inv', 'itemstock', 'monsterstock', 'branch',
          'dlev', 'plev', 't', 'oldt', 'tagorder', 'sleeping', 'resting', 'cooling', 'digging', 'blind',
          'mapping', 'glued', 'onfire', 's_grace', 'b_grace', 'v_grace', 'forcedsleep',
          'forced2sleep', 'healingsleep', 'doppelpoint', 'doppeltime',
          '_seed', '_inputs', 'featstock', 'vaultstock',
          'achievements', 'bones', 'resource', 'resource_buildup', 'resource_timeout',
          'neighbors', 'moon', 'did_moon_message'
          ]
        state = {}

        for x in atts:
            state[x] = getattr(self, x)

        if 1: #try:
            f = open('savefile.dat0', 'w')
            cPickle.dump(state, f)
        #except:
        #    return

        dg.state_save('savefile.dat1')

        self.msg.m('Saved!')
        self.p.done = True


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
            f = open('savefile.dat0', 'r')
            state = cPickle.load(f)
        except:
            return False

        for k,v in state.iteritems():
            setattr(self, k, v)

        dg.state_load('savefile.dat1')

        #log.f = open('LOG.%d' % self._seed, 'a')

        dg.random_init(self._seed)
        global _inputs
        _inputs = self._inputs

        self.make_map()
        self.make_paths()

        # HACK
        dg.neighbors_init(self.d.w, self.h)

        return True


    def form_highscore(self):

        # Clobber the savefile.
        try:
            open('savefile.dat0', 'w').truncate(0)
            open('savefile.dat1', 'w').truncate(0)
        except:
            pass

        # Form bones.
        bones = []
        try:
            bf = open('bones', 'r')
            bones = cPickle.load(bf)
        except:
            pass

        bones.append((self.p.plev, self.dlev, [i for i in self.p.inv if i is not None and i.liveexplode is None]))

        for i in bones[-1][2]:
            i.tag = None

        bones = bones[-3:]

        try:
            bf = open('bones', 'w')
            cPickle.dump(bones, bf)
        except:
            pass

        # Save to highscore.

        self.p.achievements.finish(self.p.plev, self.d.dlev,
                                   self.d.moon, self.health().reason)

        conn = sqlite3.connect('highscore.db')
        c = conn.cursor()

        tbl_games = 'Games%s' % _version.replace('.', '')
        tbl_achievements = 'Achievements%s' % _version.replace('.', '')

        c.execute('create table if not exists ' + tbl_games + \
                  ' (id INTEGER PRIMARY KEY, seed INTEGER, score INTEGER, bones BLOB, inputs BLOB)')
        c.execute('create table if not exists ' + tbl_achievements + \
                  ' (achievement TEXT, game_id INTEGER)')

        # Scores are normalized to about 1000 max points,
        # regardless of which branch you play. (Provided you
        # only play one branch; playing several branches can
        # land you a score above the max.

        score = self.p.plev * 5
        score += min(self.dlev, 21) * 5

        for x in self.p.achievements.killed_monsters:
            if x[1] in self.monsterstock.norms:
                score += x[0] * self.monsterstock.norms[x[1]]

        score = int(round(score))


        bones = cPickle.dumps(self.bones)
        inputs = cPickle.dumps(self._inputs)

        c.execute('insert into ' + tbl_games + '(id, seed, score, bones, inputs) values (NULL, ?, ?, ?, ?)',
                  (self._seed, score,
                   sqlite3.Binary(bones),
                   sqlite3.Binary(inputs)))

        gameid = c.lastrowid

        for a in self.p.achievements:
            c.execute('insert into ' + tbl_achievements + '(achievement, game_id) values (?, ?)',
                      (a.tag, gameid))

        conn.commit()


        # Show placements.

        c.execute('select sum(score >= %d),count(*) from %s' % (score, tbl_games))
        place, total = c.fetchone()

        atotals = []
        achievements = []

        for a in self.p.achievements:
            c.execute(('select sum(score >= %d),count(*) from ' % score) + \
                      (' %s join %s on (game_id = id)' % (tbl_games, tbl_achievements)) + \
                      ' where achievement = ?', (a.tag,))
            p1,t1 = c.fetchone()
            atotals.append((p1, 100 - a.weight, t1, a.desc))
            achievements.append(a.tag)

        c.close()
        conn.close()

        atotals.sort()

        if len(atotals) >= 5:
            atotals = atotals[:5]

        s = []

        s.append('%cYour score: %c%d%c.    (#%c%d%c of %d%s)' % \
                (libtcod.COLCTRL_5, libtcod.COLCTRL_1, score, libtcod.COLCTRL_5,
                 libtcod.COLCTRL_1, place, libtcod.COLCTRL_5, total, '!' if place == 1 else '.'))
        s.append('')
        s.append('Your achievements:')
        s.append('')

        for p1,w,t1,a in atotals:
            s.append('%c%s%c:%s     #%c%d%c of %d%s' % (libtcod.COLCTRL_1, a, libtcod.COLCTRL_5,
                     ' '*max(0, 50 - len(a)), libtcod.COLCTRL_1, p1,
                     libtcod.COLCTRL_5, t1, '!' if p1 == 1 else '.'))
            s.append('')

        s.append('-' * 50)
        s.extend((x[1] for x in self.msg.strings[2:8]))
        s.append('')
        s.append('%cUpload your score to http://diggr.name? (Press Y or N)%c' % (libtcod.COLCTRL_3, libtcod.COLCTRL_1))

        while 1:
            c = draw_window(s, self.d.w, self.h)
            if c == 'n' or c == 'N':
                break
            elif c == 'y' or c == 'Y':

                done = False

                while not done:
                    done = self.upload_score(self._seed, score, bones, inputs, achievements)

                    if not done:
                        c = draw_window(['',
                                         'Uploading failed!',
                                         'Most likely, you entered the wrong password.',
                                         '',
                                         'Try again? (Press Y or N)'],
                                        self.d.w, self.h)
                        if c == 'n' or c == 'N':
                            done = True
                break



        s[-1] = ('Press space to ' + ('exit.' if self.p.done else 'try again.'))

        while 1:
            if draw_window(s, self.d.w, self.h) == ' ':
                break



    def upload_score(self, seed, score, bones, inputs, achievements):

        import string
        import httplib
        import hashlib

        username = ''

        while 1:
            k = draw_window(['',
                             'Enter username: ' + username,
                             '',
                             "      If you don't have an account with that username, it will",
                             '      be created for you automatically.'],
                            self.d.w, self.h)

            if k in string.letters or k in string.digits or k in '.-_':
                username = username + k.lower()
            elif ord(k) == 8 or ord(k) == 127:
                if len(username) > 0:
                    username = username[:-1]
            elif k in '\r\n':
                break

        password = ''
        stars = ''

        while 1:
            k = draw_window(['',
                             'Enter password: ' + stars,
                             '',
                             'NOTE: Your password will never be sent or stored in plaintext.',
                             '      Only a secure password hash will be used.'],
                            self.d.w, self.h)

            if k in string.letters or k in string.digits or k in '_-':
                password = password + k
                stars = stars + '*'
            elif ord(k) == 8 or ord(k) == 127:
                if len(password) > 0:
                    password = password[:-1]
                    stars = stars[:-1]
            elif k in '\r\n':
                break

        form = {'upload': '1',
                'version': _version,
                'username': username,
                'pwhash': hashlib.sha512(password).hexdigest(),
                'seed': str(seed),
                'score': str(score),
                'bones': bones,
                'inputs': inputs }

        boundary = '----diggr-multipart-upload'
        multipart = ''

        def mpart(k,v):
            ret = ''
            ret += '--%s\r\n' % boundary
            ret += 'Content-Disposition: form-data; name="%s"\r\n' % k
            ret += '\r\n'
            ret += v
            ret += '\r\n'
            return ret

        for k,v in form.iteritems():
            multipart += mpart(k, v)

        for a in achievements:
            multipart += mpart('ach', a)

        multipart += '--%s--\r\n' % boundary
        multipart += '\r\n'

        hclient = httplib.HTTPConnection('diggr.name')
        hclient.putrequest('POST', '/scripts/global-highscore.py')
        hclient.putheader('content-type',
                          'multipart/form-data; boundary=%s' % boundary)
        hclient.putheader('content-length', str(len(multipart)))
        hclient.endheaders()
        hclient.send(multipart)

        resp = hclient.getresponse()
        r = resp.read()

        if r == "OK\n":
            return True
        #print r
        return False



    def toggle_fullscreen(self):
        # HACK
        if self.save_disabled:
            return

        self.config.fullscreen = not self.config.fullscreen
        libtcod.console_set_fullscreen(self.config.fullscreen)


    def toggle_sound(self):
        # HACK
        if self.save_disabled:
            return
        isok = self.config.sound.toggle_mute()
        if not isok:
            if self.config.music_n >= 0:
                self.config.sound.stop(self.config.music_n)
            self.config.music_n = -1
            self.msg.m('Sound OFF.')
        else:
            self.config.music_n = self.config.sound.play("music", rate=min(10, 2.0+(0.5*self.dlev)))
            self.msg.m('Sound ON.')

    def toggle_music(self):
        # HACK
        if self.save_disabled:
            return

        if self.config.music_n >= 0:
            self.config.sound.stop(self.config.music_n)
            self.config.music_n = -1
            self.msg.m('Music OFF.')
        else:
            self.config.music_n = self.config.sound.play("music", rate=min(10, 2.0+(0.5*self.dlev)))
            self.msg.m('Music ON.')




def start_game(world, w, h, oldseed=None, oldbones=None):

    if oldseed or not world.load():
        if oldseed:
            world._seed = oldseed
        else:
            world._seed = int(time.time())

        if oldbones is not None:
            world.bones = oldbones
        else:
            world.load_bones()

        #log.f = open('LOG.%d' % world._seed, 'a')

        dg.random_init(world._seed)
        global _inputs
        _inputs = world._inputs

        world.regen(w, h)
        world.generate_inv()
        world.msg.m("Kill all the monsters in the dungeon or reach dungeon level 26 to win the game.", True)
        world.msg.m("Please press '?' to see help.")

def check_autoplay(world):

    if world.p.sleeping > 0:
        if world.stats.sleep.x >= 3.0 and not world.p.forcedsleep and not world.p.forced2sleep:
            world.msg.m('You wake up.')
            world.p.sleeping = 0
            world.p.healingsleep = False
            return 1
        else:
            world.do_sleep()
            return -1

    if world.resting:
        if world.stats.tired.x >= 3.0:
            world.msg.m('You stop resting.')
            world.resting = False
            return 1

        elif world.new_visibles:
            world.resting = False
            return 1

        else:
            world.do_rest()
            return -1

    if world.digging:
        height = dg.grid_get_height(world.digging[0], world.digging[1])

        if height <= -10:
            world.convert_to_floor(world.digging[0], world.digging[1], False)
            world.digging = None
            return 1

        elif world.new_visibles:
            world.digging = None
            return 1

        else:
            dg.grid_set_height(world.digging[0], world.digging[1], height - world.digging[2])
            world.tick()
            return -1

    return 0


def main(config, replay=None):

    #log.f = open('qqq1', 'a')
    #log.log('START')

    oldseed = None
    oldbones = None

    if replay is not None:
        oldseed = replay[0]
        oldinputs = replay[1]
        oldbones = replay[2]

        global _inputqueue
        _inputqueue = oldinputs

    w = 80
    h = 25


    #libtcod.sys_set_renderer(libtcod.RENDERER_SDL)

    config.load()

    font = 'font.png' #'terminal10x16_gs_ro.png'
    libtcod.console_set_custom_font(font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(w, h, 'Diggr', config.fullscreen, libtcod.RENDERER_SDL)
    libtcod.sys_set_fps(30)
    #cons = libtcod.console_new(w, h)
    #cons = None

    world = World(config)
    world.make_keymap()

    if replay is not None:
        world.save_disabled = True

    start_game(world, w, h, oldseed=oldseed, oldbones=oldbones)

    if config.music_n != -1:
        config.music_n = config.sound.play("music", rate=min(10, 2.0+(0.5*world.dlev)))

    while 1:

        if libtcod.console_is_window_closed():
            if replay is None:
                # MEGATON-SIZED HACK!
                # To make replays work.
                _inputs.append((ord('S'), 0))

                world.save()
            break

        if world.p.done or world.dead:
            break

        world.draw()
        libtcod.console_flush()

        r = check_autoplay(world)
        if r == -1:
            libtcod.console_check_for_keypress()
            continue
        elif r == 1:
            world.draw()
            libtcod.console_flush()


        if world.p.dead: break

        key = console_wait_for_keypress()

        if chr(key.c) in world.ckeys:
            world.ckeys[chr(key.c)]()

        elif key.vk in world.vkeys:
            world.vkeys[key.vk]()



    if world.p.dead and not world.p.done:
        world.msg.m('You die.', True)

    if config.music_n >= 0:
        config.sound.stop(config.music_n)

    world.oldt = world.t
    world.msg.m('*** Press any key ***', True)
    world.draw()
    libtcod.console_flush()
    libtcod.console_wait_for_keypress(True)

    if replay is None and world.p.dead:
        world.form_highscore()

    #log.log('DONE')
    #log.f.close()
    #log.f = None

    return world.p.done


#import cProfile
#cProfile.run('main()')

if __name__=='__main__':
    config = Config()
    while 1:
        if main(config):
            break
