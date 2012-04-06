
import monsters

m = monsters.MonsterStock()

cols = {}

for k in monsters.libtcod.__dict__:
    if k[0].lower() != k[0] or k[0] == '_':
        continue
    try:
        cols[getattr(monsters.libtcod, k)] = k
    except:
        pass

def reprr(v, issym=False):
    if type(v) == type(True) and v == True:
        return 'true'
    elif type(v) == type(False) and v == False:
        return 'false'
    elif type(v) == type(''):
        return "'" + v.replace("'", "\\'") + "'"
    elif type(v) == type([]):
        return '!!!' + str(type(v))
    elif v in cols:
        return "'" + cols[v] + "'"
    elif type(v) == type(1):
        if issym:
            return '(%d char->Sym)' % v
        return '%d' % v
    elif type(v) == type(1.0):
        return '%g' % v
    else:
        return '!!!' + str(type(v))

ms = []
for v2 in m.monsters.itervalues():
    for v1 in v2.itervalues():
        for v in v1:
            ms.append(v)

def cmp(m1, m2):
    k1 = (m1.branch, m1.level, m1.name)
    k2 = (m2.branch, m2.level, m2.name)
    if k1 < k2: return -1
    if k1 > k2: return 1
    return 0

types = {}
booltypes = set()
inttypes = set()
tuptypes = {}

ms.sort(cmp=cmp)
for m in ms:
    for v in m.__dict__:
        t = type(getattr(m, v))
        if v not in types:
            types[v] = set()
        types[v].add(t)

        if t == type((0,)):
            if v not in tuptypes:
                tuptypes[v] = set()
            tuptypes[v].add(len(getattr(m, v)))


for k,v in types.iteritems():
    if len(v) == 1:
        tt = list(v)[0]
        print k, tt
        if tt == type(True):
            booltypes.add(k)
        if tt == type(0):
            inttypes.add(k)

print

for k,v in types.iteritems():
    if len(v) != 1:
        print k, list(v)

print

class Foo:
    pass

def printmon(prev, m):

    if type(m) == type({}):
        mc = Foo()
        for k,v in m.iteritems():
            setattr(mc, k, v)
        m = mc

    if prev:
        print '[ %s (%s monsterstock_get {\n   ' % (reprr(m.idtag), reprr(prev)),
    else:
        print '[ %s\n  Monster{\n   ' % reprr(m.idtag),

    dd = m.__dict__.keys()

    for xx in ['psyattack', 'defence', 'attack', 'count', 'level', 'branch', 'name', 'skin']:
        if xx in dd:
            dd.remove(xx)
            dd.insert(0, xx)

    dd.insert(-1, '')

    if 'desc' in dd:
        dd.remove('desc')
        dd.insert(-1, 'desc')

    n = 0
    for v in dd:
        if v == '':
            print '\n   ',
            continue

        vv = getattr(m, v)
        if v in booltypes and vv == False:
            continue
        if v in inttypes and vv == 0:
            continue
        if type(None) in types[v] and vv == None:
            continue

        if v in ('xy', 'known_pxy', 'hp', 'items', 'idtag'):
            continue

        n += 1
        if (n % 6) == 0:
            print '\n   ',

        if v == 'skin':
            print ("skin=Skin{ char=%s color=%s }" % (reprr(vv[0], True), reprr(vv[1]))),
        elif v == 'desc':
            print ("desc=%s" % reprr('\\n'.join(vv))),
        elif v in tuptypes and len(tuptypes[v]) == 1 and type(vv) == type((0,)):
            if v == 'summon':
                print ('summon=Summon{mon=%s timeout=%s}' % (reprr(vv[0]), reprr(vv[1]))),
            elif v == 'bloodsucker':
                print ('%s=TimedEffect{damage=%s timeout=%s}' % (v, reprr(vv[0]), reprr(vv[1]))),
            elif v == 'summononce' or v == 'raise_dead':
                print ('%s=NumEffect{num=%s timeout=%s}' % (v, reprr(vv[0]), reprr(vv[1]))),
            print ('%s=[ %s ]' % (v, ' '.join(reprr(x) for x in vv))),
        else:
            print ("%s=%s" % (v, reprr(vv))),
    if prev:
        print '} ) ]'
    else:
        print '} ]'
    print


def mdiffs(m1, m2):
    d1 = m1.__dict__.keys()
    d2 = m2.__dict__.keys()
    ret = {}
    for k in set(d1) | set(d2):
        if k in d1 and k in d2 and getattr(m1, k) == getattr(m2, k):
            continue
        ret[k] = getattr(m1, k)
    return ret

sortd = []

linked = {}

def walk_linked(frm, to):
    if frm not in linked:
        return False

    q = linked[frm]
    if q == to:
        return True
    return walk_linked(q, to)

for m in ms:
    minm = None
    minidtag = None
    for m2 in ms:
        if m == m2: continue

        if walk_linked(m2.idtag, m.idtag):
            continue

        md = mdiffs(m, m2)
        if minm is None or len(md) < len(minm):
            minm = md
            minidtag = m2.idtag

    if minidtag is None:
        minidtag = None
        minm = m

    sortd.append((m.branch, m.level, m.name, minidtag, minm))
    linked[m.idtag] = minidtag
    print m.idtag

sortd.sort()

print '-------------------------------------------------------'

for b,l,n,minidtag,minm in sortd:
    printmon(minidtag, minm)


