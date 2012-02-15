#!/usr/bin/env python

import math
import os
import copy
import time

import cPickle

import libtcodpy as libtcod

import libdiggrpy as dg

import moon

from xy import *

import dgsys
import scores

##
##
##

from flair import *

from coeffs import * 

from stats import * 
from messages import *
from inventory import *
from achievements import *

from items import *
from monsters import *
from features import *
from vaults import *
from quests import *
from celauto import *




class Player:
    def __init__(self):

        self.stats = Stats()
        self.inv = Inventory()
        self.achievements = Achievements()
        self.msg = Messages()

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

        self.did_moon_message = False


class Dungeon:
    def __init__(self):

        self.w = None
        self.h = None

        self.featmap = {}
        self.itemap = {}
        self.monmap = {}
        self.exit = None

        self.dlev = 1

        self.pc = (None, None)

        self.branch = None
        self.moon = None

        self.doppelpoint = None
        self.doppeltime = 0

        self.neighbors = None



class World:
    def __init__(self):

        self.coef = Coeffs()
        self.itemstock = ItemStock()
        self.monsterstock = MonsterStock()
        self.featstock = FeatureStock()
        self.vaultstock = VaultStock()
        self.queststock = QuestStock()

        self.t = 0
        self.oldt = -1

        self._seed = None
        self.bones = []


class Game:

    def __init__(self, config):

        self.p = Player()
        self.d = Dungeon()
        self.w = World()

        self.ckeys = None
        self.vkeys = None

        self.celautostock = CelAutoStock()

        self.monsters_in_view = None
        self.new_visibles = False

        self.save_disabled = False

        self.config = config
        self.last_played_themesound = 0

        self.quit_right_now = False

        ### 

        self.theme = { 'a': (libtcod.lime,),
                       'b': (libtcod.red,),
                       'c': (libtcod.sky,),
                       'd': (libtcod.darkest_grey,),
                       'e': (libtcod.lightest_yellow,),
                       's': (libtcod.darkest_blue,),
                       'q': (libtcod.white,),
                       'qk': (libtcod.grey,) }
        
        self.make_keymap()

        ###

    
    ###

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
            '.': self.do_rest,
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
            'S': self.save,
            chr(1): self.save_now
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


    ##

    def health(self): return self.p.stats.health
    def sleep(self):  return self.p.stats.sleep
    def tired(self):  return self.p.stats.tired
    def hunger(self): return self.p.stats.hunger
    def thirst(self): return self.p.stats.thirst
    def warmth(self): return self.p.stats.warmth

    def generate_and_take_item(self, itemname):
        self.p.inv.take(self.w.itemstock.find(itemname))

    ##

    def try_feature(self, xy, att, deflt=None):
        if xy not in self.d.featmap:
            return deflt
        return getattr(self.d.featmap[xy], att, deflt)


    ##

    def get_inv_attr(self, slots, attr, default=None):
        ix = [ self.p.inv._items[slot] for slot in slots ]
        return [ getattr(i, attr, default) for i in ix ]

    def get_fires(self):
        return self.get_inv_attr(['e'], 'fires')[0]

    def get_glueimmune(self):
        return self.get_inv_attr(['d'], 'glueimmune')[0]

    def get_digspeed(self):
        return sum(self.get_inv_attr(['a', 'e', 'h', 'i'], 'digbonus', 0))

    def get_springy(self):
        return (self.get_inv_attr(['g'], 'springy')[0] or 
                (self.p.resource_timeout and self.p.resource == 'y'))

    def get_heatbonus(self):
        return sum(self.get_inv_attr(['c', 'f'], 'heatbonus', 0))

    def get_radimmune(self):
        return (self.get_inv_attr(['c'], 'radimmune')[0] or
                (self.p.resource_timeout and self.p.resource == 'b'))

    def get_explodeimmune(self):
        return (self.get_inv_attr(['c'], 'explodeimmune')[0] or
                (self.p.resource_timeout and self.p.resource == 'b'))

    def get_confattack(self):
        for tmp in self.get_inv_attr(['e', 'd'], 'confattack'):
            if tmp:
                return tmp
        return None

    def get_psyimmune(self):
        return any(self.get_inv_attr(['a', 'e', 'd'], 'psyimmune'))

    def get_repelrange(self):
        return max(self.get_inv_attr(['c', 'd'], 'repelrange', 0))

    def get_telepathyrange(self):
        tmp = max(self.get_inv_attr(['a'], 'telepathyrange', 0))

        if self.p.resource_timeout and self.p.resource == 'p':
            tmp = max(self.w.coef.purple_telerange, tmp)

        return tmp


    def get_camorange(self, monrange):
        tmp = min(self.get_inv_attr(['c', 'g', 'b'], 
                                    'camorange', monrange))

        if self.p.resource_timeout and self.p.resource == 'p':
            tmp = min(self.w.coef.purple_camorange, tmp)

        if self.p.b_grace:
            rang = 12 - int(9 * (float(self.p.b_grace) / 
                                 self.w.coef.b_graceduration))
            tmp = min(rang, tmp)

        return tmp

    def get_attack(self):
        if self.p.resource_timeout and self.p.resource == 'g':
            baseattack = self.w.coef.green_attack
        else:
            baseattack = self.w.coef.unarmedattack

        return max(sum(self.get_inv_attr(['e', 'd', 'g'], 
                                         'attack', 0)),
                   baseattack)

    def get_defence(self):
        tmp = max(sum(self.get_inv_attr(['a', 'd', 'c', 
                                         'f', 'g'], 'defence', 0)),
                  self.w.coef.unarmeddefence)

        if self.p.glued:
            tmp /= self.w.coef.gluedefencepenalty
        return tmp

    def get_lightradius(self, default):

        if self.p.resource_timeout and self.p.resource == 'y':
            ret = self.w.coef.yellow_lightradius
        else:
            tmp = sum(self.get_inv_attr(['a', 'b', 'f', 'e', 'c'],
                                        'lightradius', 0))
            ret = min(max(tmp + (default or 0), 2), 15)

        if self.p.blind:
            ret /= 2

        if self.p.b_grace:
            n = int(15 * (float(self.p.b_grace) / self.w.coef.b_graceduration))
            ret = max(ret, n)

        if self.d.moon == moon.NEW:
            ret += 1
        elif self.d.moon == moon.FULL:
            ret -= 2

        ret += self.try_feature(self.d.pc, 'lightbonus', 0)

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

    ###


    # XXX 


    def makegrid(self, w_, h_):

        self.d.w = w_
        self.d.h = h_

        dg.grid_init(w_, h_)

        self.d.featmap = {}

        self.d.neighbors = {}
        for x in xrange(0, w_):
            for y in xrange(0, h_):
                self.d.neighbors[(x,y)] = []
                for xi in xrange(-1, 2):
                    for yi in xrange(-1, 2):
                        if xi == 0 and yi == 0:
                            continue

                        ki = (x+xi, y+yi)

                        if ki[0] < 0 or ki[0] >= w_ or ki[1] < 0 or ki[1] >= h_:
                            continue

                        self.d.neighbors[(x,y)].append(ki)

        dg.neighbors_init(w_, h_)
        dg.render_clear()

      

    def set_renderprops(self, xy):

        x, y = xy

        feat = None
        if xy in self.d.featmap:
            feat = self.d.featmap[xy]

        if feat and feat.lit:
            dg.render_set_is_lit(x, y, True)
        else:
            dg.render_set_is_lit(x, y, False)

        if feat and feat.back:
            dg.render_set_back(x, y, feat.back)
        else:
            dg.render_set_back(x, y, libtcod.black)

        fore = self.theme[self.d.branch][0]
        fore2 = fore
        fore_i = 0
        is_terrain = False
        c = ' '

        walkable = dg.grid_is_walk(x, y)

        if feat and feat.skin:
            c, fore = feat.skin

        elif walkable:
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

        ## 
        if feat:
            dg.render_set_is_viewblock(x, y, not feat.visible)
            dg.render_set_is_walkblock(x, y, not feat.walkable)
        else:
            dg.render_set_is_viewblock(x, y, not walkable)
            dg.render_set_is_walkblock(x, y, not walkable)



    def unset_feature(self, xy):
        if xy in self.d.featmap:
            del self.d.featmap[xy]
            self.set_renderprops(xy)

    def set_feature(self, xy, f_):
        x, y = xy

        if xy in self.d.featmap and self.d.featmap[xy].stairs:
            return

        if not f_:
            if xy in self.d.featmap:
                del self.d.featmap[xy]

            if f_ is None:
                dg.grid_set_walk(x, y, True)
                dg.grid_set_height(x, y, -10.0)

            else:
                dg.grid_set_walk(x, y, False)
                dg.grid_set_height(x, y, 0.0)

            self.set_renderprops(xy)
            return

        f = self.w.featstock.f[f_]
        w = f.walkable
        v = f.visible

        if f.nofeature:
            if xy in self.d.featmap:
                del self.d.featmap[xy]
        else:
            self.d.featmap[xy] = f

        if w:
            dg.grid_set_walk(x, y, True)
        else:
            dg.grid_set_walk(x, y, False)

        dg.grid_set_height(x, y, f.height)

        if f.water:
            dg.grid_set_water(x, y, True)
        elif f.water is not None:
            dg.grid_set_water(x, y, False)

        self.set_renderprops(xy)



    def set_item(self, xy, itms):
        while 1:
            if not self.try_feature(xy, 'stairs'):

                if xy not in self.d.itemap:
                    self.d.itemap[xy] = []
                iis = self.d.itemap[xy]

                while len(iis) < 5 and len(itms) > 0:
                    iis.append(itms.pop(0))

                if len(itms) == 0:
                    break

            d = [ k for k in self.d.neighbors[xy] if dg.grid_is_walk(k[0], k[1]) ]
            if len(d) == 0:
                iis.extend(itms)
                return
            xy = d[dg.random_n(len(d))]


    def paste_vault(self, v):
        xy = (None, None)

        if v.anywhere:
            xy = (dg.random_n(self.d.w - v.w), dg.random_n(self.d.h - v.h))

        else:
            for x in xrange(10):
                d = dg.grid_one_of_floor()

                xy0 = xy_sub(d, v.anchor)

                if xy_outside(xy0, (v.w, v.h), 0, 0, self.d.w, self.d.h):
                    continue

                xy = xy0
                break

        if xy_none(xy):
            return

        if v.message:
            for msg in reversed(v.message):
                self.p.msg.m(msg, True)

        for yi in xrange(v.h):
            for xi in xrange(v.w):
                z = v.pic[yi]
                if xi >= len(z):
                    continue
                z = z[xi]
                z = v.syms[z]
                if z is None:
                    continue

                xxyy = xy_add(xy, (xi, yi))
                self.set_feature(xxyy, z[0])

                if len(z) >= 3:
                    if z[1] is True:
                        dg.grid_add_nogen(xxyy[0], xxyy[1])
                    else:
                        itm = self.w.itemstock.get(z[1])
                        if itm:
                            self.set_item(xxyy, [itm])


    def make_feats(self):

        self.d.featmap = {}
        dg.celauto_init()

        # HACK!
        # This is done here, and not in make_items(),
        # so that vaults could generate items.
        self.d.itemap = {}

        oldvaults = set()
        while 1:
            vault = self.w.vaultstock.get(self.d.branch, self.d.dlev, oldvaults)

            if vault:
                self.paste_vault(vault)
                oldvaults.add(vault)

            if not vault or not vault.free:
                break

        # Quests
        if self.w.queststock.get(self.d.branch):
            return

        d = dg.grid_one_of_floor()

        self.set_feature(d, '>')
        self.d.exit = d

        dg.grid_add_nogen(d[0], d[1])

        if self.d.moon == moon.NEW:
            d = dg.grid_one_of_floor()
            self.set_feature(d, 'bb')

        elif self.d.moon == moon.FULL:
            d = dg.grid_one_of_floor()
            self.set_feature(d, 'dd')
            self.paste_celauto(d, self.celautostock.FERN)

        else:
            a = dg.random_range(-1, 1)
            d = dg.grid_one_of_floor()
            if a == -1:
                self.set_feature(d, 's')
            elif a == 0:
                self.set_feature(d, 'b')
            elif a == 1:
                self.set_feature(d, 'v')

        nfounts = int(round(dg.random_gauss(3, 1)))

        for tmp in xrange(nfounts):
            d = dg.grid_one_of_water()
            self.set_feature(d, ['C','V','B','N','M'][dg.random_n(5)])


    def place_monster(self, xy, mon):
        mon.xy = xy
        self.d.monmap[xy] = mon

        dg.render_set_is_walkblock(xy[0], xy[1], True)
        if mon.large:
            dg.render_set_is_viewblock(xy[0], xy[1], True)

    def remove_monster(self, mon):
        xy = mon.xy
        dg.render_set_is_walkblock(xy[0], xy[1], False)
        if mon.large:
            dg.render_set_is_viewblock(xy[0], xy[1], False)
        
        del self.d.monmap[xy]


    def make_monsters(self):

        self.w.monsterstock.clear_gencount()
        self.d.monmap = {}

        # Quests
        quest = self.w.queststock.get(self.d.branch)

        if quest:
            n = quest.moncounts.get(self.d.dlev, 0)

        else:
            n = int(max(dg.random_gauss(*self.w.coef.nummonsters), 1))

        i = 0
        while i < n:
            lev = self.d.dlev + dg.random_gauss(0, self.w.coef.monlevel)
            lev = max(int(round(lev)), 1)

            # Quests
            if quest:
                lev = min(max(lev, quest.monlevels[0]), quest.monlevels[1])

            while 1:
                xy = dg.grid_one_of_walk()
                if xy not in self.d.monmap: break

            m = self.w.monsterstock.generate(self.d.branch, lev, self.w.itemstock, self.d.moon)
            if m:
                self.place_monster(xy, m)
                dg.grid_add_nogen(xy[0], xy[1])

                if m.inanimate:
                    continue

            i += 1


        # Generate some mold.
        if quest:
            return

        if dg.random_range(1, self.w.coef.moldchance) == 1:
            xy = dg.grid_one_of_floor()
            m = self.w.monsterstock.generate('x', self.d.dlev, self.w.itemstock, self.d.moon)
            if m:
                self.place_monster(xy, m)


    def make_items(self):

        ## Quests
        quest = self.w.queststock.get(self.d.branch)

        if quest:
            n = quest.itemcounts.get(self.d.dlev, 0)
        else:
            n = int(max(dg.random_gauss(self.w.coef.numitems[0] + self.d.dlev, self.w.coef.numitems[1]), 1))

        for i in xrange(n):
            lev = self.d.dlev + dg.random_gauss(0, self.w.coef.itemlevel)
            lev = max(int(round(lev)), 1)
            xy = dg.grid_one_of_walk()
            item = self.w.itemstock.generate(lev)
            if item:
                self.set_item(xy, [item])

        ## Quests
        if quest:
            return

        for pl,dl,itm in self.w.bones:
            if dl == self.d.dlev and len(itm) > 0:
                itm2 = [copy.copy(i) for i in itm]

                xy = dg.grid_one_of_walk()

                self.set_item(xy, itm2)


    def place(self):

        # Do not place a player in an unfair position.
        # Otherwise, the monster will get a free move and might
        # kill the player.
        monn = set(k for k in self.d.monmap.iterkeys())

        for x in xrange(3):
            monn2 = set()
            for k in monn:
                for ki in self.d.neighbors[k]:
                    monn2.add(ki)
            monn.update(monn2)

        for k in monn:
            dg.grid_add_nogen(k[0], k[1])

        xy = dg.grid_one_of_walk()
        self.d.pc = xy

        
    def regen(self, w_, h_):
        if self.d.branch is None:
            self.d.branch = ['a', 'b', 'c', 'd', 'e'][dg.random_n(5)]

        if self.d.moon is None:
            m = moon.phase(self.w._seed)
            self.d.moon = m['phase']

        self.makegrid(w_, h_)

        # Quests
        if not self.w.queststock.get(self.d.branch):
            gentype = 0

            if self.d.moon in (moon.NEW, moon.FULL):
                gentype = 1
            elif self.d.moon in (moon.FIRST_QUARTER, moon.LAST_QUARTER):
                gentype = -1

            dg.grid_generate(gentype)

        self.make_feats()
        self.make_monsters()
        self.make_items()
        self.place()

        for x in xrange(w_):
            for y in xrange(h_):
                self.set_renderprops((x, y))

        if self.d.moon == moon.FULL:
            dg.render_set_env(libtcod.gray, 0.6)
        elif self.d.moon == moon.NEW:
            dg.render_set_env(libtcod.darkest_blue, 0.4)
        else:
            dg.render_set_env(libtcod.white, 0)


    def generate_inv(self):
        if self.d.moon == moon.FULL:
            self.generate_and_take_item("miner's lamp")
        else:
            self.generate_and_take_item('lamp')
            
        self.generate_and_take_item('pickaxe')


        pl = [k for k in self.d.neighbors[self.d.pc] if dg.grid_is_walk(k[0], k[1])] + [self.d.pc]

        for x in xrange(9):
            k = pl[dg.random_n(len(pl))]
            i = self.w.itemstock.generate(1)

            self.set_item(k, [i])


    def move(self, _dxy, do_spring=True):

        if self.p.glued > 0:
            self.p.glued -= 1
            if self.p.glued == 0:
                self.p.msg.m('You dislodge yourself from the glue.')
                if self.try_feature(self.d.pc, 'sticky'):
                    self.unset_feature(self.d.pc)
            else:
                self.p.msg.m('You are stuck in the glue!')
                self.tick()
                return

        dxy = xy_add(_dxy, self.d.pc)

        if dg.grid_is_walk(dxy[0], dxy[1]) and not xy_out_wh(dxy, self.d.w, self.d.h):

            if dxy in self.d.monmap:
                self.fight(self.d.monmap[dxy], True)
                self.tick()
                return
            else:
                self.d.pc = dxy

                if self.d.pc in self.d.itemap:
                    if len(self.d.itemap[self.d.pc]) > 1:
                        self.p.msg.m("You see several items here.")
                    else:
                        self.p.msg.m("You see " + str(self.d.itemap[self.d.pc][0]) + '.')

                sign = self.try_feature(self.d.pc, 'sign')
                if sign:
                    self.p.msg.m('You see an engraving: ' + sign)

                if self.p.onfire > 0:
                    self.seed_celauto(self.d.pc, self.celautostock.FIRE)
                    self.set_feature(self.d.pc, '"')

                if self.try_feature(self.d.pc, 'sticky') and not self.get_glueimmune():
                    self.p.msg.m('You just stepped in some glue!', True)
                    self.p.glued = max(int(dg.random_gauss(*self.w.coef.glueduration)), 1)


        else:
            return

        is_springy = self.get_springy()

        if do_spring and is_springy:
            self.move(_dxy, do_spring=False)
            return

        self.tick()


    def tick_checkstats(self):

        self.w.t += 1

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
                        self.summon(self.d.pc, i.summon[0], i.summon[1])
                    elif i.radexplode:
                        self.rayblast(self.d.pc, i.radius)
                    elif i.swampgas:
                        self.paste_celauto(self.d.pc, self.celautostock.SWAMPGAS)
                    else:
                        self.explode(self.d.pc, i.radius)
                    return False, True

            elif n == 2:
                i.selfdestruct -= 1
                if i.selfdestruct == 0:
                    self.p.msg.m('Your ' + i.name + ' falls apart!', True)
                    return False, True
            return False, False

        self.filter_inv(is_destruct, do_destruct)


        fdmg = self.try_feature(self.d.pc, 'fire')
        if fdmg > 0:
            self.health().dec(fdmg, "fire", self.config.sound)
            self.p.onfire = max(self.w.coef.burnduration, self.p.onfire)
        elif self.p.onfire > 0:
            if self.p.cooling == 0:
                self.health().dec(self.w.coef.burndamage, "fire", self.config.sound)
            self.p.onfire -= 1

        if self.p.cooling > 0:
            self.p.cooling -= 1
            if self.p.cooling == 0:
                self.p.msg.m("Your layer of cold mud dries up.")

        if self.d.doppeltime > 0:
            self.d.doppeltime -= 1

        if self.p.resource_timeout > 0: 
            if self.p.resource == 'r':
                self.health().inc(self.w.coef.regeneration)
                self.warmth().inc(self.w.coef.regeneration)
                self.hunger().inc(self.w.coef.regeneration)

            self.p.resource_timeout -= 1
            if self.p.resource_timeout == 0: self.p.resource = None

        if self.p.dead: return

        if self.try_feature(self.d.pc, 'warm'):
            self.warmth().inc(self.w.coef.watercold)
        elif dg.grid_is_water(self.d.pc[0], self.d.pc[1]):
            self.warmth().dec(self.w.coef.watercold)
        else:
            self.warmth().inc(self.get_heatbonus())

        p = self.try_feature(self.d.pc, 'queasy')
        if p:
            self.p.msg.m('You feel queasy.', True)
            self.thirst().dec(p)
            self.hunger().dec(p)

        if self.warmth().x <= -3.0:
            self.p.msg.m("Being so cold makes you sick!", True)
            self.health().dec(self.w.coef.colddamage, "cold", self.config.sound)
            if self.p.resting: self.p.resting = False
            if self.p.digging: self.p.digging = None

        if self.thirst().x <= -3.0:
            self.p.msg.m('You desperately need something to drink!', True)
            self.health().dec(self.w.coef.thirstdamage, "thirst", self.config.sound)
            if self.p.resting: self.p.resting = False
            if self.p.digging: self.p.digging = None

        if self.hunger().x <= -3.0:
            self.p.msg.m('You desperately need something to eat!', True)
            self.health().dec(self.w.coef.hungerdamage, "hunger", self.config.sound)
            if self.p.resting: self.p.resting = False
            if self.p.digging: self.p.digging = None

        p = self.try_feature(self.d.pc, 'poison')
        if p:
            self.p.msg.m('You feel very sick!', True)
            self.health().dec(p, 
                              'black mold' if self.try_feature(self.d.pc, 'pois2') else 'Ebola infection', 
                              self.config.sound)

        if self.health().x <= -3.0:
            self.p.dead = True
            return

        if self.tired().x <= -3.0:
            self.p.msg.m('You pass out from exhaustion!', True)
            self.start_sleep(force=True, quick=True)
            return

        if self.sleep().x <= -3.0:
            self.p.msg.m('You pass out from lack of sleep!', True)
            self.start_sleep(force=True)
            return


    def tick(self):
        self.tired().dec(self.w.coef.movetired)
        self.sleep().dec(self.w.coef.movesleep)
        self.thirst().dec(self.w.coef.movethirst)
        self.hunger().dec(self.w.coef.movehunger)

        if self.p.b_grace > 0: self.p.b_grace -= 1
        if self.p.v_grace > 0: self.p.v_grace -= 1
        if self.p.s_grace > 0: self.p.s_grace -= 1

        self.tick_checkstats()


    def do_rest(self):
        self.tired().inc(self.w.coef.resttired)
        self.sleep().dec(self.w.coef.restsleep)
        self.thirst().dec(self.w.coef.restthirst)
        self.hunger().dec(self.w.coef.resthunger)

        self.tick_checkstats()


    def do_sleep(self):
        self.tired().inc(self.w.coef.sleeptired)
        self.sleep().inc(self.w.coef.sleepsleep)
        self.thirst().dec(self.w.coef.sleepthirst)
        self.hunger().dec(self.w.coef.sleephunger)

        if self.p.healingsleep:
            self.health().inc(self.w.coef.healingsleep)

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
            self.p.msg.m('You don\'t feel like sleeping yet.')
            return

        if quick:
            self.p.sleeping = int(dg.random_gauss(*self.w.coef.quicksleeptime))
        else:
            if not realforced2:
                self.p.msg.m('You fall asleep.')
            self.p.sleeping = int(dg.random_gauss(*self.w.coef.sleeptime))

        self.p.digging = None
        self.p.resting = False

        if realforced:
            self.p.forcedsleep = True
        elif realforced2:
            self.p.forced2sleep = True

    def start_rest(self):
        self.p.msg.m('You start resting.')
        self.p.resting = True

        
    def colordrink(self, fount):
        if self.p.resource and (self.p.resource != fount):
            self.p.msg.m('You feel confused.')
            self.p.resource = None
            self.p.resource_timeout = 0
            self.p.resource_buildup = 0
            return

        if fount == 'r': self.p.msg.m('You drink something red.')
        elif fount == 'g': self.p.msg.m('You drink something green.')
        elif fount == 'y': self.p.msg.m('You drink something yellow.')
        elif fount == 'b': self.p.msg.m('You drink something blue.')
        elif fount == 'p': self.p.msg.m('You drink something purple.')
        self.p.resource = fount

        bonus = False
        
        if self.p.resource_timeout:
            self.p.resource_timeout += (self.w.coef.resource_timeouts[fount]/6)
        else:
            self.p.resource_buildup += 1

            if self.p.resource_buildup >= 6:
                if self.p.resource == 'r':
                    self.p.msg.m('You gain superhuman regeneration power!', True)
                elif self.p.resource == 'g':
                    self.p.msg.m('Hulk Smash! You gain superhuman strength.', True)
                elif self.p.resource == 'y':
                    self.p.msg.m('You gain superhuman speed and vision!', True)
                elif self.p.resource == 'b':
                    self.p.msg.m('You are now immune to explosions and radiation!', True)
                elif self.p.resource == 'p':
                    self.p.msg.m('You gain telepathy and superhuman stealth!', True)

                bonus = True
                self.p.resource_buildup = 0
                self.p.resource_timeout = self.w.coef.resource_timeouts[fount]

        self.p.achievements.resource_use(fount, bonus)


    def drink(self):

        if self.try_feature(self.d.pc, 'healingfountain'):
            nn = min(3.0 - self.health().x, self.hunger().x + 3.0)
            if nn <= 0:
                self.p.msg.m('Nothing happens.')
                return

            self.p.msg.m('You drink from the eternal fountain.')
            self.health().inc(nn)
            self.hunger().dec(nn)
            return

        fount = self.try_feature(self.d.pc, 'resource')
        if fount:
            self.colordrink(fount)
            self.unset_feature(self.d.pc)
            return
            
        if not dg.grid_is_water(self.d.pc[0], self.d.pc[1]):
            self.p.msg.m('There is no water here you could drink.')
            return

        if self.p.v_grace:
            self.p.msg.m('Your religion prohibits drinking from the floor.')
            return

        self.thirst().inc(6)

        x = abs(dg.random_gauss(0, 0.7))
        tmp = x - self.w.coef.waterpois
        if tmp > 0:
            self.health().dec(tmp, "unclean water", self.config.sound)
            if tmp > 0.2:
                self.p.msg.m('This water has a bad smell.')
        else:
            self.p.msg.m('You drink from the puddle.')

        self.tick()

    def pray(self):
        if self.d.pc not in self.d.featmap:
            self.p.msg.m('You need to be standing at a shrine to pray.')
            return

        a = self.d.featmap[self.d.pc]

        if a.bb_shrine:

            def bb_shrine_func(i, n):
                self.p.msg.m("Ba'al-Zebub accepts your sacrifice!")

                i2 = self.w.itemstock.generate(self.d.dlev)
                if i2:
                    self.set_item(self.d.pc, [i2])
                return False, True

            if self.filter_inv((lambda i,slot: i.corpse), bb_shrine_func):
                return

            self.p.msg.m("Ba'al-Zebub needs to be sated with blood!!")
            return

        if a.s_shrine:
            if self.p.b_grace or self.p.v_grace:
                self.p.msg.m("You don't believe in Shiva.")
                return
            if self.p.s_grace > self.w.coef.s_graceduration - self.w.coef.s_praytimeout:
                self.p.msg.m('Nothing happens.')
                return

            ss = "hwp"
            decc = self.w.coef.shivadecstat
            ss = ss[dg.random_n(len(ss))]

            if ss == 'h': self.hunger().dec(decc)
            elif ss == 'w': self.warmth().dec(decc)
            elif ss == 'p': self.health().dec(decc, 'the grace of Shiva', self.config.sound)

            self.p.msg.m('You pray to Shiva.')
            self.wish('Shiva grants you a wish.')
            self.p.s_grace = self.w.coef.s_graceduration
            self.tick()
            self.p.achievements.pray('s')

        elif a.b_shrine:
            if self.p.s_grace or self.p.v_grace:
                self.p.msg.m("You don't believe in Brahma.")
                return
            self.p.msg.m('As a follower of Brahma, you are now forbidden hand-to-hand combat.')
            self.p.msg.m('You feel enlightened.')
            self.p.b_grace = self.w.coef.b_graceduration
            self.tick()
            self.p.achievements.pray('b')

        elif a.v_shrine:
            if self.p.s_grace or self.p.b_grace:
                self.p.msg.m("You don't believe in Vishnu.")
                return

            if self.p.v_grace > self.w.coef.v_graceduration - self.w.coef.v_praytimeout:
                self.p.msg.m('Nothing happens.')
                return

            self.p.msg.m('As a follower of Vishnu, you are now forbidden '
                       'medicine, alcohol and unclean food.')
            self.p.msg.m('You meditate on the virtues of Vishnu.')
            self.start_sleep(force=True, realforced2=True)

            self.health().inc(6.0)
            self.sleep().inc(6.0)
            self.tired().inc(6.0)
            self.hunger().inc(6.0)
            self.thirst().inc(6.0)
            self.warmth().inc(6.0)
            self.p.v_grace = self.w.coef.v_graceduration
            self.tick()
            self.p.achievements.pray('v')

        elif a.special == 'kali':

            def kalifunc(i, n):
                self.p.msg.m('You return the Eye to Kali.', True)
                self.victory(msg=('winkali', 'Returned the Eye of Kali'))
                return True, False

            if self.filter_inv((lambda i,slot: i.special == 'kali'), kalifunc):
                return

            self.p.msg.m('Kali is silent. Perhaps she requires an offering?', True)

        elif a.special == 'monolith':
            self.victory(msg=('winmono', 'Rubbed the Monolith'))

        else:
            self.p.msg.m('You need to be standing at a shrine to pray.')
            return


    def convert_to_floor(self, xy, rubble):
        if self.try_feature(xy, 'permanent'):
            return

        if not rubble:
            self.set_feature(xy, None)
        else:
            self.set_feature(xy, '*')


    def find_blink_targ(self, _xy, range):
        _x, _y = _xy

        l = []
        for x in xrange(_x - range, _x + range + 1):
            for y in [_y - range, _x + range]:
                if x >= 0 and y >= 0 and dg.grid_is_walk(x,y) and (x,y) not in self.d.monmap:
                    l.append((x,y))

        for y in xrange(_y - range - 1, _y + range):
            for x in [_x - range, _x + range]:
                if x >= 0 and y >= 0 and dg.grid_is_walk(x,y) and (x,y) not in self.d.monmap:
                    l.append((x,y))

        if len(l) == 0:
            return _x, _y

        l = l[dg.random_n(len(l))]
        return l


    def showinv(self):
        return self.p.inv.draw(self.d.dlev, self.p.plev)


    def showinv_apply(self):
        slot = self.p.inv.draw(self.d.dlev, self.p.plev)
        i = self.p.inv.drop(slot)
        if not i:
            if slot in 'abcdefghi':
                self.p.msg.m('You have no item in that slot.')
            return

        if not i.applies:
            self.p.msg.m('This item cannot be applied.')
            self.p.inv.take(i, slot)
            return

        self.apply_from_inv_aux(i)


    def tagged_apply(self):

        iss = self.p.inv.get_tagged()

        if len(iss) == 0:
            self.p.msg.m("Tag an item from your inventory to use this command.")
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


    def delete_item(self, items, c, xy):
        del items[c]
        if len(items) == 0:
            del self.d.itemap[xy]
            return True
        return False


    def take_aux(self, items, c):

        i = items[c]
        did_scavenge = False

        def takepred(ii, slot):
            if ii.name == i.name:
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

                self.p.msg.m('You now have ' + str(ii) + '.')

                if i.count == 0:
                    if self.delete_item(items, c, self.d.pc):
                        return True, False

            elif whc == 2:
                n = min(ii.ammochance[1] - ii.ammo, i.ammo)
                ii.ammo += n
                i.ammo -= n
                self.p.msg.m("You find some ammo for your " + ii.name + '.')
            return False, False

        if self.filter_inv(takepred, takefunc):
            self.tick()
            return

        ok = self.p.inv.take(i)
        if ok:
            self.p.msg.m('You take ' + str(i) + '.')
            self.delete_item(items, c, self.d.pc)
        else:
            self.p.msg.m('You have no free inventory slot for ' + str(i) + '!')

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
        if self.d.pc not in self.d.itemap:
            self.p.msg.m('You see no item here to take.')
            return

        self.showinv_interact(takestuff=True)

    def showinv_interact(self, takestuff=False):

        floorstuff = None
        flooritems = {}
        items = []

        if self.d.pc in self.d.itemap:
            floorstuff = ['','Items on the floor:','']

            items = self.d.itemap[self.d.pc]
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
            slot = self.p.inv.draw(self.d.dlev, self.p.plev, floor=floorstuff)

        i = None
        if slot in flooritems:
            i = items[flooritems[slot]]
        else:
            i = self.p.inv.check(slot)

        if not i:
            if slot in 'abcdefghi':
                self.p.msg.m('You have no item in that slot.')
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
        cc = draw_window(s)

        if cc not in choices:
            return

        if cc == 'a' and i.applies:
            if slot not in flooritems:
                i = self.p.inv.drop(slot)

            if slot in flooritems:
                self.apply_from_ground_aux(i, self.d.pc)
            else:
                self.apply_from_inv_aux(i)

        elif cc == 'z':
            if not i.tag and i.applies:
                i.tag = self.p.tagorder
                self.p.tagorder += 1

            elif i.tag:
                i.tag = None

        elif cc == 'c' and i.desc:
            ss = i.desc[:]
            ss.append('')
            ss.append('Slot: ' + self.slot_to_name(i.slot))

            if i.converts:
                inew = self.w.itemstock.get(i.converts)
                if inew:
                    ss.append('Slot that needs to be free to use this item: ' + self.slot_to_name(inew.slot))

            self.draw()
            draw_window(ss)

        elif cc == 'd':
            i = self.p.inv.drop(slot)
            self.set_item(self.d.pc, [i])
            self.tick()

        elif cc == 'q':

            if draw_window(['','Really destroy ' + str(i) +'? (Y/N)', '']) in ('y','Y'):
                if slot in flooritems:
                    self.delete_item(items, flooritems[slot], self.d.pc)
                else:
                    self.p.inv.drop(slot)
                self.tick()

        elif cc == 'f':
            while 1:
                nxy = self.target(i.throwrange)
                if not xy_none(nxy):
                    break

            if nxy[0] >= 0:
                if slot not in flooritems:
                    i = self.p.inv.drop(slot)

                self.p.msg.m('You throw ' + str(i) + '.')

                self.set_item(nxy, [i])

                if slot in flooritems:
                    self.delete_item(items, flooritems[slot], self.d.pc)

                self.tick()

        elif cc == 'x':
            if slot in flooritems:
                item2 = self.p.inv.drop(i.slot)
                ok = self.p.inv.take(i)
                if ok:
                    self.delete_item(items, flooritems[slot], self.d.pc)

                    if item2:
                        if not self.p.inv.take(item2):
                            self.set_item(self.d.pc, [item2])

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
                    backpack1 = self.p.inv.check('h')
                    backpack2 = self.p.inv.check('i')

                    if backpack1 and backpack1.slot == slot:
                        slt2 = 'h'
                    elif backpack2 and backpack2.slot == slot:
                        slt2 = 'i'

                    if slt2:
                        i = self.p.inv.drop(slot)
                        item2 = self.p.inv.drop(slt2)
                        self.p.inv.take(item2)
                        self.p.inv.take(i)
                    else:
                        if not backpack1:
                            self.p.inv.take(self.p.inv.drop(slot), 'h')
                        elif not backpack2:
                            self.p.inv.take(self.p.inv.drop(slot), 'i')

            self.tick()

        elif cc == 't':
            self.take_aux(items, flooritems[slot])



    def apply(self, item):
        if not item.applies:
            return item

        if item.applies_in_slot and self.p.inv.check(item.slot) is not None:
            self.p.msg.m("You can only use this item if it's in the " + self.slot_to_name(item.slot) + ' slot.', True)
            return item

        if item.converts:
            inew = self.w.itemstock.get(item.converts)

            if self.p.inv.check(inew.slot) is not None:
                self.p.msg.m('Your ' + self.slot_to_name(inew.slot) + ' slot needs to be free to use this.')
                return item

            self.p.inv.take(inew)
            s = str(inew)
            s = s[0].upper() + s[1:]
            self.p.msg.m(s + ' is now in your ' + self.slot_to_name(inew.slot) + ' slot!', True)

            self.p.achievements.use(item)
            return None

        elif item.craft:

            newi = None

            for i2,slot in self.p.inv:
                if i2 and i2.craft:
                    if item.craft[0] in i2.craft[1]:
                        newi = self.w.itemstock.get(i2.craft[1][item.craft[0]])
                        break

                    elif i2.craft[0] in item.craft[1]:
                        newi = self.w.itemstock.get(item.craft[1][i2.craft[0]])
                        break

            if not newi:
                self.p.msg.m('You have nothing you can combine with this item.')
                return item

            self.p.inv.purge(i2)
            self.p.achievements.craft_use(newi)
            self.p.msg.m('Using %s and %s you have crafted %s!' % (item, i2, newi))
            return newi

        elif item.digging:
            k = draw_window(['Dig in which direction?'], True)

            digspeed = self.get_digspeed() + item.digbonus

            self.p.digging = None
            if k == 'h': self.p.digging = (xy_add(self.d.pc, (-1, 0)), digspeed)
            elif k == 'j': self.p.digging = (xy_add(self.d.pc, (0, 1)), digspeed)
            elif k == 'k': self.p.digging = (xy_add(self.d.pc, (0, -1)), digspeed)
            elif k == 'l': self.p.digging = (xy_add(self.d.pc, (1, 0)), digspeed)
            else:
                return -1 #item

            if xy_out_wh(self.p.digging[0], self.d.w, self.d.h):
                self.p.digging = None
                return item

            if dg.grid_is_walk(self.p.digging[0][0], self.p.digging[0][1]):
                self.p.msg.m('There is nothing to dig there.')
                self.p.digging = None
            else:
                self.p.msg.m("You start hacking at the wall.")
                self.p.achievements.use(item)

        elif item.healing:

            if self.p.v_grace:
                self.p.msg.m('Your religion prohibits taking medicine.')
                return item

            if item.bonus < 0:
                self.p.msg.m('This pill makes your eyes pop out of their sockets!', True)
                self.tired().dec(max(dg.random_gauss(*item.healing), 0))
                self.sleep().dec(max(dg.random_gauss(*item.healing), 0))
            else:
                self.p.msg.m('Eating this pill makes you dizzy.')
                self.health().inc(max(dg.random_gauss(*item.healing), 0))
                self.hunger().dec(max(dg.random_gauss(*item.healing), 0))
                self.sleep().dec(max(dg.random_gauss(*item.healing), 0))

            self.p.achievements.use(item)
            return None


        elif item.healingsleep:

            if self.p.v_grace:
                self.p.msg.m('Your religion prohibits taking medicine.')
                return item

            if item.bonus < 0:
                self.p.msg.m('You drift into a restless sleep!', True)
                self.p.sleeping = max(dg.random_gauss(*item.healingsleep), 1)
                self.p.forced2sleep = True
            else:
                self.p.msg.m('You drift into a gentle sleep.')
                self.p.sleeping = max(dg.random_gauss(*item.healingsleep), 1)
                self.p.forced2sleep = True
                self.p.healingsleep = True

            self.p.achievements.use(item)

            if item.count == 0:
                return item
            return None

        elif item.food:

            if self.p.v_grace:
                self.p.msg.m('Your religion prohibits eating unclean food.')
                return item

            if item.bonus < 0:
                self.p.msg.m('Yuck, eating this makes you vomit!', True)
                self.hunger().dec(max(dg.random_gauss(*item.food), 0))
            else:
                self.p.msg.m('Mm, yummy.')
                self.hunger().inc(max(dg.random_gauss(*item.food), 0))

            self.p.achievements.use(item)
            return None

        elif item.booze:

            if self.p.v_grace:
                self.p.msg.m('Your religion prohibits alcohol.')
                return item

            if item.bonus < 0:
                self.p.msg.m("This stuff is contaminated! You fear you're going blind!", True)
                self.p.blind = True
            else:
                self.p.msg.m('Aaahh.')
                self.sleep().dec(max(dg.random_gauss(*self.w.coef.boozestrength), 0))
                self.warmth().inc(max(dg.random_gauss(*self.w.coef.boozestrength), 0))

            self.p.achievements.use(item)
            return None

        elif item.nodoz:
            
            if self.p.v_grace:
                self.p.msg.m('Your religion prohibits eating pills.')
                return item

            if item.bonus < 0:
                self.p.msg.m('Your heart starts palpitating!', True)
                self.tired().x = min(-2.9, self.tired().x)
            else:
                n = self.tired().x - (-2.9)

                if n <= 0:
                    self.p.msg.m('Nothing happens.')
                else:
                    self.p.msg.m('Wow, what a kick!')
                    self.sleep().inc(n)
                    self.tired().dec(n)

            self.p.achievements.use(item)
            return None

        elif item.homing:
            d = xy_dist(self.d.pc, self.d.exit)

            if d > 30:
                self.p.msg.m('Cold as ice!')
            elif d > 20:
                self.p.msg.m('Very cold!')
            elif d > 15:
                self.p.msg.m('Cold!')
            elif d > 10:
                self.p.msg.m('Getting warmer...')
            elif d > 5:
                self.p.msg.m('Warm and getting warmer!')
            elif d > 3:
                self.p.msg.m("This thing is buring!")
            else:
                self.p.msg.m('You are at the spot. Look around.')

            self.p.achievements.use(item)

        elif item.sounding:
            k = draw_window(['Check in which direction?'], True)

            s = None
            if k == 'h': s = (-1, 0)
            elif k == 'j': s = (0, 1)
            elif k == 'k': s = (0, -1)
            elif k == 'l': s = (1, 0)
            else:
                return -1 #item

            n = 0
            xy = self.d.pc
            while not xy_out_wh(xy, self.d.w, self.d.h):
                xy = xy_add(xy, s)
                if dg.grid_is_walk(xy[0], xy[1]):
                    break
                n += 1

            draw_window(['Rock depth: ' + str(n)])
            self.p.achievements.use(item)

        elif item.detector:
            s = []
            if item.detect_monsters:
                s.append('You detect the following monsters:')
                s.extend(sorted('  '+str(v) for v in self.d.monmap.itervalues()))
                s.append('')

            if item.detect_items:
                s.append('You detect the following items:')
                s.extend(sorted('  '+str(vv) for v in self.d.itemap.itervalues() for vv in v))
                s.append('')

            if len(s) > 19:
                s = s[:19]
                s.append('(There is more information, but it does not fit on the screen)')

            draw_window(s)
            self.p.achievements.use(item)

        elif item.cooling:
            self.p.cooling = max(int(dg.random_gauss(*self.w.coef.coolingduration)), 1)
            self.p.msg.m("You cover yourself in cold mud.")

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
                for y in xrange(self.d.h):
                    dg.render_set_is_lit(x, y, True)

            self.p.achievements.use(item)
            return None

        elif item.jinni:
            l = []
            for ki in self.d.neighbors[self.d.pc]:
                if dg.grid_is_walk(ki[0], ki[1]) and ki not in self.d.monmap:
                    l.append(ki)

            if len(l) == 0:
                self.p.msg.m('Nothing happened.')
                return None

            jinni = Monster('Jinni', level=self.p.plev+1,
                            attack=self.d.dlev*0.1,
                            defence=self.d.dlev*0.2,
                            range=max(self.d.dlev-1, 1),
                            skin=('&', libtcod.yellow),
                            desc=['A supernatural fire fiend.'])

            self.p.msg.m('A malevolent spirit appears!')
            q = l[dg.random_n(len(l))]
            jinni.items = [self.w.itemstock.get('wishing')]
            self.place_monster(q, jinni)

            self.p.achievements.use(item)
            return None

        elif item.digray:
            if item.digray[0] == 1:
                for x in xrange(0, self.d.w):
                    self.convert_to_floor((x, self.d.pc[1]), False)
            if item.digray[1] == 1:
                for y in xrange(0, self.d.h):
                    self.convert_to_floor((self.d.pc[0], y), False)
            self.p.msg.m('The wand explodes in a brilliant white flash!')

            self.p.achievements.use(item)
            return None

        elif item.jumprange:
            xy = self.find_blink_targ(self.d.pc, item.jumprange)
            self.d.pc = xy

            self.p.achievements.use(item)

            if item.count is None:
                return item
            return None

        elif item.makestrap:
            if self.d.pc in self.d.featmap:
                self.p.msg.m('Nothing happens.')
                return item

            if dg.grid_is_water(self.d.pc[0], self.d.pc[1]):
                self.p.msg.m("That won't work while you're standing on water.")
                return item

            self.set_feature(self.d.pc, '^')
            self.p.msg.m('You spread the glue liberally on the floor.')

            self.p.achievements.use(item)

            if item.count is None:
                return item
            return None

        elif item.ebola:
            self.p.msg.m('The Ebola virus is unleashed!')
            self.paste_celauto(self.d.pc, self.celautostock.EBOLA)
            self.p.achievements.use(item)
            return None

        elif item.smoke:
            self.paste_celauto(self.d.pc, self.celautostock.SMOKE)
            self.p.achievements.use(item)
            return item

        elif item.trapcloud:
            self.p.msg.m('You set the nanobots to work.')
            self.paste_celauto(self.d.pc, self.celautostock.TRAPMAKER)

            self.p.achievements.use(item)

            if item.count is None:
                return item
            return None

        elif item.airfreshener:
            if item.ammo == 0:
                self.p.msg.m("It's out of ammo!")
                return item

            self.airfreshen(self.d.pc, item.airfreshener)
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
            self.summon(self.d.pc, item.summon[0], item.summon[1])
            self.p.achievements.use(item)
            return None

        elif item.switch_moon:
            self.d.moon = item.switch_moon
            self.regen(self.d.w, self.d.h)
            self.p.achievements.use(item)
            self.p.msg.m('The local space-time continuum shifts slightly.', True)
            return None

        elif item.doppel:
            self.d.doppelpoint = self.d.pc
            self.d.doppeltime = item.doppel
            self.p.achievements.use(item)
            self.p.msg.m('You activate the doppelganger.')
            return None

        elif item.winning:
            self.victory(msg=item.winning)
            return None
                    
        elif item.rangeattack or item.rangeexplode or item.fires:
            if item.ammo == 0:
                self.p.msg.m("It's out of ammo!")
                return item

            while 1:
                nxy = self.target(item.range[1],
                                  minrange=item.range[0],
                                  monstop=item.straightline,
                                  lightradius=item.lightradius)
                if not xy_none(nxy):
                    break
            if nxy[0] < 0:
                return -1 #item

            if not item.rangeexplode and not item.fires and nxy not in self.d.monmap:
                return -1 #item

            dg.render_draw_line(self.d.pc[0], self.d.pc[1], nxy[0], nxy[1], 
                                (libtcod.gray, libtcod.darkest_gray), 
                                lambda x, y: True)

            if item.ammo > 0:
                item.ammo -= 1

            if item.rangeexplode:
                self.explode(nxy, item.radius)
            elif item.fires:
                self.seed_celauto(nxy, self.celautostock.FIRE)
                self.set_feature(nxy, '"')
            else:
                self.fight(self.d.monmap[nxy], True, item=item)

            self.p.achievements.use(item)

            if item.ammo == 0:
                return None


        return item


    def descend(self):

        ss = self.try_feature(self.d.pc, 'stairs')
        if not ss:
            self.p.msg.m('You can\'t descend, there is no hole here.')
            return

        self.p.msg.m('You climb down the hole.')
        self.d.dlev += ss

        b = self.try_feature(self.d.pc, 'branch')
        if b:
            self.d.branch = b

        # Quests
        quest = self.w.queststock.get(b)

        if quest:
            self.d.dlev = quest.dlevels[0]

        if self.d.dlev >= 26:
            self.victory()
            return

        self.regen(self.d.w, self.d.h)
        self.tick()
        self.p.achievements.descend(self.p.plev, self.d.dlev, self.d.branch)

        if self.config.music_n >= 0:
            self.config.sound.set(self.config.music_n, rate=min(10, 2.0+(0.5*self.d.dlev)))


    def drop(self):
        slot = self.showinv()
        i = self.p.inv.drop(slot)
        if not i:
            if slot in 'abcdefghi':
                self.p.msg.m('There is no item in that slot.')
            return

        self.p.msg.m('You drop ' + str(i) +'.')
        self.set_item(self.d.pc, [i])
        self.tick()


    def apply_from_ground_aux(self, i, pc):

        def _purge():
            # The item might be deleted already by the time we get here.
            if pc not in self.d.itemap:
                return

            for ix in xrange(len(self.d.itemap[pc])):
                if id(self.d.itemap[pc][ix]) == id(i):

                    self.delete_item(self.d.itemap[pc], ix, pc)
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
            self.set_item(pc, [i2])

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

        c = draw_window(s)
        c = ord(c) - 97

        if c < 0 or c >= len(items):
            return None, None

        i = items[c]
        return i, c

    def ground_apply(self):
        pc = self.d.pc

        if pc not in self.d.itemap:
            self.p.msg.m('There is no item here to apply.')
            return

        items = self.d.itemap[pc]
        items = [i for i in items if i.applies]

        if len(items) == 0:
            self.p.msg.m('There is no item here to apply.')
            return

        i,c = self.pick_one_item(items)
        if not i:
            return

        self.apply_from_ground_aux(i, pc)


    def filter_items(self, xy, func, ret):
        if xy not in self.d.itemap:
            return

        i2 = []
        for i in self.d.itemap[xy]:
            q1,q2 = func(i)
            if q1:
                if ret is not None:
                    ret.append((xy,q2))
            else:
                i2.append(i)

        if len(i2) > 0:
            self.d.itemap[xy] = i2
        else:
            del self.d.itemap[xy]



    def victory(self, msg=None):
        while 1:
            c = draw_window(['Congratulations! You have won the game.', '', 'Press space to exit.'])
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
            self.p.msg.m('You just gained level ' + str(mon.level) + '!', True)
            self.p.plev = mon.level

        if do_drop:
            itemdrop = mon.items

            # HACK
            is_noncorpse = False
            if mon.flavor in ('digital', 'air', 'robot') or mon.boulder:
                is_noncorpse = True

            if self.try_feature(mon.xy, 'special') == 'cthulhu' and not is_noncorpse:
                # HACK HACK!
                itm = self.w.itemstock.get(['cthulhu_o1', 'cthulhu_o2', 'cthulhu_o3'][dg.random_n(3)])
                if itm:
                    itemdrop = [itm]

            elif self.d.moon == moon.NEW and not mon.itemdrop and not is_noncorpse:
                corpse = self.w.itemstock.get('corpse')
                corpse.corpse = mon
                itemdrop = itemdrop[:]
                itemdrop.append(corpse)

            if len(itemdrop) > 0:
                self.set_item(mon.xy, itemdrop)

        winner, exting = self.w.monsterstock.death(mon, self.d.moon)

        if exting:
            self.p.achievements.mondone()

        # Quests
        quest = self.w.queststock.get(self.d.branch)

        if quest and sum(1 for m in self.d.monmap.itervalues() if not m.inanimate) == 1:

            questdone = (quest.dlevels[1] == self.d.dlev)

            for msg in quest.messages[self.d.dlev]:
                self.p.msg.m(msg, True)

            if questdone:
                self.p.achievements.questdone(self.d.branch)
            else:
                self.set_feature(mon.xy, '>')

            qis = []
            for g in quest.gifts[self.d.dlev]:
                if g:
                    i = self.w.itemstock.get(g)
                else:
                    i = self.w.itemstock.generate(self.d.dlev)
                if i:
                    qis.append(i)

            self.set_item(mon.xy, qis)

            return

        if winner:
            self.victory()


    def rayblast(self, xy0, rad):

        x0, y0 = xy0

        def func(x, y):
            xy = (x, y)

            if xy == self.d.pc:
                if not self.get_radimmune():
                    self.health().dec(self.w.coef.raddamage, "radiation", self.config.sound)

            if xy in self.d.monmap:
                mon = self.d.monmap[xy]
                if not mon.radimmune:
                    mon.hp -= self.w.coef.raddamage
                    if mon.hp <= -3.0:
                        self.handle_mondeath(mon, is_rad=True)
                        self.remove_monster(mon)

        dg.render_draw_fov_circle(x0, y0, rad, (libtcod.light_azure, libtcod.darkest_blue), func)


    def explode(self, xy0, rad):

        chains = set()

        def f_explod(xy):
            if xy == self.d.pc:
                if not self.get_explodeimmune():
                    self.health().dec(6.0, "explosion", self.config.sound)
                    self.p.dead = True

            if xy in self.d.itemap:
                for i in self.d.itemap[xy]:
                    if i.explodes:
                        chains.add((xy, i.radius, True))
                        break
                del self.d.itemap[xy]

            if xy in self.d.monmap:
                mon = self.d.monmap[xy]
                if not mon.explodeimmune:
                    self.handle_mondeath(mon, do_drop=False, is_explode=True)

                    for i in mon.items:
                        if i.explodes:
                            chains.add((xy, i.radius, True))
                            break

                    self.remove_monster(mon)


        def func_ff(x, y):
            xy = (x, y)
            f_explod(xy)

            is_gas = False
            if self.try_feature(xy, 'explode'):
                is_gas = True

            self.set_feature(xy, None)
            return is_gas


        def func_r(x, y):
            xy = (x, y)
            f_explod(xy)

            if self.try_feature(xy, 'explode'):
                dg.render_draw_floodfill(x, y, (libtcod.yellow, libtcod.darkest_red), func_ff)

            self.convert_to_floor(xy, (dg.random_range(0, 5) == 0))


        dg.render_draw_circle(xy0[0], xy0[1], rad, (libtcod.yellow, libtcod.darkest_red), func_r)

        for xy, r, d in sorted(chains):
            self.explode(xy, r)



    def airfreshen(self, xy0, rad):

        x0, y0 = xy0

        def func(x, y):
            self.clear_celauto((x,y))

        dg.render_draw_fov_circle(x0, y0, rad, (libtcod.yellow, libtcod.darkest_blue), func)

    def raise_dead(self, xy0, rad):

        x0, y0 = xy0

        ret = []

        def func(x, y):
            self.filter_items((x, y), lambda i: (i.corpse, i.corpse), ret)

        dg.render_draw_fov_circle(x0, y0, rad, None, func)
        return ret


    def fight(self, mon, player_move, item=None):

        sm = str(mon)
        smu = sm[0].upper() + sm[1:]

        ##

        if mon.boulder:
            if player_move:
                mon.bld_delta = xy_sub(mon.xy, self.d.pc)

                if mon.bld_delta[0] < -1: mon.bld_delta = (-1, mon.bld_delta[1])
                elif mon.bld_delta[0] > 1: mon.bld_delta = (1, mon.bld_delta[1])
                if mon.bld_delta[1] < -1: mon.bld_delta = (mon.bld_delta[0], -1)
                elif mon.bld_delta[1] > 1: mon.bld_delta = (mon.bld_delta[0], 1)

                self.p.msg.m('You push ' + sm)
                return
            else:
                self.health().dec(6, sm, self.config.sound)
                self.p.msg.m('You got squashed. What a silly way to die!')
                self.p.dead = True
                return

        ##

        d = xy_dist(mon.xy, self.d.pc)
        d = int(round(d))

        if player_move and item:
            plev = min(max(self.p.plev - d + 1, 1), self.p.plev)
            attack = item.rangeattack
            #log.log('+', d, plev, attack)

        else:
            if self.p.b_grace and player_move:
                self.p.msg.m('Your religion prohibits you from fighting.')
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
                defence /= self.w.coef.gluedefencepenalty

            dmg = roll(attack, plev, defence, mon.level)

            mon.hp -= dmg

            if dmg > 0:
                m = max(0.1, min(1.0, dmg/3))
                self.config.sound.play("klang1", mul=m)

            if mon.hp <= -3.0:
                if mon.visible or mon.visible_old:
                    self.p.msg.m('You killed ' + sm + '!')
                self.handle_mondeath(mon)
                self.remove_monster(mon)
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
                        self.p.msg.m(smu + ' looks totally dazed!')
                    mon.confused += int(max(dg.random_gauss(*ca), 1))

                if fires and dmg > 0 and not mon.fireimmune:
                    mon.onfire = max(self.w.coef.burnduration, mon.onfire)

                if not (mon.visible or mon.visible_old):
                    pass

                elif dmg > 4:
                    self.p.msg.m('You mortally wound ' + sm + '!')
                elif dmg > 2:
                    self.p.msg.m('You seriously wound ' + sm + '.')
                elif dmg > 0.5:
                    self.p.msg.m('You wound ' + sm + '.')
                elif dmg > 0:
                    self.p.msg.m('You barely wound ' + sm + '.')
                else:
                    self.p.msg.m('You miss ' + sm + '.')

            if dmg > 0 and (mon.visible or mon.visible_old):
                mon.known_pxy = self.d.pc


        else:

            attack = None
            defence = None
            psy = False

            if d > 1 and mon.psyattack > 0:
                if self.get_psyimmune():
                    return
                attack = mon.psyattack
                defence = self.w.coef.unarmeddefence
                psy = True
            else:
                attack = mon.attack
                defence = self.get_defence()

            if attack == 0:
                return

            dmg = roll(attack, mon.level, defence, plev)

            if psy:
                if dmg > 0:
                    self.p.msg.m(smu + ' is attacking your brain!')
            else:
                if dmg > 0:
                    self.p.msg.m(smu + ' hits!')
                else:
                    self.p.msg.m(smu + ' misses.')

            if mon.sleepattack:
                if dmg > 0:
                    self.p.msg.m('You fall asleep!')
                    self.start_sleep(force=True, quick=True, realforced=True)

            elif mon.bloodsucker:
                if dmg > 0:
                    self.p.msg.m('You feel weak!')
                    self.hunger().dec(mon.bloodsucker[0])
                    self.health().dec(mon.bloodsucker[0], sm, self.config.sound)
                    mon.fleetimeout = mon.bloodsucker[1]

            elif mon.hungerattack:
                self.hunger().dec(dmg)

            else:
                self.health().dec(dmg, sm, self.config.sound)

            if self.p.resting:
                self.p.msg.m('You stop resting.')
                self.p.resting = False

            if self.p.digging:
                self.p.msg.m('You stop digging.')
                self.p.digging = None

            if self.p.sleeping and not self.p.forced2sleep:
                self.p.sleeping = 0
                self.p.forcedsleep = False
                self.p.healingsleep = False

            if self.health().x <= -3.0:
                self.p.dead = True


    def look(self):
        txy = self.d.pc

        while 1:
            seen = self.draw(txy)

            s = []

            if txy == self.d.pc:
                s.append('This is you.')
                s.append('')

            if not seen:
                s.append('You see nothing.')

            else:
                if txy in self.d.monmap:
                    m = self.d.monmap[txy]
                    s.append('You see ' + str(m) + ':')
                    s.append('')
                    s.extend(m.desc)
                    s.append('')

                if txy in self.d.itemap:
                    i = self.d.itemap[txy]
                    s.append('You see the following items:')
                    for ix in xrange(len(i)):
                        if ix > 5:
                            s.append('(And some other items)')
                            break
                        s.append(str(i[ix]))
                    s.append('')

                if txy in self.d.featmap:
                    f = self.d.featmap[txy]
                    s.append('You see ' + f.name + '.')

                elif dg.grid_is_walk(txy[0], txy[1]):
                    if dg.grid_is_water(txy[0], txy[1]):
                        s.append('You see a water-covered floor.')
                    else:
                        s.append('You see a cave floor.')

                else:
                        s.append('You see a cave wall.')

            k = draw_window(s, True)

            if   k == 'h': txy = xy_add(txy, (-1, 0))
            elif k == 'j': txy = xy_add(txy, (0, 1))
            elif k == 'k': txy = xy_add(txy, (0, -1))
            elif k == 'l': txy = xy_add(txy, (1, 0))
            elif k == 'y': txy = xy_add(txy, (-1, -1))
            elif k == 'u': txy = xy_add(txy, (1, -1))
            elif k == 'b': txy = xy_add(txy, (-1, 1))
            elif k == 'n': txy = xy_add(txy, (1, 1))
            else:
                break

            txy = (max(0, min(txy[0], self.d.w - 1)),
                   max(0, min(txy[1], self.d.h - 1)))



    def _target(self, point, range, firstcall, minrange=0, monstop=False, lightradius=None):

        self.draw(range=(minrange, range), lightradius=lightradius)

        #monx = None
        #mony = None

        if xy_none(point) and firstcall:
            for i in xrange(len(self.monsters_in_view)):
                mon = self.monsters_in_view[i]
                d = xy_dist(self.d.pc, mon.xy)

                if d > range:
                    continue

                if d < minrange:
                    continue

                #log.log(" # ok")
                #monx = mon.x
                #mony = mon.y
                point = mon.xy

                del self.monsters_in_view[i]
                self.monsters_in_view.append(mon)
                break

        tmsg = ['Pick a target.  '
                "HJKL YUBN for directions, "
                "<space> to choose and '.' to fire."]

        if not xy_none(point):
            self.draw(point, range=(minrange, range), 
                      lightradius=lightradius)
            if point[1] <= 2:
                tmsg = []

        k = draw_window(tmsg, True)

        #poiok = (not xy_none(point))
        final_choice = False
                           
        
        dpt = None

        if k == 'h':   dpt = (-1, 0)
        elif k == 'j': dpt = (0, 1)
        elif k == 'k': dpt = (0, -1)
        elif k == 'l': dpt = (1, 0)
        elif k == 'y': dpt = (-1, -1)
        elif k == 'u': dpt = (1, -1)
        elif k == 'b': dpt = (-1, 1)
        elif k == 'n': dpt = (1, 1)
        elif k == '.':
            if xy_none(point):
                return (None, None), False, False
            else:
                final_choice = True
        elif k == ' ':
            return (None, None), False, True
        else:
            return (-1, -1), True, True

        if dpt:
            if not xy_none(point):
                point = xy_add(point, dpt)
            else:
                if dpt[0] == 0 or dpt[1] == 0:
                    dpt = (dpt[0] * range, dpt[1] * range)
                else:
                    dpt = (dpt[0] * int(range * 0.71), dpt[1] * int(range * 0.71))
                point = xy_add(self.d.pc, dpt)

            point = (max(0, min(point[0], self.d.w - 1)),
                     max(0, min(point[1], self.d.h - 1)))



        xxyy = [None, None]

        def check_target(x, y, ptref=xxyy):
            if dg.grid_is_walk(x, y) or self.try_feature((x, y), 'shootable'):

                if minrange > 0:
                    d = xy_dist((x, y), self.d.pc)
                    if d < minrange:
                        return True

                ptref[0] = x
                ptref[1] = y

                if monstop and (x, y) in self.d.monmap:
                    return False
                return True

            else:
                return False

        dg.render_draw_line(self.d.pc[0], self.d.pc[1], point[0], point[1], 
                            None, check_target)

        xxyy = (xxyy[0], xxyy[1])

        if final_choice and xxyy == point:
            return xxyy, True, False
        return xxyy, False, False



    def target(self, range, minrange=0, monstop=False, lightradius=None):

        point = (None, None)
        firstcall = True
        while 1:
            point, ok, firstcall = self._target(point, range, firstcall,
                                                minrange=minrange, 
                                                monstop=monstop, 
                                                lightradius=lightradius)

            if ok:
                return point



    def show_messages(self):
        self.p.msg.show_all()


    def wish(self, msg=None):
        s = ''
        while 1:
            if msg:
                k = draw_window([msg, '', 'Wish for what? : ' + s])
            else:
                k = draw_window(['Wish for what? : ' + s])

            k = k.lower()
            if k in "abcdefghijklmnopqrstuvwxyz' -":
                s = s + k
            elif ord(k) == 8 or ord(k) == 127:
                if len(s) > 0:
                    s = s[:-1]
            elif k in '\r\n':
                break

        i = self.w.itemstock.find(s)

        self.p.achievements.wish()

        if not i:
            self.p.msg.m('Nothing happened!')
        else:
            self.p.msg.m('Suddenly, ' + str(i) + ' appears at your feet!')
            self.set_item(self.d.pc, [i])


    def move_down(self): self.move((0, 1))
    def move_up(self): self.move((0, -1))
    def move_left(self): self.move((-1, 0))
    def move_right(self): self.move((1, 0))
    def move_upleft(self): self.move((-1, -1))
    def move_upright(self): self.move((1, -1))
    def move_downleft(self): self.move((-1, 1))
    def move_downright(self): self.move((1, 1))



    def quit(self):
        k = draw_window(["Really quit? Press 'y' if you are truly sure."])
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
        draw_window(s)

    def walk_monster(self, mon, dist, xy):

        if mon.moldspew and (self.w.t % mon.moldspew[2]) == 0:
            for ki in self.d.neighbors[xy]:
                if dg.random_range(1, mon.moldspew[1]) == 1:
                    self.seed_celauto(ki, mon.moldspew[0])

        if mon.static:
            return (None, None)

        if mon.slow and (self.w.t & 1) == 0:
            return (None, None)

        if mon.glued > 0:
            mon.glued -= 1
            if mon.glued == 0:
                if self.try_feature(xy, 'sticky'):
                    self.unset_feature(xy)
            else:
                return (None, None)

        if mon.boulder:
            if mon.bld_delta:
                ret = xy_add(xy, mon.bld_delta)

                if not dg.grid_is_walk(ret[0], ret[1]):
                    mon.bld_delta = None
                    return (None, None)
                else:
                    return ret
            else:
                return (None, None)

        rang = self.get_camorange(mon.range)

        if self.try_feature(xy, 'confuse'):
            rang = 1

        if dist > rang or mon.confused or (mon.sleepattack and self.p.sleeping):
            mdxy = xy_add(xy, 
                          (dg.random_range(-1, 1), 
                           dg.random_range(-1, 1)))

            if not dg.grid_is_walk(mdxy[0], mdxy[1]):
                mdxy = (None, None)
            if mon.confused:
                mon.confused -= 1

        else:

            if mon.psyrange > 0 and dist <= mon.psyrange:
                self.fight(mon, False)

            repelrange = self.get_repelrange()

            if repelrange and dist <= repelrange and dist > 1:
                 return (None, None)

            if mon.heatseeking:
                if (dg.grid_is_water(self.d.pc[0], self.d.pc[1]) or self.p.cooling or mon.onfire):
                    if xy_none(mon.known_pxy):
                        mon.known_pxy = mon.xy
                else:
                    mon.known_pxy = self.d.pc
            else:
                if self.d.doppeltime > 0:
                    mon.known_pxy = self.d.doppelpoint
                else:
                    mon.known_pxy = self.d.pc

            if mon.straightline:

                tmp = [xy[0], xy[1]]
                def line_once(x, y, ref=tmp):
                    tmp[0] = x
                    tmp[1] = y
                    if tmp[0] != xy[0] or tmp[1] != xy[1]:
                        return False
                    return True

                dg.render_draw_line(xy[0], xy[1], mon.known_pxy[0], mon.known_pxy[1], None, line_once)
                mdxy = (tmp[0], tmp[1])

            else:

                flee = False

                if mon.blink_away and dist < 2.0:
                    mdxy = self.find_blink_targ(xy, mon.blink_away)
                    return mdxy

                elif mon.fleerange and dist <= mon.fleerange:
                    if math.fabs(dist - mon.fleerange) < 0.9:
                        return (None, None)
                    flee = True

                elif mon.fleetimeout > 0 and dist <= mon.range - 2:
                    flee = True
                    mon.fleetimeout -= 1

                if flee:
                    mdxy = (None, None)
                    for _xy in self.d.neighbors[xy]:
                        if dg.grid_is_walk(_xy[0], _xy[1]) and \
                           ((mon.known_pxy[0] >= xy[0] and _xy[0] < xy[0]) or \
                            (mon.known_pxy[0] <= xy[0] and _xy[0] > xy[0]) or \
                            (mon.known_pxy[1] <= xy[1] and _xy[1] > xy[1]) or \
                            (mon.known_pxy[1] >= xy[1] and _xy[1] < xy[1])):
                            mdxy = _xy
                            break

                else:
                    mdxy = dg.render_path_walk(xy[0], xy[1], 
                                               mon.known_pxy[0], mon.known_pxy[1], 
                                               2 if mon.fast else 1,
                                               rang*2)
                    
                    if xy_none(mdxy):
                        mdxy = xy_add(xy, (dg.random_range(-1, 1),
                                           dg.random_range(-1, 1)))

                        if not dg.grid_is_walk(mdxy[0], mdxy[1]):
                            mdxy = (None, None)


        if mon.stoneeating:
            if not xy_none(mdxy):
                if self.try_feature(mdxy, 'permanent'):
                    return (None, None)

                if not dg.grid_is_walk(mdxy[0], mdxy[1]):
                    self.convert_to_floor(mdxy, True)

        return mdxy

    def process_monstep(self, mon):
        mdxy = mon.xy

        if self.try_feature(mdxy, 'sticky') and not mon.flying:
            if mon.visible or mon.visible_old:
                mn = str(mon)
                mn = mn[0].upper() + mn[1:]
                self.p.msg.m(mn + ' gets stuck in some glue!')
            mon.glued = max(int(dg.random_gauss(*self.w.coef.glueduration)), 1)


    def monster_conflict(self, mon_attack, mon_defend):
        if mon_attack.boulder:
            if mon_defend.large:
                mon_attack.bld_delta = None
            else:
                if mon_defend.visible or mon_defend.visible_old:
                    sm = str(mon_attack)
                    smu = sm[0].upper() + sm[1:]
                    self.p.msg.m(smu + ' squashes ' + str(mon_defend) + '!')
                return True

        return False

    def summon(self, xy, monname, n):
        if monname is None:
            m = []
            for ii in xrange(n):
                mmi = self.w.monsterstock.generate(self.d.branch, self.d.dlev, self.w.itemstock, self.d.moon)
                if mmi and not mmi.inanimate:
                    m.append(mmi)

        else:
            m = self.w.monsterstock.find(monname, n, self.w.itemstock)
            if len(m) == 0:
                return []

        l = []
        for ki in self.d.neighbors[xy]:
            if dg.grid_is_walk(ki[0], ki[1]) and ki not in self.d.monmap and ki != self.d.pc:
                l.append(ki)

        ret = []
        for i in xrange(len(m)):
            if len(l) == 0:
                return ret
            j = dg.random_n(len(l))
            xxyy = l[j]
            del l[j]

            self.place_monster(xxyy, m[i])
            ret.append(m[i])

        return ret


    def moon_message(self):
        if self.p.did_moon_message:
            return

        if self.w.t - self.p.msg.last_msg_t > 9:
            d = {moon.NEW:  'New moon tonight. A perfect night for evil and the dark arts.',
                 moon.FULL: 'Full moon tonight. The lunatics are out in droves.',
                 moon.FIRST_QUARTER: 'First quarter moon tonight. Watch out for the UFOs.',
                 moon.LAST_QUARTER: 'Last quarter moon tonight. Watch out for the UFOs.',
                 moon.WAXING_CRESCENT: "Tonight's moon is waxing crescent.",
                 moon.WAXING_GIBBOUS: "Tonight's moon is waxing gibbous.",
                 moon.WANING_CRESCENT: "Tonight's moon is waning crescent.",
                 moon.WANING_GIBBOUS: "Tonight's moon is waning gibbous."}

            self.p.msg.m(d[self.d.moon], True)
            self.p.did_moon_message = True


    def monster_flavor_message(self, mon, dist):
        def msg(flavor, dist):
            m = max(0.1, min(1.0, 1.0 - (dist/50)))

            if flavor == 'air':
                self.p.msg.m('You hear the hissing of air.')
                self.config.sound.play("air", mul=m)

            elif flavor == 'animal':
                self.p.msg.m('You hear the sounds of a restless animal.')
                self.config.sound.play("hooves", mul=m)

            elif flavor == 'carnivore':
                self.p.msg.m('You hear the roar of an animal.')
                self.config.sound.play("roar", mul=m)

            elif flavor == 'digital':
                self.p.msg.m('You hear the sounds of 8-bit music.')
                self.config.sound.play("nintendo", mul=m)

            elif flavor == 'earthshake':
                self.p.msg.m('You feel the earth shake.')
                self.config.sound.play("quake", mul=m)

            elif flavor == 'faerie':
                self.p.msg.m('You hear the tinkling of bells.')
                self.config.sound.play("bells", mul=m)

            elif flavor == 'flying':
                self.p.msg.m('You hear the flapping of wings.')
                self.config.sound.play("wings", mul=m)

            elif flavor == 'giant':
                self.p.msg.m('You hear a loud rumble.')
                self.config.sound.play("boom", mul=m)

            elif flavor == 'humanwarrior':
                self.p.msg.m('You hear the angry sounds of a foreign language.')
                self.config.sound.play("mutter", mul=m)

            elif flavor == 'humanweird':
                self.p.msg.m('You hear somebody wildly gibber.')
                self.config.sound.play("laugh", mul=m)

            elif flavor == 'robot':
                self.p.msg.m('You hear the clanking of metal.')
                self.config.sound.play("robot", mul=m)

            elif flavor == 'snake':
                self.p.msg.m('You hear something slither.')
                self.config.sound.play("slither", mul=m)

            elif flavor == 'weird':
                self.p.msg.m('You faintly sense eldritch chanting.')
                self.config.sound.play("cthulhu", mul=m)

            elif flavor == 'wizard':
                self.p.msg.m('You hear incantations of arcana.')
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


    def paste_celauto(self, xy, ca):
        self.celautostock.paste(xy, self.d.w, self.d.h, ca)

    def seed_celauto(self, xy, ca):
        self.celautostock.seed(xy, ca)

    def clear_celauto(self, xy):
        def cboff(x, y, ca):
            self.celauto_off((x, y), ca)
        self.celautostock.clear(xy, cboff)
        


    def celauto_on(self, xy, ca):
        x, y = xy

        ca = self.celautostock.stock[ca]

        if ca.watertoggle is not None:
            dg.grid_set_water(x, y, True)
        elif ca.featuretoggle:
            if xy not in self.d.featmap and dg.grid_is_walk(x, y):
                self.set_feature(xy, ca.featuretoggle)
        elif ca.floorfeaturetoggle:
            if xy not in self.d.featmap and dg.grid_is_walk(x, y) and not dg.grid_is_water(x, y):
                self.set_feature(xy, ca.floorfeaturetoggle)

        if ca.littoggle is not None and dg.grid_is_walk(x, y):
            dg.render_set_is_lit(x, y, True)

    def celauto_off(self, xy, ca):
        x, y = xy

        ca = self.celautostock.stock[ca]

        if ca.watertoggle is not None:
            dg.grid_set_water(x, y, False)
        elif ca.featuretoggle and xy in self.d.featmap and self.d.featmap[xy] == self.w.featstock.f[ca.featuretoggle]:
            self.unset_feature(xy)

        if ca.littoggle is not None and dg.grid_is_walk(x, y):
            dg.render_set_is_lit(x, y, False)


    def process_world(self):

        def cbon(x, y, ca):
            self.celauto_on((x,y),ca)

        def cboff(x, y, ca):
            self.celauto_off((x,y),ca)

        self.celautostock.celauto_step(cbon, cboff)

        explodes = set()
        mons = []
        delitems = []
        rblasts = []

        for k,v in sorted(self.d.itemap.iteritems()):
            for i in v:
                if i.liveexplode > 0:
                    i.liveexplode -= 1
                    if i.liveexplode == 0:
                        if i.summon:
                            self.summon(k, i.summon[0], i.summon[1])
                        elif i.radexplode:
                            rblasts.append((k, i.radius))
                        elif i.swampgas:
                            self.paste_celauto(self.d.pc, self.celautostock.SWAMPGAS)
                        else:
                            explodes.add((k, i.radius))

                        delitems.append(k)

        for xy,r in rblasts:
            self.rayblast(xy, r)

        for ixy in delitems:
            self.filter_items(ixy, lambda i: (i.liveexplode == 0, None), None)

        summons = []
        raise_dead = []

        for xy,mon in sorted(self.d.monmap.iteritems()):
            #log.log('  tick:', k)

            x, y = xy
            if mon.static:
                dist = 0
            else:
                dist = xy_dist(self.d.pc, xy)

            mon.do_move = None

            if mon.static:
                pass

            elif (mon.visible or mon.visible_old) and not (mon.was_seen) and not self.p.mapping:
                mon.was_seen = True
                self.p.msg.m('You see ' + str(mon) + '.')
                m = max(0.25, min(3, 0.5 * (mon.level - self.p.plev)))
                self.config.sound.play("wobble", dur=m)

            elif not mon.visible:
                self.monster_flavor_message(mon, dist)


            p = self.try_feature(xy, 'poison')
            if p and not mon.poisimmune:
                mon.hp -= p
                if mon.hp <= -3.0:
                    if mon.visible:
                        smu = str(mon)
                        smu = smu[0].upper() + smu[1:]
                        self.p.msg.m(smu + ' falls over and dies!')

                    self.handle_mondeath(mon, do_gain=False, 
                                         is_poison=(False if self.try_feature(xy, 'pois2') else True))
                    mon.do_die = True
                    mons.append(mon)
                    continue

            p = self.try_feature(xy, 'fire')
            if (p or mon.onfire) and not mon.fireimmune:
                mon.hp -= (p or self.w.coef.burndamage)
                if mon.hp <= -3.0:
                    if mon.visible:
                        smu = str(mon)
                        smu = smu[0].upper() + smu[1:]
                        self.p.msg.m(smu + ' burns ' + ('up.' if mon.boulder else 'to death!'))

                    self.handle_mondeath(mon, do_gain=True)
                    mon.do_die = True
                    mons.append(mon)
                    continue

                elif p:
                    mon.onfire = max(self.w.coef.burnduration, mon.onfire)

                else:
                    mon.onfire -= 1
                    self.seed_celauto(xy, self.celautostock.FIRE)
                    self.set_feature(xy, '"')



            msumm = (mon.summon or mon.summononce)

            if msumm and (mon.visible or mon.static) and (self.w.t % msumm[1]) == 0:
                summons.append((xy, mon))
                continue

            if mon.raise_dead and (mon.visible or mon.static) and (self.w.t % mon.raise_dead[1]) == 0:
                raise_dead.extend(self.raise_dead(mon.xy, mon.raise_dead[0]))

            mon.visible_old = mon.visible
            mon.visible = False

            mdxy = self.walk_monster(mon, dist, xy)

            if not xy_none(mdxy):
                if mdxy == self.d.pc:
                    if mon.selfdestruct:
                        smu = str(mon)
                        smu = smu[0].upper() + smu[1:]
                        self.p.msg.m(smu + ' suddenly self-destructs!')
                        self.handle_mondeath(mon, do_gain=False)
                        mon.do_die = True
                    else:
                        self.fight(mon, False)
                else:
                    mon.do_move = mdxy
                    
                    if mon.do_move in self.d.monmap:
                        mon2 = self.d.monmap[mon.do_move]
                        if self.monster_conflict(mon, mon2):
                            self.handle_mondeath(mon2)
                            mon2.do_die = True
                            mons.append(mon2)

                mons.append(mon)


        for k,mon in summons:
            smu = str(mon)
            smu = smu[0].upper() + smu[1:]

            if mon.summon:
                q = self.summon(k, mon.summon[0], 1)
                if len(q) > 0:
                    if not mon.static:
                        self.p.msg.m(smu + ' summons ' + str(q[0]) + '!')
                else:
                    mon.summon = None

            elif mon.summononce:
                q = self.summon(k, None, mon.summononce[0])
                if len(q) > 0:
                    self.p.msg.m(smu + ' summons monsters!')
                    mon.summononce = None



        for xy,mon in raise_dead:
            if dg.grid_is_walk(xy[0], xy[1]) and xy not in self.d.monmap and xy != self.d.pc:
                smu = str(mon)
                smu = smu[0].upper() + smu[1:]
                self.p.msg.m(smu + ' rises from the dead!')
                mon.reset()
                self.place_monster(xy, mon)

        for mon in mons:
            if mon.do_die:
                if mon.xy in self.d.monmap:
                    self.remove_monster(mon)
            elif mon.do_move:
                mon.old_pos = mon.xy
                self.remove_monster(mon)

        for mon in mons:
            if mon.do_die:
                continue

            elif mon.do_move:
                if mon.do_move in self.d.monmap:
                    mon.do_move = mon.old_pos

                self.place_monster(mon.do_move, mon)
                mon.do_move = None

                self.process_monstep(mon)

        for xy, r in sorted(explodes):
            self.explode(xy, r)



    def draw_hud(self):

        def do_sline(label, x):
            if x >= 2.0:    n = 3 
            elif x >= 1.0:  n = 2
            elif x >= 0.0:  n = 1
            elif x >= -1.0: n = -1
            elif x >= -2.0: n = -2
            else:           n = -3

            if x >= 1.5:    col = libtcod.darker_green
            elif x >= -0.5: col = libtcod.yellow
            else:           col = libtcod.red

            dg.render_push_hud_line(label, libtcod.white, True, n,
                                    (('-', col),
                                     ('+', col)))

        do_sline("Health", self.health().x)
        do_sline("Warmth", self.warmth().x)
        do_sline("Tired",  self.tired().x)
        do_sline("Sleep",  self.sleep().x)
        do_sline("Thirst", self.thirst().x)
        do_sline("Hunger", self.hunger().x)

        
        def do_rline(grace, duration, timeout, char):
            nt = (grace > duration - timeout)

            dg.render_push_hud_line(char+'Grace', 
                                    libtcod.white, 
                                    False, 
                                    ((grace * 6) / duration) + 1,
                                    ((chr(175), libtcod.red if nt else libtcod.yellow),
                                     (' ', libtcod.white)))

        if self.p.s_grace:
            do_rline(self.p.s_grace, self.w.coef.s_graceduration, self.w.coef.s_praytimeout, chr(234))

        elif self.p.v_grace:
            do_rline(self.p.v_grace, self.w.coef.v_graceduration, self.w.coef.v_praytimeout, chr(233))

        elif self.p.b_grace:
            do_rline(self.p.b_grace, self.w.coef.b_graceduration, 0, chr(127))


        if self.p.resource:
            if self.p.resource_timeout:
                n = ((self.p.resource_timeout * 6) / self.w.coef.resource_timeouts[self.p.resource] + 1)
            else:
                n = self.p.resource_buildup

            labels = {'r': ("   Red", libtcod.red),
                      'g': (" Green", libtcod.dark_green),
                      'y': ("Yellow", libtcod.yellow),
                      'b': ("  Blue", libtcod.blue),
                      'p': ("Purple", libtcod.purple) }

            label, labelcolor = labels[self.p.resource]

            dg.render_push_hud_line(label, labelcolor, False, n, 
                                    ((chr(175), labelcolor if self.p.resource_timeout else libtcod.white),
                                     (' ', libtcod.white)))

        dg.render_push_hud_line("Luck", libtcod.white, True, -2,
                                ((chr(18), libtcod.red),
                                 (chr(17), libtcod.yellow)))


    ### 

    def draw(self, _hlxy=(1000,1000), range=(0,1000), lightradius=None):

        withtime = False
        if self.w.oldt != self.w.t:
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
                    for y in xrange(self.d.h):
                        dg.render_set_is_lit(x, y, False)


        if withtime:
            self.process_world()

        do_m_i_v = False
        if withtime or self.monsters_in_view is None:
            do_m_i_v = True
            self.monsters_in_view = []

        # hack, after process_world because confusing features may be created
        if self.try_feature(self.d.pc, 'confuse'):
            lightradius = 1

        
        did_highlight = False

        telerange = self.get_telepathyrange()

        ###

        for k,v in sorted(self.d.itemap.iteritems()):
            itm = v[0]

            if itm.corpse:
                dg.render_push_skin(k[0], k[1], itm.corpse.skin[1], itm.skin[0], libtcod.black, 0, False)
            else:
                dg.render_push_skin(k[0], k[1], itm.skin[1], itm.skin[0], libtcod.black, 0, False)


        if self.d.doppeltime > 0:
            dg.render_push_skin(self.d.doppelpoint[0], self.d.doppelpoint[1],
                                libtcod.white, '@', libtcod.black, 0, False)

        lit_mons = set()

        for k,v in sorted(self.d.monmap.iteritems()):
            dg.render_push_skin(k[0], k[1], v.skin[1], v.skin[0], libtcod.black, 0, v.boulder)

            if telerange and not v.inanimate:
                d = xy_dist(self.d.pc, k)

                if d <= telerange:
                    lit_mons.add(k)
                    dg.render_set_is_lit(k[0], k[1], True)


        pc = '@'
        if self.p.sleeping > 1 and (self.w.t & 1) == 1:
            pc = '*'
        elif self.p.resting and (self.w.t & 1) == 1:
            pc = '.'
        elif self.p.digging and (self.w.t & 1) == 1:
            pc = '('
        else:
            pc = '@'

        pccol = libtcod.white
        if self.p.onfire:
            pccol = libtcod.amber
        dg.render_push_skin(self.d.pc[0], self.d.pc[1], pccol, pc, libtcod.black, 0, False)

        ###
        
        do_hud = not did_mapping
        if do_hud:
            self.draw_hud()

        did_highlight = dg.render_draw(self.w.t, self.d.pc[0], self.d.pc[1], 
                                       _hlxy[0], _hlxy[1], range[0], range[1], lightradius,
                                       do_hud)
        
        ###

        dg.render_pop_skin(self.d.pc[0], self.d.pc[1])

        self.new_visibles = False

        for k,v in sorted(self.d.monmap.iteritems()):
            dg.render_pop_skin(k[0], k[1])
            if k in lit_mons:
                dg.render_set_is_lit(k[0], k[1], False)

            if do_m_i_v and dg.render_is_in_fov(k[0], k[1]):
                self.monsters_in_view.append(v)
                v.visible = True

                # Hack
                if not v.visible_old:
                    self.new_visibles = True


        if self.d.doppeltime > 0:
            dg.render_pop_skin(self.d.doppelpoint[0], self.d.doppelpoint[1])

        for k,v in sorted(self.d.itemap.iteritems()):
            dg.render_pop_skin(k[0], k[1])

        ### 

        # hack
        if withtime:
            self.moon_message()
            self.w.oldt = self.w.t
            self.p.msg.t = self.w.t

        return did_highlight


    def save(self):
        # HACK! For supporting replays of games that have been saved and then loaded.
        if self.save_disabled:
            dg.random_init(self.w._seed)
            return

        f = None
        atts = [ 'p', 'd', 'w' ]
        state = {}

        for x in atts:
            state[x] = getattr(self, x)

        if 1: #try:
            f = open('savefile.dat0', 'w')
            cPickle.dump(state, f)
        #except:
        #    return

        dg.state_save('savefile.dat1')

        self.p.msg.m('Saved!')
        self.p.done = True

    def save_now(self):
        self.save()
        if not self.save_disabled:
            self.quit_right_now = True


    def load_bones(self):
        self.w.bones = []
        try:
            bf = open('bones', 'r')
            self.w.bones = cPickle.load(bf)
        except:
            pass


    def load(self):
        f = None
        state = None

        print 'LOADING'

        try:
            f = open('savefile.dat0', 'r')
            state = cPickle.load(f)
        except:
            print 'LOAD FAILED 1'
            return False

        for k,v in state.iteritems():
            setattr(self, k, v)

        dg.state_load('savefile.dat1')

        #log.f = open('LOG.%d' % self._seed, 'a')

        dg.random_init(self.w._seed)

        # HACK
        dg.neighbors_init(self.d.w, self.d.h)

        print 'LOAD OK'
        return True


    def save_bones(self):

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

        bones.append((self.p.plev, self.d.dlev, [i for i,slot in self.p.inv if i is not None and i.liveexplode is None]))

        for i in bones[-1][2]:
            i.tag = None

        bones = bones[-3:]

        try:
            bf = open('bones', 'w')
            cPickle.dump(bones, bf)
        except:
            pass



    def toggle_fullscreen(self):
        # HACK
        if self.save_disabled:
            return

        self.config.fullscreen = not self.config.fullscreen

        dg.render_init(self.d.w, self.d.h, self.config.fontfile, "Diggr", self.config.fullscreen)



    def toggle_sound(self):
        # HACK
        if self.save_disabled:
            return
        isok = self.config.sound.toggle_mute()
        if not isok:
            if self.config.music_n >= 0:
                self.config.sound.stop(self.config.music_n)
            self.config.music_n = -1
            self.p.msg.m('Sound OFF.')
        else:
            self.config.music_n = self.config.sound.play("music", rate=min(10, 2.0+(0.5*self.d.dlev)))
            self.p.msg.m('Sound ON.')

    def toggle_music(self):
        # HACK
        if self.save_disabled:
            return

        if self.config.music_n >= 0:
            self.config.sound.stop(self.config.music_n)
            self.config.music_n = -1
            self.p.msg.m('Music OFF.')
        else:
            self.config.music_n = self.config.sound.play("music", rate=min(10, 2.0+(0.5*self.d.dlev)))
            self.p.msg.m('Music ON.')



    def form_highscore(self):
        
        self.save_bones()

        self.p.achievements.finish(self.p.plev, self.d.dlev,
                                   self.d.moon, self.health().reason)

        # Scores are normalized to about 1000 max points,
        # regardless of which branch you play. (Provided you
        # only play one branch; playing several branches can
        # land you a score above the max.

        score = self.p.plev * 5
        score += min(self.d.dlev, 21) * 5

        for x in self.p.achievements.killed_monsters:
            if x[1] in self.w.monsterstock.norms:
                score += x[0] * self.w.monsterstock.norms[x[1]]

        score = int(round(score))

        scores.form_highscore(score, self.w._seed, self.w.bones, self.p.achievements, 
                              self.health().reason, self.w.t, self.p.done)

        


    def start_game(self, w, h, oldseed=None, oldbones=None):

        dg.render_init(w, h, self.config.fontfile, "Diggr", self.config.fullscreen)

        if oldseed or not self.load():
            if oldseed:
                self.w._seed = oldseed
            else:
                self.w._seed = int(time.time())

            if oldbones is not None:
                self.w.bones = oldbones
            else:
                self.load_bones()

            #log.f = open('LOG.%d' % self._seed, 'a')

            dg.random_init(self.w._seed)

            self.regen(w, h)
            self.generate_inv()
            self.p.msg.m("Kill all the monsters in the dungeon or reach dungeon level 26 to win the game.", True)
            self.p.msg.m("Please press '?' to see help.")

        if self.config.music_n != -1:
            self.config.music_n = self.config.sound.play("music", 
                                                         rate=min(10, 2.0+(0.5*self.d.dlev)))


    def check_autoplay(self):

        if self.p.sleeping > 0:
            if self.sleep().x >= 3.0 and not self.p.forcedsleep and not self.p.forced2sleep:
                self.p.msg.m('You wake up.')
                self.p.sleeping = 0
                self.p.healingsleep = False
                return 1
            else:
                self.do_sleep()
                return -1

        if self.p.resting:
            if self.tired().x >= 3.0:
                self.p.msg.m('You stop resting.')
                self.p.resting = False
                return 1

            elif self.new_visibles:
                self.p.resting = False
                return 1

            else:
                self.do_rest()
                return -1

        if self.p.digging:
            height = dg.grid_get_height(self.p.digging[0][0], self.p.digging[0][1])

            if height <= -10:
                self.convert_to_floor(self.p.digging[0], False)
                self.p.digging = None
                return 1

            elif self.new_visibles:
                self.p.digging = None
                return 1

            else:
                dg.grid_set_height(self.p.digging[0][0], self.p.digging[0][1], height - self.p.digging[1])
                self.tick()
                return -1

        return 0


    def endgame(self, do_highscore):
        if self.p.dead and not self.p.done:
            self.p.msg.m('You die.', True)

        if self.config.music_n >= 0:
            self.config.sound.stop(self.config.music_n)

        if not self.quit_right_now:
            self.w.oldt = self.w.t
            self.p.msg.m('*** Press any key ***', True)
            self.draw()
            dg.render_wait_for_anykey()

        if do_highscore and self.p.dead:
            self.form_highscore()


    def mainloop(self, do_highscore):
        __tt = time.time()

        if self.p.done or self.p.dead:
            self.endgame(do_highscore)
            return False

        self.draw()

        r = self.check_autoplay()
        if r == -1:
            dg.render_skip_input()
            return True

        elif r == 1:
            self.draw()

        if self.p.dead:
            self.endgame(do_highscore)
            return False

        print ' . ', time.time() - __tt
        key = dgsys.console_wait_for_keypress()

        __tt = time.time()

        if key.c in self.ckeys:
            self.ckeys[key.c]()

        elif key.vk in self.vkeys:
            self.vkeys[key.vk]()

        print ' x ', time.time() - __tt

        return True



######

def main(config, replay=None):

    oldseed = None
    oldbones = None

    if replay is not None:
        oldseed = replay[0]
        oldinputs = replay[1]
        oldbones = replay[2]

        dgsys._inputqueue = oldinputs

    w = 80
    h = 25

    config.load()

    game = Game(config)

    if replay is not None:
        game.save_disabled = True

    game.start_game(w, h, oldseed=oldseed, oldbones=oldbones)


    while 1:

        ok = game.mainloop(replay is None)

        if not ok:
            break

    return game.p.done


#import cProfile
#cProfile.run('main()')

if __name__=='__main__':
    config = dgsys.Config()
    while 1:
        if main(config):
            break
