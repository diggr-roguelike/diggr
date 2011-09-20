#!/usr/bin/env python2.6

import cgi

import cgitb
cgitb.enable()

import sqlite3
import json




def ach_tag_to_text(tag):
    whole = {'loser': 'Scored *no* kills',
             'tourist' : 'Dived to a very deep dungeon',
             'small_tourist': 'Dived to a deep dungeon',
             'religion': 'Worshipped a god',
             'nowish': 'Never wished for an item',
             'nogun': 'Never used a firearm',
             'winner': ' =*= Won the game =*= ',
             'stealth': 'Killed a monster massively out of depth',
             'small_stealth': 'Killed a monster out of depth',
             'onebranch': 'Visited only one dungeon branch',
             'norod': 'Never used a dowsing rod',
             'teetotal': 'Never ate food, drank alcohol or used medicine',
             'nofood': 'Never ate a mushroom',
             'nopill': 'Never used medicine',
             'nobooze': 'Never drank alcohol',
             'nuked': 'Killed a monster with radiation',
             'nodig': 'Never used a pickaxe'
             }

    prefix = {'plev': 'Reached player level %s',
              'dlev': 'Reached dungeon level %s',
              'dead_': 'Killed by %s'
              }

    suffix = {'kills': 'Killed at least %s monsters',
              'gods': 'Worshipped %s gods',
              'prayers': 'Prayed at least %s times',
              'uses': 'Used an item at least %s times',
              'wish': 'Wished for an item %s times',
              'fires': 'Used a firearm at least %s times',
              'branch': 'Visited %s dungeon branches',
              'xting': 'Extinguished %s monster species',
              'food': 'Dined on mushrooms at least %s times',
              'booze': 'Drank booze at least %s times',
              'pill': 'Swallowed a pill at least %s times',
              'nuked': 'Killed at least %s monsters with radiation',
              'exploded': 'Exploded at least %s monsters'
              }

    if tag in whole:
        return whole[tag]

    for k,v in prefix.iteritems():
        if tag.startswith(k):
            return v % tag[len(k):]

    for k,v in suffix.iteritems():
        if tag.endswith(k):
            return v % tag[:-len(k)]

    return tag


def makeversion(v):
    s = set("0123456789")
    return ''.join(x for x in v if x in s)


def get_achievements(version='11.09.18'):

    tbl_games = 'Games%s' % makeversion(version)
    tbl_achievements = 'Achievements%s' % makeversion(version)

    conn = sqlite3.connect('highscore.db')
    c = conn.cursor()

    c.execute('select achievement, count(*) from %s join %s '
              'on (game_id = id) group by 1 order by 2 desc' % \
              (tbl_games, tbl_achievements))

    l = []    
    for ach,count in c.fetchall():              
        l.append({"achievement": ach, "count": count, 
                  "text": ach_tag_to_text(ach)})

    l.sort(cmp=lambda a,b: cmp(a['text'], b['text']))
    return l


def gameinfo(version='11.09.18', gameid=0):
    tbl_games = 'Games%s' % makeversion(version)
    tbl_achievements = 'Achievements%s' % makeversion(version)

    conn = sqlite3.connect('highscore.db')
    c = conn.cursor()

    c.execute('select score,seed from %s where id = %d' % (tbl_games, gameid))

    score, seed = c.fetchone()

    c.execute('select sum(score >= %d),count(*) from %s' % (score, tbl_games))

    place,total = c.fetchone()

    l = {}
    l['id'] = gameid
    l['score'] = score
    l['time'] = seed
    l['place'] = place
    l['numgames'] = total
    ach = []
    l['achievements'] = ach

    c.execute('select achievement from %s where game_id = %d' % (tbl_achievements, gameid))

    for aach in c.fetchall():
        aach = aach[0].encode('ascii')
        c.execute('select sum(score >= %d),count(*) from %s join %s on (game_id = id) where achievement = ?' % \
                      (score, tbl_games, tbl_achievements), (aach,))
        place1,total1 = c.fetchone()

        ach.append({'place': place1, 'numgames': total1,
                    'achievement': aach, 'text': ach_tag_to_text(aach)})

    ach.sort(cmp=lambda a,b: cmp((a['place'], a['numgames']),
                                 (b['place'], b['numgames'])))

    return l


def scoretable(version='11.09.18', sort=1, achievements=None, 
               limit=50, offset=0):

    tbl_games = 'Games%s' % makeversion(version)
    tbl_achievements = 'Achievements%s' % makeversion(version)

    conn = sqlite3.connect('highscore.db')
    c = conn.cursor()

    if achievements:
        c.execute('select distinct id, seed, score from %s join %s on (game_id = id) '
                  ' where achievement in (%s) order by %s desc'
                  ' limit %d offset %d' % \
                      (tbl_games, tbl_achievements, 
                       ','.join(['?'] * len(achievements)),
                       'seed' if sort == 1 else 'score',
                       limit, offset),
                  tuple(achievements))
    else:
        c.execute('select distinct id, seed, score from %s order by %s desc '
                  'limit %d offset %d' % \
                      (tbl_games, 
                       'seed' if sort == 1 else 'score',
                       limit, offset))

    l = []
    for gameid,seed,score in c.fetchall():
        c.execute('select achievement from %s where game_id = %d' % \
                      (tbl_achievements, gameid))
        achs = set(x[0] for x in c.fetchall())

        if achievements and not achs >= achievements:
            continue

        l.append({'id': gameid, 'time':seed, 'score':score,
                  'achievements': list(achs)})

    return l


def run():
    form = cgi.FieldStorage()

    f = {}

    if 'version' in form:
        f['version'] = form.getfirst('version')

    if 'get_achievements' in form:
        achs = get_achievements(**f)
        print "Content-Type: application/json"
        print
        print json.dumps(achs)
        return

    if 'gameid' in form:
        f['gameid'] = int(form.getfirst('gameid'))
        gamenf = gameinfo(**f)
        print "Content-Type: application/json"
        print
        print json.dumps(gamenf)
        return


    if 'sort' in form:
        f['sort'] = int(form.getfirst('sort'))

    if 'limit' in form:
        f['limit'] = int(form.getfirst('limit'))

    if 'offset' in form:
        f['offset'] = int(form.getfirst('offset'))

    if 'ach' in form:
        f['achievements'] = set(form.getlist('ach'))

    elif 'ach[]' in form:
        f['achievements'] = set(form.getlist('ach[]'))

    scores = scoretable(**f)

    print "Content-Type: application/json"
    print
    print json.dumps(scores)

run()
