#!/usr/bin/env python

import math
import os
import random
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

log = Logger()

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



global _version
_version = '11.12.18'

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
        self.sound = sounds.Engine(sound_enabled)
        self.music_n = None


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
    #log.log('  key:', k.c, k.vk)
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
        self.burndamage = 0.333

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

    def draw(self, x, y, grace=None, resource=None):
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
        self.head = None
        self.neck = None
        self.trunk = None
        self.left = None
        self.right = None
        self.legs = None
        self.feet = None
        self.backpack1 = None
        self.backpack2 = None

    def draw(self, w, h, dlev, plev, floor=None):
        s = [
            ("a)       Head: %c%s", self.head),
            ("b)       Neck: %c%s", self.neck),
            ("c)      Trunk: %c%s", self.trunk),
            ("d)  Left hand: %c%s", self.left),
            ("e) Right hand: %c%s", self.right),
            ("f)       Legs: %c%s", self.legs),
            ("g)       Feet: %c%s", self.feet),
            ("h) Backpack 1: %c%s", self.backpack1),
            ("i) Backpack 2: %c%s", self.backpack2)]

        if floor:
            s.extend(floor)

        s.extend(["",
                  "Character level: %d" % plev,
                  "  Dungeon level: %d" % dlev])

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

    def get_tagged(self):
        i = []

        def chk(j, slot):
            if j and j.tag:
                i.append((j.tag, slot, j))

        chk(self.head, 'a')
        chk(self.neck, 'b')
        chk(self.trunk, 'c')
        chk(self.left, 'd')
        chk(self.right, 'e')
        chk(self.legs, 'f')
        chk(self.feet, 'g')
        chk(self.backpack1, 'h')
        chk(self.backpack2, 'i')

        i.sort()
        return i

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
               getattr(self.right, 'lightradius', 0) + \
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
        return getattr(self.right, 'confattack', None) or \
               getattr(self.left, 'confattack', None)

    def get_psyimmune(self):
        return getattr(self.head, 'psyimmune', None) or \
               getattr(self.right, 'psyimmune', None) or \
               getattr(self.left, 'psyimmune', None)

    def get_camorange(self):
        l = (getattr(self.trunk, 'camorange', None),
             getattr(self.feet, 'camorange', None),
             getattr(self.neck, 'camorange', None))
        l = [q for q in l if q]
        if len(l) == 0: return None
        return min(l)

    def get_repelrange(self):
        l = (getattr(self.trunk, 'repelrange', None),
             getattr(self.left, 'repelrange', None))
        l = [q for q in l if q]
        if len(l) == 0: return None
        return max(l)

    def get_fires(self):
        return getattr(self.right, 'fires', None)

    def get_glueimmune(self):
        return getattr(self.left, 'glueimmune', None)

    def get_digspeed(self):
        return getattr(self.head, 'digbonus', 0)


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

    def finish(self, world):
        self.add('plev%d' % world.plev, 'Reached player level %d' % world.plev)
        self.add('dlev%d' % world.dlev, 'Reached dungeon level %d' % world.dlev)

        moonstr = moon.phase_string(world.moon)
        self.add('moon_%s' % moonstr, 'Played on a %s moon' % moonstr)

        if len(self.killed_monsters) == 0:
            self.add('loser', 'Scored *no* kills')
        else:
            killbucket = ((len(self.killed_monsters) / 5) * 5)
            if killbucket > 0:
                self.add('%dkills' % killbucket, 'Killed at least %d monsters' % killbucket, weight=10*killbucket)

        reason = world.stats.health.reason
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

        if self.food == 0 and self.booze == 0 and self.healing == 0:
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


    def descend(self, world):
        if world.dlev >= world.plev+5:
            self.add('tourist', 'Dived to a very deep dungeon', weight=50, once=True)

        elif world.dlev >= world.plev+2:
            self.add('small_tourist', 'Dived to a deep dungeon', weight=15, once=True)

        self.branches.add(world.branch)

    def questdone(self, branch):
        if branch == 'q':
            self.add('thunderdome_win', 'Became a Thunderdome champion', weight=78)

    def winner(self):
        self.add('winner', ' =*= Won the game =*= ', weight=100)

    def mondone(self):
        self.extinguished += 1

    def mondeath(self, world, mon, is_rad=False, is_explode=False, is_poison=False):
        if mon.inanimate:
            return

        if mon.is_mold:
            self.killed_molds += 1
            return

        if mon.level >= world.plev+5:
            self.add('stealth', 'Killed a monster massively out of depth', weight=50)
        elif mon.level >= world.plev+2:
            self.add('small_stealth', 'Killed a monster out of depth', weight=10)

        if is_poison:
            self.ebola += 1
        else:
            self.killed_monsters.append((mon.level * mon.pointsfac, mon.branch, mon.name, world.dlev, world.plev))

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



class World:

    def __init__(self, config):
        self.grid = None

        self.walkmap = None
        self.watermap = None
        self.featmap = {}
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
        self.featstock = FeatureStock()
        self.vaultstock = VaultStock()
        self.achievements = Achievements()

        self.dlev = 1
        self.plev = 1
        self.branch = None
        self.moon = None
        self.did_moon_message = False
        self.t = 0
        self.oldt = -1
        self.tagorder = 1
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

        self.celautostock = CelAutoStock()

        self.floorpath = None

        self.resource = None
        self.resource_buildup = 0
        self.resource_timeout = 0

        self.monsters_in_view = []

        self._seed = None
        self._inputs = []

        self.save_disabled = False

        self.sparkleinterp = [ math.sin(x/math.pi)**2 for x in xrange(10) ]

        self.config = config
        self.last_played_themesound = 0

        ### 

        self.theme = { 'a': (libtcod.lime,),
                       'b': (libtcod.red,),
                       'c': (libtcod.sky,),
                       'd': (libtcod.darkest_grey,),
                       'e': (libtcod.lightest_yellow,),
                       's': (libtcod.darkest_blue,),
                       'q': (libtcod.white,) }

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
        
        self.quests = {'q': quest1}

        self.neighbors = None



    def makegrid(self, w_, h_):
        self.w = w_
        self.h = h_
        self.grid = [[10 for x in xrange(self.w)] for y in xrange(self.h)]

        self.walkmap = set()
        self.watermap = set()
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

        for ki in self.neighbors[(x,y)]:
            zx, zy = ki
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

        for x,y in gout:
            if self.grid[y][x] <= 0:
                self.walkmap.add((x,y))

        watr = [(v,k) for (k,v) in watr.iteritems()]
        watr.sort()
        watr.reverse()

        pctwater = random.gauss(5, 1)
        if pctwater <= 1: pctwater = 1
        watr = watr[:int(len(watr)/pctwater)]

        for n,v in watr:
            self.watermap.add(v)

            
    def flatten_pass(self):
        towalk = set()
        towater = set()

        for x in xrange(0,self.w):
            for y in xrange(self.h):
                nwall = 0
                nwater = 0
                for k in self.neighbors[(x,y)]:
                    if k not in self.walkmap:
                        nwall += 1
                    if k in self.watermap:
                        nwater += 1

                if (x,y) not in self.walkmap and nwall < 3:
                    towalk.add((x,y))

                if (x,y) not in self.watermap and nwater > 2:
                    towater.add((x,y))

        self.walkmap.update(towalk)
        self.walkmap.update(towater)
        self.watermap.update(towater)

    def unflow(self):
        unwater = set()

        for k in self.watermap:
            nwater = 0
            for k2 in self.neighbors[k]:
                if k2 in self.watermap:
                    nwater += 1
        
            if nwater < 5:
                unwater.add(k)

        self.watermap.difference_update(unwater)


    def flatten(self):
        if self.moon in (moon.NEW, moon.FULL):
            for x in xrange(5):
                self.flatten_pass()

        elif self.moon in (moon.FIRST_QUARTER, moon.LAST_QUARTER):
            self.unflow()
        

    def make_map(self):
        self.tcodmap = libtcod.map_new(self.w, self.h)
        libtcod.map_clear(self.tcodmap)

        for x in xrange(self.w):
            for y in xrange(self.h):
                if (x,y) in self.walkmap:
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

        elif (x,y) in self.walkmap:
            if (x,y) in self.watermap:
                c = 251
                fore = libtcod.light_azure
                fore2 = libtcod.dark_azure
                fore_i = 1
            else:
                c = 250
                is_terrain = True

        else:
            if (x,y) in self.watermap:
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
                self.walkmap.add((x, y))

                libtcod.map_set_properties(self.tcodmap, x, y, True, True)
                self.grid[y][x] = -10
            else:
                self.walkmap.discard((x, y))
                libtcod.map_set_properties(self.tcodmap, x, y, False, False)
                self.grid[y][x] = 0

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
            self.walkmap.add((x, y))
        else:
            if (x, y) in self.walkmap:
                self.walkmap.discard((x, y))
        self.grid[y][x] = f.height

        if f.water:
            self.watermap.add((x, y))
        elif f.water is not None:
            if (x, y) in self.watermap:
                self.watermap.discard((x, y))


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

            d = [ k for k in self.neighbors[(x,y)] if k in self.walkmap ]
            if len(d) == 0:
                iis.extend(itms)
                return
            x,y = d[random.randint(0, len(d)-1)]


    def paste_vault(self, v, m, nogens):
        x = None
        y = None

        if v.anywhere:
            x = random.randint(0, self.w - v.w - 1)
            y = random.randint(0, self.h - v.h - 1)

        else:
            for x in xrange(10):
                d = m[random.randint(0, len(m)-1)]

                x0 = d[0] - v.anchor[0]
                y0 = d[1] - v.anchor[1]

                if x0 < 0 or y0 < 0 or x0 + v.w >= self.w or y0 + v.h >= self.h:
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
                        nogens.add((xx,yy))
                    else:
                        itm = self.itemstock.get(z[1])
                        if itm:
                            self.set_item(xx, yy, [itm])


    def make_feats(self, nogens):

        self.featmap = {}
        dg.celauto_init()

        # HACK!
        # This is done here, and not in make_items(),
        # so that vaults could generate items.
        self.itemap = {}

        m = list(self.walkmap - self.watermap)

        oldvaults = set()
        while 1:
            vault = self.vaultstock.get(self.branch, self.dlev, oldvaults)

            if vault:
                self.paste_vault(vault, m, nogens)
                oldvaults.add(vault)

            if not vault or not vault.free:
                break

        m = list(self.walkmap - self.watermap)

        if len(m) == 0: return

        # Quests
        if self.branch in self.quests:
            return

        stairsi = random.randint(0, len(m)-1)
        d = m[stairsi]

        self.set_feature(d[0], d[1], '>')
        self.exit = d
        del m[stairsi]

        if self.moon == moon.NEW:
            d = m[random.randint(0, len(m)-1)]
            self.set_feature(d[0], d[1], 'bb')

        elif self.moon == moon.FULL:
            d = m[random.randint(0, len(m)-1)]
            self.set_feature(d[0], d[1], 'dd')
            self.paste_celauto(d[0], d[1], self.celautostock.FERN)

        else:
            a = random.randint(-1, 1)
            d = m[random.randint(0, len(m)-1)]
            if a == -1:
                self.set_feature(d[0], d[1], 's')
            elif a == 0:
                self.set_feature(d[0], d[1], 'b')
            elif a == 1:
                self.set_feature(d[0], d[1], 'v')

        nfounts = int(round(random.gauss(3, 1)))
        ww = list(self.walkmap & self.watermap)

        if len(ww) == 0:
            return

        for tmp in xrange(nfounts):
            d = ww[random.randint(0, len(ww)-1)]
            self.set_feature(d[0], d[1], random.choice(['C','V','B','N','M']))



    def try_feature(self, x, y, att, deflt=None):
        if (x,y) not in self.featmap:
                return deflt
        return getattr(self.featmap[(x, y)], att, deflt)


    def make_paths(self):
        #log.log('  making path')
        if self.floorpath:
            libtcod.path_delete(self.floorpath)

        def floor_callback(xfrom, yfrom, xto, yto, world):
            if (xto, yto) in world.monmap:
                return 0.0
            elif (xto, yto) in world.walkmap:
                return 1.0
            return 0.0

        self.floorpath = libtcod.path_new_using_function(self.w, self.h, floor_callback, self, 1.0)

    def make_monsters(self, nogens):

        self.monsterstock.clear_gencount()
        self.monmap = {}

        # Quests
        if self.branch in self.quests:
            n = self.quests[self.branch].moncounts.get(self.dlev, 0)

        else:
            n = int(max(random.gauss(*self.coef.nummonsters), 1))

        ll = list(self.walkmap - nogens)

        i = 0
        while i < n:
            lev = self.dlev + random.gauss(0, self.coef.monlevel)
            lev = max(int(round(lev)), 1)

            # Quests
            if self.branch in self.quests:
                lev = min(max(lev, self.quests[self.branch].monlevels[0]), 
                          self.quests[self.branch].monlevels[1])

            while 1:
                x, y = ll[random.randint(0, len(ll)-1)]
                if (x, y) not in self.monmap: break

            m = self.monsterstock.generate(self.branch, lev, self.itemstock, self.moon)
            if m:
                m.x = x
                m.y = y
                self.monmap[(x, y)] = m

                if m.inanimate:
                    continue

            i += 1


        # Generate some mold.
        if self.branch in self.quests:
            return

        if random.randint(1, self.coef.moldchance) == 1:
            ll = list(self.walkmap - self.watermap - set(self.monmap.iterkeys()))
            x, y = ll[random.randint(0, len(ll)-1)]
            m = self.monsterstock.generate('x', self.dlev, self.itemstock, self.moon)
            if m:
                m.x = x
                m.y = y
                self.monmap[(x, y)] = m


    def make_items(self, nogens):

        ## Quests
        if self.branch in self.quests:
            n = self.quests[self.branch].itemcounts.get(self.dlev, 0)
        else:
            n = int(max(random.gauss(self.coef.numitems[0] + self.dlev, self.coef.numitems[1]), 1))

        ll = list(self.walkmap - nogens)

        for i in xrange(n):
            lev = self.dlev + random.gauss(0, self.coef.itemlevel)
            lev = max(int(round(lev)), 1)
            x, y = ll[random.randint(0, len(ll)-1)]
            item = self.itemstock.generate(lev)
            if item:
                self.set_item(x, y, [item])

        ## Quests
        if self.branch in self.quests:
            return

        for pl,dl,itm in self.bones:
            if dl == self.dlev and len(itm) > 0:
                itm2 = [copy.copy(i) for i in itm]

                x, y = ll[random.randint(0, len(ll)-1)]

                self.set_item(x, y, itm2)


    def place(self, nogens):
        s = self.walkmap - nogens - set(self.monmap.iterkeys())

        # Do not place a player in an unfair position.
        # Otherwise, the monster will get a free move and might
        # kill the player.
        for k in self.monmap.iterkeys():
            for ki in self.neighbors[k]:
                if ki in s:
                    s.remove(ki)

        s = list(s)
        x, y = s[random.randint(0, len(s)-1)]
        self.px = x
        self.py = y

        
    def regen(self, w_, h_):
        if self.branch is None:
            self.branch = random.choice(['a', 'b', 'c', 'd', 'e'])

        if self.moon is None:
            m = moon.phase(self._seed)
            self.moon = m['phase']

        nogens = set()

        self.makegrid(w_, h_)

        # Quests
        if self.branch not in self.quests:
            self.terra()
            self.makerivers()
            self.flatten()

        self.make_feats(nogens)
        self.make_paths()
        self.make_monsters(nogens)
        self.make_items(nogens)
        self.make_map()
        self.place(nogens)

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
            self.inv.take(self.itemstock.find("miner's lamp"))
        else:
            self.inv.take(self.itemstock.find('lamp'))
            
        self.inv.take(self.itemstock.find('pickaxe'))
        self.inv.take(self.itemstock.find('magic mapper'))        
        self.inv.take(self.itemstock.find('flamethrow'))        

        pl = [k for k in self.neighbors[(self.px,self.py)] if k in self.walkmap] + [(self.px,self.py)]

        for x in xrange(9):
            k = pl[random.randint(0,len(pl)-1)]
            i = self.itemstock.generate(1)

            self.set_item(k[0], k[1], [i])



    def move(self, _dx, _dy, do_spring=True):

        if self.glued > 0:
            self.glued -= 1
            if self.glued == 0:
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

        if (dx,dy) in self.walkmap and dx >= 0 and dx < self.w and dy < self.h:

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

                fdmg = self.try_feature(self.px, self.py, 'fire')
                if fdmg > 0:
                    self.stats.health.dec(fdmg, "fire", self.config.sound)
                    self.onfire = max(self.coef.burnduration, self.onfire)
                elif self.onfire:
                    self.stats.health.dec(self.coef.burndamage, "fire", self.config.sound)

                if self.onfire > 0:
                    self.onfire -= 1
                    self.seed_celauto(self.px, self.py, self.celautostock.FIRE)
                    self.set_feature(self.px, self.py, '"')

                if self.try_feature(self.px, self.py, 'sticky') and not self.inv.get_glueimmune():
                    self.msg.m('You just stepped in some glue!', True)
                    self.glued = max(int(random.gauss(*self.coef.glueduration)), 1)


        else:
            return

        is_springy = False

        if self.inv.feet and self.inv.feet.springy:
            is_springy = True
        elif self.resource_timeout and self.resource == 'y':
            is_springy = True

        if do_spring and is_springy:
            self.move(_dx, _dy, do_spring=False)
            return

        self.tick()

    def tick(self):
        self.stats.tired.dec(self.coef.movetired)
        self.stats.sleep.dec(self.coef.movesleep)
        self.stats.thirst.dec(self.coef.movethirst)
        self.stats.hunger.dec(self.coef.movehunger)

        if self.try_feature(self.px, self.py, 'warm'):
            self.stats.warmth.inc(self.coef.watercold)
        elif (self.px, self.py) in self.watermap:
            self.stats.warmth.dec(self.coef.watercold)
        else:
            self.stats.warmth.inc(self.inv.get_heatbonus())

        if self.b_grace > 0: self.b_grace -= 1
        if self.v_grace > 0: self.v_grace -= 1
        if self.s_grace > 0: self.s_grace -= 1

        if self.resource_timeout > 0: 
            if self.resource == 'r':
                self.stats.health.inc(self.coef.regeneration)
                self.stats.warmth.inc(self.coef.regeneration)
                self.stats.hunger.inc(self.coef.regeneration)

            self.resource_timeout -= 1
            if self.resource_timeout == 0: self.resource = None

        

        self.tick_checkstats()
        self.t += 1

    def tick_checkstats(self):

        for i in self.inv:
            if i and i.liveexplode > 0:
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
                    self.inv.purge(i)

            elif i and i.selfdestruct > 0 and \
                 i != self.inv.backpack1 and i != self.inv.backpack2:
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

        p = self.try_feature(self.px, self.py, 'queasy')
        if p:
            self.msg.m('You feel queasy.', True)
            self.stats.thirst.dec(p)
            self.stats.hunger.dec(p)

        if self.stats.warmth.x <= -3.0:
            self.msg.m("Being so cold makes you sick!", True)
            self.stats.health.dec(self.coef.colddamage, "cold", self.config.sound)
            if self.resting: self.resting = False
            if self.digging: self.digging = None

        if self.stats.thirst.x <= -3.0:
            self.msg.m('You desperately need something to drink!', True)
            self.stats.health.dec(self.coef.thirstdamage, "thirst", self.config.sound)
            if self.resting: self.resting = False
            if self.digging: self.digging = None

        if self.stats.hunger.x <= -3.0:
            self.msg.m('You desperately need something to eat!', True)
            self.stats.health.dec(self.coef.hungerdamage, "hunger", self.config.sound)
            if self.resting: self.resting = False
            if self.digging: self.digging = None

        p = self.try_feature(self.px, self.py, 'poison')
        if p:
            self.msg.m('You feel very sick!', True)
            self.stats.health.dec(p, 
                                  'black mold' if self.featmap[(self.px,self.py)].pois2 else 'Ebola infection', 
                                  self.config.sound)

        if self.stats.health.x <= -3.0:
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

        if self.try_feature(self.px, self.py, 'warm'):
            self.stats.warmth.inc(self.coef.watercold)
        elif (self.px, self.py) in self.watermap:
            self.stats.warmth.dec(self.coef.watercold)
        else:
            self.stats.warmth.inc(self.inv.get_heatbonus())

        if self.resource_timeout > 0: 
            if self.resource == 'r':
                self.stats.health.inc(self.coef.regeneration)
                self.stats.warmth.inc(self.coef.regeneration)
                self.stats.hunger.inc(self.coef.regeneration)

            self.resource_timeout -= 1
            if self.resource_timeout == 0: self.resource = None

        self.tick_checkstats()
        self.t += 1

    def sleep(self):
        self.stats.tired.inc(self.coef.sleeptired)
        self.stats.sleep.inc(self.coef.sleepsleep)
        self.stats.thirst.dec(self.coef.sleepthirst)
        self.stats.hunger.dec(self.coef.sleephunger)

        if self.try_feature(self.px, self.py, 'warm'):
            self.stats.warmth.inc(self.coef.watercold)
        elif (self.px, self.py) in self.watermap:
            self.stats.warmth.dec(self.coef.watercold)
        else:
            self.stats.warmth.inc(self.inv.get_heatbonus())

        if self.healingsleep:
            self.stats.health.inc(self.coef.healingsleep)

        if self.resource_timeout > 0: 
            if self.resource == 'r':
                self.stats.health.inc(self.coef.regeneration)
                self.stats.warmth.inc(self.coef.regeneration)
                self.stats.hunger.inc(self.coef.regeneration)

            self.resource_timeout -= 1
            if self.resource_timeout == 0: self.resource = None

        self.tick_checkstats()

        if self.sleeping > 0:
            self.sleeping -= 1

            if self.sleeping == 0:
                self.forcedsleep = False
                self.forced2sleep = False
                self.healingsleep = False
        self.t += 1


    def start_sleep(self, force = False, quick = False,
                    realforced = False, realforced2 = False):
        if not force and self.stats.sleep.x > -2.0:
            self.msg.m('You don\'t feel like sleeping yet.')
            return

        if quick:
            self.sleeping = int(random.gauss(*self.coef.quicksleeptime))
        else:
            if not realforced2:
                self.msg.m('You fall asleep.')
            self.sleeping = int(random.gauss(*self.coef.sleeptime))

        self.digging = None
        self.resting = False

        if realforced:
            self.forcedsleep = True
        elif realforced2:
            self.forced2sleep = True

    def start_rest(self):
        self.msg.m('You start resting.')
        self.resting = True

        
    def colordrink(self, fount):
        if self.resource and (self.resource != fount):
            self.msg.m('You feel confused.')
            self.resource = None
            self.resource_timeout = 0
            self.resource_buildup = 0
            return

        if fount == 'r': self.msg.m('You drink something red.')
        elif fount == 'g': self.msg.m('You drink something green.')
        elif fount == 'y': self.msg.m('You drink something yellow.')
        elif fount == 'b': self.msg.m('You drink something blue.')
        elif fount == 'p': self.msg.m('You drink something purple.')
        self.resource = fount

        bonus = False
        
        if self.resource_timeout:
            self.resource_timeout += (self.coef.resource_timeouts[fount]/6)
        else:
            self.resource_buildup += 1

            if self.resource_buildup >= 6:
                if self.resource == 'r':
                    self.msg.m('You gain superhuman regeneration power!', True)
                elif self.resource == 'g':
                    self.msg.m('Hulk Smash! You gain superhuman strength.', True)
                elif self.resource == 'y':
                    self.msg.m('You gain superhuman speed and vision!', True)
                elif self.resource == 'b':
                    self.msg.m('You are now immune to explosions and radiation!', True)
                elif self.resource == 'p':
                    self.msg.m('You gain telepathy and superhuman stealth!', True)

                bonus = True
                self.resource_buildup = 0
                self.resource_timeout = self.coef.resource_timeouts[fount]

        self.achievements.resource_use(fount, bonus)


    def drink(self):

        if self.try_feature(self.px, self.py, 'healingfountain'):
            nn = min(3.0 - self.stats.health.x, self.stats.hunger.x + 3.0)
            if nn <= 0:
                self.msg.m('Nothing happens.')
                return

            self.msg.m('You drink from the eternal fountain.')
            self.stats.health.inc(nn)
            self.stats.hunger.dec(nn)
            return

        fount = self.try_feature(self.px, self.py, 'resource')
        if fount:
            self.colordrink(fount)
            self.unset_feature(self.px, self.py)
            return
            
        if (self.px,self.py) not in self.watermap:
            self.msg.m('There is no water here you could drink.')
            return

        if self.v_grace:
            self.msg.m('Your religion prohibits drinking from the floor.')
            return

        self.stats.thirst.inc(6)

        x = abs(random.gauss(0, 0.7))
        tmp = x - self.coef.waterpois
        if tmp > 0:
            self.stats.health.dec(tmp, "unclean water", self.config.sound)
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
            for i in self.inv:
                if i and i.corpse:
                    self.msg.m("Ba'al-Zebub accepts your sacrifice!")
                    self.inv.purge(i)

                    i2 = self.itemstock.generate(self.dlev)
                    if i2:
                        self.set_item(self.px, self.py, [i2])
                    return
            self.msg.m("Ba'al-Zebub needs to be sated with blood!!")
            return

        if a.s_shrine:
            if self.b_grace or self.v_grace:
                self.msg.m("You don't believe in Shiva.")
                return
            if self.s_grace > self.coef.s_graceduration - self.coef.s_praytimeout:
                self.msg.m('Nothing happens.')
                return

            ss = "hwp"
            decc = self.coef.shivadecstat
            ss = ss[random.randint(0, len(ss)-1)]

            if ss == 'h': self.stats.hunger.dec(decc)
            elif ss == 'w': self.stats.warmth.dec(decc)
            elif ss == 'p': self.stats.health.dec(decc, 'the grace of Shiva', self.config.sound)

            self.msg.m('You pray to Shiva.')
            self.wish('Shiva grants you a wish.')
            self.s_grace = self.coef.s_graceduration
            self.tick()
            self.achievements.pray('s')

        elif a.b_shrine:
            if self.s_grace or self.v_grace:
                self.msg.m("You don't believe in Brahma.")
                return
            self.msg.m('As a follower of Brahma, you are now forbidden hand-to-hand combat.')
            self.msg.m('You feel enlightened.')
            self.b_grace = self.coef.b_graceduration
            self.tick()
            self.achievements.pray('b')

        elif a.v_shrine:
            if self.s_grace or self.b_grace:
                self.msg.m("You don't believe in Vishnu.")
                return

            if self.v_grace > self.coef.v_graceduration - self.coef.v_praytimeout:
                self.msg.m('Nothing happens.')
                return

            self.msg.m('As a follower of Vishnu, you are now forbidden '
                       'medicine, alcohol and unclean food.')
            self.msg.m('You meditate on the virtues of Vishnu.')
            self.start_sleep(force=True, realforced2=True)

            self.stats.health.inc(6.0)
            self.stats.sleep.inc(6.0)
            self.stats.tired.inc(6.0)
            self.stats.hunger.inc(6.0)
            self.stats.thirst.inc(6.0)
            self.stats.warmth.inc(6.0)
            self.v_grace = self.coef.v_graceduration
            self.tick()
            self.achievements.pray('v')

        else:
            self.msg.m('You need to be standing at a shrine to pray.')
            return


    def convert_to_floor(self, x, y, rubble=0):
        if rubble == 0:
            self.set_feature(x, y, None)
        else:
            self.set_feature(x, y, '*')


    def find_blink_targ(self, _x, _y, range):
        l = []
        for x in xrange(_x - range, _x + range + 1):
            for y in [_y - range, _x + range]:
                if x >= 0 and y >= 0 and (x,y) in self.walkmap:
                    l.append((x,y))

        for y in xrange(_y - range - 1, _y + range):
            for x in [_x - range, _x + range]:
                if x >= 0 and y >= 0 and (x,y) in self.walkmap:
                    l.append((x,y))

        l = l[random.randint(0, len(l)-1)]
        return l[0], l[1]


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

        self.apply_from_inv_aux(i)


    def tagged_apply(self):

        iss = self.inv.get_tagged()

        if len(iss) == 0:
            self.msg.m("Tag an item from your inventory to use this command.")
            return

        items = [i[2] for i in iss]

        i,c = self.pick_one_item(items)
        if not i:
            return

        i = self.inv.drop(iss[c][1])

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


    def take_aux(self, items, c):

        i = items[c]
        did_scavenge = False

        for ii in self.inv:
            if ii and ii.name == i.name:
                if ii.stackrange and ii.count < ii.stackrange:
                    n = min(ii.stackrange - ii.count, i.count)
                    ii.count += n
                    i.count -= n

                    self.msg.m('You now have ' + str(ii) + '.')
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
                    self.msg.m("You find some ammo for your " + ii.name + '.')
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


    def apply_from_inv_aux(self, i):
        i2 = self.apply(i)

        if i2 == -1:
            self.inv.take(i)
            return

        if i2:
            self.inv.take(i2)
        else:
            if i.count > 0:
                i.count -= 1
            if i.count > 0:
                self.inv.take(i)

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
            slot = self.inv.draw(self.w, self.h, self.dlev, self.plev, floor=floorstuff)

        i = None
        if slot in flooritems:
            i = items[flooritems[slot]]
        else:
            i = self.inv.check(slot)

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

            elif slot in 'abcdefg' and \
                    (not self.inv.backpack1 or self.inv.backpack1.slot == slot or \
                     not self.inv.backpack2 and self.inv.backpack2.slot == slot):
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
        cc = draw_window(s, self.w, self.h)

        if cc not in choices:
            return

        if cc == 'a' and i.applies:
            if slot not in flooritems:
                i = self.inv.drop(slot)

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
            draw_window(ss, self.w, self.h)

        elif cc == 'd':
            i = self.inv.drop(slot)
            self.set_item(self.px, self.py, [i])
            self.tick()

        elif cc == 'q':
            if slot in flooritems:
                del items[flooritems[slot]]
                if len(items) == 0:
                    del self.itemap[(self.px, self.py)]
            else:
                self.inv.drop(slot)
            self.tick()

        elif cc == 'f':
            while 1:
                nx, ny = self.target(i.throwrange)
                if nx is not None:
                    break

            if nx >= 0:
                if slot not in flooritems:
                    i = self.inv.drop(slot)

                self.msg.m('You throw ' + str(i) + '.')

                self.set_item(nx, ny, [i])

                if slot in flooritems:
                    del items[flooritems[slot]]
                    if len(items) == 0:
                        del self.itemap[(self.px, self.py)]

                self.tick()

        elif cc == 'x':
            if slot in flooritems:
                item2 = self.inv.drop(i.slot)
                ok = self.inv.take(i)
                if ok:
                    del items[flooritems[slot]]
                    if len(items) == 0:
                        del self.itemap[(self.px, self.py)]

                    if item2:
                        if not self.inv.take(item2):
                            self.set_item(self.px, self.py, [item2])

                elif item2:
                    self.inv.take(item2)

            else:
                if slot != i.slot:
                    i = self.inv.drop(slot)
                    item2 = self.inv.drop(i.slot)
                    self.inv.take(i)
                    if item2:
                        self.inv.take(item2)

                else:
                    slt2 = None
                    if self.inv.backpack1 and self.inv.backpack1.slot == slot:
                        slt2 = 'h'
                    elif self.inv.backpack2 and self.inv.backpack2.slot == slot:
                        slt2 = 'i'

                    if slt2:
                        i = self.inv.drop(slot)
                        item2 = self.inv.drop(slt2)
                        self.inv.take(item2)
                        self.inv.take(i)
                    else:
                        if not self.inv.backpack1:
                            self.inv.backpack1 = self.inv.drop(slot)
                        elif not self.inv.backpack2:
                            self.inv.backpack2 = self.inv.drop(slot)

            self.tick()

        elif cc == 't':
            self.take_aux(items, flooritems[slot])



    def apply(self, item):
        if not item.applies:
            return item

        if item.applies_in_slot and self.inv.check(item.slot) is not None:
            self.msg.m("You can only use this item if it's in the " + self.slot_to_name(item.slot) + ' slot.', True)
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

            self.achievements.use(item)
            return None

        elif item.craft:

            newi = None

            for i2 in self.inv:
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

            self.inv.purge(i2)
            self.achievements.craft_use(newi)
            self.msg.m('Using %s and %s you have crafted %s!' % (item, i2, newi))
            return newi

        elif item.digging:
            k = draw_window(['Dig in which direction?'], self.w, self.h, True)

            digspeed = self.inv.get_digspeed() + 0.1

            self.digging = None
            if k == 'h': self.digging = (self.px - 1, self.py, digspeed)
            elif k == 'j': self.digging = (self.px, self.py + 1, digspeed)
            elif k == 'k': self.digging = (self.px, self.py - 1, digspeed)
            elif k == 'l': self.digging = (self.px + 1, self.py, digspeed)
            else:
                return -1 #item

            if self.digging[0] < 0 or self.digging[0] >= self.w:
                self.digging = None
            if self.digging[1] < 0 or self.digging[1] >= self.h:
                self.digging = None

            if not self.digging:
                return item

            if self.digging[:2] in self.walkmap:
                self.msg.m('There is nothing to dig there.')
                self.digging = None
            else:
                self.msg.m("You start hacking at the wall.")
                self.achievements.use(item)

        elif item.healing:

            if self.v_grace:
                self.msg.m('Your religion prohibits taking medicine.')
                return item

            if item.bonus < 0:
                self.msg.m('This pill makes your eyes pop out of their sockets!', True)
                self.stats.tired.dec(max(random.gauss(*item.healing), 0))
                self.stats.sleep.dec(max(random.gauss(*item.healing), 0))
            else:
                self.msg.m('Eating this pill makes you dizzy.')
                self.stats.health.inc(max(random.gauss(*item.healing), 0))
                self.stats.hunger.dec(max(random.gauss(*item.healing), 0))
                self.stats.sleep.dec(max(random.gauss(*item.healing), 0))

            self.achievements.use(item)
            return None


        elif item.healingsleep:

            if self.v_grace:
                self.msg.m('Your religion prohibits taking medicine.')
                return item

            if item.bonus < 0:
                self.msg.m('You drift into a restless sleep!', True)
                self.sleeping = max(random.gauss(*item.healingsleep), 1)
                self.forced2sleep = True
            else:
                self.msg.m('You drift into a gentle sleep.')
                self.sleeping = max(random.gauss(*item.healingsleep), 1)
                self.forced2sleep = True
                self.healingsleep = True

            self.achievements.use(item)

            if item.count == 0:
                return item
            return None

        elif item.food:

            if self.v_grace:
                self.msg.m('Your religion prohibits eating unclean food.')
                return item

            if item.bonus < 0:
                self.msg.m('Yuck, eating this makes you vomit!', True)
                self.stats.hunger.dec(max(random.gauss(*item.food), 0))
            else:
                self.msg.m('Mm, yummy.')
                self.stats.hunger.inc(max(random.gauss(*item.food), 0))

            self.achievements.use(item)
            return None

        elif item.booze:

            if self.v_grace:
                self.msg.m('Your religion prohibits alcohol.')
                return item

            if item.bonus < 0:
                self.msg.m("This stuff is contaminated! You fear you're going blind!", True)
                self.blind = True
            else:
                self.msg.m('Aaahh.')
                self.stats.sleep.dec(max(random.gauss(*self.coef.boozestrength), 0))
                self.stats.warmth.inc(max(random.gauss(*self.coef.boozestrength), 0))

            self.achievements.use(item)
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

            self.achievements.use(item)

        elif item.sounding:
            k = draw_window(['Check in which direction?'], self.w, self.h, True)

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
            while x >= 0 and y >= 0 and x < self.w and y < self.h:
                x += s[0]
                y += s[1]
                if (x,y) in self.walkmap:
                    break
                n += 1

            draw_window(['Rock depth: ' + str(n)], self.w, self.h)
            self.achievements.use(item)

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
            self.achievements.use(item)

        elif item.cooling:
            self.cooling = max(int(random.gauss(*self.coef.coolingduration)), 1)
            self.msg.m("You cover yourself in cold mud.")

            self.achievements.use(item)
            return None

        elif item.wishing:
            self.wish()

            self.achievements.use(item)
            return None

        elif item.mapper:
            self.mapping = item.mapper

            # HACK
            for x in xrange(self.w):
                for y in xrange(self.h):
                    dg.render_set_is_lit(x, y, True)

            self.achievements.use(item)
            return None

        elif item.jinni:
            l = []
            for ki in self.neighbors[(self.px,self.py)]:
                if ki in self.walkmap and ki not in self.monmap:
                    l.append(ki)

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

            self.achievements.use(item)
            return None

        elif item.digray:
            if item.digray[0] == 1:
                for x in xrange(0, self.w):
                    self.convert_to_floor(x, self.py)
            if item.digray[1] == 1:
                for y in xrange(0, self.h):
                    self.convert_to_floor(self.px, y)
            self.msg.m('The wand explodes in a brilliant white flash!')

            self.achievements.use(item)
            return None

        elif item.jumprange:
            x, y = self.find_blink_targ(self.px, self.py, item.jumprange)
            self.px = x
            self.py = y

            self.achievements.use(item)

            if item.count is None:
                return item
            return None

        elif item.makestrap:
            if (self.px,self.py) in self.featmap:
                self.msg.m('Nothing happens.')
                return item

            if (self.px,self.py) in self.watermap:
                self.msg.m("That won't work while you're standing on water.")
                return item

            #self.featmap[(self.px, self.py)] = self.featstock.f['^']
            self.set_feature(self.px, self.py, '^')
            self.msg.m('You spread the glue liberally on the floor.')

            self.achievements.use(item)

            if item.count is None:
                return item
            return None

        elif item.ebola:
            self.msg.m('The Ebola virus is unleashed!')
            self.paste_celauto(self.px, self.py, self.celautostock.EBOLA)
            self.achievements.use(item)
            return None

        elif item.smoke:
            self.paste_celauto(self.px, self.py, self.celautostock.SMOKE)
            self.achievements.use(item)
            return item

        elif item.trapcloud:
            self.msg.m('You set the nanobots to work.')
            self.paste_celauto(self.px, self.py, self.celautostock.TRAPMAKER)

            self.achievements.use(item)

            if item.count is None:
                return item
            return None

        elif item.airfreshener:
            if item.ammo == 0:
                self.msg.m("It's out of ammo!")
                return item

            self.airfreshen(self.px, self.py, item.airfreshener)
            self.achievements.use(item)

            if item.ammo > 0:
                item.ammo -= 1

            if item.ammo == 0:
                return None
            return item

        elif item.resource:
            self.achievements.use(item)
            self.colordrink(item.resource)
            return None

        elif item.summon:
            self.summon(self.px, self.py, item.summon[0], item.summon[1])
            self.achievements.use(item)
            return None

        elif item.switch_moon:
            self.moon = item.switch_moon
            self.regen(self.w, self.h)
            self.achievements.use(item)
            self.msg.m('The local space-time continuum shifts slightly.', True)
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

            self.achievements.use(item)

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

        self.regen(self.w, self.h)
        self.tick()
        self.achievements.descend(self)

        if self.config.music_n >= 0:
            self.config.sound.set(self.config.music_n, rate=min(10, 2.0+(0.5*self.dlev)))


    def drop(self):
        slot = self.showinv()
        i = self.inv.drop(slot)
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
                    del self.itemap[(px, py)][ix]

                    if len(self.itemap[(px, py)]) == 0:
                        del self.itemap[(px, py)]
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

        c = draw_window(s, self.w, self.h)
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


    def handle_mondeath(self, mon, do_drop=True, do_gain=True,
                        is_rad=False, is_explode=False, is_poison=False):

        if mon.inanimate:
            do_gain = False

        if do_gain and mon.level > self.plev:
            self.msg.m('You just gained level ' + str(mon.level) + '!', True)
            self.plev = mon.level

        if do_drop:
            itemdrop = mon.items

            # HACK
            if self.moon == moon.NEW and not mon.itemdrop and \
               mon.flavor not in ('digital', 'air', 'robot') and not mon.boulder:
                corpse = self.itemstock.get('corpse')
                corpse.corpse = mon
                itemdrop = itemdrop[:]
                itemdrop.append(corpse)

            if len(itemdrop) > 0:
                self.set_item(mon.x, mon.y, itemdrop)

        winner, exting = self.monsterstock.death(mon, self.moon)

        if do_gain:
            self.achievements.mondeath(self, mon, is_rad=is_rad, is_explode=is_explode)
        elif is_poison:
            self.achievements.mondeath(self, mon, is_poison=True)

        if exting:
            self.achievements.mondone()

        # Quests
        if self.branch in self.quests and sum(1 for m in self.monmap.itervalues() if not m.inanimate) == 1:
            quest = self.quests[self.branch]

            questdone = (quest.dlevels[1] == self.dlev)

            for msg in quest.messages[self.dlev]:
                self.msg.m(msg, True)

            if questdone:
                self.achievements.questdone(self.branch)
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
            while 1:
                c = draw_window(['Congratulations! You have won the game.', '', 'Press space to exit.'], self.w, self.h)
                if c == ' ': break

            self.stats.health.reason = 'winning'
            self.done = True
            self.dead = True
            self.achievements.winner()


    def rayblast(self, x0, y0, rad):

        libtcod.map_compute_fov(self.tcodmap, x0, y0, rad,
                                False, libtcod.FOV_SHADOW)

        def func1(x, y):
            return libtcod.map_is_in_fov(self.tcodmap, x, y)

        def func2(x, y):
            if x == self.px and y == self.py:
                radimmune = False
                if self.inv.trunk and self.inv.trunk.radimmune:
                    radimmune = True
                elif self.resource_timeout and self.resource == 'b':
                    radimmune = True

                if not radimmune:
                    self.stats.health.dec(self.coef.raddamage, "radiation", self.config.sound)

            if (x, y) in self.monmap:
                mon = self.monmap[(x, y)]
                if not mon.radimmune:
                    mon.hp -= self.coef.raddamage
                    if mon.hp <= -3.0:
                        self.handle_mondeath(mon, is_rad=True)
                        del self.monmap[(x, y)]

        draw_blast2(x0, y0, self.w, self.h, rad, func1, func2)


    def explode(self, x0, y0, rad):

        chains = set()

        def f_explod(x, y):
            if x == self.px and y == self.py:

                explimmune = False
                if self.inv.trunk and self.inv.trunk.explodeimmune:
                    explimmune = True
                elif self.resource_timeout and self.resource == 'b':
                    explimmune = True

                if not explimmune:
                    self.stats.health.dec(6.0, "explosion", self.config.sound)
                    self.dead = True

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
                draw_floodfill(x, y, self.w, self.h, func_ff)

            if random.randint(0, 5) == 0:
                self.set_feature(x, y, '*')
            else:
                self.set_feature(x, y, None)


        draw_blast(x0, y0, self.w, self.h, rad, func_r)

        for x, y, r, d in sorted(chains):
            self.explode(x, y, r)



    def airfreshen(self, x0, y0, rad):

        libtcod.map_compute_fov(self.tcodmap, x0, y0, rad,
                                False, libtcod.FOV_SHADOW)

        def func1(x, y):
            return libtcod.map_is_in_fov(self.tcodmap, x, y)

        def func2(x, y):
            self.clear_celauto(x, y)

        draw_blast2(x0, y0, self.w, self.h, rad, func1, func2, color=libtcod.yellow)


    def raise_dead(self, x0, y0, rad):

        libtcod.map_compute_fov(self.tcodmap, x0, y0, rad,
                                False, libtcod.FOV_SHADOW)

        ret = []

        def func1(x, y):
            return libtcod.map_is_in_fov(self.tcodmap, x, y)

        def func2(x, y):
            if (x,y) in self.itemap:
                i2 = []
                for i in self.itemap[(x,y)]:
                    if i.corpse:
                        ret.append((x,y,i.corpse))
                    else:
                        i2.append(i)

                if len(i2) > 0:
                    self.itemap[(x,y)] = i2
                else:
                    del self.itemap[(x,y)]

        draw_blast2(x0, y0, self.w, self.h, rad, func1, func2, color=None)
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
                self.stats.health.dec(6, sm, self.config.sound)
                self.msg.m('You got squashed. What a silly way to die!')
                self.dead = True
                return

        ##

        d = math.sqrt(math.pow(abs(mon.x - self.px), 2) +
                      math.pow(abs(mon.y - self.py), 2))
        d = int(round(d))

        if player_move and item:
            plev = min(max(self.plev - d + 1, 1), self.plev)
            attack = item.rangeattack
            #log.log('+', d, plev, attack)

        else:
            if self.b_grace and player_move:
                self.msg.m('Your religion prohibits you from fighting.')
                return

            plev = self.plev
            attack = max(self.inv.get_attack(), self.coef.unarmedattack)

            if self.resource_timeout and self.resource == 'g':
                attack = max(self.coef.green_attack, attack)


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
                    ca = self.inv.get_confattack()
                    fires = self.inv.get_fires()

                if ca and dmg > 0 and not mon.confimmune:
                    if mon.visible or mon.visible_old:
                        self.msg.m(smu + ' looks totally dazed!')
                    mon.confused += int(max(random.gauss(*ca), 1))

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
                if dmg > 0:
                    self.msg.m('You fall asleep!')
                    self.start_sleep(force=True, quick=True, realforced=True)

            elif mon.bloodsucker:
                if dmg > 0:
                    self.msg.m('You feel weak!')
                    self.stats.hunger.dec(mon.bloodsucker[0])
                    self.stats.health.dec(mon.bloodsucker[0], sm, self.config.sound)
                    mon.fleetimeout = mon.bloodsucker[1]

            elif mon.hungerattack:
                self.stats.hunger.dec(dmg)

            else:
                self.stats.health.dec(dmg, sm, self.config.sound)

            if self.resting:
                self.msg.m('You stop resting.')
                self.resting = False

            if self.digging:
                self.msg.m('You stop digging.')
                self.digging = None

            if self.sleeping and not self.forced2sleep:
                self.sleeping = 0
                self.forcedsleep = False
                self.healingsleep = False

            if self.stats.health.x <= -3.0:
                self.dead = True


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

        tmsg = ['Pick a target. '
                "HJKL YUBN for directions, "
                "<space> to pick target and and '.' to fire."]

        if point[0] is not None:
            self.draw(point[0], point[1], range=(minrange, range), 
                      lightradius=lightradius)
            if point[1] <= 2:
                tmsg = []

        k = draw_window(tmsg,
                        self.w, self.h, True)

        poiok = (point[0] is not None)

        if k == 'h':
            if poiok: return (max(point[0]-1,0), point[1]), False
            else:     return (max(self.px-range,0), self.py), False
        elif k == 'j':
            if poiok: return (point[0], min(point[1]+1,self.h-1)), False
            else:     return (self.px, min(self.py+range, self.h-1)), False
        elif k == 'k':
            if poiok: return (point[0], max(point[1]-1,0)), False
            else:     return (self.px, max(self.py-range,0)), False
        elif k == 'l':
            if poiok: return (min(point[0]+1,self.w-1), point[1]), False
            else:     return (min(self.px+range,self.w-1), self.py), False
        elif k == 'y':
            if poiok: return (max(point[0]-1,0), max(point[1]-1,0)), False
            else:     return (max(self.px - int(range * 0.71), 0),
                              max(self.py - int(range * 0.71), 0)), False
        elif k == 'u':
            if poiok: return (min(point[0]+1,self.w-1), max(point[1]-1,0)), False
            else:     return (min(self.px + int(range * 0.71), self.w - 1),
                              max(self.py - int(range * 0.71), 0)), False
        elif k == 'b':
            if poiok: return (max(point[0]-1,0), min(point[1]+1,self.h-1)), False
            else:     return (max(self.px - int(range * 0.71), 0),
                              min(self.py + int(range * 0.71), self.h - 1)), False
        elif k == 'n':
            if poiok:  return (min(point[0]+1,self.w-1), min(point[1]+1,self.h-1)), False
            else:      return (min(self.px + int(range * 0.71), self.w - 1),
                               min(self.py + int(range * 0.71), self.h - 1)), False
        elif k == '.':
            if poiok is None:
                return (None, None), False
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
                return (xx, yy), True

            if (tmpx, tmpy) in self.walkmap or self.try_feature(tmpx, tmpy, 'shootable'):

                if minrange > 0:
                    d = math.sqrt(math.pow(abs(tmpx - self.px), 2) +
                                  math.pow(abs(tmpy - self.py), 2))
                    if d < minrange:
                        continue

                xx = tmpx
                yy = tmpy

                if monstop and (tmpx, tmpy) in self.monmap:
                    return (xx, yy), True

            else:
                return (xx, yy), True

    def target(self, range, minrange=0, monstop=False, lightradius=None):

        point = (None, None)
        while 1:
            point, ok = self._target(point, range, 
                                     minrange=minrange, 
                                     monstop=monstop, 
                                     lightradius=lightradius)

            if ok:
                print 'RET:',point
                return point



    def show_messages(self):
        self.msg.show_all(self.w, self.h)


    def wish(self, msg=None):
        s = ''
        while 1:
            if msg:
                k = draw_window([msg, '', 'Wish for what? : ' + s],
                                self.w, self.h)
            else:
                k = draw_window(['Wish for what? : ' + s], self.w, self.h)

            k = k.lower()
            if k in "abcdefghijklmnopqrstuvwxyz' -":
                s = s + k
            elif ord(k) == 8 or ord(k) == 127:
                if len(s) > 0:
                    s = s[:-1]
            elif k in '\r\n':
                break

        i = self.itemstock.find(s)

        self.achievements.wish()

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
        k = draw_window(["Really quit? Press 'y' if you are truly sure."], self.w, self.h)
        if k == 'y':
            self.stats.health.reason = 'quitting'
            #self.done = True
            self.dead = True


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
        draw_window(s, self.w, self.h)


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
                if random.randint(1, mon.moldspew[1]) == 1:
                    self.seed_celauto(ki[0], ki[1], mon.moldspew[0])

        if mon.onfire > 0:
            mon.onfire -= 1
            self.seed_celauto(mon.x, mon.y, self.celautostock.FIRE)
            self.set_feature(mon.x, mon.y, '"')

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

                if ret not in self.walkmap:
                    mon.bld_delta = None
                    return None, None
                else:
                    return ret[0], ret[1]
            else:
                return None, None

        rang = mon.range

        if self.b_grace:
            rang = 12 - int(9 * (float(self.b_grace) / self.coef.b_graceduration))
            rang = min(rang, mon.range)

        camorange = self.inv.get_camorange()

        if self.resource_timeout and self.resource == 'p':
            camorange = min(self.coef.purple_camorange, camorange)

        if camorange:
            rang = min(rang, camorange)

        if self.try_feature(x, y, 'confuse'):
            rang = 1

        if dist > rang or mon.confused or (mon.sleepattack and self.sleeping):
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

            repelrange = self.inv.get_repelrange()

            if repelrange and dist <= repelrange and dist > 1:
                 return None, None

            if mon.known_px is None or mon.known_py is None:
                mon.known_px = self.px
                mon.known_py = self.py

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
                        if (_x,_y) in self.walkmap and \
                           ((mon.known_px >= x and _x < x) or \
                            (mon.known_px <= x and _x > x) or \
                            (mon.known_py <= y and _y > y) or \
                            (mon.known_py >= y and _y < y)):
                            mdx, mdy = _x, _y
                            break

                else:
                    libtcod.path_compute(self.floorpath, x, y, mon.known_px, mon.known_py)
                    mdx, mdy = libtcod.path_walk(self.floorpath, True)

                    if mon.fast:
                        mdx2, mdy2 = libtcod.path_walk(self.floorpath, True)
                        if mdx2 is not None and mdy2 is not None:
                            mdx, mdy = mdx2, mdy2
                    


        if mon.stoneeating:
            if mdx is not None:
                if (mdx, mdy) not in self.walkmap:
                    self.convert_to_floor(mdx, mdy, rubble=1)

        return mdx, mdy

    def process_monstep(self, mon):
        mdx = mon.x
        mdy = mon.y

        if self.try_feature(mdx, mdy, 'sticky') and not mon.flying:
            if mon.visible or mon.visible_old:
                mn = str(mon)
                mn = mn[0].upper() + mn[1:]
                self.msg.m(mn + ' gets stuck in some glue!')
            mon.glued = max(int(random.gauss(*self.coef.glueduration)), 1)


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
            if ki in self.walkmap and \
               ki not in self.monmap and \
               (ki[0] != self.px or ki[1] != self.py):
                l.append(ki)

        ret = []
        for i in xrange(len(m)):
            if len(l) == 0:
                return ret
            j = random.randint(0, len(l)-1)
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


        d = (mon.level - self.plev)
        if d >= 2:
            ok = False
            if d == 2 and random.randint(0, 50) == 1:
                ok = True
            elif d == 3 and random.randint(0, 20) == 1:
                ok = True
            elif random.randint(0, 10) == 1:
                ok = True

            if ok:
                t = int(time.time())
                if t - self.last_played_themesound < 5:
                    return

                msg(mon.flavor, dist)
                self.last_played_themesound = t


    def paste_celauto(self, x, y, ca):
        self.celautostock.paste(x, y, self.w, self.h, ca)

    def seed_celauto(self, x, y, ca):
        self.celautostock.seed(x, y, ca)

    def clear_celauto(self, x, y):
        def cboff(x,y,ca):
            self.celauto_off(x,y,ca)
        self.celautostock.clear(x, y, cboff)
        


    def celauto_on(self, x, y, ca):
        ca = self.celautostock.stock[ca]

        if ca.watertoggle is not None:
            self.watermap.add((x, y))
        elif ca.featuretoggle:
            if (x, y) not in self.featmap and (x, y) in self.walkmap:
                self.set_feature(x, y, ca.featuretoggle)
        elif ca.floorfeaturetoggle:
            if (x, y) not in self.featmap and (x, y) in self.walkmap and (x, y) not in self.watermap:
                self.set_feature(x, y, ca.floorfeaturetoggle)

    def celauto_off(self, x, y, ca):
        ca = self.celautostock.stock[ca]

        if ca.watertoggle is not None:
            self.watermap.discard((x, y))
        elif ca.featuretoggle and (x, y) in self.featmap and \
             self.featmap[(x, y)] == self.featstock.f[ca.featuretoggle]:
            self.unset_feature(x, y)

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
                            delitems.append(k)
                        elif i.radexplode:
                            rblasts.append((k[0], k[1], i.radius))
                            delitems.append(k)
                        elif i.swampgas:
                            self.paste_celauto(self.px, self.py, self.celautostock.SWAMPGAS)
                            delitems.append(k)
                        else:
                            explodes.add((k[0], k[1], i.radius))

        for x,y,r in rblasts:
            self.rayblast(x, y, r)

        for ix,iy in delitems:
            if (ix,iy) in self.itemap:
                l2 = []
                for i in self.itemap[(ix,iy)]:
                    if i.liveexplode != 0:
                        l2.append(i)

                if len(l2) > 0:
                    self.itemap[(ix,iy)] = l2
                else:
                    del self.itemap[(ix,iy)]


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

            elif (mon.visible or mon.visible_old) and not (mon.was_seen) and not self.mapping:
                mon.was_seen = True
                self.msg.m('You see ' + str(mon) + '.')
                m = max(0.25, min(3, 0.5 * (mon.level - self.plev)))
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
                        self.msg.m(smu + ' burns to death!')

                    self.handle_mondeath(mon, do_gain=True)
                    mon.do_die = True
                    mons.append(mon)
                    continue

                elif p:
                    mon.onfire = max(self.coef.burnduration, mon.onfire)


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
            if (x,y) in self.walkmap and (x,y) not in self.monmap and not (x == self.px and y == self.py):
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
            del self.itemap[(x, y)]
            self.explode(x, y, r)



    def draw(self, _hlx=1000, _hly=1000, range=(0,1000), lightradius=None):

        withtime = False
        if self.oldt != self.t:
            withtime = True

        if self.resource_timeout and self.resource == 'y':
            lightradius = self.coef.yellow_lightradius
        else:
            lightradius = min(max(self.inv.get_lightradius() + (lightradius or 0), 2), 15)

        if self.blind:
            lightradius /= 2

        if self.b_grace:
            n = int(15 * (float(self.b_grace) / self.coef.b_graceduration))
            lightradius = max(lightradius, n)

        if self.moon == moon.NEW:
            lightradius += 1
        elif self.moon == moon.FULL:
            lightradius -= 2

        lightradius += self.try_feature(self.px, self.py, 'lightbonus', 0)

        if lightradius < 1:
            lightradius = 1

        if self.mapping > 0:
            if withtime:
                self.mapping -= 1

            if self.mapping > 0:
                lightradius = 25

            else:
                # HACK
                for x in xrange(self.w):
                    for y in xrange(self.h):
                        dg.render_set_is_lit(x, y, False)


        if withtime:
            self.process_world()
            self.monsters_in_view = []


        # hack, after process_world because confusing features may be created
        if self.try_feature(self.px, self.py, 'confuse'):
            lightradius = 1

        
        did_highlight = False


        telerange = 0
        if self.resource_timeout and self.resource == 'p':
            telerange = self.coef.purple_telerange
        elif self.inv.head and self.inv.head.telepathyrange:
            telerange = self.inv.head.telepathyrange


        ###

        for k,v in sorted(self.itemap.iteritems()):
            itm = v[0]

            if itm.corpse:
                dg.render_push_skin(k[0], k[1], itm.corpse.skin[1], itm.skin[0], libtcod.black, 0, False)
            else:
                dg.render_push_skin(k[0], k[1], itm.skin[1], itm.skin[0], libtcod.black, 0, False)

        lit_mons = set()

        for k,v in sorted(self.monmap.iteritems()):
            dg.render_push_skin(k[0], k[1], v.skin[1], v.skin[0], libtcod.black, 0, v.boulder)

            if telerange and not v.inanimate:
                d = math.sqrt(math.pow(abs(self.px - k[0]),2) + math.pow(abs(self.py - k[1]),2))

                if d <= telerange:
                    lit_mons.add(k)
                    dg.render_set_is_lit(k[0], k[1], True)

            # TODO! Visible monsters, mon.visible, monsters_in_view

        pc = '@'
        if self.sleeping > 1 and (self.t & 1) == 1:
            pc = '*'
        elif self.resting and (self.t & 1) == 1:
            pc = '.'
        elif self.digging and (self.t & 1) == 1:
            pc = '('
        else:
            pc = '@'

        pccol = libtcod.white
        if self.onfire:
            pccol = libtcod.amber
        dg.render_push_skin(self.px, self.py, pccol, pc, libtcod.black, 0, False)

        ###

        did_highlight = dg.render_draw(self.tcodmap, self.t, self.px, self.py, 
                                       _hlx, _hly, range[0], range[1], lightradius)
        
        ###

        dg.render_pop_skin(self.px, self.py)


        for k,v in sorted(self.monmap.iteritems()):
            dg.render_pop_skin(k[0], k[1])
            if k in lit_mons:
                dg.render_set_is_lit(k[0], k[1], False)

            if withtime and dg.render_is_in_fov(k[0], k[1]):
                self.monsters_in_view.append(v)
                v.visible = True

        for k,v in sorted(self.itemap.iteritems()):
            dg.render_pop_skin(k[0], k[1])

        ### 

        statsgrace = None
        if self.s_grace:
            statsgrace = (chr(234),
                          ((self.s_grace * 6) / self.coef.s_graceduration) + 1,
                          (self.s_grace > self.coef.s_graceduration - self.coef.s_praytimeout))

        elif self.v_grace:
            statsgrace = (chr(233),
                          ((self.v_grace * 6) / self.coef.v_graceduration) + 1,
                          (self.v_grace > self.coef.v_graceduration - self.coef.v_praytimeout))

        elif self.b_grace:
            statsgrace = (chr(127),
                          ((self.b_grace * 6) / self.coef.b_graceduration) + 1,
                          False)

        statsresource = None
        if self.resource:
            if self.resource_timeout:
                n = ((self.resource_timeout * 6) / self.coef.resource_timeouts[self.resource] + 1)
            else:
                n = self.resource_buildup

            statsresource = (self.resource, n,
                             True if self.resource_timeout else False)

        if self.px > self.w / 2:
            self.stats.draw(0, 0, grace=statsgrace, resource=statsresource)
        else:
            self.stats.draw(self.w - 14, 0, grace=statsgrace, resource=statsresource)

        if self.py > self.h / 2:
            self.msg.draw(15, 0, self.w - 30, self.t)
        else:
            self.msg.draw(15, self.h - 3, self.w - 30, self.t)


        # hack
        if withtime:
            self.moon_message()
            self.oldt = self.t

        return did_highlight


    def save(self):
        # HACK! For supporting replays of games that have been saved and then loaded.
        if self.save_disabled:
            random.seed(self._seed)
            return


        f = None
        atts = [
          'grid', 'walkmap', 'watermap', 'exit', 'itemap', 'monmap', 
          'featmap', 'px', 'py', 'w', 'h',
          'done', 'dead', 'stats', 'msg', 'coef', 'inv', 'itemstock', 'monsterstock', 'branch',
          'dlev', 'plev', 't', 'oldt', 'tagorder', 'sleeping', 'resting', 'cooling', 'digging', 'blind',
          'mapping', 'glued', 'onfire', 's_grace', 'b_grace', 'v_grace', 'forcedsleep',
          'forced2sleep', 'healingsleep',
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
            f = open('savefile.dat0', 'r')
            state = cPickle.load(f)
        except:
            return False

        for k,v in state.iteritems():
            setattr(self, k, v)

        dg.state_load('savefile.dat1')

        random.seed(self._seed)
        global _inputs
        _inputs = self._inputs

        self.make_map()
        self.make_paths()

        # HACK
        dg.neighbors_init(self.w, self.h)

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

        bones.append((self.plev, self.dlev, [i for i in self.inv if i is not None and i.liveexplode is None]))

        for i in bones[-1][2]:
            i.tag = None

        bones = bones[-3:]

        try:
            bf = open('bones', 'w')
            cPickle.dump(bones, bf)
        except:
            pass

        # Save to highscore.

        self.achievements.finish(self)


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

        score = self.plev * 5
        score += min(self.dlev, 21) * 5

        for x in self.achievements.killed_monsters:
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

        for a in self.achievements:
            c.execute('insert into ' + tbl_achievements + '(achievement, game_id) values (?, ?)',
                      (a.tag, gameid))

        conn.commit()


        # Show placements.

        c.execute('select sum(score >= %d),count(*) from %s' % (score, tbl_games))
        place, total = c.fetchone()

        atotals = []
        achievements = []

        for a in self.achievements:
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
            c = draw_window(s, self.w, self.h)
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
                                        self.w, self.h)
                        if c == 'n' or c == 'N':
                            done = True
                break



        s[-1] = ('Press space to ' + ('exit.' if self.done else 'try again.'))

        while 1:
            if draw_window(s, self.w, self.h) == ' ':
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
                            self.w, self.h)

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
                            self.w, self.h)

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
        self.config.sound.toggle_mute()
        if self.config.sound.mute:
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

        random.seed(world._seed)
        global _inputs
        _inputs = world._inputs

        world.regen(w, h)
        world.generate_inv()
        world.msg.m("Kill all the monsters in the dungeon to win the game.")
        world.msg.m("Please press '?' to see help.")

def check_autoplay(world):

    if world.sleeping > 0:
        if world.stats.sleep.x >= 3.0 and not world.forcedsleep and not world.forced2sleep:
            world.msg.m('You wake up.')
            world.sleeping = 0
            world.healingsleep = False
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
            world.grid[world.digging[1]][world.digging[0]] -= world.digging[2]
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

        if world.done or world.dead:
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


        if world.dead: break

        key = console_wait_for_keypress()

        if chr(key.c) in world.ckeys:
            world.ckeys[chr(key.c)]()

        elif key.vk in world.vkeys:
            world.vkeys[key.vk]()



    if world.dead and not world.done:
        world.msg.m('You die.', True)

    if config.music_n >= 0:
        config.sound.stop(config.music_n)

    world.oldt = world.t
    world.msg.m('*** Press any key ***', True)
    world.draw()
    libtcod.console_flush()
    libtcod.console_wait_for_keypress(True)

    if replay is None and world.dead:
        world.form_highscore()

    #log.log('DONE')
    #log.f.close()
    #log.f = None

    return world.done


#import cProfile
#cProfile.run('main()')

if __name__=='__main__':
    config = Config()
    while 1:
        print '-----============----'
        if main(config):
            break
