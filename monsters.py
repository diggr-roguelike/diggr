import libtcodpy as libtcod
import libdiggrpy as dg
import copy



class Monster:
    def __init__(self, name, skin=('x', libtcod.cyan), count=10, level=1,
                 attack=0.5, defence=0.5, explodeimmune=False, range=11,
                 itemdrop=None, heatseeking=False, desc=[], psyattack=0,
                 psyrange=0, confimmune=False, slow=False, selfdestruct=False,
                 straightline=False, stoneeating=False, sleepattack=False,
                 hungerattack=False, flying=False, radimmune=False, no_a=False,
                 summon=False, branch=None, fireimmune=False, poisimmune=False,
                 flavor=None, idtag=None, static=False, moldspew=None, is_mold=False,
                 boulder=False, inanimate=False, large=False, moon=None, fleerange=None,
                 no_exting=False, raise_dead=None, bloodsucker=None, summononce=None,
                 pointscontrib=1, pointsfac=1, fast=False, blink_away=None):
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
        self.radimmune = radimmune
        self.no_a = no_a
        self.summon = summon
        self.branch = branch
        self.fireimmune = fireimmune
        self.poisimmune = poisimmune
        self.flavor = flavor
        self.static = static
        self.moldspew = moldspew
        self.is_mold = is_mold
        self.boulder = boulder
        self.inanimate = inanimate
        self.large = large
        self.moon = moon
        self.fleerange = fleerange
        self.no_exting = no_exting
        self.raise_dead = raise_dead
        self.bloodsucker = bloodsucker
        self.summononce = summononce
        self.pointscontrib = pointscontrib
        self.pointsfac = pointsfac
        self.fast = fast
        self.blink_away = blink_away

        if not idtag:
            self.idtag = name
        else:
            self.idtag = idtag

        self.reset()

    def reset(self):
        self.xy = (0, 0)
        self.known_pxy = (None, None)
        self.do_move = None
        self.do_die = False
        self.hp = 3.0
        self.items = []
        self.confused = 0
        self.glued = 0
        self.visible = False
        self.visible_old = False
        self.was_seen = False
        self.gencount = 0
        self.onfire = 0
        self.bld_delta = None
        self.fleetimeout = 0


    def __str__(self):
        s = self.name
        if not self.no_a:
            if s[0] in 'aeiouAEIOU':
                s = 'an ' + s
            else:
                s = 'a ' + s
        if self.onfire:
            s += ' (on fire)'
        return s


class MonsterStock:
    def __init__(self):
        self.monsters = {}

        # Probabilities, of the N/9 form.
        # : (New, waxing, Quarter, waxing, Full, waning, Quarter, waning)

        newmoon_aligned  = (9, 7, 5, 3, 1, 3, 5, 7)
        fullmoon_aligned = (1, 3, 5, 7, 9, 7, 5, 3)
        quartermoon_bias = (5, 7, 2, 7, 9, 7, 2, 7)

        newmoon_only     = (9, 0, 0, 0, 0, 0, 0, 0)
        fullmoon_only    = (0, 0, 0, 0, 9, 0, 0, 0)
        quartermoon_only = (0, 0, 9, 0, 0, 0, 9, 0)

        # Megafauna dungeon branch

        self.add(Monster('Australopithecus afarensis', skin=('h', libtcod.sepia),
                         branch='a', attack=0.1, defence=0.3, range=4, level=1,
                         itemdrop='booze', count=9, no_a=True,
                         desc=['An early hominid, this creature walked upright',
                               'but lacked the intelligence of the modern human.']))

        self.add(Monster('Calvatia gigantea', skin=('x', libtcod.white),
                         branch='a', attack=0.0, defence=0.2, range=1, level=1,
                         itemdrop='mushrooms', confimmune=True, count=8, no_a=True,
                         desc=['(Also known as the giant puffball.)',
                               'An edible mushroom about the same size, color and texture',
                               'as a volleyball.']))

        self.add(Monster('Meganeura monyi', skin=('X', libtcod.light_gray),
                         branch='a', attack=0.5, defence=1.7, range=5, level=2,
                         count=7, confimmune=True, no_a=True, flying=True, flavor='flying',
                         moon=newmoon_aligned,
                         desc=['One of the largest insects to have ever lived,',
                               'it is a relative of the modern-day dragonfly from',
                               'the Carboniferous period.',
                               "It's about the same size as a modern-day crow."]))

        self.add(Monster('Sus barbatus', skin=('q', libtcod.dark_sepia),
                         branch='a', attack=1.2, defence=0.6, range=4, level=2,
                         count=6, no_a=True, flavor='animal',
                         moon=fullmoon_aligned,
                         desc=['(Also known as the bearded pig.)',
                               'A species of pig. It is characterized by its beard-like',
                               'facial hair. It is native to the tropics.']))

        self.add(Monster('Dinornis giganteus', skin=('B', libtcod.light_sepia),
                         branch='a', attack=1.0, defence=0.5, range=7, level=2,
                         count=5, no_a=True, flavor='animal',
                         moon=newmoon_aligned,
                         desc=['(Also known as the giant moa.)',
                               'A gigantic flightless bird, like the modern-day',
                               'ostrich, only about twice as big.']))

        self.add(Monster('Megatherium americanum', skin=('Q', libtcod.light_amber),
                         branch='a', attack=0.5, defence=3.5, range=5, level=3,
                         count=6, no_a=True, slow=True, flavor='animal', large=True,
                         moon=fullmoon_aligned,
                         desc=['A gigantic ground sloth from the Pliocene period.',
                               'It was one of the largest land animals to ever live,',
                               'larger than the modern-day African elephant.']))

        self.add(Monster('Argentavis magnificens', skin=('B', libtcod.dark_blue),
                         branch='a', attack=3.0, defence=0.3, range=17, level=3,
                         count=6, no_a=True, flying=True, flavor='flying',
                         moon=newmoon_aligned,
                         desc=['The largest flying bird to have ever lived.',
                               'A relative of the modern-day Andean condor,',
                               'this bird had a wingspan of 7 meters and weighed',
                               'up to 80 kilograms.']))

        self.add(Monster('Bos primigenius', skin=('Q', libtcod.lightest_gray),
                         branch='a', attack=7.0, defence=1.0, range=10, level=3,
                         count=3, no_a=True, flavor='animal', 
                         moon=fullmoon_aligned,
                         desc=['(Also known as the aurochs.)',
                               'This magnificent animal was the ancesor of modern-day',
                               'domestic cattle. It is much larger and stronger than any',
                               'domestic bull.']))

        self.add(Monster('Crocodylus porosus', skin=('R', libtcod.green),
                         branch='a', attack=5.0, defence=3.0, range=9, level=4,
                         moon=newmoon_aligned,
                         count=7, no_a=True, slow=True, heatseeking=True, flavor='snake',
                         desc=['(Also known as the saltwater crocodile.)',
                               'The largest of all living reptiles.']))

        self.add(Monster('Varanus komodoensis', skin=('R', libtcod.gray),
                         branch='a', attack=2.0, defence=2.0, range=9, level=4,
                         count=7, no_a=True, flavor='snake',
                         moon=newmoon_aligned,
                         desc=['(Also known as the Komodo dragon.)',
                               'Not as large as a crocodile, this truly huge',
                               'lizard is still a fearsome opponent.']))

        self.add(Monster('Colossochelys atlas', skin=('O', libtcod.darkest_green),
                         branch='a', attack=1.0, defence=24.0, explodeimmune=True,
                         range=10, confimmune=True, slow=True, level=5, count=4, no_a=True,
                         flavor='giant', large=True,
                         moon=fullmoon_aligned,
                         desc=['The largest land turtle, ever.',
                               'Found in the Pleistoce perood, it is the size and weight',
                               'of your average SUV vehicle.']))

        self.add(Monster('Gigantophis garstini', skin=('S', libtcod.green),
                         branch='a', attack=4.0, defence=1.0, range=20, level=5, count=9, no_a=True,
                         heatseeking=True, confimmune=True, flavor='snake',
                         moon=newmoon_aligned,
                         desc=['One of the largest snakes known, it is an almost',
                               '10 meter long ancient relative of the modern boa constrictor.']))

        self.add(Monster('Arctotherium bonariense', skin=('Q', libtcod.dark_sepia),
                         branch='a', attack=10.0, defence=2.0, range=10, level=6, count=3, no_a=True,
                         flavor='carnivore', large=True,
                         moon=fullmoon_aligned,
                         desc=['The most fearsome mammal to have ever lived, this bear',
                               'lived during the Pleistocene epoch.',
                               'It is more than twice the size of the modern-day grizzly bear.']))

        self.add(Monster('Glyptodon perforatus', skin=('o', libtcod.brass),
                         branch='a', attack=0.2, defence=20.0, range=7, count=7, no_a=True,
                         explodeimmune=True, level=6, heatseeking=True, flavor='giant', large=True,
                         moon=fullmoon_aligned,
                         desc=['A relative of the armadillo from the Pleistocene epoch.',
                               'Unlike the modern armadillos, this armored monstrocity is',
                               'the size and weight of a car.']))

        self.add(Monster('Pteranodon longiceps', skin=('B', libtcod.lightest_lime),
                         branch='a', attack=3.0, defence=4.0, range=10, level=7, count=8,
                         no_a=True, flavor='flying', large=True,
                         moon=newmoon_aligned,
                         desc=['A flying reptile that had a wingspan of over 6 meters!',
                               'It was a very common animal during the Cretaceous period.']))

        self.add(Monster('Hippopotamus gorgops', skin=('Q', libtcod.light_azure),
                         branch='a', attack=8.0, defence=2.0, range=4, level=7, count=5, no_a=True,
                         flavor='animal', large=True,
                         moon=fullmoon_aligned,
                         desc=['This hippo from the Miocene period was much, much larger than',
                               'its modern-day living relatives.']))

        self.add(Monster('Velociraptor mongoliensis', skin=('d', libtcod.yellow),
                         branch='a', attack=1.5, defence=1.0, range=20, level=8, count=24,
                         no_a=True, summon=('Velociraptor mongoliensis', 4),
                         flavor='animal',
                         desc=['A small theropod from the Cretaceous period.',
                               'It is about the size of a chicken and is covered with',
                               'bright, feathery plumage. It has a relatively large, ',
                               'dangerous-looking beak.',
                               'It was also a vicious pack-hunting carnivore.']))

        self.add(Monster('Titanoceratops ouranos', skin=('D', libtcod.sepia), branch='a',
                         attack=11.0, defence=4.0, range=3, level=8, count=8,
                         no_a=True, flavor='giant', large=True,
                         moon=fullmoon_aligned,
                         desc=['The largest of many species of triceratops.',
                               'You recognize the familiar triceratops profile from',
                               'numerous film, cartoon and book descriptions of this',
                               'dinosaur.']))

        self.add(Monster('Indricotherium transouralicum', skin=('Q', libtcod.sepia),
                         branch='a', attack=1.0, defence=6.0, range=7, level=9, count=6,
                         no_a=True, flavor='giant', large=True,
                         moon=fullmoon_aligned,
                         desc=['Named after the mystical Indrik-Beast, this is the ',
                               'largest land mammal ever to have lived!',
                               'A relative of the rhinoceros, it looks like a ridiculously',
                               'muscled cross between wooly mammoth and a giraffe.',
                               'Its long neck reaches to 8 meters in height, more than',
                               'a 3-story building!']))

        self.add(Monster('Mammuthus primigenius', skin=('Q', libtcod.darker_amber),
                         branch='a', attack=3.0, defence=4.0, range=6, level=9, count=6,
                         no_a=True, flavor='giant', large=True,
                         moon=newmoon_aligned,
                         desc=['Also known as the wooly mammoth.']))

        self.add(Monster('Tyrannosaurus rex', skin=('D', libtcod.light_lime), branch='a',
                         attack=15.0, defence=15.0, range=20, level=10, count=1, no_a=True,
                         confimmune=True, flavor='carnivore', large=True,
                         moon=newmoon_aligned,
                         desc=['The Tyrant Lizard King, in person. No introduction necessary.']))

        self.add(Monster('Sauroposeidon proteles', skin=('D', libtcod.light_azure), branch='a',
                         attack=1.0, defence=64.0, range=10, level=11, count=1, no_a=True,
                         slow=True, confimmune=True, explodeimmune=True, radimmune=True,
                         flavor='earthshake', large=True,
                         moon=fullmoon_aligned,
                         desc=['The Earthshaker-Lizard. A sauropod so truly, veritably huge that',
                               'it might have indeed caused earthquakes merely by walking.',
                               "Also, the World's Largest Dinosaur.",
                               'For a creature so large, researchers have wondered how it survived',
                               'with its tiny brain.']))

        # Eldritch/Faerie dungeon branch

        self.add(Monster('gibbering maniac', skin=('h', libtcod.gray),
                         attack=0.3, defence=0.1, range=3, level=1,
                         itemdrop='booze', count=7, branch='b',
                         desc=['Eldritch horrors have driven this poor wretch',
                               'to the cusp of insanity.',
                               "He's probably an alumnus of Miskatonic University."]))

        self.add(Monster('chanterelle', skin=('x', libtcod.orange),
                         attack=0.0, defence=0.3, range=1, level=1,
                         itemdrop='mushrooms', confimmune=True, count=6, branch='b',
                         desc=['It looks delicious.']))

        self.add(Monster('brownie', skin=('h', libtcod.light_red),
                         attack=1.5, defence=0.2, range=8, level=2, count=4, branch='b',
                         flavor='faerie',
                         moon=fullmoon_aligned,
                         desc=['Once a friendly house spirit, this small fey humanoid',
                               'has been driven to hate humanity after years of neglect',
                               'and abuse by its master.']))

        self.add(Monster('pixie', skin=('h', libtcod.green),
                         attack=1.0, defence=0.7, range=6, level=2, count=4, branch='b',
                         flavor='faerie',
                         moon=fullmoon_aligned,
                         desc=['A magical creature that has been driven underground',
                               'by human pollution and habitat loss.']))

        self.add(Monster('sprite', skin=('f', libtcod.light_lime),
                         attack=0.5, defence=0.9, range=8, level=2, count=3, branch='b',
                         poisimmune=True, flavor='faerie',
                         moon=newmoon_aligned,
                         desc=['A ghost of a dead faerie.']))

        self.add(Monster('nematode', skin=('w', libtcod.yellow),
                         attack=0, psyattack=2.0, defence=0.1, range=30, psyrange=4,
                         level=3, count=5, branch='b', flavor='snake',
                         moon=newmoon_aligned,
                         desc=['A gigantic (5 meter long) yellow worm.',
                               'It has no visible eyes, but instead has a ',
                               'giant, bulging, pulsating brain.']))

        self.add(Monster('shoggoth', skin=('x', libtcod.dark_sepia),
                         attack=0.7, psyattack=0.5, defence=0.6, range=5, psyrange=3, level=3,
                         count=3, branch='b', flavor='weird',
                         moon=newmoon_aligned,
                         desc=['A creature of a terrible servant race created by the',
                               'Elder Things. A shapeless congeries of protoplasmic',
                               'bubbles, faintly self-luminous.']))

        self.add(Monster('ghost', skin=('h', libtcod.dark_grey),
                         attack=0.5, defence=2.5, range=7, level=3,
                         hungerattack=True, count=3, branch='b', fireimmune=True,
                         poisimmune=True, flavor='air',
                         moon=newmoon_aligned,
                         desc=['A spirit of an adventurer that perished in these',
                               'terrible and wondorous caves.',
                               'Its eyes are glowing with a malignant hunger.']))

        self.add(Monster('satyr', skin=('h', libtcod.light_sepia),
                         attack=7.0, defence=0.01, range=5, level=4,
                         count=4, branch='b', flavor='weird',
                         moon=fullmoon_aligned,
                         desc=["A savage worshipper of the Mad God Dionysus.",
                                'He is completely naked and gibbering wildly.']))

        self.add(Monster('sylphid', skin=('f', libtcod.light_blue),
                         attack=1.4, defence=1.4, range=4, level=4,
                         count=4, psyattack=0.1, psyrange=10, branch='b',
                         flavor='air',
                         moon=fullmoon_aligned,
                         desc=['An air elemental. It takes the form of a beautiful',
                               'young woman.']))

        self.add(Monster('chthonian', skin=('W', libtcod.dark_blue),
                         attack=4.0, psyattack=2.0, defence=1.0, range=8, psyrange=2,
                         level=5, count=4, straightline=True, stoneeating=True, branch='b',
                         flavor='weird',
                         moon=newmoon_aligned,
                         desc=['An immense squid-like creature that burrows in the',
                               "dark, loathsome depths of the Earth's crust.",
                               'It is covered in slime and is accompanied by a faint',
                               'chanting sound.']))

        self.add(Monster('gnophkeh', skin=('h', libtcod.gray),
                         attack=7.0, defence=1.0, range=18,
                         level=5, count=4, branch='b', flavor='weird',
                         moon=newmoon_aligned,
                         desc=['A member of a race of disgusting, hairy cannibal humanoids.']))

        self.add(Monster('sleep faerie', skin=('f', libtcod.light_pink),
                         attack=1.0, defence=1.0, range=9, level=6, count=5,
                         sleepattack=True, flying=True, branch='b',
                         flavor='faerie',
                         moon=fullmoon_aligned,
                         desc=["A tiny fay creature dressed in pink ballet clothes.",
                               "It looks adorable."]))

        self.add(Monster('aelf', skin=('f', libtcod.green),
                         attack=3.0, defence=2.0, range=20, level=6, count=5,
                         confimmune=True, flying=True, branch='b', fireimmune=True,
                         moon=fullmoon_aligned,
                         flavor='faerie',
                         desc=["A faery creature from the elemental plane of Aelfrice."]))

        self.add(Monster('leipreachan', skin=('f', libtcod.azure),
                         attack=2.5, defence=1.5, range=9, level=7, count=5,
                         moon=fullmoon_aligned,
                         hungerattack=True, branch='b', flavor='faerie',
                         desc=['A fay creature in the form of a dirty, lecherous old man.']))

        self.add(Monster('black knight', skin=('k', libtcod.darker_grey),
                         attack=6.0, defence=4.5, range=8, level=7, count=6, branch='b',
                         flavor='humanwarrior',
                         moon=newmoon_aligned,
                         desc=['An evil humanoid in black cast-iron armor.',
                               'He is armed with a longsword.']))

        self.add(Monster('frost giant', skin=('k', libtcod.lighter_sky),
                         attack=6.0, defence=4.5, range=8, level=8, count=5, branch='b',
                         flavor='giant', large=True,
                         moon=fullmoon_aligned,
                         desc=['A humanoid about twice the size of a human.',
                               'He is an evil, emotionless immigrant from the dark',
                               'planes of Jotunheim.']))

        self.add(Monster('Oberon', skin=('F', libtcod.purple),
                         attack=3.0, defence=3.0, range=10, level=9, count=1,
                         flying=True, explodeimmune=True, confimmune=True,
                         psyrange=8, psyattack=2.0, branch='b', no_a=True,
                         flavor='faerie', large=True,
                         moon=fullmoon_aligned,
                         desc=['A faerie king.',
                               'He takes on the appearance of a 2 meter tall',
                               'handsome man, wearing a delicate crown.']))

        self.add(Monster('Caliban', skin=('H', libtcod.sea),
                         attack=7.0, defence=7.0, range=10, level=9, count=1,
                         confimmune=True, branch='b', no_a=True,
                         flavor='humanweird',
                         moon=fullmoon_aligned,
                         desc=["A deformed beast-man. Half-devil on his father's side,"
                               'he is a resentful slave of Prospero.']))

        self.add(Monster('Prospero', skin=('H', libtcod.purple),
                         attack=2.0, defence=7.0, range=20, level=10, count=1,
                         explodeimmune=True, flying=True, confimmune=True,
                         psyrange=2, psyattack=2.0, branch='b',
                         summon=('black knight', 2), no_a=True,
                         poisimmune=True, flavor=None, large=True,
                         moon=fullmoon_aligned,
                         desc=["Self-styled royalty, self-styled wizard, self-styled",
                               'ruler of this dungeon.',
                               'He has instilled unthinking loyalty into his subjects',
                               'and slaves.']))

        self.add(Monster('Yog-Sothoth', skin=('X', libtcod.pink),
                         attack=2.0, defence=7.0, range=20, level=11, count=1,
                         explodeimmune=True, flying=True, confimmune=True,
                         psyrange=20, psyattack=2.0, branch='b', fireimmune=True,
                         summon=('Prospero', 2), no_a=True, poisimmune=True,
                         flavor='weird', large=True,
                         moon=newmoon_aligned,
                         desc=['An Outer God: The Lurker at the Threshold, The Key and the Gate,',
                               'The Beyond One, Opener of the Way, The All-in-One',
                               'and the One-in-All.',
                               ' "Only a congeries of iridescent globes, yet stupendous',
                               '  in its malign suggestiveness."']))


        # Cyberspace dungeon branch.


        self.add(Monster('cyberpunk', skin=('h', libtcod.light_purple),
                         attack=0.2, defence=0.1, range=4, level=1,
                         itemdrop='booze', count=6, branch='c',
                         desc=['Stoned out of his gourd, he is chatting with his avatar',
                               'in cyberspace while wearing VR glasses.']))

        self.add(Monster('cramration', skin=('x', libtcod.pink),
                         attack=0.0, defence=0.2, range=1, level=1,
                         itemdrop='mushrooms', confimmune=True, count=6, branch='c',
                         desc=['A mushroom/pork genetically engineered vegetarian',
                               'food ration. It sports tiny legs.']))

        self.add(Monster('snorlax', skin=('v', libtcod.purple),
                         attack=1.0, defence=1.2, range=5, slow=True, level=2, count=5,
                         branch='c', flavor='digital',
                         moon=fullmoon_aligned,
                         desc=['A 2 meter tall, enourmously obese creature of',
                               'some indeterminate cat-bear-dog race. It has',
                               'a pinkish-purple hide.']))

        self.add(Monster('charizard', skin=('v', libtcod.green),
                         attack=1.0, defence=0.4, range=8, level=2, count=5,
                         branch='c', flavor='digital',
                         moon=fullmoon_aligned,
                         desc=['A creature of indeterminate race, looking like',
                               'some sort of small dragonish flying reptile.',
                               'It is greenish in color.']))

        self.add(Monster('squirtle', skin=('v', libtcod.light_blue),
                         attack=0.4, defence=1.0, range=6, level=2, count=7,
                         heatseeking=True, branch='c', flavor='digital',
                         moon=fullmoon_aligned,
                         desc=['A bluish creature of indeterminate race.',
                               'It looks like a cute turtle.']))

        self.add(Monster('spore plant', skin=('x', libtcod.dark_yellow),
                         attack=0.3, defence=0.2, range=7, level=3,
                         itemdrop='bomb', confimmune=True, count=7,
                         heatseeking=True, branch='c', flavor=None,
                         moon=newmoon_aligned,
                         desc=['A large plantlike carnivorous creature.',
                               'It has large bulbous appendages growing out of its stalk.',
                               'It looks like it is radiating heat from the inside.']))

        self.add(Monster('scavenger drone', skin=('Z', libtcod.silver),
                         attack=1.0, defence=24.0, explodeimmune=True, range=10,
                         confimmune=True, slow=True, level=3, count=4, branch='c',
                         fireimmune=True, poisimmune=True, flavor='robot', 
                         moon=newmoon_aligned,
                         desc=['A remotely-controlled robot used for exploring the dungeon.']))

        self.add(Monster('memetic virus', skin=('v', libtcod.dark_gray),
                         attack=0.3, defence=0.3, explodeimmune=True, radimmune=True,
                         branch='c', fireimmune=True, poisimmune=True, flavor=None,
                         range=30, level=3, count=16, summon=('memetic virus', 5),
                         moon=fullmoon_aligned,
                         desc=["It doesn't exist. It's a memetic virus."]))

        self.add(Monster('spore', skin=('x', libtcod.pink),
                         attack=0, defence=0.2, range=30, level=4,
                         itemdrop='bomb', heatseeking=True, selfdestruct=True,
                         confimmune=True, count=7, flying=True, branch='c', flavor='air',
                         moon=newmoon_aligned,
                         desc=['A pulsating pink spherical spore, about 1 meter in diameter.',
                               'It is levitating.',
                               'It looks like it is radiating heat from the inside.']))

        self.add(Monster('xenomorph', skin=('X', libtcod.silver),
                         attack=7.0, defence=7.0, range=5, level=4,
                         count=2, confimmune=True, radimmune=True, branch='c', fireimmune=True,
                         poisimmune=True, flavor='snake',
                         moon=newmoon_aligned,
                         desc=["A horrifying alien creature. It looks like a giant,",
                               "very evil insect. It is truly scary."]))

        self.add(Monster('cthulhumon', skin=('v', libtcod.gray),
                         attack=3.0, psyattack=2.0, defence=1.0, range=8, psyrange=8,
                         level=5, confimmune=True, count=4, branch='c', flavor='digital',
                         moon=newmoon_aligned,
                         desc=['The other Pokemon nobody told you about.']))

        self.add(Monster('cyberdemon', skin=('Z', libtcod.red),
                         attack=7.0, defence=2.0, range=4, level=5, count=2,
                         explodeimmune=True, summon=('spore', 2), branch='c',
                         flavor='robot', large=True,
                         moon=newmoon_aligned,
                         desc=['A 3 meter tall hellish demon-robot hybrid.',
                               'Fleshy parts of its demonic body have rotted away,',
                               'to be replaced with crude stainless-steel robotic parts.']))

        self.add(Monster('shai-hulud', skin=('W', libtcod.gray),
                         attack=2.0, defence=4.5, explodeimmune=True, range=30,
                         level=6, count=4, straightline=True, stoneeating=True,
                         heatseeking=True, branch='c', flavor='giant', large=True,
                         moon=fullmoon_aligned,
                         desc=['A giant worm. It is gray in color and has a skin made of something like granite.',
                               'It is about 15 meters in length.']))

        self.add(Monster('klingon', skin=('k', libtcod.brass),
                         attack=5.0, defence=0.5, range=5, level=6,
                         count=5, branch='c', flavor='humanwarrior',
                         moon=fullmoon_aligned,
                         desc=["A member of a chivalrous warrior race of extraterrestrial aliens."]))

        self.add(Monster('autobot', skin=('z', libtcod.silver),
                         attack=1.5, defence=1.5, range=15, level=7,
                         itemdrop='bomb', confimmune=True, radimmune=True,
                         explodeimmune=True, count=7, branch='c', poisimmune=True,
                         flavor='robot',
                         moon=fullmoon_aligned,
                         desc=['An extraterrestrial sentient robot from the planet',
                               'Cybertron. Powered by the energy source Nucleon,',
                               'he fights for intergalactic Good.']))

        self.add(Monster('T-1 terminator', skin=('z', libtcod.lightest_sepia),
                         attack=0.4, defence=0.4, range=7, level=7,
                         itemdrop='radblob', confimmune=True, count=7,
                         radimmune=True, heatseeking=True, branch='c', fireimmune=True,
                         poisimmune=True, flavor='robot',
                         moon=newmoon_aligned,
                         desc=["The very first model in Cyberdine's robot-killer lineup.",
                               '(Brought to you by Skynet.)']))

        self.add(Monster('decepticon', skin=('z', libtcod.dark_gray),
                         attack=1.5, defence=1.5, range=15, level=8,
                         confimmune=True, radimmune=True, branch='c',
                         explodeimmune=True, count=7, summon=('autobot', 3),
                         poisimmune=True, flavor='robot',
                         moon=newmoon_aligned,
                         desc=['An extraterrestrial sentient robot from the planet',
                               'Cybertron. Powered by the energy source Nucleon,',
                               'he fights for intergalactic Evil.']))

        self.add(Monster('triffid', skin=('x', libtcod.peach),
                         attack=2.0, defence=2.0, range=5, level=8, count=16,
                         itemdrop='triffidlarva', confimmune=True, branch='c',
                         flavor=None,
                         moon=fullmoon_aligned,
                         desc=['A carnivorous plant. It is a sneaky pest that is very',
                               'hard to get rid of.']))

        self.add(Monster('mosura-chan', skin=('x', libtcod.dark_lime),
                         attack=0, defence=0.2, range=30, level=9,
                         itemdrop='radblob', selfdestruct=True,
                         radimmune=True, explodeimmune=True, branch='c',
                         confimmune=True, count=16, flying=True, no_a=True,
                         flavor='flying',
                         moon=fullmoon_aligned,
                         desc=['A bird-sized, moth-like creature.',
                               'It has a strange green glow.']))

        self.add(Monster('Wintermute', skin=('V', libtcod.azure),
                         attack=0.5, defence=4.0, range=30, sleepattack=True,
                         confimmune=True, explodeimmune=True, radimmune=True, flying=True,
                         no_a=True, count=2, level=9, branch='c', fireimmune=True,
                         poisimmune=True, flavor='digital', large=True,
                         moon=newmoon_aligned,
                         desc=["A manifestation of the powerful AI construct named 'Wintermute'."]))

        self.add(Monster('Voltron', skin=('Z', libtcod.white),
                         attack=6.0, defence=5.0, range=5, level=10, count=1, no_a=True,
                         explodeimmune=True, confimmune=True, branch='c', heatseeking=True,
                         fireimmune=True, poisimmune=True, flavor='robot', large=True,
                         moon=fullmoon_aligned,
                         desc=['Defender of the Universe.']))

        self.add(Monster('Gojira-sama', skin=('G', libtcod.green),
                         attack=6.0, defence=5.0, range=10, level=11, count=1,
                         radimmune=True, explodeimmune=True, branch='c', no_a=True,
                         summon=('mosura-chan', 3), itemdrop=['gbomb', 'radsuit'],
                         flavor='earthshake', large=True,
                         moon=newmoon_aligned,
                         desc=['She really hates Japan after what they did',
                               'to the nuclear power plant.']))

        # Urthian dungeon branch.


        self.add(Monster('omophagist', skin=('h', libtcod.dark_purple),
                         attack=0.3, defence=0.1, range=4, level=1,
                         count=4, branch='d',
                         desc=['A poor, degenerate inhabitant of the poorest parts of the City.',
                               '(Those parts that are composed of mostly ancient ruins.)',
                               'He might be a little insane and a cannibal, as well.']))

        self.add(Monster('avern', skin=('x', libtcod.green),
                         attack=0.3, defence=0.01, range=1, level=1,
                         itemdrop='avern', confimmune=True, count=4, branch='d',
                         desc=['A poisonous, carnivorous species of plant.',
                               '(It might actually be at least in part an animal.)']))

        self.add(Monster('armiger', skin=('k', libtcod.silver),
                         attack=2.0, defence=1.0, range=8, level=2,
                         count=4, branch='d', flavor='humanwarrior',
                         desc=['A member of the warrior caste.']))

        self.add(Monster('exultant', skin=('h', libtcod.gold),
                         attack=0.5, defence=0.5, range=8, level=2,
                         count=3, branch='d', summon=('armiger', 2),
                         flavor='humanwarrior',
                         desc=['A member of the nobility caste.']))

        self.add(Monster('aquastor', skin=('v', libtcod.gray),
                         attack=1.5, defence=1.0, range=10, level=3, count=4,
                         hungerattack=True, branch='d', flying=True, poisimmune=True,
                         flavor=None,
                         moon=newmoon_aligned,
                         desc=['An entity formed by the power of a concentrated thought',
                               'and which assumed a physical form.']))

        self.add(Monster('eidolon', skin=('v', libtcod.white),
                         attack=0.0, defence=2.0, range=8, level=3,
                         count=4, psyattack=1.5, psyrange=7, branch='d', flying=True,
                         fireimmune=True, poisimmune=True, flavor='faerie',
                         moon=fullmoon_aligned,
                         desc=["A spirit-image of a living or dead person;",
                               "a shade or phantom look-alike of the human form."]))

        self.add(Monster('destrier', skin=('q', libtcod.dark_gray),
                         attack=2.5, defence=1.5, range=6, level=4, count=3,
                         branch='d', flavor='carnivore',
                         moon=fullmoon_aligned,
                         desc=['A mount; A highly modified horse, possessing',
                               'clawed feet (for better traction) and large canine teeth.',
                               'It is carnivorous.']))

        self.add(Monster('cacogen', skin=('u', libtcod.silver),
                         attack=0.5, defence=1.0, range=10, level=4, count=3,
                         summon=('eidolon', 2), itemdrop='radblob',
                         branch='d', poisimmune=True, flavor='humanweird',
                         moon=fullmoon_aligned,
                         desc=['In fact an extraterrestrial who disguises itself as an',
                               'urthly monster.']))

        self.add(Monster('ascian', skin=('h', libtcod.gray),
                         attack=2.0, defence=1.0, range=5, level=5,
                         psyattack=1.5, psyrange=10,
                         count=4, branch='d', flavor='weird',
                         moon=newmoon_aligned,
                         desc=['A human from Ascia, the tyrannical empire ruled',
                               'by the evil Abaia. His mind is warped to the point',
                               'where he cannot any longer speak or understand any',
                               'real human language.']))

        self.add(Monster('smilodon', skin=('Q', libtcod.dark_orange),
                         attack=2.5, defence=1.5, range=12, level=5, count=3,
                         branch='d', flavor='carnivore',
                         moon=fullmoon_aligned,
                         desc=['An ancient genetically-engineered feline animal.',
                               'It looks somewhat like the familiar sabre-toothed tiger.']))

        self.add(Monster('alzabo', skin=('u', libtcod.darkest_red),
                         attack=2.0, defence=2.0, range=12, level=6, count=3,
                         branch='d', itemdrop='alzabobrain', flavor='carnivore',
                         moon=newmoon_aligned,
                         desc=[' "The red orbs of the alzabo were something more, neither',
                               '  the intelligence of humankind nor the the innocence of',
                               '  the brutes. So a fiend might look, I thought, when it had',
                               '  at last struggled up from the pit of some dark star."']))

        self.add(Monster('undine', skin=('u', libtcod.darkest_blue),
                         attack=0.7, defence=3.0, range=10, level=6, count=5,
                         sleepattack=True, branch='d', flavor='snake', large=True,
                         moon=newmoon_aligned,
                         desc=["A monstrous slave-servant of its megetherian overlords.",
                               'It looks like humongous, deformed mermaid.']))

        self.add(Monster('Scylla', skin=('U', libtcod.white),
                         attack=10, defence=10, range=15, level=7, count=1,
                         branch='d', no_a=True, flavor='giant', large=True,
                         desc=['A megatherian: an evil, immortal, gigantic creature of',
                               'possibly extraterrestrial origin. They are hellbent on ruling',
                               'Urth. They are powerful enough and amoral enough to be',
                               'essentially equal to gods.']))

        self.add(Monster('Uroboros', skin=('U', libtcod.light_green),
                         attack=10, defence=10, range=15, level=8, count=1,
                         branch='d', confimmune=True, no_a=True, flavor='giant', large=True,
                         desc=['A megatherian: an evil, immortal, gigantic creature of',
                               'possibly extraterrestrial origin. They are hellbent on ruling',
                               'Urth. They are powerful enough and amoral enough to be',
                               'essentially equal to gods.']))

        self.add(Monster('Erebus', skin=('U', libtcod.light_pink),
                         attack=10, defence=10, range=15, level=9, count=1,
                         branch='d', confimmune=True, explodeimmune=True, no_a=True,
                         fireimmune=True, flavor='giant', large=True,
                         desc=['A megatherian: an evil, immortal, gigantic creature of',
                               'possibly extraterrestrial origin. They are hellbent on ruling',
                               'Urth. They are powerful enough and amoral enough to be',
                               'essentially equal to gods.']))

        self.add(Monster('Arioch', skin=('U', libtcod.light_sky),
                         attack=10, defence=10, range=15, level=10, count=1, no_a=True,
                         branch='d', confimmune=True, explodeimmune=True, radimmune=True,
                         fireimmune=True, flavor='earthshake', large=True,
                         desc=['A megatherian: an evil, immortal, gigantic creature of',
                               'possibly extraterrestrial origin. They are hellbent on ruling',
                               'Urth. They are powerful enough and amoral enough to be',
                               'essentially equal to gods.']))

        self.add(Monster('Abaia', skin=('U', libtcod.grey),
                         attack=10, defence=10, range=15, level=11, count=1,
                         branch='d', confimmune=True, explodeimmune=True, radimmune=True,
                         fireimmune=True, flavor='earthshake', large=True,
                         summon=('undine', 3), no_a=True, itemdrop='gluegun',
                         desc=['A megatherian: an evil, immortal, gigantic creature of',
                               'possibly extraterrestrial origin. They are hellbent on ruling',
                               'Urth. They are powerful enough and amoral enough to be',
                               'essentially equal to gods.']))

        # Hyborian dungeon branch

        self.add(Monster('peasant', skin=('h', libtcod.dark_sepia),
                         attack=0.1, defence=0.2, range=3, level=1,
                         itemdrop='booze', count=9, branch='e',
                         desc=["He's dirty, suspicious and closed-minded."]))

        self.add(Monster('lichen', skin=('x', libtcod.light_purple),
                         attack=0.3, defence=0.2, range=1, level=1, branch='e',
                         itemdrop='mushrooms', confimmune=True, count=9,
                         desc=['Looks yummy.']))

        self.add(Monster('Aquilonian marshall', skin=('h', libtcod.dark_blue),
                         attack=0.5, defence=0.5, range=6, level=2, count=8,
                         summon=('Aquilonian marshall', 5), branch='e',
                         flavor='humanwarrior',
                         moon=fullmoon_aligned,
                         desc=['A mercenary, sent from the Aquilonian cities on',
                               'the surface to partol these dangerous tunnels.']))

        self.add(Monster('giant spider', skin=('X', libtcod.gray),
                         attack=0.7, defence=0.7, range=5, level=2, count=8,
                         branch='e', flavor='snake',
                         moon=newmoon_aligned,
                         desc=['A huge, very ugly and disturbing spider.']))

        self.add(Monster('Turanian nomad', skin=('h', libtcod.orange),
                         attack=1.3, defence=0.4, range=7, level=2, count=8,
                         branch='e', flavor='humanwarrior',
                         moon=fullmoon_aligned,
                         desc=['A nomad from the boundless steppes of Turania.']))

        self.add(Monster('Cimmerian pirate', skin=('h', libtcod.red),
                         attack=1.2, defence=0.6, range=7, level=3, count=8,
                         branch='e', summon=('Cimmerian pirate', 4),
                         flavor='humanwarrior',
                         moon=fullmoon_aligned,
                         desc=['A cruel-hearted Cimmerian tribesman, turned to piracy',
                               'in search of loot and women.',
                               "The poor man is probably looking for treasure in these",
                               'caves.']))

        self.add(Monster('giant serpent', skin=('S', libtcod.darkest_lime),
                         attack=1.8, defence=0.5, range=9, level=3, count=8,
                         branch='e', flavor='snake',
                         moon=newmoon_aligned,
                         desc=['A malevolent nag, a giant snake borne from the',
                               'unholy mixture of human and cobra seed.']))

        self.add(Monster('Hyperborean barbarian', skin=('h', libtcod.peach),
                         attack=2.2, defence=0.9, range=6, level=3, count=6,
                         branch='e', flavor='humanwarrior',
                         desc=['A barbarian who hails from one of the hearty tribes',
                               'of great frosty Hyperborea.']))

        self.add(Monster('Stygian priest', skin=('h', libtcod.light_sepia),
                         attack=1.0, defence=1.0, range=8, level=4, count=6,
                         branch='e', summon=('giant serpent', 3),
                         flavor='wizard',
                         moon=newmoon_aligned,
                         desc=['Hailing from the banks of the river Stygs, he has',
                               'a swarthy complexion and sports a completely shaved head.',
                               'He is skilled in the arcane worship of the enigmatic',
                               'Stygian gods.']))

        self.add(Monster('giant slug', skin=('w', libtcod.purple),
                         attack=0.7, defence=2.8, range=4, level=4, count=10,
                         branch='e', summon=('giant slug', 2), flavor='snake',
                         moon=newmoon_aligned,
                         desc=['It is truly giant and truly disgusting.']))

        self.add(Monster('zombie', skin=('y', libtcod.silver),
                         attack=1.8, defence=2.9, range=3, level=4, count=10,
                         branch='e', poisimmune=True, flavor=None,
                         moon=newmoon_aligned,
                         desc=['A decomposed corpse brought back to unlife by',
                               'the darkest arts.']))

        self.add(Monster('Amazon warrior', skin=('h', libtcod.pink),
                         attack=1.8, defence=1.8, range=10, level=5, count=8,
                         branch='e', flavor='humanwarrior',
                         moon=fullmoon_aligned,
                         desc=['She is a woman-warrior from the enigmatic Amazonian tribe.',
                               'She hates men.']))

        self.add(Monster('wolf', skin=('q', libtcod.silver),
                         attack=3.5, defence=3.0, range=7, level=5, count=10,
                         branch='e', flavor='animal',
                         moon=fullmoon_aligned,
                         desc=['A man-eating wolf.']))

        self.add(Monster('Thulian price', skin=('h', libtcod.sky),
                         attack=1.0, defence=1.0, range=18, level=6, count=8,
                         branch='e', summon=('Amazon warrior', 1),
                         flavor='humanweird',
                         moon=fullmoon_aligned,
                         desc=['Ultima Thule is the mystical land of fancy and dark legend.',
                               "You're not sure he is really from Thule, much less a real price."]))

        self.add(Monster('cannibal', skin=('h', libtcod.dark_purple),
                         attack=2.0, defence=2.0, range=15, level=6, count=8,
                         branch='e', flavor='humanweird',
                         moon=newmoon_aligned,
                         desc=['A deranged human who developed an unnatural, unholy',
                               'addiction to human flesh.']))

        self.add(Monster('Lemurian wizard', skin=('h', libtcod.dark_han),
                         attack=1.2, defence=1.2, range=15, level=7, count=6,
                         branch='e', summon=('cannibal', 2),
                         flavor='wizard',
                         moon=newmoon_aligned,
                         desc=['Lemuria is the mythical island-empire of evil magicians',
                               'and demon-worshippers.']))

        self.add(Monster('apeman', skin=('h', libtcod.light_pink),
                         attack=2.5, defence=2.5, range=10, level=7, count=8,
                         branch='e', flavor='humanweird',
                         moon=fullmoon_aligned,
                         desc=['Part human, part ape, if he has any intelligence, then his',
                               'gaze does not betray any, only pure malevolence.']))

        self.add(Monster('Atlantian sorceror', skin=('h', libtcod.light_han),
                         attack=1.2, defence=1.2, range=15, level=8, count=6,
                         branch='e', summon=('evil demon', 2),
                         flavor='wizard',
                         moon=fullmoon_aligned,
                         desc=['Atlantis is another evil island-empire, the competitor',
                               'to Lemuria in the dark art of demon-worship.']))

        self.add(Monster('evil demon', skin=('Y', libtcod.red),
                         attack=1.0, defence=1.6, range=10, level=8, count=6,
                         branch='e', summon=('wolf', 2), fireimmune=True, poisimmune=True,
                         flavor='wizard',
                         moon=newmoon_aligned,
                         desc=['Summoned from the depths of Infernus to commit',
                               'unspeakable deeds of evil and hatred.']))

        self.add(Monster('carrion crawler', skin=('w', libtcod.white),
                         attack=2.0, defence=2.0, range=5, level=9, count=16,
                         itemdrop='cclarva', branch='e', poisimmune=True,
                         flavor='snake',
                         moon=newmoon_aligned,
                         desc=['A creature that looks like a maggot,',
                               'only a thousand times bigger.']))

        self.add(Monster('vampire', skin=('Y', libtcod.blue),
                         attack=2.5, defence=2.5, range=15, level=9, count=5,
                         branch='e', summon=('zombie', 1), poisimmune=True,
                         flavor='air', 
                         moon=newmoon_aligned,
                         desc=['One of the Elder Ones, the most ancient and powerful of',
                               'vampires.']))

        self.add(Monster('Conan', skin=('K', libtcod.sepia),
                         attack=7.5, defence=5.5, range=8, level=10, count=1,
                         confimmune=True,  branch='e', no_a=True,
                         flavor='humanwarrior', itemdrop='eyeofkali',
                         desc=['A well-muscled adventurer,',
                               'he looks like he just stepped off a movie poster.',
                               "He hates competition."]))

        self.add(Monster('Crom', skin=('K', libtcod.peach),
                         attack=7.5, defence=7.5, range=10, level=11, count=1,
                         explodeimmune=True, fireimmune=True, branch='e',
                         confimmune=True, summon=('Conan', 1), no_a=True, poisimmune=True,
                         flavor='earthshake', large=True, itemdrop='excalibur',
                         desc=['The most high god of all Cimmerians, Crom is the god',
                               'of valor and battle. He is a dark, vengeful and',
                               'judgemental god.']))

        # #
        self.add(Monster('acolyte of Kali', skin=('h', libtcod.gray),
                         attack=3.5, defence=2.5, range=8, level=7, count=3,
                         confimmune=True,  branch='qk', idtag='akali_1',
                         psyattack=0.15, psyrange=6,
                         desc=['A bloodthirsty worshipper of Kali Ma.']))

        self.add(Monster('acolyte of Kali', skin=('h', libtcod.gray),
                         attack=3.5, defence=2.5, range=10, level=8, count=3,
                         confimmune=True,  branch='qk', idtag='akali_2',
                         psyattack=0.20, psyrange=10,
                         desc=['A bloodthirsty worshipper of Kali Ma.']))

        self.add(Monster('acolyte of Kali', skin=('h', libtcod.gray),
                         attack=3.5, defence=2.5, range=14, level=9, count=3,
                         confimmune=True,  branch='qk', idtag='akali_3',
                         psyattack=0.25, psyrange=14,
                         desc=['A bloodthirsty worshipper of Kali Ma.']))

        self.add(Monster('acolyte of Kali', skin=('h', libtcod.gray),
                         attack=3.5, defence=2.5, range=18, level=10, count=3,
                         confimmune=True,  branch='qk', idtag='akali_4',
                         psyattack=0.25, psyrange=18,
                         desc=['A bloodthirsty worshipper of Kali Ma.']))

        
        ## Moon-special monsters.

        def template(m, **args):
            m = copy.copy(m)
            for k,v in args.iteritems():
                setattr(m, k, v)
            self.add(m)

        priestmon = Monster("vile priest of Ba'al-Zebub", skin=('p', libtcod.crimson),
                            attack=2.0, defence=1.0, range=25, fleerange=5, flavor='wizard',
                            branch='a', count=1, level=2, idtag='priest_a2', moon=newmoon_only,
                            no_exting=True, raise_dead=(15, 2), pointscontrib=0,
                            desc=["A depraved worshipper of Ba'al-Zebub, the unclean undead god."])

        nosferatu = Monster("Nosferatu", skin=('y', libtcod.han),
                            attack=7.0, defence=7.0, range=25, flavor='air', branch='a', count=1, 
                            level=2, idtag='nosf_a2', moon=newmoon_only, no_exting=True,
                            bloodsucker=(0.25, 50), no_a=True, pointscontrib=0,
                            desc=['A bloodsucking walking corpse.'])

        template(priestmon, branch='a', level=2, idtag='priest_a2')
        template(priestmon, branch='a', level=3, idtag='priest_a3')
        template(priestmon, branch='a', level=4, idtag='priest_a4')
        template(priestmon, branch='a', level=5, idtag='priest_a5')
        template(priestmon, branch='a', level=6, idtag='priest_a6')
        template(priestmon, branch='a', level=7, idtag='priest_a7')
        template(priestmon, branch='a', level=8, idtag='priest_a8')
        template(priestmon, branch='a', level=9, idtag='priest_a9')

        template(priestmon, branch='b', level=2, idtag='priest_b2')
        template(priestmon, branch='b', level=3, idtag='priest_b3')
        template(priestmon, branch='b', level=4, idtag='priest_b4')
        template(priestmon, branch='b', level=5, idtag='priest_b5')
        template(priestmon, branch='b', level=6, idtag='priest_b6')
        template(priestmon, branch='b', level=7, idtag='priest_b7')
        template(priestmon, branch='b', level=8, idtag='priest_b8')
        template(priestmon, branch='b', level=9, idtag='priest_b9')

        template(priestmon, branch='c', level=2, idtag='priest_c2')
        template(priestmon, branch='c', level=3, idtag='priest_c3')
        template(priestmon, branch='c', level=4, idtag='priest_c4')
        template(priestmon, branch='c', level=5, idtag='priest_c5')
        template(priestmon, branch='c', level=6, idtag='priest_c6')
        template(priestmon, branch='c', level=7, idtag='priest_c7')
        template(priestmon, branch='c', level=8, idtag='priest_c8')
        template(priestmon, branch='c', level=9, idtag='priest_c9')

        template(priestmon, branch='d', level=2, idtag='priest_d2')
        template(priestmon, branch='d', level=3, idtag='priest_d3')
        template(priestmon, branch='d', level=4, idtag='priest_d4')
        template(priestmon, branch='d', level=5, idtag='priest_d5')
        template(priestmon, branch='d', level=6, idtag='priest_d6')
        template(priestmon, branch='d', level=7, idtag='priest_d7')
        template(priestmon, branch='d', level=8, idtag='priest_d8')
        template(priestmon, branch='d', level=9, idtag='priest_d9')

        template(priestmon, branch='e', level=2, idtag='priest_e2')
        template(priestmon, branch='e', level=3, idtag='priest_e3')
        template(priestmon, branch='e', level=4, idtag='priest_e4')
        template(priestmon, branch='e', level=5, idtag='priest_e5')
        template(priestmon, branch='e', level=6, idtag='priest_e6')
        template(priestmon, branch='e', level=7, idtag='priest_e7')
        template(priestmon, branch='e', level=8, idtag='priest_e8')
        template(priestmon, branch='e', level=9, idtag='priest_e9')

        #

        template(nosferatu, branch='a', level=2, idtag='nosf_a2')
        template(nosferatu, branch='a', level=3, idtag='nosf_a3')
        template(nosferatu, branch='a', level=4, idtag='nosf_a4')
        template(nosferatu, branch='a', level=5, idtag='nosf_a5')
        template(nosferatu, branch='a', level=6, idtag='nosf_a6')
        template(nosferatu, branch='a', level=7, idtag='nosf_a7')
        template(nosferatu, branch='a', level=8, idtag='nosf_a8')
        template(nosferatu, branch='a', level=9, idtag='nosf_a9')

        template(nosferatu, branch='b', level=2, idtag='nosf_b2')
        template(nosferatu, branch='b', level=3, idtag='nosf_b3')
        template(nosferatu, branch='b', level=4, idtag='nosf_b4')
        template(nosferatu, branch='b', level=5, idtag='nosf_b5')
        template(nosferatu, branch='b', level=6, idtag='nosf_b6')
        template(nosferatu, branch='b', level=7, idtag='nosf_b7')
        template(nosferatu, branch='b', level=8, idtag='nosf_b8')
        template(nosferatu, branch='b', level=9, idtag='nosf_b9')

        template(nosferatu, branch='c', level=2, idtag='nosf_c2')
        template(nosferatu, branch='c', level=3, idtag='nosf_c3')
        template(nosferatu, branch='c', level=4, idtag='nosf_c4')
        template(nosferatu, branch='c', level=5, idtag='nosf_c5')
        template(nosferatu, branch='c', level=6, idtag='nosf_c6')
        template(nosferatu, branch='c', level=7, idtag='nosf_c7')
        template(nosferatu, branch='c', level=8, idtag='nosf_c8')
        template(nosferatu, branch='c', level=9, idtag='nosf_c9')

        template(nosferatu, branch='d', level=2, idtag='nosf_d2')
        template(nosferatu, branch='d', level=3, idtag='nosf_d3')
        template(nosferatu, branch='d', level=4, idtag='nosf_d4')
        template(nosferatu, branch='d', level=5, idtag='nosf_d5')
        template(nosferatu, branch='d', level=6, idtag='nosf_d6')
        template(nosferatu, branch='d', level=7, idtag='nosf_d7')
        template(nosferatu, branch='d', level=8, idtag='nosf_d8')
        template(nosferatu, branch='d', level=9, idtag='nosf_d9')

        template(nosferatu, branch='e', level=2, idtag='nosf_e2')
        template(nosferatu, branch='e', level=3, idtag='nosf_e3')
        template(nosferatu, branch='e', level=4, idtag='nosf_e4')
        template(nosferatu, branch='e', level=5, idtag='nosf_e5')
        template(nosferatu, branch='e', level=6, idtag='nosf_e6')
        template(nosferatu, branch='e', level=7, idtag='nosf_e7')
        template(nosferatu, branch='e', level=8, idtag='nosf_e8')
        template(nosferatu, branch='e', level=9, idtag='nosf_e9')

        ##

        lunatic = Monster("lunatic", skin=('h', libtcod.desaturated_blue),
                          attack=1.0, defence=2.2, range=0, flavor='humanweird',
                          branch='a', count=1, level=2, idtag='luna_a2', moon=fullmoon_only,
                          no_exting=True, summononce=(6, 12), pointscontrib=0,
                          desc=["Strange, selenic emanations have driven this poor soul",
                                "to eternally walk the moon-lit dungeon, whispering softly",
                                "to the pale, round face of the Moon."])
        
        lycan = Monster("lycanthrope", skin=('l', libtcod.gray),
                        attack=4.0, defence=1.5, range=20, heatseeking=True, fast=True,
                        branch='a', count=1, level=2, idtag='lyca_a2', moon=fullmoon_only,
                        no_exting=True, pointscontrib=0,
                        desc=['Idem: a werewolf, a shapeshifter, warg, lycan, versipellis.'])


        template(lunatic, branch='a', level=2, idtag='luna_a2')
        template(lunatic, branch='a', level=3, idtag='luna_a3')
        template(lunatic, branch='a', level=4, idtag='luna_a4')
        template(lunatic, branch='a', level=5, idtag='luna_a5')
        template(lunatic, branch='a', level=6, idtag='luna_a6')
        template(lunatic, branch='a', level=7, idtag='luna_a7')
        template(lunatic, branch='a', level=8, idtag='luna_a8')
        template(lunatic, branch='a', level=9, idtag='luna_a9')

        template(lunatic, branch='b', level=2, idtag='luna_b2')
        template(lunatic, branch='b', level=3, idtag='luna_b3')
        template(lunatic, branch='b', level=4, idtag='luna_b4')
        template(lunatic, branch='b', level=5, idtag='luna_b5')
        template(lunatic, branch='b', level=6, idtag='luna_b6')
        template(lunatic, branch='b', level=7, idtag='luna_b7')
        template(lunatic, branch='b', level=8, idtag='luna_b8')
        template(lunatic, branch='b', level=9, idtag='luna_b9')

        template(lunatic, branch='c', level=2, idtag='luna_c2')
        template(lunatic, branch='c', level=3, idtag='luna_c3')
        template(lunatic, branch='c', level=4, idtag='luna_c4')
        template(lunatic, branch='c', level=5, idtag='luna_c5')
        template(lunatic, branch='c', level=6, idtag='luna_c6')
        template(lunatic, branch='c', level=7, idtag='luna_c7')
        template(lunatic, branch='c', level=8, idtag='luna_c8')
        template(lunatic, branch='c', level=9, idtag='luna_c9')

        template(lunatic, branch='d', level=2, idtag='luna_d2')
        template(lunatic, branch='d', level=3, idtag='luna_d3')
        template(lunatic, branch='d', level=4, idtag='luna_d4')
        template(lunatic, branch='d', level=5, idtag='luna_d5')
        template(lunatic, branch='d', level=6, idtag='luna_d6')
        template(lunatic, branch='d', level=7, idtag='luna_d7')
        template(lunatic, branch='d', level=8, idtag='luna_d8')
        template(lunatic, branch='d', level=9, idtag='luna_d9')

        template(lunatic, branch='e', level=2, idtag='luna_e2')
        template(lunatic, branch='e', level=3, idtag='luna_e3')
        template(lunatic, branch='e', level=4, idtag='luna_e4')
        template(lunatic, branch='e', level=5, idtag='luna_e5')
        template(lunatic, branch='e', level=6, idtag='luna_e6')
        template(lunatic, branch='e', level=7, idtag='luna_e7')
        template(lunatic, branch='e', level=8, idtag='luna_e8')
        template(lunatic, branch='e', level=9, idtag='luna_e9')


        
        template(lycan, branch='a', level=2, idtag='lyca_a2')
        template(lycan, branch='a', level=3, idtag='lyca_a3')
        template(lycan, branch='a', level=4, idtag='lyca_a4')
        template(lycan, branch='a', level=5, idtag='lyca_a5')
        template(lycan, branch='a', level=6, idtag='lyca_a6')
        template(lycan, branch='a', level=7, idtag='lyca_a7')
        template(lycan, branch='a', level=8, idtag='lyca_a8')
        template(lycan, branch='a', level=9, idtag='lyca_a9')

        template(lycan, branch='b', level=2, idtag='lyca_b2')
        template(lycan, branch='b', level=3, idtag='lyca_b3')
        template(lycan, branch='b', level=4, idtag='lyca_b4')
        template(lycan, branch='b', level=5, idtag='lyca_b5')
        template(lycan, branch='b', level=6, idtag='lyca_b6')
        template(lycan, branch='b', level=7, idtag='lyca_b7')
        template(lycan, branch='b', level=8, idtag='lyca_b8')
        template(lycan, branch='b', level=9, idtag='lyca_b9')

        template(lycan, branch='c', level=2, idtag='lyca_c2')
        template(lycan, branch='c', level=3, idtag='lyca_c3')
        template(lycan, branch='c', level=4, idtag='lyca_c4')
        template(lycan, branch='c', level=5, idtag='lyca_c5')
        template(lycan, branch='c', level=6, idtag='lyca_c6')
        template(lycan, branch='c', level=7, idtag='lyca_c7')
        template(lycan, branch='c', level=8, idtag='lyca_c8')
        template(lycan, branch='c', level=9, idtag='lyca_c9')

        template(lycan, branch='d', level=2, idtag='lyca_d2')
        template(lycan, branch='d', level=3, idtag='lyca_d3')
        template(lycan, branch='d', level=4, idtag='lyca_d4')
        template(lycan, branch='d', level=5, idtag='lyca_d5')
        template(lycan, branch='d', level=6, idtag='lyca_d6')
        template(lycan, branch='d', level=7, idtag='lyca_d7')
        template(lycan, branch='d', level=8, idtag='lyca_d8')
        template(lycan, branch='d', level=9, idtag='lyca_d9')

        template(lycan, branch='e', level=2, idtag='lyca_e2')
        template(lycan, branch='e', level=3, idtag='lyca_e3')
        template(lycan, branch='e', level=4, idtag='lyca_e4')
        template(lycan, branch='e', level=5, idtag='lyca_e5')
        template(lycan, branch='e', level=6, idtag='lyca_e6')
        template(lycan, branch='e', level=7, idtag='lyca_e7')
        template(lycan, branch='e', level=8, idtag='lyca_e8')
        template(lycan, branch='e', level=9, idtag='lyca_e9')

        ##

        ufo = Monster("rigellian", skin=('a', libtcod.dark_lime),
                      attack=7.0, defence=22.0, range=25, 
                      branch='a', count=1, level=2, idtag='ufo_a2', moon=quartermoon_only,
                      no_exting=True, 
                      fleerange=8, explodeimmune=True, confimmune=True,
                      radimmune=True, poisimmune=True, fireimmune=True,
                      flying=True, blink_away=5,
                      itemdrop='deathray', pointsfac=5,
                      desc=['An evil alien overlord.',
                            'He studies humanity and plots plans of world domination.',
                            'He might also be the one responsible for abductions of',
                            'immocents civilians and cattle.'])


        template(ufo, branch='a', level=2, idtag='ufo_a2')
        template(ufo, branch='a', level=4, idtag='ufo_a4')
        template(ufo, branch='a', level=6, idtag='ufo_a6', psyattack=0.25, psyrange=3)
        template(ufo, branch='a', level=8, idtag='ufo_a8', psyattack=0.25, psyrange=5)
        template(ufo, branch='a', level=10, idtag='ufo_a10', psyattack=0.25, psyrange=6)

        template(ufo, branch='b', level=2, idtag='ufo_b2')
        template(ufo, branch='b', level=4, idtag='ufo_b4')
        template(ufo, branch='b', level=6, idtag='ufo_b6', psyattack=0.25, psyrange=3)
        template(ufo, branch='b', level=8, idtag='ufo_b8', psyattack=0.25, psyrange=5)
        template(ufo, branch='b', level=10, idtag='ufo_b10', psyattack=0.25, psyrange=6)

        template(ufo, branch='c', level=2, idtag='ufo_c2')
        template(ufo, branch='c', level=4, idtag='ufo_c4')
        template(ufo, branch='c', level=6, idtag='ufo_c6', psyattack=0.25, psyrange=3)
        template(ufo, branch='c', level=8, idtag='ufo_c8', psyattack=0.25, psyrange=5)
        template(ufo, branch='c', level=10, idtag='ufo_c10', psyattack=0.25, psyrange=6)

        template(ufo, branch='d', level=2, idtag='ufo_d2')
        template(ufo, branch='d', level=4, idtag='ufo_d4')
        template(ufo, branch='d', level=6, idtag='ufo_d6', psyattack=0.25, psyrange=3)
        template(ufo, branch='d', level=8, idtag='ufo_d8', psyattack=0.25, psyrange=5)
        template(ufo, branch='d', level=10, idtag='ufo_d10', psyattack=0.25, psyrange=6)

        template(ufo, branch='e', level=2, idtag='ufo_e2')
        template(ufo, branch='e', level=4, idtag='ufo_e4')
        template(ufo, branch='e', level=6, idtag='ufo_e6', psyattack=0.25, psyrange=3)
        template(ufo, branch='e', level=8, idtag='ufo_e8', psyattack=0.25, psyrange=5)
        template(ufo, branch='e', level=10, idtag='ufo_e10', psyattack=0.25, psyrange=6)


        ## Secret branch

        self.add(Monster('Harry Potter', skin=(164, libtcod.blue),
                         attack=5.0, defence=5.0, range=20, level=6,
                         count=1, no_a=True, branch='s',
                         desc=['A rich, spoiled, snooty kid who attends a prestigious school.',
                               "Not much of a student, but at least he's good at athletics."]))

        self.add(Monster('Ron Weasley', skin=(164, libtcod.light_blue),
                         attack=7.0, defence=4.0, range=15, level=6,
                         count=1, no_a=True, branch='s',
                         desc=['A brawnier, dumber and much more low-class hanger-on ',
                               'friend to Harry Potter.']))

        self.add(Monster('Robert Langdon', skin=(131, libtcod.light_green),
                         attack=7.0, defence=3.0, range=18, level=6,
                         count=1, no_a=True, branch='s', confimmune=True,
                         desc=['A self-styled "symbolologist".',
                               "He's probably looking for clues of the Illuminati",
                               'in these dungeons.']))

        self.add(Monster('Bella Swan', skin=(152, libtcod.gray),
                         attack=3.0, defence=3.0, range=20, level=7,
                         count=1, no_a=True, branch='s', summon=('Edward Cullen', 1),
                         desc=['A clumsy and very forgettable teenage girl.',
                               'The only notable thing about her is that she hates',
                               'herself enough to want to become an undead vampire.']))

        self.add(Monster('Edward Cullen', skin=(152, libtcod.silver),
                         attack=8.0, defence=6.0, range=20, level=7,
                         count=1, no_a=True, branch='s', confimmune=True,
                         poisimmune=True, radimmune=True,
                         desc=["No, he's not really a vegetarian!"]))

        self.add(Monster('Dumbledore', skin=(146, libtcod.lightest_lime),
                         attack=2.0, defence=7.0, psyattack=5.0, psyrange=6,
                         range=15, level=8, count=1, no_a=True, branch='s',
                         confimmune=True, fireimmune=True, poisimmune=True,
                         sleepattack=True,
                         desc=['The head of Hogwarts School of Magic.',
                               'Purportedly a white wizard and a paragod of Good,',
                               "though you'd never guess it by looking at him."]))

        self.add(Monster('Shredder', skin=(153, libtcod.gray),
                         attack=8.0, defence=7.0, 
                         range=25, level=8, count=1, no_a=True, branch='s',
                         confimmune=True, fireimmune=True, poisimmune=True,
                         explodeimmune=True,
                         desc=['He hates turtles.']))

        self.add(Monster('Darth Vader', skin=(154, libtcod.dark_gray),
                         attack=6.0, defence=9.0, psyattack=6.0, psyrange=8,
                         range=30, level=9, count=1, no_a=True, branch='s',
                         confimmune=True, fireimmune=True, poisimmune=True,
                         flying=True,
                         desc=['A dark Sith Lord and a formidable enemy.']))

        self.add(Monster('Hagbard Celine', skin=(144, libtcod.gold),
                         attack=6.0, defence=9.0, psyattack=1.0, psyrange=2,
                         range=30, level=10, count=1, no_a=True, branch='s',
                         confimmune=True, poisimmune=True, radimmune=True,
                         explodeimmune=True, sleepattack=True,
                         hungerattack=True,
                         desc=['Hail Eris!']))

        self.add(Monster('Iucounu', skin=(142, libtcod.purple),
                         attack=3.0, defence=11.0, 
                         range=30, level=11, count=1, no_a=True, branch='s',
                         confimmune=True, poisimmune=True, radimmune=True,
                         explodeimmune=True, fireimmune=True, flying=True,
                         desc=['The Laughing Magician.']))


        ## Thunderdome

        self.add(Monster('mutant turtle', skin=('o', libtcod.green),
                         attack=1.5, defence=0.2, range=8, level=3, count=200, branch='q',
                         desc=['Your adversary in the Thunderdome.']))

        self.add(Monster('gremlin', skin=('f', libtcod.green),
                         attack=2.0, defence=0.5, range=6, level=3, count=200, branch='q',
                         desc=['Your adversary in the Thunderdome.']))

        self.add(Monster('kobold', skin=('h', libtcod.lightest_green),
                         attack=1.4, defence=0.9, range=9, level=3, count=200, branch='q',
                         desc=['Your adversary in the Thunderdome.']))

        self.add(Monster('orc', skin=('h', libtcod.gray),
                         attack=1.7, defence=0.7, range=7, level=4, count=200, branch='q',
                         desc=['Your adversary in the Thunderdome.']))

        self.add(Monster('orge', skin=('H', libtcod.light_gray),
                         attack=2.1, defence=1.9, range=5, level=4, count=200, branch='q',
                         desc=['Your adversary in the Thunderdome.']))

        self.add(Monster('dark elf', skin=('f', libtcod.darkest_gray),
                         psyattack=0.5, psyrange=4,
                         attack=1.0, defence=0.9, range=9, level=4, count=200, branch='q',
                         desc=['Your adversary in the Thunderdome.']))

        self.add(Monster('Beef Supreme', skin=('h', libtcod.pink),
                         attack=2.7, defence=0.5, range=7, level=5, branch='q',
                         no_a=True, count=1,
                         desc=['Your adversary in the Thunderdome.']))

        self.add(Monster('Tylenol Jones', skin=('h', libtcod.light_blue),
                         psyattack=0.25, psyrange=3, no_a=True, count=1,
                         attack=1.5, defence=1.0, range=8, level=5, branch='q',
                         desc=['Your adversary in the Thunderdome.']))

        self.add(Monster('Frito Pendejo', skin=('h', libtcod.dark_sky),
                         attack=2.0, defence=0.8, range=9, level=5, count=1, branch='q',
                         no_a=True,
                         desc=['Your adversary in the Thunderdome.']))
        
        self.add(Monster('Formica Davis', skin=('h', libtcod.light_crimson),
                         attack=2.0, defence=1.7, range=10, level=6, count=1, branch='q',
                         no_a=True,
                         desc=['Your adversary in the Thunderdome.']))

        self.add(Monster('Hormel Chavez', skin=('h', libtcod.light_blue),
                         attack=1.4, defence=2.2, range=12, level=6, count=1, branch='q',
                         no_a=True,
                         desc=['Your adversary in the Thunderdome.']))

        self.add(Monster('Brawndo Mutilator', skin=('z', libtcod.silver),
                         psyattack=0.5, psyrange=3, 
                         attack=3.0, defence=0.8, range=6, level=6, count=1, branch='q',
                         no_a=True,
                         desc=['Your adversary in the Thunderdome.']))


        self.add(Monster('Meatcleaver', skin=('h', libtcod.dark_crimson),
                         attack=3.0, defence=3.5, range=10, level=7, count=1, branch='q',
                         no_a=True,
                         desc=['Your adversary in the Thunderdome.']))

        self.add(Monster('Captain Electric', skin=('h', libtcod.lightest_blue),
                         psyattack=0.15, psyrange=7, 
                         attack=3.0, defence=1.0, range=5, level=7, count=1, branch='q',
                         no_a=True,
                         desc=['Your adversary in the Thunderdome.']))

        self.add(Monster('Buzzsaw', skin=('z', libtcod.lightest_yellow),
                         attack=6.0, defence=4.0, range=6, level=7, count=1, branch='q',
                         no_a=True, slow=True,
                         desc=['Your adversary in the Thunderdome.']))


        self.add(Monster('Dynamo', skin=('h', libtcod.dark_crimson),
                         psyattack=0.4, psyrange=5, 
                         attack=3.0, defence=0.5, range=10, level=8, count=1, branch='q',
                         no_a=True,
                         desc=['Your adversary in the Thunderdome.']))

        self.add(Monster('Master Blaster', skin=('h', libtcod.lightest_blue),
                         attack=3.0, defence=6.0, range=5, level=8, count=1, branch='q',
                         no_a=True,
                         desc=['Your adversary in the Thunderdome.']))

        self.add(Monster('President Dwayne Elizondo Mountain Dew Herbert Camacho', 
                         skin=('H', libtcod.light_sky),
                         attack=3.0, defence=8.0, range=7, level=8, count=1, branch='q',
                         no_a=True, 
                         desc=['Your adversary in the Thunderdome.']))

        ## Mold

        MOLD = 5

        self.add(Monster('black mold', no_a=True, attack=0, defence=5.0, range=0, branch='x',
                         level=1, count=5, static=True, summon=('bmold1', 10), idtag='bmold1',
                         moldspew=(MOLD,3,3), poisimmune=True, skin=('x',libtcod.gray), is_mold=True,
                         moon=quartermoon_bias, no_exting=True, pointsfac=0.5,
                         desc=['Stachybotrys chartarum, a toxic and sometimes deadly',
                               'species of mold.']))

        self.add(Monster('black mold', no_a=True, attack=0, defence=5.0, range=0, branch='x',
                         level=2, count=15, static=True, summon=('bmold1', 10), idtag='bmold1',
                         moldspew=(MOLD,3,3), poisimmune=True, skin=('x',libtcod.gray), is_mold=True,
                         moon=quartermoon_bias, no_exting=True, pointsfac=0.5,
                         desc=['Stachybotrys chartarum, a toxic and sometimes deadly',
                               'species of mold.']))

        self.add(Monster('black mold', no_a=True, attack=0, defence=5.0, range=0, branch='x',
                         level=4, count=15, static=True, summon=('bmold2', 10), idtag='bmold2',
                         moldspew=(MOLD,3,3), poisimmune=True, skin=('x',libtcod.gray), is_mold=True,
                         moon=quartermoon_bias, no_exting=True, pointsfac=0.5,
                         desc=['Stachybotrys chartarum, a toxic and sometimes deadly',
                               'species of mold.']))

        self.add(Monster('black mold', no_a=True, attack=0, defence=5.0, range=0, branch='x',
                         level=6, count=15, static=True, summon=('bmold3', 10), idtag='bmold3',
                         moldspew=(MOLD,3,3), poisimmune=True, skin=('x',libtcod.gray), is_mold=True,
                         moon=quartermoon_bias, no_exting=True, pointsfac=0.5,
                         desc=['Stachybotrys chartarum, a toxic and sometimes deadly',
                               'species of mold.']))

        self.add(Monster('black mold', no_a=True, attack=0, defence=5.0, range=0, branch='x',
                         level=8, count=15, static=True, summon=('mold4', 10), idtag='bmold4',
                         moldspew=(MOLD,3,3), poisimmune=True, skin=('x',libtcod.gray), is_mold=True,
                         moon=quartermoon_bias, no_exting=True, pointsfac=0.5,
                         desc=['Stachybotrys chartarum, a toxic and sometimes deadly',
                               'species of mold.']))


        ## Boulders

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='a', skin=('0', libtcod.gray),
                         level=1, count=3, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='ba1', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='a', skin=('0', libtcod.gray),
                         level=2, count=5, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='ba2', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='a', skin=('0', libtcod.gray),
                         level=3, count=8, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='ba3', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='a', skin=('0', libtcod.gray),
                         level=4, count=8, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='ba4', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='a', skin=('0', libtcod.gray),
                         level=5, count=5, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='ba5', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='a', skin=('0', libtcod.gray),
                         level=6, count=4, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='ba6', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='a', skin=('0', libtcod.gray),
                         level=7, count=3, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='ba7', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='a', skin=('0', libtcod.gray),
                         level=8, count=2, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='ba8', desc=['A gigantic rock of spherical shape.']))

        # 

        self.add(Monster('mountain of meat', boulder=True, inanimate=True, branch='b', skin=('0', libtcod.red),
                         level=3, count=2, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bc1', desc=['A mountain of quivering, perverse, vomitous flesh.']))

        self.add(Monster('mountain of meat', boulder=True, inanimate=True, branch='b', skin=('0', libtcod.red),
                         level=4, count=4, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bc2', desc=['A mountain of quivering, perverse, vomitous flesh.']))

        self.add(Monster('mountain of meat', boulder=True, inanimate=True, branch='b', skin=('0', libtcod.red),
                         level=5, count=12, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bc3', desc=['A mountain of quivering, perverse, vomitous flesh.']))

        self.add(Monster('mountain of meat', boulder=True, inanimate=True, branch='b', skin=('0', libtcod.red),
                         level=6, count=4, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bc4', desc=['A mountain of quivering, perverse, vomitous flesh.']))

        self.add(Monster('mountain of meat', boulder=True, inanimate=True, branch='b', skin=('0', libtcod.red),
                         level=7, count=2, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bc5', desc=['A mountain of quivering, perverse, vomitous flesh.']))

        # 

        self.add(Monster('rollerball', boulder=True, inanimate=True, branch='c', skin=('0', libtcod.dark_blue),
                         level=2, count=3, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bb1', desc=['A huge metal ball with sharp spikes all over it.']))

        self.add(Monster('rollerball', boulder=True, inanimate=True, branch='c', skin=('0', libtcod.dark_blue),
                         level=3, count=4, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bb2', desc=['A huge metal ball with sharp spikes all over it.']))

        self.add(Monster('rollerball', boulder=True, inanimate=True, branch='c', skin=('0', libtcod.dark_blue),
                         level=4, count=5, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bb3', desc=['A huge metal ball with sharp spikes all over it.']))

        self.add(Monster('rollerball', boulder=True, inanimate=True, branch='c', skin=('0', libtcod.dark_blue),
                         level=5, count=6, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bb4', desc=['A huge metal ball with sharp spikes all over it.']))

        self.add(Monster('rollerball', boulder=True, inanimate=True, branch='c', skin=('0', libtcod.dark_blue),
                         level=6, count=7, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bb5', desc=['A huge metal ball with sharp spikes all over it.']))

        self.add(Monster('rollerball', boulder=True, inanimate=True, branch='c', skin=('0', libtcod.dark_blue),
                         level=7, count=8, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bb6', desc=['A huge metal ball with sharp spikes all over it.']))

        self.add(Monster('rollerball', boulder=True, inanimate=True, branch='c', skin=('0', libtcod.dark_blue),
                         level=8, count=9, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bb7', desc=['A huge metal ball with sharp spikes all over it.']))

        self.add(Monster('rollerball', boulder=True, inanimate=True, branch='c', skin=('0', libtcod.dark_blue),
                         level=9, count=10, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bb8', desc=['A huge metal ball with sharp spikes all over it.']))

        #

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='d', skin=('0', libtcod.gray),
                         level=2, count=6, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bd1', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='d', skin=('0', libtcod.gray),
                         level=3, count=6, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bd2', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='d', skin=('0', libtcod.gray),
                         level=4, count=6, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bd3', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='d', skin=('0', libtcod.gray),
                         level=5, count=3, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bd4', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='d', skin=('0', libtcod.gray),
                         level=6, count=2, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bd5', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='d', skin=('0', libtcod.gray),
                         level=7, count=1, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='bd6', desc=['A gigantic rock of spherical shape.']))

        # 

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='e', skin=('0', libtcod.gray),
                         level=1, count=3, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='be1', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='e', skin=('0', libtcod.gray),
                         level=2, count=3, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='be2', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='e', skin=('0', libtcod.gray),
                         level=3, count=3, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='be3', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='e', skin=('0', libtcod.gray),
                         level=4, count=3, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='be4', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='e', skin=('0', libtcod.gray),
                         level=5, count=3, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='be5', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='e', skin=('0', libtcod.gray),
                         level=6, count=3, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='be6', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='e', skin=('0', libtcod.gray),
                         level=7, count=3, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='be7', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='e', skin=('0', libtcod.gray),
                         level=8, count=3, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='be8', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='e', skin=('0', libtcod.gray),
                         level=9, count=3, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='be9', desc=['A gigantic rock of spherical shape.']))

        self.add(Monster('boulder', boulder=True, inanimate=True, branch='e', skin=('0', libtcod.gray),
                         level=10, count=3, poisimmune=True, confimmune=True, radimmune=True,
                         pointscontrib=0, no_exting=True,
                         idtag='be10', desc=['A gigantic rock of spherical shape.']))

    
        self.renormalize()


    def renormalize(self):

        self.norms = {}
        for branch,v in self.monsters.iteritems():
            n = 0
            for lev,v2 in v.iteritems():
                moncount = 0
                for mon in v2:
                    moncount += (mon.count * mon.pointscontrib)
                n += lev * moncount

            n = 840.0 / n
            self.norms[branch] = n

        # HACK don't give too many points for cleaning up mold.
        #self.norms['x'] /= 2


    def add(self, mon):
        if mon.branch not in self.monsters:
            self.monsters[mon.branch] = {}

        mms = self.monsters[mon.branch]

        if mon.level not in mms:
            mms[mon.level] = [mon]
        else:
            mms[mon.level].append(mon)


    def clear_gencount(self):
        for v2 in self.monsters.itervalues():
            for v in v2.itervalues():
                for m in v:
                    m.gencount = 0


    def find(self, idtag, n, itemstock):
        for v2 in self.monsters.itervalues():
            for v in v2.itervalues():
                for m in v:
                    if m.idtag == idtag:
                        l = []

                        if m.gencount >= m.count:
                            return l

                        n2 = min(n, m.count - m.gencount)
                        m.gencount += n2

                        for x in xrange(n2):
                            mm = copy.copy(m)
                            if mm.itemdrop:
                                if type(mm.itemdrop) == type(''):
                                    item = itemstock.get(mm.itemdrop)
                                    if item:
                                        mm.items = [item]
                                else:
                                    item = [itemstock.get(ii) for ii in mm.itemdrop]
                                    mm.items = [ii for ii in item if ii]
                            l.append(mm)

                        return l

        return []

    def generate(self, branch, level, itemstock, moon):

        while level > 0 and level not in self.monsters[branch]:
            level -= 1

        if level == 0:
            return None

        tmp = None

        while 1:
            m = self.monsters[branch][level]

            okix = []
            for x in xrange(len(m)):
                if m[x].gencount >= m[x].count:
                    continue

                if m[x].moon:
                    tmp = dg.random_range(1,9)
                    if tmp > m[x].moon[moon-1]:
                        continue

                okix.append(x)

            if len(okix) == 0:
                level += 1
                if level not in self.monsters[branch]:
                    return None
                continue

            tmp = okix[dg.random_n(len(okix))]
            tmp = m[tmp]
            tmp.gencount += 1
            break
            
        m = copy.copy(tmp)

        if m.itemdrop:
            if type(m.itemdrop) == type(''):
                i = itemstock.get(m.itemdrop)
                if i:
                    m.items = [i]
            else:
                item = [itemstock.get(ii) for ii in m.itemdrop]
                m.items = [ii for ii in item if ii]

        return m

    def death(self, mon, moon):

        if not mon.branch:
            return (False, False)

        if mon.level not in self.monsters[mon.branch]:
            return (len(self.monsters[mon.branch]) == 0, False)

        m = self.monsters[mon.branch][mon.level]

        ret = False

        for x in xrange(len(m)):
            if mon.idtag == m[x].idtag:

                if m[x].count <= 1:
                    del m[x]
                    ret = True
                else:
                    m[x].count -= 1
                break

        nc = 0
        for m_ in m:
            if m_.inanimate or (m_.moon and m_.moon[moon-1] <= 0):
                continue
            nc += 1

        if nc == 0:
            del self.monsters[mon.branch][mon.level]

        winner = False

        if len(self.monsters[mon.branch]) == 0:
            winner = True

        if mon.no_exting:
            ret = False

        # HACK you can win by cleaning up mold.

        return (winner, ret)

