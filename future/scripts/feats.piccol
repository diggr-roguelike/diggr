
def {
  char: Sym
  color: Sym
} Skin;

def { v:Int } Toggle;

toggled Toggle->Bool :- 
   <: \v < 0 :> ? false ;
   <: \v > 0 :> ? true.

toggled Bool->Toggle :-
   \v ? Toggle{v=1};
   Toggle{v=-1}.

def {
  water: Toggle
  height: Int
  lit
  walkable 
  visible
} Gridprops;


def {
  confuse
  sticky
  pois2
  shootable
  v_shrine
  s_shrine
  healingfountain
  bb_shrine
  permanent
  warm
  b_shrine

  lightbonus: Int
  explode: Int
  stairs: Int

  poison: Real
  queasy: Real
  fire: Real

  name: Sym
  special: Sym
  branch: Sym
  sign: Sym
  resource: Sym
} Flags;


def {
  flags: Flags
  props: Gridprops
  back: Sym
} FeatNoSkin;

def {
  flags: Flags
  props: Gridprops
  skin: Skin
} Feat;


def [tag:Sym feat:Feat];
def [tag:Sym feat:FeatNoSkin];
def [tag:Sym props:Gridprops];

floor Void->Gridprops :- Gridprops{ walkable=true visible=true height=-10 }.
glass Int->Gridprops :- Gridprops{ walkable=false visible=true height=\v }.
wall Int->Gridprops :- Gridprops{ walkable=false visible=false height=\v }.
water Bool->Gridprops :- Gridprops{ walkable=true visible=true height=-10 water=(\v toggled->Toggle) }.

char Int->Sym :- \v $to_sym.


featstock_set [Sym Feat]->Void :-.
featstock_set [Sym FeatNoSkin]->Void :-.
featstock_set [Sym Gridprops]->Void :-.

featstock_init Void->Void :-

[ 'signcth2' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(250 char->Sym) color='red'}
        flags=Flags{name='eldritch engravings' sign='MGLW\'NAFH' } } ] featstock_set

[ 'signcth3' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(250 char->Sym) color='red'}
        flags=Flags{name='eldritch engravings' sign='CTHULHU' } } ] featstock_set

[ 'signcth1' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(250 char->Sym) color='red'}
        flags=Flags{name='eldritch engravings' sign='PH\'NGLUI' } } ] featstock_set

[ 'signcth6' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(250 char->Sym) color='red'}
        flags=Flags{name='eldritch engravings' sign='FHTAGN' } } ] featstock_set

[ 'signcth4' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(250 char->Sym) color='red'}
        flags=Flags{name='eldritch engravings' sign='R\'LYEH' } } ] featstock_set

[ 'signcth5' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(250 char->Sym) color='red'}
        flags=Flags{name='eldritch engravings' sign='WGAH\'NAGL' } } ] featstock_set

[ '##' 
  Feat{ props=(1 wall->Gridprops)
        skin=Skin{char=(176 char->Sym) color='grey'}
        flags=Flags{name='carbonized graphite' } } ] featstock_set

[ 'kali' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(234 char->Sym) color='white'}
        flags=Flags{special='kali' name='a statue of Kali' } } ] featstock_set

[ '#!' 
  Feat{ props=(1000 wall->Gridprops)
        skin=Skin{char=(176 char->Sym) color='grey'}
        flags=Flags{permanent=true name='crystalline graphite' } } ] featstock_set

[ '+.' 
  Feat{ props=(0 glass->Gridprops)
        skin=Skin{char=(206 char->Sym) color='gray'}
        flags=Flags{name='bulletproof glass' } } ] featstock_set

[ 'Y' 
  Feat{ props=(5 wall->Gridprops)
        skin=Skin{char=(157 char->Sym) color='green'}
        flags=Flags{name='a tree' } } ] featstock_set

[ 'cthulhu' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(16 char->Sym) color='gray'}
        flags=Flags{special='cthulhu' name='an unholy stone' } } ] featstock_set

[ 'monolith' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(8 char->Sym) color='light_gray'}
        flags=Flags{special='monolith' name='the Monolith' } } ] featstock_set

[ '!' 
  Feat{ props=Gridprops{ walkable=true visible=false height=-10 lit=false }
        skin=Skin{char=(173 char->Sym) color='dark_green'}
        flags=Flags{name='a giant fern' } } ] featstock_set

[ 'Z.' 
  Feat{ props=(0 glass->Gridprops)
        skin=Skin{char=(185 char->Sym) color='gray'}
        flags=Flags{name='bulletproof glass' } } ] featstock_set

[ '\"' 
  FeatNoSkin{ props=(floor->Gridprops)
              back='red'
              flags=Flags{fire=0.333 name='napalm' } } ] featstock_set

[ '$' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(20 char->Sym) color='light_sky'}
        flags=Flags{healingfountain=true name='a Fountain of Youth' } } ] featstock_set

[ '&' 
  FeatNoSkin{ props=Gridprops{ walkable=true visible=true height=-10 lit=true }
              back='darkest_blue'
              flags=Flags{explode=3 queasy=0.1 name='swamp gas' } } ] featstock_set

[ '+' 
  Feat{ props=(0 wall->Gridprops)
        skin=Skin{char=(206 char->Sym) color='white'}
        flags=Flags{name='a smooth stone wall' } } ] featstock_set

[ '*' 
  Feat{ props=Gridprops{ walkable=true visible=false height=-10 lit=false }
        skin=Skin{char='*' color='lightest_green'}
        flags=Flags{name='rubble' } } ] featstock_set

[ '-' 
  Feat{ props=(0 wall->Gridprops)
        skin=Skin{char=(205 char->Sym) color='white'}
        flags=Flags{name='a smooth stone wall' } } ] featstock_set

[ 'J.' 
  Feat{ props=(0 glass->Gridprops)
        skin=Skin{char=(202 char->Sym) color='gray'}
        flags=Flags{name='bulletproof glass' } } ] featstock_set

[ '/' 
  Feat{ props=(0 wall->Gridprops)
        skin=Skin{char=(188 char->Sym) color='white'}
        flags=Flags{name='a smooth stone wall' } } ] featstock_set

[ '.' (false water->Gridprops) ] featstock_set

[ '1' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char='>' color='lime'}
        flags=Flags{branch='a' stairs=1 name='a hole in the floor' } } ] featstock_set

[ 'signvault' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(254 char->Sym) color='white'}
        flags=Flags{name='an engraving on the floor' sign='"Entrance to the Vault. Robbers beware."' } } ] featstock_set

[ '3' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char='>' color='sky'}
        flags=Flags{branch='c' stairs=1 name='a hole in the floor' } } ] featstock_set

[ '2' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char='>' color='crimson'}
        flags=Flags{branch='b' stairs=1 name='a hole in the floor' } } ] featstock_set

[ '5' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char='>' color='light_gray'}
        flags=Flags{branch='e' stairs=1 name='a hole in the floor' } } ] featstock_set

[ '4' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char='>' color='dark_gray'}
        flags=Flags{branch='d' stairs=1 name='a hole in the floor' } } ] featstock_set

[ '7' 
  Feat{ props=(0 wall->Gridprops)
        skin=Skin{char=(187 char->Sym) color='white'}
        flags=Flags{name='a smooth stone wall' } } ] featstock_set

[ '6' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(175 char->Sym) color='white'}
        flags=Flags{branch='s' stairs=1 name='a hole in the floor' } } ] featstock_set

[ '8' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(175 char->Sym) color='red'}
        flags=Flags{branch='q' stairs=1 name='an entrance to the Rehabilitation Thunderdome' } } ] featstock_set

[ ':' 
  Feat{ props=(0 wall->Gridprops)
        skin=Skin{char=(9 char->Sym) color='white'}
        flags=Flags{name='a column' } } ] featstock_set

[ '=' 
  Feat{ props=(-10 glass->Gridprops)
        skin=Skin{char=(196 char->Sym) color='gray'}
        flags=Flags{name='barricades' shootable=true } } ] featstock_set

[ '>' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char='>' color='white'}
        flags=Flags{stairs=1 name='a hole in the floor' } } ] featstock_set

[ '@' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(15 char->Sym) color='yellow'}
        flags=Flags{warm=true name='a hearth' } } ] featstock_set

[ 'C' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(20 char->Sym) color='dark_green'}
        flags=Flags{resource='g' name='a Green Fountain' } } ] featstock_set

[ 'B' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(20 char->Sym) color='dark_yellow'}
        flags=Flags{resource='y' name='a Yellow Fountain' } } ] featstock_set

[ 'bb' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(16 char->Sym) color='crimson'}
        flags=Flags{bb_shrine=true name='an Altar of Ba\'al-Zebub' } } ] featstock_set

[ 'F' 
  Feat{ props=(0 wall->Gridprops)
        skin=Skin{char=(204 char->Sym) color='white'}
        flags=Flags{name='a smooth stone wall' } } ] featstock_set

[ 'L.' 
  Feat{ props=(0 glass->Gridprops)
        skin=Skin{char=(200 char->Sym) color='gray'}
        flags=Flags{name='bulletproof glass' } } ] featstock_set

[ '7.' 
  Feat{ props=(0 glass->Gridprops)
        skin=Skin{char=(187 char->Sym) color='gray'}
        flags=Flags{name='bulletproof glass' } } ] featstock_set

[ 'dd' 
  Feat{ props=Gridprops{ walkable=true visible=true height=-10 lit=true }
        skin=Skin{char='^' color='white'}
        flags=Flags{lightbonus=7 name='a dolmen' } } ] featstock_set

[ 'J' 
  Feat{ props=(0 wall->Gridprops)
        skin=Skin{char=(202 char->Sym) color='white'}
        flags=Flags{name='a smooth stone wall' } } ] featstock_set

[ 'M' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(20 char->Sym) color='dark_purple'}
        flags=Flags{resource='p' name='a Purple Fountain' } } ] featstock_set

[ 'L' 
  Feat{ props=(0 wall->Gridprops)
        skin=Skin{char=(200 char->Sym) color='white'}
        flags=Flags{name='a smooth stone wall' } } ] featstock_set

[ 'N' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(20 char->Sym) color='dark_sky'}
        flags=Flags{resource='b' name='a Blue Fountain' } } ] featstock_set

[ 'T.' 
  Feat{ props=(0 glass->Gridprops)
        skin=Skin{char=(203 char->Sym) color='gray'}
        flags=Flags{name='bulletproof glass' } } ] featstock_set

[ '!f' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(24 char->Sym) color='desaturated_green'}
        flags=Flags{name='a flowering fern' } } ] featstock_set

[ 'R' 
  Feat{ props=(0 wall->Gridprops)
        skin=Skin{char=(201 char->Sym) color='white'}
        flags=Flags{name='a smooth stone wall' } } ] featstock_set

[ 'T' 
  Feat{ props=(0 wall->Gridprops)
        skin=Skin{char=(203 char->Sym) color='white'}
        flags=Flags{name='a smooth stone wall' } } ] featstock_set

[ 'W' (true water->Gridprops) ] featstock_set

[ 'V' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(20 char->Sym) color='dark_red'}
        flags=Flags{resource='r' name='a Red Fountain' } } ] featstock_set

[ '|.' 
  Feat{ props=(0 glass->Gridprops)
        skin=Skin{char=(186 char->Sym) color='gray'}
        flags=Flags{name='bulletproof glass' } } ] featstock_set

[ 'signkali' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char='.' color='white'}
        flags=Flags{name='an engraving on the floor' sign='kali ma, kali ma shakti de' } } ] featstock_set

[ 'R.' 
  Feat{ props=(0 glass->Gridprops)
        skin=Skin{char=(201 char->Sym) color='gray'}
        flags=Flags{name='bulletproof glass' } } ] featstock_set

[ 'Z' 
  Feat{ props=(0 wall->Gridprops)
        skin=Skin{char=(185 char->Sym) color='white'}
        flags=Flags{name='a smooth stone wall' } } ] featstock_set

[ '^' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(248 char->Sym) color='red'}
        flags=Flags{sticky=true name='a cave floor covered with glue' } } ] featstock_set

[ 'a' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(254 char->Sym) color='green'}
        flags=Flags{name='an abandoned altar stone' } } ] featstock_set

[ '/.' 
  Feat{ props=(0 glass->Gridprops)
        skin=Skin{char=(188 char->Sym) color='gray'}
        flags=Flags{name='bulletproof glass' } } ] featstock_set

[ 'b' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(127 char->Sym) color='white'}
        flags=Flags{name='a shrine to Brahma' b_shrine=true } } ] featstock_set

[ 'e' 
  FeatNoSkin{ props=(floor->Gridprops)
              back='desaturated_green'
              flags=Flags{poison=0.5 name='a cloud of Ebola virus' } } ] featstock_set

[ 'd' 
  Feat{ props=(-10 glass->Gridprops)
        skin=Skin{char=(217 char->Sym) color='gray'}
        flags=Flags{name='barricades' shootable=true } } ] featstock_set

[ 'g' 
  FeatNoSkin{ props=(floor->Gridprops)
              back='dark_green'
              flags=Flags{pois2=true poison=0.25 name='spores of black mold' } } ] featstock_set

[ 'f' 
  FeatNoSkin{ props=(floor->Gridprops)
              back='gray'
              flags=Flags{confuse=true name='confusing smoke' } } ] featstock_set

[ 'h' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(242 char->Sym) color='white'}
        flags=Flags{stairs=6 name='a dropchute' } } ] featstock_set

[ '-.' 
  Feat{ props=(0 glass->Gridprops)
        skin=Skin{char=(205 char->Sym) color='gray'}
        flags=Flags{name='bulletproof glass' } } ] featstock_set

[ 'l' 
  Feat{ props=(-10 glass->Gridprops)
        skin=Skin{char=(179 char->Sym) color='gray'}
        flags=Flags{name='barricades' shootable=true } } ] featstock_set

[ 'q' 
  Feat{ props=(-10 glass->Gridprops)
        skin=Skin{char=(191 char->Sym) color='gray'}
        flags=Flags{name='barricades' shootable=true } } ] featstock_set

[ 'p' 
  Feat{ props=(-10 glass->Gridprops)
        skin=Skin{char=(192 char->Sym) color='gray'}
        flags=Flags{name='barricades' shootable=true } } ] featstock_set

[ 's' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(234 char->Sym) color='darker_grey'}
        flags=Flags{s_shrine=true name='a shrine to Shiva' } } ] featstock_set

[ 'r' 
  Feat{ props=(-10 glass->Gridprops)
        skin=Skin{char=(218 char->Sym) color='gray'}
        flags=Flags{name='barricades' shootable=true } } ] featstock_set

[ 'w' 
  Feat{ props=(true water->Gridprops)
        skin=Skin{char='-' color='sky'}
        flags=Flags{name='a pool of water' } } ] featstock_set

[ 'v' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(233 char->Sym) color='azure'}
        flags=Flags{v_shrine=true name='a shrine to Vishnu' } } ] featstock_set

[ 'qk' 
  Feat{ props=(floor->Gridprops)
        skin=Skin{char=(175 char->Sym) color='dark_gray'}
        flags=Flags{branch='qk' stairs=1 name='an entrace to the temple of Kali' } } ] featstock_set

[ '|' 
  Feat{ props=(0 wall->Gridprops)
        skin=Skin{char=(186 char->Sym) color='white'}
        flags=Flags{name='a smooth stone wall' } } ] featstock_set

[ 'F.' 
  Feat{ props=(0 glass->Gridprops)
        skin=Skin{char=(204 char->Sym) color='gray'}
        flags=Flags{name='bulletproof glass' } } ] featstock_set

.