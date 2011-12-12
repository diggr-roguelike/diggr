import libtcodpy as libtcod
import random
import copy

import moon


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
                 trapcloud=False, glueimmune=False, craft=None, resource=None,
                 hide_count=False, swampgas=False, digbonus=0, airfreshener=None, 
                 corpse=None, switch_moon=None):
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
        self.glueimmune = glueimmune
        self.craft = craft
        self.resource = resource
        self.hide_count = hide_count
        self.swampgas = swampgas
        self.digbonus = digbonus
        self.airfreshener = airfreshener
        self.switch_moon = switch_moon

        self.corpse = corpse
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

        if self.hide_count:
            if self.count > 0:
                s = s + ' [%d]' % self.count

        elif self.count > 1:
            s = str(self.count) + " " + s.replace('$s', 's')
        elif self.count != 0 and len(s) > 0:
            if self.count == 1:
                s = s.replace('$s', '')

            if self.use_an or s[0] in 'aeiouAEIOU':
                s = 'an ' + s
            else:
                s = 'a ' + s

        if self.corpse:
            s = s + ' of %s' % str(self.corpse)

        if self.ammo and self.ammo > 0:
            s = s + ' [%d]' % self.ammo

        if self.tag:
            s = s + ' {tagged}'
        return s

    def postprocess(self):
        if self.cursedchance:
            if random.randint(0, self.cursedchance) == 0:
                self.bonus = -1

        if self.ammochance:
            if self.ammochance[0] < 0:
                self.ammo = -1
            else:
                self.ammo = random.randint(self.ammochance[0], self.ammochance[1])

        if self.selfdestruct:
            self.selfdestruct = int(max(random.gauss(*self.selfdestruct), 1))


class ItemStock:
    def __init__(self):
        self.necklamp = Item("miner's lamp", slot='b', lightradius=8, rarity=8,
                             desc=['A lamp that provides light while you are cave-crawling.'])

        self.helmet = Item("miner's hardhat", slot='a', rarity=8,
                           skin=('[', libtcod.sepia), defence=0.25,
                           digbonus=0.05,
                           desc=['A simple plastic item of protective headgear.',
                                 'Miners claim that it helps them dig faster,',
                                 'for some inexplicable reason.'])

        self.minirockets = Item('minirocket launcher', slot='e', rarity=8,
                                skin=('(', libtcod.light_red), applies=True,
                                rangeexplode=True, range=(4,15),
                                explodes=True, radius=2, attack=0, 
                                ammochance=(3,3),
                                desc=['A shoulder-mounted rocket launcher that holds',
                                      'three tiny rockets.'])

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
                         rangeattack=3.5, range=(0, 7), ammochance=(9, 30),
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

        self.gasspore = Item('swamp gas spore', slot='', skin=(',', libtcod.dark_blue),
                             rarity=5, swampgas=True, throwable=True, liveexplode=3, 
                             desc=['A concentrated globe of pent-up swamp gas.'])


        self.airfresh = Item('air freshener', skin=(')', libtcod.blue), airfreshener=4,
                             slot='d', rarity=8, ammochance=(20,45), applies=True,
                             desc=['Used for cleaning up noxious fumes, gases and spores.'])

        self.boulder1 = Item('scroll of boulder fort', skin=('{', libtcod.desaturated_cyan),
                             slot='d', summon=('ba4', 8), applies=True, rarity=3, 
                             desc=["It's labeled HACKEM MUCHE. Whatever that means..."])

        self.boulder2 = Item('scroll of boulder fort', skin=('{', libtcod.desaturated_cyan),
                             slot='d', summon=('bc3', 8), applies=True, rarity=3, 
                             desc=["It's labeled HACKEM MUCHE. Whatever that means..."])

        self.boulder3 = Item('scroll of boulder fort', skin=('{', libtcod.desaturated_cyan),
                             slot='d', summon=('bb8', 8), applies=True, rarity=3, 
                             desc=["It's labeled HACKEM MUCHE. Whatever that means..."])

        self.full_moon = Item('prism of the Full Moon', skin=('~', libtcod.blue),
                              slot='', applies=True, rarity=2, switch_moon=moon.FULL,
                              desc=['An ancient and very powerful artifact.',
                                    'Rumor has it that it affects the very fabric of space',
                                    'and time.'])

        self.new_moon = Item('prism of the New Moon', skin=('~', libtcod.dark_crimson),
                             slot='', applies=True, rarity=2, switch_moon=moon.NEW,
                             desc=['An ancient and very powerful artifact.',
                                   'Rumor has it that it affects the very fabric of space',
                                   'and time.'])

        # Corpse

        self.corpse = Item('corpse', skin=(21, libtcod.yellow), slot='', rarity=0, desc=[''])

        ###
        ### Special item crafting.
        ###

        self.craft_a = Item('anointing oil', slot='', skin=('$', libtcod.green),
                            rarity=4, count=0, applies=True,
                            craft=('a', {'d':'craft_ad',
                                         'f':'craft_af',
                                         'n':'craft_an',
                                         't':'craft_at'}),
                            desc=['This special item needs to be combined with',
                                  "dragon's blood, a flaming phial, nanite compound or a titanium rod",
                                  'to make something very interesting.'])

        self.craft_b = Item('bootsoles', slot='', skin=('$', libtcod.green),
                            rarity=4, count=0, applies=True,
                            craft=('b', {'u':'craft_bu',
                                         'd':'craft_bd',
                                         'g':'craft_bg',
                                         'n':'craft_bn'}),
                            desc=['This special item needs to be combined with',
                                  "buckshot, dragon's blood, gunpowder or nanite compound",
                                  'to make something very interesting.'])

        self.craft_u = Item('buckshot', slot='', skin=('$', libtcod.green),
                            rarity=4, count=0, applies=True,
                            craft=('u',{'b':'craft_bu',
                                        'd':'craft_du',
                                        'g':'craft_gu',
                                        'n':'craft_nu',
                                        't':'craft_tu'}),
                            desc=['This special item needs to be combined with',
                                  "bootsoles, dragon's blood, gunpowder, nanite compound or a titanium rod",
                                  'to make something very interesting.'])

        self.craft_d = Item("dragon's blood", slot='', skin=('$', libtcod.green),
                            rarity=4, count=0, applies=True,
                            craft=('d',{'a':'craft_ad',
                                        'b':'craft_bd',
                                        'u':'craft_du',
                                        'f':'craft_df',
                                        'n':'craft_dn'}),
                            desc=['This special item needs to be combined with',
                                  'anointing oil, bootsoles, buckshot, a flaming phial or nanite compound',
                                  'to make something very interesting.'])

        self.craft_f = Item('flaming phial', slot='', skin=('$', libtcod.green),
                            rarity=4, applies=True,
                            craft=('f',{'a':'craft_af',
                                        'd':'craft_df',
                                        'g':'craft_fg',
                                        't':'craft_ft'}),
                            desc=['This special item needs to be combined with',
                                  "anointing oil, dragon's blood, gunpowder or a titanium rod",
                                  'to make something very interesting.'])

        self.craft_g = Item('gunpowder', slot='', skin=('$', libtcod.green),
                            rarity=4, count=0, applies=True,
                            craft=('g',{'b':'craft_bg',
                                        'u':'craft_gu',
                                        'f':'craft_fg',
                                        'n':'craft_gn',
                                        't':'craft_gt'}),
                            desc=['This special item needs to be combined with',
                                  'bootsoles, buckshot, a flaming phial, nanite compound or a titanium rod',
                                  'to make something very interesting.'])

        self.craft_n = Item('nanite compound', slot='', skin=('$', libtcod.green),
                            rarity=4, applies=True,
                            craft=('n',{'a':'craft_an',
                                        'b':'craft_bn',
                                        'u':'craft_nu',
                                        'd':'craft_dn',
                                        'g':'craft_gn'}),
                            desc=['This special item needs to be combined with',
                                  "anointing oil, bootsoles, buckshot, dragon's blood or gunpowder",
                                  'to make something very interesting.'])

        self.craft_t = Item('titanium rod', slot='', skin=('$', libtcod.green),
                            rarity=4, applies=True,
                            craft=('t',{'a':'craft_at',
                                        'u':'craft_tu',
                                        'f':'craft_ft',
                                        'g':'craft_gt'}),
                            desc=['This special item needs to be combined with',
                                  'anointing oil, buckshot, a flaming phial or gunpowder',
                                  'special item to make something very interesting.'])

        self.craft_z = Item('magic spark', slot='', skin=('$', libtcod.light_blue),
                            rarity=4, applies=True,
                            craft=('z',{'n1':'craft_a1',
                                        'n2':'craft_a2',
                                        'n3':'craft_a3',
                                        'n4':'craft_a4',
                                        'n5':'craft_a5',
                                        'n6':'craft_a6',
                                        'n7':'craft_a7',
                                        'n8':'craft_a8'}),
                            desc=['This special item needs to be combined with another very',
                                  'special item to make something very interesting.'])

        ###

        self.craft_ad = Item("dragon's oil", slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, count=0, applies=True,
                             craft=('ad',{'f':'craft_n4',
                                          'n':'craft_n6'}),
                             desc=['A useless contraption. It needs to be combined with',
                                   'a flaming phial or nanite compound to become something very interesting.'])

        self.craft_af = Item('torch phial', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, applies=True,
                             craft=('af',{'d':'craft_n4',
                                          't':'craft_n3'}),
                             desc=['A useless contraption. It needs to be combined with',
                                   "dragon's blood or a titanium rod to become something very interesting."])

        self.craft_an = Item('nanite oil', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, count=0, applies=True,
                             craft=('an',{'d':'craft_n6'}),
                             desc=['A useless contraption. It needs to be combined with',
                                   "dragon's blood to become something very interesting."])

        self.craft_at = Item('titanium oil', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, count=0, applies=True,
                             craft=('at',{'f':'craft_n3'}),
                             desc=['A useless contraption. It needs to be combined with',
                                  'a flaming phial to become something very interesting.'])

        self.craft_bu = Item('buckshot bootsoles', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, count=0, applies=True,
                             craft=('bu',{'d':'craft_n7',
                                          'n':'craft_n2'}),
                             desc=['A useless contraption. It needs to be combined with',
                                  "dragon's blood or nanite compound to become something very interesting."])

        self.craft_bd = Item('dragon boots', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, count=0, applies=True,
                             craft=('bd',{'u':'craft_n7'}),
                             desc=['A useless contraption. It needs to be combined with',
                                   'buckshot to become something very interesting.'])

        self.craft_bg = Item('powderboots', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, count=0, applies=True,
                             craft=('bg',{'n':'craft_n5'}),
                             desc=['A useless contraption. It needs to be combined with',
                                   'nanite compound to become something very interesting.'])

        self.craft_bn = Item('nanite boots', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, count=0, applies=True,
                             craft=('bn',{'u':'craft_n2',
                                          'g':'craft_n5'}),
                             desc=['A useless contraption. It needs to be combined with',
                                   'buckshot or gunpowder to become something very interesting.'])

        self.craft_du = Item('dragonshot', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, count=0, applies=True,
                             craft=('du',{'b':'craft_n7'}),
                             desc=['A useless contraption. It needs to be combined with',
                                  'bootsoles to become something very interesting.'])

        self.craft_gu = Item('gunpowder buckshot', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, count=0, applies=True,
                             craft=('gu',{'t':'craft_n1'}),
                             desc=['A useless contraption. It needs to be combined with',
                                   'a titanium rod to become something very interesting.'])

        self.craft_nu = Item('nanite buckshot', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, count=0, applies=True,
                             craft=('nu',{'b':'craft_n2'}),
                             desc=['A useless contraption. It needs to be combined with',
                                   'bootsoles to become something very interesting.'])

        self.craft_tu = Item('titanium shot', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, count=0, applies=True,
                             craft=('tu',{'g':'craft_n1'}),
                             desc=['A useless contraption. It needs to be combined with',
                                   'gunpowder to become something very interesting.'])

        self.craft_df = Item("dragon's phial", slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, applies=True,
                             craft=('df',{'a':'craft_n4'}),
                             desc=['A useless contraption. It needs to be combined with',
                                   'anointing oil to become something very interesting.'])

        self.craft_dn = Item('dragon nanites', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, count=0, applies=True,
                             craft=('dn',{'a':'craft_n6'}),
                             desc=['A useless contraption. It needs to be combined with',
                                   'anointing oil to become something very interesting.'])

        self.craft_fg = Item('powderphial', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, applies=True,
                             craft=('fg',{'t':'craft_n8'}),
                             desc=['A useless contraption. It needs to be combined with',
                                   'a titanium rod to become something very interesting.'])

        self.craft_ft = Item('titanium phial', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, applies=True,
                             craft=('ft',{'a':'craft_n3',
                                          'g':'craft_n8'}),
                             desc=['A useless contraption. It needs to be combined with',
                                   'anointing oil or gunpowder to become something very interesting.'])

        self.craft_gn = Item('nanite powder', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, count=0, applies=True,
                             craft=('gn',{'b':'craft_n5'}),
                             desc=['A useless contraption. It needs to be combined with',
                                   'bootsoles to become something very interesting.'])

        self.craft_gt = Item('gunpowder titanium', slot='', skin=('$', libtcod.dark_yellow),
                             rarity=0, count=0, applies=True,
                             craft=('gt',{'u':'craft_n1',
                                          'f':'craft_n8'}),
                             desc=['A useless contraption. It needs to be combined with',
                                   'buckshot or a flaming phial to become something very interesting.'])

        ##

        self.craft_n1 = Item('broken everlasting shotgun', slot='', skin=('$', libtcod.yellow),
                             rarity=0, applies=True,
                             craft=('n1',{'z':'craft_a1'}),
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_n2 = Item('broken camouflage nanoboots', slot='', skin=('$', libtcod.yellow),
                             rarity=0, count=0, applies=True,
                             craft=('n2',{'z':'craft_a2'}),
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_n3 = Item('lifeless flaming sword', slot='', skin=('$', libtcod.yellow),
                             rarity=0, applies=True,
                             craft=('n3',{'z':'craft_a3'}),
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_n4 = Item('lifeless Brahmic medallion', slot='', skin=('$', libtcod.yellow),
                             rarity=0, applies=True,
                             craft=('n4',{'z':'craft_a4'}),
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_n5 = Item('broken gluebot machine', slot='', skin=('$', libtcod.yellow),
                             rarity=0, applies=True,
                             craft=('n5',{'z':'craft_a5'}),
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_n6 = Item('lifeless medi-nanites', slot='', skin=('$', libtcod.yellow),
                             rarity=0, count=0, applies=True,
                             craft=('n6',{'z':'craft_a6'}),
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_n7 = Item('broken everlasting portable hole', slot='', skin=('$', libtcod.yellow),
                             rarity=0, applies=True,
                             craft=('n7',{'z':'craft_a7'}),
                             desc=["This item won't work until you apply a magic spark."])

        self.craft_n8 = Item('broken everlasting rocket launcher', slot='', skin=('$', libtcod.yellow),
                             rarity=0, applies=True,
                             craft=('n8',{'z':'craft_a8'}),
                             desc=["This item won't work until you apply a magic spark."])

        ### ### ###

        self.craft_a1 = Item('everlasting shotgun', slot='e', skin=('(', libtcod.yellow),
                             rarity=0, rangeattack=14.0, range=(2,6), ammochance=(-1,-1),
                             straightline=True, applies=True,
                             desc=["A magical shotgun than never runs out of bullets."])

        self.craft_a2 = Item('camouflage nanoboots', slot='g', skin=('[', libtcod.pink),
                             rarity=0, count=0, defence=0.1, springy=True, camorange=3,
                             desc=["Nanotechnological wonderfootwear that provides exceptional",
                                   "speed *and* stealth."])

        self.craft_a3 = Item('flaming sword ', slot='e', skin=('(', libtcod.yellow),
                             rarity=0, attack=6.0, fires=10, lightradius=6,
                             desc=["A giant sword of flame."])

        self.craft_a4 = Item('Brahmic medallion', slot='b', skin=('"', libtcod.yellow),
                             rarity=0, lightradius=8, camorange=4, rangeattack=7.0,
                             range=(0,15), ammochance=(-1,-1),
                             straightline=True, applies=True, applies_in_slot=True,
                             desc=["An amulet of neverending magical missiles that also",
                                   "provides godlike stealth."])

        self.craft_a5 = Item('gluebot machine', slot='d', skin=('{', libtcod.pink),
                             rarity=0, applies=True, trapcloud=True, count=None,
                             glueimmune=True,
                             desc=["A high-tech machine that can produce a neverending stream",
                                   "of glue nanobots. It also provides protection from the",
                                   "glue for the user."])

        self.craft_a6 = Item('medi-nanites', slot='d', skin=('%', libtcod.pink),
                             rarity=0, count=0, applies=True, healingsleep=(50, 1), repelrange=2,
                             desc=["An endless supply of advanced healing ointments."])

        self.craft_a7 = Item('everlasting portable hole', slot='d', skin=('`', libtcod.yellow),
                             rarity=0, applies=True, jumprange=4, count=None,
                             desc=["A portable hole that never runs out."])

        self.craft_a8 = Item('everlasting rocket launcher', slot='e', skin=('(', libtcod.pink),
                             rarity=0, applies=True, rangeexplode=True, range=(4, 15),
                             attack=0, ammochance=(-1,-1), radius=3,
                             desc=["A magic RPG launcher that never runs out of ammo."])

        ### Color potions to complement color fountains

        self.green = Item('green potion', slot='', skin=(':', libtcod.darkest_green),
                          rarity=3, applies=True, resource='g',
                          desc=["A flask containing a green liquid."])

        self.red = Item('red potion', slot='', skin=(':', libtcod.dark_red),
                        rarity=3, applies=True, resource='r',
                        desc=["A flask containing a red liquid."])

        self.yellow = Item('yellow potion', slot='', skin=(':', libtcod.dark_yellow),
                           rarity=3, applies=True, resource='y',
                           desc=["A flask containing a yellow liquid."])

        self.blue = Item('blue potion', slot='', skin=(':', libtcod.dark_blue),
                         rarity=3, applies=True, resource='b',
                         desc=["A flask containing a blue liquid."])

        self.purple = Item('purple potion', slot='', skin=(':', libtcod.dark_purple),
                           rarity=3, applies=True, resource='p',
                           desc=["A flask containing a purple liquid."])

        ## !

        self.deusex = Item('Deus ex machina', slot='', skin=(236, libtcod.yellow),
                           rarity=0, applies=True, wishing=True, count=7, hide_count=True,
                           desc=['Translated from the Latin, literally:',
                                 '"the god from the machine".'])



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
# 1. titanium_rod       gunpowder       buckshot
# 2. buckshot           bootsoles       nanite_compound
# 3. titanium_rod       flaming_phial   anointing_oil
# 4. flaming_phial      dragon's_blood  anointing_oil
# 5. gunpowder          bootsoles       nanite_compound
# 6. nanite_compound    dragon's_blood  anointing_oil
# 7. buckshot           bootsoles       dragon's_blood
# 8. titanium_rod       gunpowder       flaming_phial

# anointing_oil	dragon's_blood	flaming_phial	# 4
# anointing_oil	dragon's_blood	nanite_compound	# 6
# anointing_oil	flaming_phial	dragon's_blood	# 4
# anointing_oil	flaming_phial	titanium_rod	# 3
# anointing_oil	nanite_compound	dragon's_blood	# 6
# anointing_oil	titanium_rod	flaming_phial	# 3
# bootsoles	buckshot	dragon's_blood	# 7
# bootsoles	buckshot	nanite_compound	# 2
# bootsoles	dragon's_blood	buckshot	# 7
# bootsoles	gunpowder	nanite_compound	# 5
# bootsoles	nanite_compound	buckshot	# 2
# bootsoles	nanite_compound	gunpowder	# 5
# buckshot	bootsoles	dragon's_blood	# 7
# buckshot	bootsoles	nanite_compound	# 2
# buckshot	dragon's_blood	bootsoles	# 7
# buckshot	gunpowder	titanium_rod	# 1
# buckshot	nanite_compound	bootsoles	# 2
# buckshot	titanium_rod	gunpowder	# 1
# dragon's_blood	anointing_oil	flaming_phial	# 4
# dragon's_blood	anointing_oil	nanite_compound	# 6
# dragon's_blood	bootsoles	buckshot	# 7
# dragon's_blood	buckshot	bootsoles	# 7
# dragon's_blood	flaming_phial	anointing_oil	# 4
# dragon's_blood	nanite_compound	anointing_oil	# 6
# flaming_phial	anointing_oil	dragon's_blood	# 4
# flaming_phial	anointing_oil	titanium_rod	# 3
# flaming_phial	dragon's_blood	anointing_oil	# 4
# flaming_phial	gunpowder	titanium_rod	# 8
# flaming_phial	titanium_rod	anointing_oil	# 3
# flaming_phial	titanium_rod	gunpowder	# 8
# gunpowder	bootsoles	nanite_compound	# 5
# gunpowder	buckshot	titanium_rod	# 1
# gunpowder	flaming_phial	titanium_rod	# 8
# gunpowder	nanite_compound	bootsoles	# 5
# gunpowder	titanium_rod	buckshot	# 1
# gunpowder	titanium_rod	flaming_phial	# 8
# nanite_compound	anointing_oil	dragon's_blood	# 6
# nanite_compound	bootsoles	buckshot	# 2
# nanite_compound	bootsoles	gunpowder	# 5
# nanite_compound	buckshot	bootsoles	# 2
# nanite_compound	dragon's_blood	anointing_oil	# 6
# nanite_compound	gunpowder	bootsoles	# 5
# titanium_rod	anointing_oil	flaming_phial	# 3
# titanium_rod	buckshot	gunpowder	# 1
# titanium_rod	flaming_phial	anointing_oil	# 3
# titanium_rod	flaming_phial	gunpowder	# 8
# titanium_rod	gunpowder	buckshot	# 1
# titanium_rod	gunpowder	flaming_phial	# 8


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



