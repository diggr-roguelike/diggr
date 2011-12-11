#!/usr/bin/env python2.6

import cgi

import cgitb
cgitb.enable()

import sqlite3
import json

import sys
import os
import time


DEFAULT_VERSION = '11.12.18'
USERPREF = "user_"


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
             'nodig': 'Never used a pickaxe',
	     'artifact': 'Crafted a powerful artifact',
	     'ebola': 'Killed a monster via Ebolavirus',
             'thunderdome': 'Visited the Rehabilitation Thunderdome',
             'thunderdome_win': 'Became a Thunderdome champion',
             'molds': 'Cleaned up black mold',
             'colorwow': 'Used colored liquid for great success',
             '6color': 'Drank colored liquid 6 times or more',
             'full_m_prism': 'Used a prism of the Full Moon',
             'new_m_prism': 'Used a prism of the New Moon'
             }

    prefix = {'plev': 'Reached player level %s',
              'dlev': 'Reached dungeon level %s',
              'dead_': 'Killed by %s',
              'moon_': 'Played on a %s moon',
              'user_': '%s'
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
              'exploded': 'Exploded at least %s monsters',
	      'craft': 'Tried crafting %s times',
	      'afacts': 'Crafted %s powerful artifacts',
	      'ebola': 'Killed at least %s monsters via Ebolavirus',
              'molds': 'Cleaned up black mold over %s times',
              'colorwow': 'Used colored liquid for great success %s times',
              'color': 'Drank colored liquid %s times'
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


def init(version=DEFAULT_VERSION):
    tbl_games = 'Games%s' % makeversion(version)
    tbl_achievements = 'Achievements%s' % makeversion(version)

    conn = sqlite3.connect('highscore.db')
    c = conn.cursor()

    c.execute('create table if not exists ' + tbl_games + \
                  ' (id INTEGER PRIMARY KEY, seed INTEGER, score INTEGER, bones BLOB, inputs BLOB)')

    c.execute('create table if not exists ' + tbl_achievements + \
                  ' (achievement TEXT, game_id INTEGER)')

    c.execute('create table if not exists Users (name TEXT, hash BLOB)')


def download(version=DEFAULT_VERSION, gameid=0):

    tbl_games = 'Games%s' % makeversion(version)
    tbl_achievements = 'Achievements%s' % makeversion(version)

    nm = '/tmp/tmp.db.%d.%g' % (os.getpid(), time.time())

    conn1 = sqlite3.connect(nm)
    c1 = conn1.cursor()

    c1.execute('create table if not exists ' + tbl_games + \
                   ' (id INTEGER PRIMARY KEY, seed INTEGER, score INTEGER, bones BLOB, inputs BLOB)')

    c1.execute('create table if not exists ' + tbl_achievements + \
                   ' (achievement TEXT, game_id INTEGER)')

    conn = sqlite3.connect('highscore.db')
    c = conn.cursor()

    c.execute('select seed, score, bones, inputs from %s where id = %d' % \
                  (tbl_games, gameid))

    for seed,score,bones,inputs in c.fetchall():
        c1.execute('insert into ' + tbl_games + '(id, seed, score, bones, inputs) values (NULL, ?, ?, ?, ?)',
                   (seed, score, bones, inputs))
        gameid2 = c1.lastrowid

        c.execute('select achievement from %s where game_id = %d' % (tbl_achievements, gameid))

        for ach in c.fetchall():
            ach = ach[0]

            if ach.startswith(USERPREF):
                continue

            c1.execute('insert into ' + tbl_achievements + '(achievement, game_id) values (?, ?)',
                       (ach, gameid2))

    conn1.commit()
    c1.close()
    conn1.close()

    print 'Content-Type: application/octet-stream'
    print 'Content-Disposition: attachment; filename="game%d.db"' % gameid
    print 'Content-Length: %d' % os.stat(nm).st_size
    print
    sys.stdout.write(open(nm).read())
    


def get_achievements(version=DEFAULT_VERSION):

    tbl_games = 'Games%s' % makeversion(version)
    tbl_achievements = 'Achievements%s' % makeversion(version)

    conn = sqlite3.connect('highscore.db')
    c = conn.cursor()

    c.execute('select achievement, count(*) from %s join %s '
              'on (game_id = id) group by 1 order by 2 desc' % \
              (tbl_games, tbl_achievements))

    l1 = []
    l2 = []
    for ach,count in c.fetchall():              
        if ach.startswith(USERPREF):
            l = l2
        else:
            l = l1

        l.append({"achievement": ach, "count": count, 
                  "text": ach_tag_to_text(ach)})

    l1.sort(cmp=lambda a,b: cmp(a['text'], b['text']))
    l2.sort(cmp=lambda a,b: cmp(a['text'], b['text']))

    return {"achievements": l1, "usernames": l2}


def gameinfo(version=DEFAULT_VERSION, gameid=0):
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

        if aach.startswith(USERPREF):
            l['username'] = ach_tag_to_text(aach)
            continue

        c.execute('select sum(score >= %d),count(*) from %s join %s on (game_id = id) where achievement = ?' % \
                      (score, tbl_games, tbl_achievements), (aach,))
        place1,total1 = c.fetchone()

        ach.append({'place': place1, 'numgames': total1,
                    'achievement': aach, 'text': ach_tag_to_text(aach)})

    ach.sort(cmp=lambda a,b: cmp((a['place'], a['numgames']),
                                 (b['place'], b['numgames'])))

    return l


def scoretable(version=DEFAULT_VERSION, sort=1, achievements=None, 
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
                       'score' if sort == 1 else 'seed',
                       limit, offset),
                  tuple(achievements))
    else:
        c.execute('select distinct id, seed, score from %s order by %s desc '
                  'limit %d offset %d' % \
                      (tbl_games, 
                       'score' if sort == 1 else 'seed',
                       limit, offset))

    l = []
    for gameid,seed,score in c.fetchall():
        c.execute('select achievement from %s where game_id = %d' % \
                      (tbl_achievements, gameid))
        achs = set(x[0] for x in c.fetchall())

        if achievements and not achs >= achievements:
            continue

        lach = []
        username = ''
        for a in achs:
            if a.startswith(USERPREF):
                username = ach_tag_to_text(a)
            else:
                lach.append(a)

        l.append({'id': gameid, 'time':seed, 'score':score, 
                  'username': username, 'achievements': lach})

    return l


def upload(version=DEFAULT_VERSION, username='', pwhash='', 
           seed=0, score=0, bones='', inputs='', 
           achievements=None):

    tbl_games = 'Games%s' % makeversion(version)
    tbl_achievements = 'Achievements%s' % makeversion(version)

    conn = sqlite3.connect('highscore.db')
    c = conn.cursor()

    c.execute('select hash from Users where name = ?', (username,))

    n = 0
    ok = False

    for h in c.fetchall():
        h = h[0]

        if h == pwhash:
            ok = True
        n += 1

    if not ok:
        if n == 0:
            c.execute('insert into Users (name, hash) values (?, ?)',
                      (username, pwhash))
        else:
            raise Exception('Invalid password for username=' + username)


    c.execute('insert into ' + tbl_games + '(id, seed, score, bones, inputs) values (NULL, ?, ?, ?, ?)',
               (seed, score, 
                sqlite3.Binary(bones), 
                sqlite3.Binary(inputs)))

    gameid = c.lastrowid

    achievements.add(USERPREF+username)

    for ach in achievements:
        c.execute('insert into ' + tbl_achievements + '(achievement, game_id) values (?, ?)',
                  (ach, gameid))

    conn.commit()
    c.close()
    conn.close()


def run():
    form = cgi.FieldStorage()

    f = {}

    if 'version' in form:
        f['version'] = form.getfirst('version')

    if 'do_init' in form:
        init(**f)
        print "Content-Type: text/html"
        print
        return

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

    if 'download' in form:
        f['gameid'] = int(form.getfirst('download'))
        download(**f)
        return

    if 'ach' in form:
        f['achievements'] = set(form.getlist('ach'))

    elif 'ach[]' in form:
        f['achievements'] = set(form.getlist('ach[]'))

    if 'upload' in form:
        f['username'] = form.getfirst('username')
        f['pwhash'] = form.getfirst('pwhash')
        f['seed'] = int(form.getfirst('seed'))
        f['score'] = int(form.getfirst('score'))
        f['bones'] = form.getfirst('bones')
        f['inputs'] = form.getfirst('inputs')

        upload(**f)
        print "Content-Type: text/plain"
        print
        print "OK"
        return

    ###

    if 'sort' in form:
        f['sort'] = int(form.getfirst('sort'))

    if 'limit' in form:
        f['limit'] = int(form.getfirst('limit'))

    if 'offset' in form:
        f['offset'] = int(form.getfirst('offset'))

    scores = scoretable(**f)

    print "Content-Type: application/json"
    print
    print json.dumps(scores)

run()
