import libtcodpy as libtcod
import random


class Vault:
    def __init__(self, syms=None, pic=None, chance=1, level=(1,10), count=10, branch=None,
                 message=None, anywhere=False, free=False):
        self.syms = syms
        self.pic = pic
        self.chance = chance
        self.level = level
        self.count = count
        self.branch = branch
        self.message = message
        self.anywhere = anywhere
        self.free = free

    def postprocess(self):
        a = None
        for k,v in self.syms.iteritems():
            if v and v[-1]:
                a = k

        self.h = len(self.pic)
        self.w = max(len(x) for x in self.pic)

        for y in xrange(len(self.pic)):
            for x in xrange(len(self.pic[y])):
                if self.pic[y][x] == a:
                    self.anchor = (x, y)
                    return

        self.anchor = (0, 0)


class VaultStock:

    def __init__(self):
        self.vaults = {}

        syms = {' ': None,
                '.': (None, False),
                '#': (0, False),
                'o': (':', False),
                'R': ('R', False),
                'L': ('L', False),
                'T': ('T', False),
                'F': ('F', False),
                'J': ('J', False),
                'Z': ('Z', False),
                '7': ('7', False),
                '/': ('/', False),
                '-': ('-', False),
                '|': ('|', False),
                '+': ('+', False),
                'a': ('a', False),
                'h': ('h', False),
                '=': ('=', False),
                'l': ('l', False),
                'p': ('p', False),
                'r': ('r', False),
                'q': ('q', False),
                'd': ('d', False),
                '*': ('@', True),
                '$': ('$', True),
                '^': ('^', False),
                '1': (None, 'mushrooms', False),
                '2': (None, 'medpack', False),
                '3': (None, 'killerwand', False),
                '4': (None, 'cclarva', False),
                '5': (None, 'stickyglue', False),
                '6': (None, 'minibomb', False),
                '9': (None, 'coolpack', False),
                '8': (None, 'gbomb', False),
                'v': ('v', True),
                's': ('s', True),
                'b': ('b', True),
                'Y': ('Y', False),
                '!': ('!', False),
                'w': ('w', False),
                '@': (None, True)}

        symsb = { '1': ('1', True),
                  '2': ('2', True),
                  '3': ('3', True),
                  '4': ('4', True),
                  '5': ('5', True),
                  '9': ('6', True),
                  '6': ('1', False),
                  '7': ('2', False),
                  '8': ('3', False),
                  '9': ('4', False),
                  '0': ('5', False),
                  'z': ('8', True),
                  '.': (None, False) }


        #
        self.add(Vault(syms=symsb, pic=["z"], chance=2, level=(1,3), count=3, free=True, branch='a'))
        self.add(Vault(syms=symsb, pic=["z"], chance=2, level=(1,3), count=3, free=True, branch='b'))
        self.add(Vault(syms=symsb, pic=["z"], chance=2, level=(1,3), count=3, free=True, branch='c'))
        self.add(Vault(syms=symsb, pic=["z"], chance=2, level=(1,3), count=3, free=True, branch='d'))
        self.add(Vault(syms=symsb, pic=["z"], chance=2, level=(1,3), count=3, free=True, branch='e'))

        self.add(Vault(syms=symsb, pic=["...",
                                        ".9.",
                                        "..."],
                       chance=2, level=(5,6), count=1, branch='a'))

        self.add(Vault(syms=symsb, pic=["...",
                                        ".9.",
                                        "..."],
                       chance=2, level=(5,6), count=1, branch='b'))

        self.add(Vault(syms=symsb, pic=["...",
                                        ".9.",
                                        "..."],
                       chance=2, level=(5,6), count=1, branch='c'))

        self.add(Vault(syms=symsb, pic=["...",
                                        ".9.",
                                        "..."],
                       chance=2, level=(5,6), count=1, branch='d'))

        self.add(Vault(syms=symsb, pic=["...",
                                        ".9.",
                                        "..."],
                       chance=2, level=(5,6), count=1, branch='e'))


        self.add(Vault(syms=symsb, pic=["5"], chance=3, level=(3,3), count=1, branch='a'))
        self.add(Vault(syms=symsb, pic=["5"], chance=3, level=(6,6), count=1, branch='a'))
        self.add(Vault(syms=symsb, pic=["5"], chance=3, level=(9,9), count=1, branch='a'))
        self.add(Vault(syms=symsb, pic=["2"], chance=3, level=(3,3), count=1, branch='a'))
        self.add(Vault(syms=symsb, pic=["2"], chance=3, level=(6,6), count=1, branch='a'))
        self.add(Vault(syms=symsb, pic=["2"], chance=3, level=(9,9), count=1, branch='a'))
        self.add(Vault(syms=symsb, pic=["3"], chance=3, level=(3,3), count=1, branch='a'))
        self.add(Vault(syms=symsb, pic=["3"], chance=3, level=(6,6), count=1, branch='a'))
        self.add(Vault(syms=symsb, pic=["3"], chance=3, level=(9,9), count=1, branch='a'))
        self.add(Vault(syms=symsb, pic=["4"], chance=3, level=(3,3), count=1, branch='a'))
        self.add(Vault(syms=symsb, pic=["4"], chance=3, level=(6,6), count=1, branch='a'))
        self.add(Vault(syms=symsb, pic=["4"], chance=3, level=(9,9), count=1, branch='a'))

        self.add(Vault(syms=symsb, pic=["1"], chance=3, level=(3,3), count=1, branch='b'))
        self.add(Vault(syms=symsb, pic=["1"], chance=3, level=(6,6), count=1, branch='b'))
        self.add(Vault(syms=symsb, pic=["1"], chance=3, level=(9,9), count=1, branch='b'))
        self.add(Vault(syms=symsb, pic=["5"], chance=3, level=(3,3), count=1, branch='b'))
        self.add(Vault(syms=symsb, pic=["5"], chance=3, level=(6,6), count=1, branch='b'))
        self.add(Vault(syms=symsb, pic=["5"], chance=3, level=(9,9), count=1, branch='b'))
        self.add(Vault(syms=symsb, pic=["4"], chance=3, level=(3,3), count=1, branch='b'))
        self.add(Vault(syms=symsb, pic=["4"], chance=3, level=(6,6), count=1, branch='b'))
        self.add(Vault(syms=symsb, pic=["4"], chance=3, level=(9,9), count=1, branch='b'))
        self.add(Vault(syms=symsb, pic=["3"], chance=3, level=(3,3), count=1, branch='b'))
        self.add(Vault(syms=symsb, pic=["3"], chance=3, level=(6,6), count=1, branch='b'))
        self.add(Vault(syms=symsb, pic=["3"], chance=3, level=(9,9), count=1, branch='b'))

        self.add(Vault(syms=symsb, pic=["4"], chance=3, level=(3,3), count=1, branch='c'))
        self.add(Vault(syms=symsb, pic=["4"], chance=3, level=(6,6), count=1, branch='c'))
        self.add(Vault(syms=symsb, pic=["4"], chance=3, level=(9,9), count=1, branch='c'))
        self.add(Vault(syms=symsb, pic=["1"], chance=3, level=(3,3), count=1, branch='c'))
        self.add(Vault(syms=symsb, pic=["1"], chance=3, level=(6,6), count=1, branch='c'))
        self.add(Vault(syms=symsb, pic=["1"], chance=3, level=(9,9), count=1, branch='c'))
        self.add(Vault(syms=symsb, pic=["2"], chance=3, level=(3,3), count=1, branch='c'))
        self.add(Vault(syms=symsb, pic=["2"], chance=3, level=(6,6), count=1, branch='c'))
        self.add(Vault(syms=symsb, pic=["2"], chance=3, level=(9,9), count=1, branch='c'))
        self.add(Vault(syms=symsb, pic=["5"], chance=3, level=(3,3), count=1, branch='c'))
        self.add(Vault(syms=symsb, pic=["5"], chance=3, level=(6,6), count=1, branch='c'))
        self.add(Vault(syms=symsb, pic=["5"], chance=3, level=(9,9), count=1, branch='c'))

        self.add(Vault(syms=symsb, pic=["3"], chance=3, level=(3,3), count=1, branch='d'))
        self.add(Vault(syms=symsb, pic=["3"], chance=3, level=(6,6), count=1, branch='d'))
        self.add(Vault(syms=symsb, pic=["3"], chance=3, level=(9,9), count=1, branch='d'))
        self.add(Vault(syms=symsb, pic=["2"], chance=3, level=(3,3), count=1, branch='d'))
        self.add(Vault(syms=symsb, pic=["2"], chance=3, level=(6,6), count=1, branch='d'))
        self.add(Vault(syms=symsb, pic=["2"], chance=3, level=(9,9), count=1, branch='d'))
        self.add(Vault(syms=symsb, pic=["5"], chance=3, level=(3,3), count=1, branch='d'))
        self.add(Vault(syms=symsb, pic=["5"], chance=3, level=(6,6), count=1, branch='d'))
        self.add(Vault(syms=symsb, pic=["5"], chance=3, level=(9,9), count=1, branch='d'))
        self.add(Vault(syms=symsb, pic=["1"], chance=3, level=(3,3), count=1, branch='d'))
        self.add(Vault(syms=symsb, pic=["1"], chance=3, level=(6,6), count=1, branch='d'))
        self.add(Vault(syms=symsb, pic=["1"], chance=3, level=(9,9), count=1, branch='d'))

        self.add(Vault(syms=symsb, pic=["2"], chance=3, level=(3,3), count=1, branch='e'))
        self.add(Vault(syms=symsb, pic=["2"], chance=3, level=(6,6), count=1, branch='e'))
        self.add(Vault(syms=symsb, pic=["2"], chance=3, level=(9,9), count=1, branch='e'))
        self.add(Vault(syms=symsb, pic=["4"], chance=3, level=(3,3), count=1, branch='e'))
        self.add(Vault(syms=symsb, pic=["4"], chance=3, level=(6,6), count=1, branch='e'))
        self.add(Vault(syms=symsb, pic=["4"], chance=3, level=(9,9), count=1, branch='e'))
        self.add(Vault(syms=symsb, pic=["1"], chance=3, level=(3,3), count=1, branch='e'))
        self.add(Vault(syms=symsb, pic=["1"], chance=3, level=(6,6), count=1, branch='e'))
        self.add(Vault(syms=symsb, pic=["1"], chance=3, level=(9,9), count=1, branch='e'))
        self.add(Vault(syms=symsb, pic=["3"], chance=3, level=(3,3), count=1, branch='e'))
        self.add(Vault(syms=symsb, pic=["3"], chance=3, level=(6,6), count=1, branch='e'))
        self.add(Vault(syms=symsb, pic=["3"], chance=3, level=(9,9), count=1, branch='e'))

        self.add(Vault(syms=symsb, pic=["6.7.3.9.0"], chance=1, level=(1,1), count=1))

        self.add(Vault(syms=syms,
                       pic=["o.o.o.o.o.o.o.o.o.o.o.o.o",
                            ".........................",
                            "o.R-T---------------T--.o",
                            "..|.|.......@.........o..",
                            "o.|hF--.o.a.o.o.o.o.|...o",
                            "..|.|.................o..",
                            "o.L-J---------------J--.o",
                            ".........................",
                            "o.o.o.o.o.o.o.o.o.o.o.o.o"],
                       chance=3, level=(2,7), count=1, branch='b'))

        self.add(Vault(syms=syms,
                       pic=["       R7.R7.R7.R7       ",
                            "    R7.L/.L/.L/.L/.R7    ",
                            "  ..L/.............L/..  ",
                            " R7.....o........o....R7 ",
                            ".L/....o..R---7...o...L/.",
                            "......o...|h.a.....o ....",
                            ".R7....o..L---/...o...R7.",
                            " L/.....o........o....L/ ",
                            "  ..R7.............R7..  ",
                            "    L/.R7.R7.R7.R7.L/    ",
                            "       L/.L/.L/.L/       "],
                       chance=3, level=(3,8), count=1, branch='b'))

        self.add(Vault(syms=syms,
                       pic=[" !       .     ...   .   ",
                            "!....   ... . ..YY.....  ",
                            "...!!. .Y ........  .!!..",
                            "  !!...YY...YY..      ...",
                            " ...Y..Y.....YY!!   ..Y..",
                            "...YYY.!!.  !h!!!!!!!Y.. ",
                            "   .!YY...   !!!YYY...   ",
                            "!!!!!!Y..!! .@YYYY...... ",
                            "  !!!Y..... .....   !  !.",
                            " !!!....YY...  ..! !.... ",
                            "    !  ..     !.. !  !! !"],
                       chance=3, level=(2,7), count=1, branch='a'))

        self.add(Vault(syms=syms,
                       pic=[" Y   !!. .   !! ..   .   ",
                            "  !  .!.... . ..!Y..... !",
                            "  Y!!. .Y .....!.!Y .!!..",
                            "  !!...YY...!!.! YYYY ...",
                            " ...Y..Y@....  !!YYY..Y..",
                            "...YYYh!!. !.....     .. ",
                            "   .!YY...   !!!YYY..!! Y",
                            "YY!. ....!! ..YY.....!.Y ",
                            " YY!!..Y... ...YY !!!  !.",
                            " .YY  ..YY...  Y.YYY.!!. ",
                            ".  Y!! ..     !..!Y! .. Y"],
                       chance=3, level=(3,8), count=1, branch='a'))

        self.add(Vault(syms=syms,
                       pic=[" r====q.=========.r====q ",
                            "......l...........l......",
                            ".l....l...r.=.q...l....l.",
                            ".p===...==d.@.p==...===d.",
                            "......l...........l......",
                            "......l.....h.....l......",
                            ".r===...==q...r==...===q ",
                            " l....l...p.=.d...l....l.",
                            " .....l...........l..... ",
                            " p====d ========= p====d "],
                       chance=3, level=(2,7), count=1, branch='c'))

        self.add(Vault(syms=syms,
                       pic=[" r====q.=====q.=====q.=q ",
                            ".l....l......l......l....",
                            ".l..r=..=q.==..=q.==..=q.",
                            ".l..l....l...@..l......l.",
                            ".l..l..r=..=q.==..=q...l.",
                            ".l..l..l....lh.....l...l.",
                            ".l..l.....==..====..l..l ",
                            " l..p=====..........d..l.",
                            " l..........r====q.....l ",
                            " p==========d    p=====d "],
                       chance=3, level=(3,8), count=1, branch='c'))

        self.add(Vault(syms=syms,
                       pic=[" R----------T----------7 ",
                            "R/..........|..........L7",
                            "|..R--=--7.....R--=--7..|",
                            "|..|.....|..|..|.....|..|",
                            "|..|.....|.-+-.|.....|..|",
                            "l@.F--=--Z..|..F--=--Z..l",
                            "|..|.....|..|..|...h.|..|",
                            "|..L--T--/..|..L--T--/..|",
                            "L7....l...........l....R/",
                            " L---------------------/ "],
                       chance=3, level=(2,7), count=1, branch='d'))

        self.add(Vault(syms=syms,
                       pic=[" R-- -------T-------7-   ",
                            "R/.. L....../ R.....R..  ",
                            "|-. --=- 7     R--=--7.R|",
                            " ..|... .|..|..|.....|.||",
                            "|.| ..||. .-+-.|.....|.L|",
                            "l@.F--= -Z..|..F--=--Z..l",
                            "|7.|..|.. ..+..|  .h.|R7 ",
                            " ..L-  --/ .| .    --/L/ ",
                            "L ....l........  .l....R/",
                            " L-------------  ------/ "],
                       chance=3, level=(2,8), count=1, branch='d'))


        self.add(Vault(syms=syms,
                       pic=["        .........        ",
                            "    ......Y.Y.Y......    ",
                            "  .....Y.Y......Y.Y....  ",
                            " ..Y.Y....YYYYYY....Y... ",
                            "..YYY...YYwwwwwwYY....Y..",
                            ".YYYYY..YYwwh.wwYY.......",
                            "..YYY...YYwwwwwwYY....Y..",
                            " ..Y.Y....YYYYYY....Y... ",
                            "  .....Y.Y......Y.Y....  ",
                            "    ......Y.Y.Y......    ",
                            "        .........        "],
                       chance=3, level=(2,7), count=1, branch='e'))

        self.add(Vault(syms=syms,
                       pic=["wwwwwwwwwwwwwwwwwwwwwwwww",
                            "wR-----7wwwwwwwwwR-----7w",
                            "w|h....L---------/.....|w",
                            "w|.....................|w",
                            "wL-7.R-J---------J-7.R-/w",
                            "www|.|             |.|www",
                            "wR-/.L-T---/.L---T-/.L-7w",
                            "w|.....................|w",
                            "w|.....R---/.L---7.....|w",
                            "wL-----/...@.....L-----/w",
                            "wwwwwwwwwwwwwwwwwwwwwwwww"],
                       chance=3, level=(3,8), count=1, branch='e'))

        self.add(Vault(syms=syms,
                       pic=["   .......   ",
                            " ........... ",
                            ".............",
                            "......*......",
                            ".............",
                            " ........... ",
                            "   .......   "],
                       chance=3, level=(2,12), count=4))

        self.add(Vault(syms=syms,
                       pic=["  .......  ",
                            " ......... ",
                            ".....$.....",
                            " ......... ",
                            "  .......  "],
                       chance=3, level=(4,14), count=4))

        self.add(Vault(syms=syms,
                       pic=[".........@..........",
                            "====================",
                            "...................."],
                       chance=3, level=(2,5), count=2, branch='c'))

        self.add(Vault(syms=syms,
                       pic=[".l.",
                            ".l.",
                            "@l.",
                            ".l.",
                            ".l.",
                            ".l."],
                       chance=3, level=(2,5), count=2, branch='c'))

        self.add(Vault(syms=syms,
                       pic=["  .^^^^^  ",
                            " ^^.^^^^^ ",
                            "^^^^.^^^^^",
                            "^^^r=.q^^^",
                            "^^^l..l^^^",
                            "^^^l..l^^^",
                            "^^^p==d^^^",
                            "^^^^^^^^^^",
                            " ^^^^^^^^ ",
                            "  ^^^^^^  "],
                       chance=3, level=(2,10), count=1, branch='c'))

        self.add(Vault(syms=syms,
                       pic=["  ^^^^^^  ",
                            " ^^^^^^^^ ",
                            "^^^^^^^^^^",
                            "^^^r==q^^^",
                            "^^^l..l^^^",
                            "^^^l..l^^^",
                            "^^^p.=d^^^",
                            "^^^^^.^^^^",
                            " ^^^^^.^^ ",
                            "  ^^^^^.  "],
                       chance=3, level=(2,10), count=1, branch='c'))

        self.add(Vault(syms=syms,
                       pic=["  ^^^^^^  ",
                            " ^^^^^^^^.",
                            "^^^^^^^^.^",
                            "^^^r==q.^^",
                            "^^^l...^^^",
                            "^^^l..l^^^",
                            "^^^p==d^^^",
                            "^^^^^^^^^^",
                            " ^^^^^^^^ ",
                            "  ^^^^^^  "],
                       chance=3, level=(2,10), count=1, branch='c'))

        self.add(Vault(syms=syms,
                       pic=["  ^^^^^^  ",
                            " ^^^^^^^^ ",
                            "^^^^^^^^^^",
                            "^^^r==q^^^",
                            "^^^l..l^^^",
                            "^^^...l^^^",
                            "^^.p==d^^^",
                            "^.^^^^^^^^",
                            ".^^^^^^^^ ",
                            "  ^^^^^^  "],
                       chance=3, level=(2,10), count=1, branch='c'))

        self.add(Vault(syms=syms,
                       pic=["R---7",
                            "|111|",
                            "|111|",
                            "L---/"],
                       chance=3, level=(4,14), count=3))

        self.add(Vault(syms=syms,
                       pic=["R---7",
                            "|222|",
                            "|222|",
                            "L---/"],
                       chance=3, level=(6,14), count=3))

        self.add(Vault(syms=syms,
                       pic=["R---7",
                            "|444|",
                            "|444|",
                            "L---/"],
                       chance=3, level=(10,14), count=3))

        self.add(Vault(syms=syms,
                       pic=["R---7",
                            "|333|",
                            "|333|",
                            "L---/"],
                       chance=3, level=(8,14), count=3, branch='e'))

        self.add(Vault(syms=syms,
                       pic=["R---7",
                            "|555|",
                            "|555|",
                            "L---/"],
                       chance=3, level=(4,14), count=3, branch='d'))

        self.add(Vault(syms=syms,
                       pic=["R---7",
                            "|666|",
                            "|666|",
                            "L---/"],
                       chance=3, level=(4,14), count=3, branch='a'))

        self.add(Vault(syms=syms,
                       pic=["R---7",
                            "|999|",
                            "|999|",
                            "L---/"],
                       chance=3, level=(4,14), count=3, branch='c'))

        self.add(Vault(syms=syms,
                       pic=["R---7",
                            "|888|",
                            "|888|",
                            "L---/"],
                       chance=3, level=(4,14), count=3, branch='b'))


        ## The Rehabilitation Thunderdome

        symsq = {' ': None,
                 '.': (None, False),
                 ':': ('&', True, False),
                 'o': (':', False),
                 'w': ('W', False),
                 '#': (0, False),
                 '=': ('=', False),
                 'l': ('l', False),
                 'p': ('p', False),
                 'r': ('r', False),
                 'q': ('q', False),
                 'd': ('d', False),
                 'R': ('R.', False),
                 'L': ('L.', False),
                 'T': ('T.', False),
                 'F': ('F.', False),
                 'J': ('J.', False),
                 'Z': ('Z.', False),
                 '7': ('7.', False),
                 '/': ('/.', False),
                 '-': ('-.', False),
                 '|': ('|.', False),
                 '+': ('+.', False),
                 '1': ('1', True),
                 '2': ('2', True),
                 '3': ('3', True),
                 '4': ('4', True),
                 '5': ('5', True),
                 '@': (None, True)}


        self.add(Vault(syms=symsq,
                       pic=["      ::::::::::::::::::::::::::::::::::::::::::::::      ",
                            "    ::::::::::::::::::::::::::::::::::::::::::::::::::    ",
                            "   :::R--------------------------------------------7:::   ",
                            "  :::R/............................................L7:::  ",
                            " :::R/..............................................L7::: ",
                            ":::R/................................................L7:::",
                            ":::|..................................................|:::",
                            ":::|..................................................|:::",
                            ":::L7................................................R/:::",
                            " :::L7..............................................R/::: ",
                            "  :::L7............................................R/:::  ",
                            "   :::L--------------------------------------------/:::   ",
                            "    ::::::::::::::::::::::::::::::::::::::::::::::::::    ",
                            "      ::::::::::::::::::::::::::::::::::::::::::::::      "],
                       chance=1, level=(3,3), count=1, branch='q', anywhere=True,
                       message=["This is Thunderdome!",
                                "Two men enter, one man leaves!"]))

        self.add(Vault(syms=symsq,
                       pic=["      ::::::::::::::::::::::::::::::::::::::::::::::      ",
                            "    ::::::::::::::::::::::::::::::::::::::::::::::::::    ",
                            "   :::R--------------------------------------------7:::   ",
                            "  :::R/............................................L7:::  ",
                            " :::R/....o....o....o....o..oo..o....o....o....o....L7::: ",
                            ":::R/................................................L7:::",
                            ":::|......o....o....o....o..oo..o....o....o....o......|:::",
                            ":::|......o....o....o....o..oo..o....o....o....o......|:::",
                            ":::L7................................................R/:::",
                            " :::L7....o....o....o....o..oo..o....o....o....o....R/::: ",
                            "  :::L7............................................R/:::  ",
                            "   :::L--------------------------------------------/:::   ",
                            "    ::::::::::::::::::::::::::::::::::::::::::::::::::    ",
                            "      ::::::::::::::::::::::::::::::::::::::::::::::      "],
                       chance=1, level=(4,4), count=1, branch='q', anywhere=True,
                       message=["This is Thunderdome!",
                                "Two men enter, one man leaves!"]))

        self.add(Vault(syms=symsq,
                       pic=["      ::::::::::::::::::::::::::::::::::::::::::::::      ",
                            "    ::::::::::::::::::::::::::::::::::::::::::::::::::    ",
                            "   :::R--------------------------------------------7:::   ",
                            "  :::R/..........wwwwwwwwwwwwwwwwwwwwwww...........L7:::  ",
                            " :::R/..wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww..L7::: ",
                            ":::R/..wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww..L7:::",
                            ":::|...wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww...|:::",
                            ":::|...wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww...|:::",
                            ":::L7..wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww..R/:::",
                            " :::L7..wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww..R/::: ",
                            "  :::L7..........wwwwwwwwwwwwwwwwwwwwwww...........R/:::  ",
                            "   :::L--------------------------------------------/:::   ",
                            "    ::::::::::::::::::::::::::::::::::::::::::::::::::    ",
                            "      ::::::::::::::::::::::::::::::::::::::::::::::      "],
                       chance=1, level=(5,5), count=1, branch='q', anywhere=True,
                       message=["This is Thunderdome!",
                                "Three men enter, one man leaves!"]))

        self.add(Vault(syms=symsq,
                       pic=["      ::::::::::::::::::::::::::::::::::::::::::::::      ",
                            "    ::::::::::::::::::::::::::::::::::::::::::::::::::    ",
                            "   :::R--------------------------------------------7:::   ",
                            "  :::R/.......r====q..........r==========q...r===q.L7:::  ",
                            " :::R/...r====d....pq..r===q..l..........p===d...l..L7::: ",
                            ":::R/...rd..........l..l...l..p=======q..........l...L7:::",
                            ":::|...rd..r====q...l..l...l..........l...r====q.pq...|:::",
                            ":::|......rd....p===d..l...l...r===q..p===d....l..pq..|:::",
                            ":::L7.....l............l...l...l...l...........l.....R/:::",
                            " :::L7....pq...r===q...l...p===d...l...r===q...l....R/::: ",
                            "  :::L7....p===d...p===d...........p===d...p===d...R/:::  ",
                            "   :::L--------------------------------------------/:::   ",
                            "    ::::::::::::::::::::::::::::::::::::::::::::::::::    ",
                            "      ::::::::::::::::::::::::::::::::::::::::::::::      "],
                       chance=1, level=(6,6), count=1, branch='q', anywhere=True,
                       message=["This is Thunderdome!",
                                "Three men enter, one man leaves!"]))


        self.add(Vault(syms=symsq,
                       pic=["   :::..............................................:::   ",
                            "  ::.......................12345......................::  ",
                            " ::...R-----------------7.........R----------------7...:: ",
                            "::...R/.................L7.......R/................L7...::",
                            ":...R/.........#.........L7.....R/........#.........L7...:",
                            "...R/.......#######.......L-----/......#######.......L7...",
                            "...|.....####:::::####..............####:::::####.....|...",
                            "...|.....####:::::####..............####:::::####.....|...",
                            "...L7.......#######.......R-----7......#######.......R/...",
                            ":...L7.........#.........R/.....L7........#.........R/...:",
                            "::...L7.................R/.......L7................R/...::",
                            " ::...L-----------------/.........L----------------/...:: ",
                            "  ::.......................12345......................::  ",
                            "   :::..............................................:::   "],
                       chance=1, level=(7,7), count=1, branch='q', anywhere=True,
                       message=["This is Thunderdome!",
                                "Four men enter, one man leaves!"]))


    def add(self, v):
        v.postprocess()

        if v.branch:
            if v.branch not in self.vaults:
                self.vaults[v.branch] = {}

        for k,val in self.vaults.iteritems():
            if v.branch and v.branch != k:
                continue

            for x in xrange(v.level[0], v.level[1]+1):
                if x not in val:
                    val[x] = []
                val[x].append(v)

    def purge(self, vault):
        l = []

        for branch,v in self.vaults.iteritems():
            for level,v2 in v.iteritems():
                for x in xrange(len(v2)):
                    if id(vault) == id(v2[x]):
                        l.append((branch, level, x))

        for branch,level,x in l:
            del self.vaults[branch][level][x]

            if len(self.vaults[branch][level]) == 0:
                del self.vaults[branch][level]

            if len(self.vaults[branch]) == 0:
                del self.vaults[branch]


    def get(self, branch, level, vaultstoskip):

        if len(self.vaults) == 0:
            return None

        if branch not in self.vaults or len(self.vaults[branch]) == 0:
            return None

        while level > 0 and level not in self.vaults[branch]:
            level -= 1

        if level == 0:
            return None

        for x in xrange(len(self.vaults[branch][level])):
            v = self.vaults[branch][level][x]

            chance = random.randint(1, v.chance)

            if v in vaultstoskip:
                continue

            if chance != 1:
                continue

            if v.count == 1:
                self.purge(v)

            else:
                v.count -= 1

            return v

        return None

