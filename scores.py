
import cPickle

import sqlite3
import string
import httplib
import hashlib

import dgsys
import flair

import libtcodpy as libtcod
import libdiggrpy as dg


def form_highscore(score, seed, bones, achievements_, msgs, done):

    # Save to highscore.

    conn = sqlite3.connect('highscore.db')
    c = conn.cursor()

    tbl_games = 'Games%s' % dgsys._version.replace('.', '')
    tbl_achievements = 'Achievements%s' % dgsys._version.replace('.', '')

    c.execute('create table if not exists ' + tbl_games + \
                  ' (id INTEGER PRIMARY KEY, seed INTEGER, score INTEGER, bones BLOB, inputs BLOB)')
    c.execute('create table if not exists ' + tbl_achievements + \
                  ' (achievement TEXT, game_id INTEGER)')


    _inputs = []
    inpsize = dg.render_get_keylog_size()
    for x in xrange(inpsize):
        k = dg.render_get_keylog_entry(x)
        if not k:
            raise Exception('Sanity error in reading keylog for highscore entry.')
        _inputs.append(k)

    bones = cPickle.dumps(bones)
    inputs = cPickle.dumps(_inputs)

    c.execute('insert into ' + tbl_games + '(id, seed, score, bones, inputs) values (NULL, ?, ?, ?, ?)',
              (seed, score,
               sqlite3.Binary(bones),
               sqlite3.Binary(inputs)))

    gameid = c.lastrowid

    for a in achievements_:
        c.execute('insert into ' + tbl_achievements + '(achievement, game_id) values (?, ?)',
                  (a.tag, gameid))

    conn.commit()


    # Show placements.

    c.execute('select sum(score >= %d),count(*) from %s' % (score, tbl_games))
    place, total = c.fetchone()

    atotals = []
    achievements = []

    for a in achievements_:
        c.execute(('select sum(score >= %d),count(*) from ' % score) + \
                  (' %s join %s on (game_id = id)' % (tbl_games, tbl_achievements)) + \
                  ' where achievement = ?', (a.tag,))
        p1,t1 = c.fetchone()
        atotals.append((p1, 100 - a.weight, t1, a.desc))
        achievements.append(a.tag)

    c.close()
    conn.close()

    atotals.sort()

    if len(atotals) >= 5:
        atotals = atotals[:5]

    s = []

    s.append('%cYour score: %c%d%c.    (#%c%d%c of %d%s)' % \
            (libtcod.COLCTRL_5, libtcod.COLCTRL_1, score, libtcod.COLCTRL_5,
             libtcod.COLCTRL_1, place, libtcod.COLCTRL_5, total, '!' if place == 1 else '.'))
    s.append('')
    s.append('Your achievements:')
    s.append('')

    for p1,w,t1,a in atotals:
        s.append('%c%s%c:%s     #%c%d%c of %d%s' % (libtcod.COLCTRL_1, a, libtcod.COLCTRL_5,
                 ' '*max(0, 50 - len(a)), libtcod.COLCTRL_1, p1,
                 libtcod.COLCTRL_5, t1, '!' if p1 == 1 else '.'))
        s.append('')

    s.append('-' * 50)
    s.extend((x[1] for x in msgs[2:8]))
    s.append('')
    s.append('%cUpload your score to http://diggr.name? (Press Y or N)%c' % (libtcod.COLCTRL_3, libtcod.COLCTRL_1))

    while 1:
        c = flair.draw_window(s)
        if c == 'n' or c == 'N':
            break
        elif c == 'y' or c == 'Y':

            done = False

            while not done:
                done = upload_score(seed, score, bones, inputs, achievements)

                if not done:
                    c = flair.draw_window(['',
                                           'Uploading failed!',
                                           'Most likely, you entered the wrong password.',
                                           '',
                                           'Try again? (Press Y or N)'])
                    if c == 'n' or c == 'N':
                        done = True
            break

    s[-1] = ('Press space to ' + ('exit.' if done else 'try again.'))

    while 1:
        if flair.draw_window(s) == ' ':
            break



def upload_score(seed, score, bones, inputs, achievements):


    username = ''

    while 1:
        k = flair.draw_window(['',
                               'Enter username: ' + username,
                               '',
                               "      If you don't have an account with that username, it will",
                               '      be created for you automatically.'])

        if k in string.letters or k in string.digits or k in '.-_':
            username = username + k.lower()
        elif ord(k) == 8 or ord(k) == 127:
            if len(username) > 0:
                username = username[:-1]
        elif k in '\r\n':
            break

    password = ''
    stars = ''

    while 1:
        k = flair.draw_window(['',
                               'Enter password: ' + stars,
                               '',
                               'NOTE: Your password will never be sent or stored in plaintext.',
                               '      Only a secure password hash will be used.'])

        if k in string.letters or k in string.digits or k in '_-':
            password = password + k
            stars = stars + '*'
        elif ord(k) == 8 or ord(k) == 127:
            if len(password) > 0:
                password = password[:-1]
                stars = stars[:-1]
        elif k in '\r\n':
            break

    form = {'upload': '1',
            'version': dgsys._version,
            'username': username,
            'pwhash': hashlib.sha512(password).hexdigest(),
            'seed': str(seed),
            'score': str(score),
            'bones': bones,
            'inputs': inputs }

    boundary = '----diggr-multipart-upload'
    multipart = ''

    def mpart(k,v):
        ret = ''
        ret += '--%s\r\n' % boundary
        ret += 'Content-Disposition: form-data; name="%s"\r\n' % k
        ret += '\r\n'
        ret += v
        ret += '\r\n'
        return ret

    for k,v in form.iteritems():
        multipart += mpart(k, v)

    for a in achievements:
        multipart += mpart('ach', a)

    multipart += '--%s--\r\n' % boundary
    multipart += '\r\n'

    hclient = httplib.HTTPConnection('diggr.name')
    hclient.putrequest('POST', '/scripts/global-highscore.py')
    hclient.putheader('content-type',
                      'multipart/form-data; boundary=%s' % boundary)
    hclient.putheader('content-length', str(len(multipart)))
    hclient.endheaders()
    hclient.send(multipart)

    resp = hclient.getresponse()
    r = resp.read()

    if r == "OK\n":
        return True
    #print r
    return False
