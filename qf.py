
import features

f = features.FeatureStock()

cols = {}

for k in features.libtcod.__dict__:
    if k[0].lower() != k[0]:
        continue
    try:
        cols[getattr(features.libtcod, k)] = k
    except:
        pass

def get_gprops(f):
    if f.walkable and f.visible and f.height == -10 and not f.lit and f.water is None:
        return "(floor->Gridprops)"
    elif not f.walkable and f.visible and not f.lit and f.water is None:
        return "(%d glass->Gridprops)" % f.height
    elif not f.walkable and not f.visible and not f.lit and f.water is None:
        return "(%d wall->Gridprops)" % f.height
    else:
        if f.water is None:
            return "Gridprops{ walkable=%s visible=%s height=%s lit=%s }" % (reprr(f.walkable),
                                                                             reprr(f.visible),
                                                                             reprr(f.height),
                                                                             reprr(f.lit))
        elif f.walkable and f.visible and f.height == -10 and not f.lit:
            return "(%s water->Gridprops)" % reprr(f.water)
        print f.walkable, f.visible, f.height, f.lit, f.water
        return "!!!"

def reprr(v, issym=False):
    if v == True:
        return 'true'
    elif v == False:
        return 'false'
    elif type(v) == type(''):
        return "'" + v.replace("'", "\\'") + "'"
    elif v in cols:
        return "'" + cols[v] + "'"
    elif type(v) == type(1):
        if issym:
            return '(%d char->Sym)' % v
        return '%d' % v
    elif type(v) == type(1.0):
        return '%g' % v
    else:
        return '!!!'

def get_flags(f):
    s = ""
    ss = set(('walkable', 'visible', 'height', 'lit', 'water', 'skin', 'back'))
    for v in f.__dict__:
        if v in ss: continue
        if getattr(f, v):
            s += ("%s=%s " % (v, reprr(getattr(f, v))))
    return s

for k,v in f.f.iteritems():
    if v.nofeature:
        print ("[ %s %s ] featstock_set\n" % (reprr(k), get_gprops(v)))
    elif v.skin:
        print ("[ %s \n"
               "  Feat{ props=%s\n"
               "        skin=Skin{char=%s color=%s}\n"
               "        flags=Flags{%s} } ] featstock_set\n" % 
               (reprr(k), get_gprops(v), 
                reprr(v.skin[0], True), 
                reprr(v.skin[1]), get_flags(v)))
    elif v.back:
        print ("[ %s \n"
               "  FeatNoSkin{ props=%s\n"
               "              back=%s\n"
               "              flags=Flags{%s} } ] featstock_set\n" %
               (reprr(k), get_gprops(v),
                reprr(v.back), get_flags(v)))
    else:
        print "!!!"


# for k,v in f.f.iteritems():
#     #print k,v
#     for i in v.__dict__:
#         if i not in d:
#             d[i] = set()
#         d[i].add(type(getattr(v, i)))

# for k,v in d.iteritems():
#     if len(v) != 1: 
#         continue
#     print k, ':',
#     for i in v:
#         print '\t', str(i),
#     print

# for k,v in d.iteritems():
#     if len(v) == 1: 
#         continue
#     print k, ':',
#     for i in v:
#         print '\t', str(i),
#     print






