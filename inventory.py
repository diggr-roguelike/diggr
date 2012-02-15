
import tcod_colors as libtcod
from flair import *

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

    def draw(self, dlev, plev, floor=None):

        def fmt(slot):
            nm = self._slotnames[slot]
            nm = nm[0].upper() + nm[1:]
            pad = ' '*(10-len(nm))
            itm = ' -'
            tmp = self._items[slot]
            if tmp:
                itm = str(tmp)
            return "%c%c)%s %s: %c%s" % (libtcod.COLCTRL_5, 
                                         slot, pad, nm,
                                         libtcod.COLCTRL_1,
                                         itm)

        s = [fmt(slot) for slot in self._slotnums]

        if floor:
            s.extend(floor)

        s.extend(["",
                  "Character level: %d" % plev,
                  "  Dungeon level: %d" % dlev])

        return draw_window(s)

    def take(self, i, slot=None):
        if not slot:
            slot = i.slot

        if slot in self._items and not self._items[slot]:
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
        for k,v in self._items.iteritems():
            if v == item:
                self._items[k] = None
