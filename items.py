import libtcodpy as libtcod
import random
import copy

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
                 summon=None, radimmune=False, radexplode=False, fires=None,
                 camorange=None, sounding=False, healingsleep=None,
                 applies_in_slot=False, ebola=False, smoke=False,
                 trapcloud=False):
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
        self.radimmune = radimmune
        self.radexplode = radexplode
        self.fires = fires
        self.camorange = camorange
        self.sounding = sounding
        self.healingsleep = healingsleep
        self.applies_in_slot = applies_in_slot
        self.ebola = ebola
        self.smoke = smoke
        self.trapcloud = trapcloud

        self.ammo = None
        self.gencount = 0
        self.tag = None


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

        if self.tag:
            s = s + ' {tagged}'
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

        self.dynamite = Item('stick$s of dynamite', count=3, stackrange=3,
                             skin=('!', libtcod.red), applies=True, explodes=True,
                             radius=4, rarity=8, converts='litdynamite',
                             desc=['Sticks of dynamite can be lit to create an explosive device.'])

        self.minibomb = Item('minibomb$s', count=3, skin=('(', libtcod.pink),
                             applies=True, explodes=True, radius=1, rarity=8,
                             converts='litminibomb', stackrange=3,
                             desc=['Tiny hand-held grenades.'])

        self.gbomb = Item('gamma bomb$s', count=5, stackrange=5,
                          skin=('!', libtcod.azure), applies=True,
                          rarity=5, converts='litgbomb',
                          desc=["An object that looks something like a grenade, "
                                "but with a 'radiation sickness' sign painted on it."])

        self.litdynamite = Item('burning stick of dynamite',
                                skin=('!', libtcod.yellow), explodes=True,
                                liveexplode=7, slot='d', radius=4, throwable=True,
                                desc=['Watch out!!'])

        self.litminibomb = Item('armed minibomb', skin=('!', libtcod.yellow),
                                explodes=True, liveexplode=2, slot='d', radius=1,
                                throwable=True,
                                desc=['Watch out!!'])

        self.litgbomb = Item('activated gamma bomb', skin=('!', libtcod.yellow),
                             radexplode=True, liveexplode=4, slot='d', radius=12,
                             throwable=True, desc=['Watch out!!'])

        self.bomb = Item('exploding spore', skin=('!', libtcod.yellow), explodes=True,
                         liveexplode=4, slot='d', radius=3, throwable=True,
                         desc=['Uh-oh.'])

        self.radblob = Item('radiation blob', skin=('!', libtcod.yellow), radexplode=True,
                            liveexplode=2, slot='d', radius=8, throwable=True,
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

        self.sonar = Item("rock sonar", slot='d', skin=(')', libtcod.darker_cyan),
                          applies=True, rarity=7, sounding=True,
                          desc=["A device that uses sonar for discovering rock thickness."])

        self.medpack = Item("magic pill$s", slot='d', skin=('%', libtcod.white),
                            rarity=13, applies=True, healing=(3, 0.5),
                            cursedchance=7, stackrange=5, count=1,
                            desc=['A big white pill with a large red cross drawn on one side.'])

        self.herbalmed = Item("herbal palliative$s", slot='d', skin=('%', libtcod.light_green),
                              rarity=13, applies=True, healingsleep=(150, 25.0),
                              cursedchance=7, stackrange=5, count=1,
                              desc=['A large, green grassy-smelling pill.'])

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

        self.mmissile = Item("amulet of magic missile", slot='b', skin=('(', libtcod.light_azure),
                             rangeattack=7.0, range=(0,15), ammochance=(5, 25),
                             straightline=True, applies=True, rarity=7,
                             applies_in_slot=True,
                             desc=['A magical amulet that holds a clip of'
                                   'magically-induced mini-missiles.'])

        self.ak47 = Item('AK-47', slot='e', skin=('(', libtcod.desaturated_blue),
                         rangeattack=3.5, range=(0, 7), ammochance=(0, 30),
                         straightline=True, applies=True, rarity=15,
                         desc=['A semi-automatic rifle.'])

        self.shotgun = Item('shotgun', slot='e', skin=('(', libtcod.turquoise),
                            rangeattack=14.0, range=(2,5), ammochance=(1,4),
                            straightline=True, applies=True, rarity=15,
                            desc=['A powerful, killer weapon.',
                                  'You learned that much from playing videogames.'])

        self.flamethrower = Item("flamethrower", slot='e', skin=('(', libtcod.orange),
                                 rangeattack=7.0, range=(2,6), ammochance=(1, 6),
                                 straightline=True, applies=True, rarity=15, fires=10,
                                 desc=['A device for setting monsters on fire.',
                                       'Truly ingenious.'])

        self.tazer = Item("tazer", slot='e', skin=('(', libtcod.gray),
                          attack=1.0, confattack=(10, 1), rarity=5,
                          desc=['Very useful for subduing enemies.'])

        self.redgloves = Item("red hand gloves", slot='d', skin=('(', libtcod.dark_red),
                          attack=0.1, confattack=(10, 1), rarity=3, count=0,
                          desc=['These magical gloves have a very confusing red glow.'])

        self.dartgun = Item('dart gun', slot='e', skin=('(', libtcod.light_crimson),
                            attack=0.5, confattack=(30, 5), rarity=5, range=(0,5),
                            rangeattack=0.5, ammochance=(10,30), straightline=True,
                            applies=True,
                            desc=['A small plastic gun loaded with suspicious-looking darts.'])

        self.bigdartgun = Item('elephant sedative', slot='e', skin=('(', libtcod.crimson),
                               attack=0.1, confattack=(150, 5), rarity=3, range=(0,4),
                               rangeattack=4.5, ammochance=(2,4), straightline=True,
                               applies=True,
                               desc=['An applicator used for delivering ',
                                     'sedative darts to elephants.'
                                     'It looks like a small rocket launcher.'])

        self.tinfoilhat = Item('tin foil hat', slot='a', skin=('[', libtcod.gray),
                               psyimmune=True, rarity=6,
                               selfdestruct=(3000,500),
                               desc=['A metallic hat that protects against attempts of ',
                                     'mind control by various crazies.'])

        self.tinfoilcrystal = Item('crystal of tin', slot='d', skin=('{', libtcod.gray),
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
                                  desc=['A vest that provides a portable force-field shield.'])

        self.camo = Item('nanoparticle camouflage', slot='c', skin=('[', libtcod.dark_green),
                         camorange=3, rarity=3, defence=0.01, count=0,
                         selfdestruct=(1000, 100),
                         desc=['An ultra-hightech piece of camoflage clothing.',
                               "It's made of nanoparticles that render the wearer",
                               'practically invisible.'])

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

        self.portabletunnel = Item('portable tunnel$s', slot='d', skin=('`', libtcod.dark_sepia),
                                   rarity=4, applies=True, jumprange=12, stackrange=2,
                                   count=1,
                                   desc=['Like a portable hole, but much larger.'])

        self.bombsuit = Item('bomb suit', slot='c', skin=('[', libtcod.lightest_yellow),
                             explodeimmune=True, rarity=3, defence=0.1,
                             selfdestruct=(300, 50),
                             desc=['The standard protective suit for bomb squads.'])

        self.radsuit = Item('radiation suit', slot='c', skin=('[', libtcod.dark_lime),
                             radimmune=True, rarity=0, defence=0.1,
                             selfdestruct=(1000, 50),
                             desc=['A very special piece of equipment that protects against radiation.'])

        self.psyhelmet = Item('crystal helmet', slot='a', skin=('[', libtcod.white),
                               telepathyrange=6, rarity=6,
                               desc=['An ornate helmet made of crystal.',
                                     'It is a powerful artifact of psyonic magic.'])

        self.stickyglue = Item('sticky glue$s', slot='d', skin=('{', libtcod.light_yellow),
                               applies=True, makestrap=True, rarity=8, count=1,
                               stackrange=4,
                               desc=['A tube of very sticky glue. It can be used to make traps.'])

        self.gluegun = Item('gluegun', slot='d', skin=('{', libtcod.light_yellow),
                            applies=True, makestrap=True, rarity=0, count=None,
                            desc=['A device that holds a practically unlimited amount of glue.'])

        self.cclarva = Item('carrion crawler larva', slot='', skin=(',', libtcod.white),
                            rarity=0, summon=('carrion crawler', 2),
                            throwable=True, liveexplode=4,
                            desc=['A tiny larva of the carrion crawler species.'])

        self.triffidlarva = Item('triffid seed', slot='', skin=(',', libtcod.peach),
                                 rarity=0, summon=('triffid', 1),
                                 throwable=True, liveexplode=4,
                                 desc=['A tiny larva of the carrion crawler species.'])

        self.avern = Item('avern', slot='e', skin=('(', libtcod.dark_green),
                          attack=6.0, rarity=0, selfdestruct=(500, 100),
                          desc=['A makeshift weapon made from the poisonous avern plant.'])

        self.alzabobrain = Item('alzabo brain matter', slot='', skin=(',', libtcod.darkest_red),
                                 rarity=0, summon=('alzabo', 1),
                                 throwable=True, liveexplode=4, count=0,
                                 desc=["Bits and pieces of the alzabo's brain."])

        self.ebolastrain = Item('Ebola strain', slot='e',
                                skin=('{', libtcod.red), applies=True, ebola=True,
                                rarity=8, 
                                desc=['A container with biohazard signs pasted all over it.',
                                      'It contains genetically-modified strains of the',
                                      'Ebola virus. Releasing the virus into the environment',
                                      'could have potentially disastrous consequences!'])

        self.smokemachine = Item('smoke machine', slot='',
                                 skin=('{', libtcod.silver), applies=True, smoke=True,
                                 rarity=3, 
                                 desc=['A machine that produces very confusing',
                                       'shape-shifting clouds of smoke.'])

        self.trapcloud = Item('glue nanobots', slot='d', skin=('{', libtcod.dark_yellow),
                              applies=True, trapcloud=True, rarity=4, count=0,
                              desc=['Microscopic nanobots that are used in construction work.'
                                    'They are good at quickly covering large areas in glue.'])

        ###
        ### Special item crafting.
        ###

        self.craft_s1 = Item('titanium rod', slot='', skin=('$', libtcod.green),
                             rarity=4, 
                             desc=['This special item needs to be combined with another',
                                   'special item to make something very interesting.'])

        self.craft_s2 = Item('gunpowder', slot='', skin=('$', libtcod.green),
                             rarity=4, count=0,
                             desc=['This special item needs to be combined with another',
                                   'special item to make something very interesting.'])

        self.craft_s3 = Item('buckshot', slot='', skin=('$', libtcod.green),
                             rarity=4, count=0,
                             desc=['This special item needs to be combined with another',
                                   'special item to make something very interesting.'])

        self.craft_s4 = Item('bootsoles', slot='', skin=('$', libtcod.green),
                             rarity=4, count=0,
                             desc=['This special item needs to be combined with another',
                                   'special item to make something very interesting.'])

        self.craft_s5 = Item('nanite compound', slot='', skin=('$', libtcod.green),
                             rarity=4, 
                             desc=['This special item needs to be combined with another',
                                   'special item to make something very interesting.'])

        self.craft_s6 = Item('flaming phial', slot='', skin=('$', libtcod.green),
                             rarity=4, 
                             desc=['This special item needs to be combined with another',
                                   'special item to make something very interesting.'])

        self.craft_s7 = Item("dragon's blood", slot='', skin=('$', libtcod.green),
                             rarity=4, count=0,
                             desc=['This special item needs to be combined with another',
                                   'special item to make something very interesting.'])

        self.craft_s8 = Item('anointing oil', slot='', skin=('$', libtcod.green),
                             rarity=4, count=0,
                             desc=['This special item needs to be combined with another',
                                   'special item to make something very interesting.'])

        self.craft_s9 = Item('magic spark', slot='', skin=('$', libtcod.light_blue),
                             rarity=4, 
                             desc=['This special item needs to be combined with another',
                                   'special item to make something very interesting.'])

        ### 

        self.craft_1 = Item('nanite boots', slot='', skin=('$', libtcod.dark_yellow), 
                            rarity=0, count=0,
                            desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_2 = Item("dragon's oil", slot='', skin=('$', libtcod.dark_yellow), 
                            rarity=0, count=0,
                            desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_3 = Item('dragon boots', slot='', skin=('$', libtcod.dark_yellow), 
                            rarity=0, count=0,
                            desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_4 = Item('nanite powder', slot='', skin=('$', libtcod.dark_yellow), 
                            rarity=0, count=0,
                            desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_5 = Item('titanium shot', slot='', skin=('$', libtcod.dark_yellow), 
                            rarity=0, count=0,
                            desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_6 = Item('torch phial', slot='', skin=('$', libtcod.dark_yellow), 
                            rarity=0, 
                            desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_7 = Item('powderboots', slot='', skin=('$', libtcod.dark_yellow), 
                            rarity=0, count=0,
                            desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_8 = Item('powderphial', slot='', skin=('$', libtcod.dark_yellow), 
                            rarity=0, 
                            desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_9 = Item("dragon's phial", slot='', skin=('$', libtcod.dark_yellow), 
                            rarity=0,
                            desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_10 = Item('dragonshot', slot='', skin=('$', libtcod.dark_yellow), 
                             rarity=0, count=0,
                             desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_11 = Item('nanite oil', slot='', skin=('$', libtcod.dark_yellow), 
                             rarity=0, count=0,
                             desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_12 = Item('titanium oil', slot='', skin=('$', libtcod.dark_yellow), 
                             rarity=0, count=0,
                             desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_13 = Item('dragon nanites', slot='', skin=('$', libtcod.dark_yellow), 
                             rarity=0, count=0,
                             desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_14 = Item('gunpowder buckshot', slot='', skin=('$', libtcod.dark_yellow), 
                             rarity=0, count=0,
                             desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_15 = Item('buckshot bootsoles', slot='', skin=('$', libtcod.dark_yellow), 
                             rarity=0, count=0,
                             desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_16 = Item('titanium phial', slot='', skin=('$', libtcod.dark_yellow), 
                             rarity=0,
                             desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_17 = Item('gunpowder titanium', slot='', skin=('$', libtcod.dark_yellow), 
                             rarity=0, count=0,
                             desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        self.craft_18 = Item('nanite buckshot', slot='', skin=('$', libtcod.dark_yellow), 
                             rarity=0, count=0,
                             desc=['A useless contraption. It needs to be combined with',
                                  'another special item to become something very interesting.'])

        ##

        self.craft_n1 = Item('broken everlasting shotgun', slot='', skin=('$', libtcod.yellow),
                             rarity=0, 
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_n2 = Item('broken camouflage nanoboots', slot='', skin=('$', libtcod.yellow),
                             rarity=0, count=0,
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_n3 = Item('lifeless flaming sword ', slot='', skin=('$', libtcod.yellow),
                             rarity=0,
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_n4 = Item('lifeless Brahmic medallion', slot='', skin=('$', libtcod.yellow),
                             rarity=0,
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_n5 = Item('broken gluebot machine', slot='', skin=('$', libtcod.yellow),
                             rarity=0,
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_n6 = Item('lifeless medi-nanites', slot='', skin=('$', libtcod.yellow),
                             rarity=0, count=0,
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_n7 = Item('broken everlasting portable hole', slot='', skin=('$', libtcod.yellow),
                             rarity=0,
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_n8 = Item('broken everlasting rocket launcher', slot='', skin=('$', libtcod.yellow),
                             rarity=0,
                             desc=["This item won't work until you apply a magic spark."])

        ### ### ### 

        self.craft_e1 = Item('everlasting shotgun', slot='', skin=('(', libtcod.yellow),
                             rarity=0, 
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_e2 = Item('camouflage nanoboots', slot='', skin=('[', libtcod.pink),
                             rarity=0, count=0,
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_e3 = Item('flaming sword ', slot='', skin=('(', libtcod.yellow),
                             rarity=0,
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_e4 = Item('Brahmic medallion', slot='', skin=('"', libtcod.yellow),
                             rarity=0,
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_e5 = Item('gluebot machine', slot='', skin=('{', libtcod.pink),
                             rarity=0,
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_e6 = Item('medi-nanites', slot='', skin=('%', libtcod.pink),
                             rarity=0, count=0,
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_e7 = Item('everlasting portable hole', slot='', skin=('`', libtcod.yellow),
                             rarity=0,
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_e8 = Item('everlasting rocket launcher', slot='', skin=('(', libtcod.pink),
                             rarity=0,
                             desc=["This item won't work until you apply a magic spark."])


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



# 1. everlasting shotgun
# 2. camouflage nanoboots (camo+springboots)
# 3. flaming sword (sword+sets on fire+light)
# 4. brahmic medallion (light+everlasting ranged weapon)
# 5. gluebot machine (glue nanobot machine + glue immunity)
# 6. medi-nanites (everlasting magic pills with no sideeffects)
# 7. everlasting portable hole
# 8. everlasting rocket launcher
# ---
# 1. titanium rod + gunpowder + buckshot + magic spark
# 2. buckshot + bootsoles + nanite compound + magic spark
# 3. titanium rod + flaming phial + anointing oil + magic spark
# 4. flaming phial + dragon's blood + anointing oil + magic spark
# 5. gunpowder + bootsoles + nanite compound + magic spark
# 6. nanite compound + dragon's blood + anointing oil + magic spark
# 7. buckshot + bootsoles + dragon's blood + magic spark
# 8. titanium rod + gunpowder + flaming phial + magic spark

# 

# bootsoles, nanite compound       -> nanite boots
# dragon's blood, anointing oil    -> dragon's oil
# bootsoles, dragon's blood        -> dragon boots
# gunpowder, nanite compound       -> nanite powder
# titanium rod, buckshot           -> titanium shot
# flaming phial, anointing oil     -> torch phial
# gunpowder, bootsoles             -> powderboots
# gunpowder, flaming phial         -> powderphial
# flaming phial, dragon's blood    -> dragon's phial
# buckshot, dragon's blood         -> dragonshot
# nanite compound, anointing oil   -> nanite oil
# titanium rod, anointing oil      -> titanium oil
# nanite compound, dragon's blood  -> dragon nanites
# gunpowder, buckshot              -> gunpowder buckshot
# buckshot, bootsoles              -> buckshot bootsoles
# titanium rod, flaming phial      -> titanium phial
# titanium rod, gunpowder          -> gunpowder titanium
# buckshot, nanite compound        -> nanite buckshot

# 1. everlasting shotgun
# 2. camouflage nanoboots (camo+springboots)
# 3. flaming sword (sword+sets on fire+light)
# 4. brahmic medallion (light+everlasting ranged weapon)
# 5. gluebot machine (glue nanobot machine + glue immunity)
# 6. medi-nanites (everlasting magic pills with no sideeffects)
# 7. everlasting portable hole
# 8. everlasting rocket launcher



# bootsoles, nanite compound       -> nanite boots
# dragon's blood, anointing oil    -> dragon's oil
# bootsoles, dragon's blood        -> dragon boots
# gunpowder, nanite compound       -> nanite powder
# titanium rod, buckshot           -> titanium shot
# flaming phial, anointing oil     -> torch phial
# gunpowder, bootsoles             -> powderboots
# gunpowder, flaming phial         -> powderphial
# flaming phial, dragon's blood    -> dragon's phial
# buckshot, dragon's blood         -> dragonshot
# nanite compound, anointing oil   -> nanite oil
# titanium rod, anointing oil      -> titanium oil
# nanite compound, dragon's blood  -> dragon nanites
# gunpowder, buckshot              -> gunpowder buckshot
# buckshot, bootsoles              -> buckshot bootsoles
# titanium rod, flaming phial      -> titanium phial
# titanium rod, gunpowder          -> gunpowder titanium
# buckshot, nanite compound        -> nanite buckshot
