
import items

i = items.ItemStock()

cols = {}

for k in items.libtcod.__dict__:
    if k[0].lower() != k[0] or k[0] == '_':
        continue
    try:
        cols[getattr(items.libtcod, k)] = k
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
        return '%du' % v
    elif type(v) == type(1.0):
        tmp = '%g' % v
        if '.' not in tmp:
            tmp = tmp + 'f'
        return tmp
    else:
        return '!!!' + str(type(v))


types = {}
tuptypes = {}

for m in i.__dict__:
    if m[0] == '_':
        continue
    m = getattr(i, m)
    for v in m.__dict__:
        t = type(getattr(m, v))
        if v not in types:
            types[v] = set()
        types[v].add(t)

        if t == type((0,)):
            if v not in tuptypes:
                tuptypes[v] = set()
            tuptypes[v].add(len(getattr(m, v)))

print '-'*10
for t in types.iteritems():
    print t
print '-'*10
for t in tuptypes.iteritems():
    print t

crafts = []

for j in i.__dict__:
    if j[0] == '_':
        continue
    it = getattr(i, j)
    print '[ %s Item{\n ' % reprr(j),

    nnn = 0

    dic = it.__dict__.keys()

    dic.remove('desc')
    dic.append('desc')

    dic.remove('name')
    dic.insert(0, 'name')
    dic.remove('skin')
    dic.insert(1, 'skin')
    dic.remove('slot')
    dic.insert(2, 'slot')
    dic.remove('rarity')
    dic.insert(3, 'rarity')

    for f in dic:
        if f in set(('corpse', 'ammo', 'gencount', 'tag')):
            continue
        vv = getattr(it, f)
        if vv is None and type(None) in types[f]:
            if f == 'rarity':
                vv = 0
            else:
                continue
        if vv == False and type(vv) == type(False) and len(types[f]) == 1 and type(False) in types[f]:
            continue
        if vv == 0 and type(vv) == type(1) and len(types[f]) == 1 and type(1) in types[f]:
            if f != 'rarity':
                continue

        if type(vv) == type(1) and len(types[f]) == 2 and type(1.0) in types[f] and type(1) in types[f]:
            if vv == 0:
                continue
            vv = float(vv)

        nnn += 1
        if nnn % 4 == 0:
            print '\n ',
        if f == 'skin':
            print ("skin=([%s %s] item->Skin)" % (reprr(vv[0], True), reprr(vv[1]))),
        elif f == 'desc':
            if nnn % 4 != 0:
                print '\n ',
            print ("desc=%s\n " % reprr('\\n'.join(vv))),
        elif f == 'craft':
            print 'craft=%s' % (reprr(vv[0])),
            crafts.append(vv)
        elif f == 'cursedchance':
            print '%s=GaussChance{stddev=%s thold=%s}' % (f, reprr(float(vv[0])), reprr(float(vv[1]))),
        elif f == 'winning':
            print '%s=Achievement{name=%s desc=%s}' % (f, reprr(vv[0]), reprr(vv[1])),
        elif f == 'selfdestruct' or f == 'confattack' or f == 'healingsleep':
            print '%s=GaussNat{mean=%s stddev=%s}' % (f, reprr(vv[0]), reprr(vv[1])),
        elif f == 'food' or f == 'healing':
            print '%s=Gauss{mean=%s stddev=%s}' % (f, reprr(float(vv[0])), reprr(float(vv[1]))),
        elif f == 'ammochance' or f == 'range':
            print '%s=Range{lo=%s hi=%s}' % (f, reprr(vv[0]), reprr(vv[1])),
        elif f == 'summon':
            print '%s=SummonN{mon=%s count=%s}' % (f, reprr(vv[0]), reprr(vv[1])),
        else:
            print '%s=%s' % (f, reprr(vv)),

    print '}] itemstock_set'
    print

print 'check_craft [Sym Sym]->Sym :- '
print '  <:[case] \\a : '
cc = []
for f,to in crafts:
    t = "    '%s' ? \\b->Sym( <:[case] \\v : \n" % f
    l = []
    for k,v in to.iteritems():
        l.append("      '%s' ? '%s'" % (k, v))
    t += ';\n'.join(l)
    t += ':>)'
    cc.append(t)
print ';\n'.join(cc)
print ':>.'


