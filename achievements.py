
import moon

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

    def finish(self, plev, dlev, moon_, reason):
        self.add('plev%d' % plev, 'Reached player level %d' % plev)
        self.add('dlev%d' % dlev, 'Reached dungeon level %d' % dlev)

        moonstr = moon.phase_string(moon_)
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
