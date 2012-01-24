#!/usr/bin/env python

import cPickle
import time
import string
import os

import libtcodpy as libtcod

import sqlite3

import diggr

Item = diggr.Item



def ach_tag_to_text(tag):
    whole = {'loser': 'Scored *no* kills',
             'tourist' : 'Dived to a very deep dungeon',
             'small_tourist': 'Dived to a deep dungeon',
             'religion': 'Worshipped a god',
             'nowish': 'Never wished for an item',
             'nogun': 'Never used a firearm',
             'winner': ' =*= Won the game =*= ',
             'winkali': 'Returned the Eye of Kali',
             'winroot': 'Hacked for the root password',
             'wincthulhu': 'Called upon Cthulhu',
             'stealth': 'Killed a monster massively out of depth',
             'small_stealth': 'Killed a monster out of depth',
             'onebranch': 'Visited only one dungeon branch',
             'norod': 'Never used a dowsing rod',
             'teetotal': 'Never ate food, drank alcohol or used medicine',
             'nofood': 'Never ate a mushroom',
             'nopill': 'Never used medicine',
             'nopep': 'Never used No-Doz pills',
             'nobooze': 'Never drank alcohol',
             'nuked': 'Killed a monster with radiation',
             'nodig': 'Never used a pickaxe',
             'artifact': 'Crafted a powerful artifact',
             'ebola': 'Killed a monster via Ebolavirus',
             'thunderdome': 'Visited the Rehabilitation Thunderdome',
             'thunderdome_win': 'Became a Thunderdome champion',
             'kalitemple': 'Visited the temple of Kali',
             'molds': 'Cleaned up black mold',
             'colorwow': 'Used colored liquid for great success',
             '6color': 'Drank colored liquid 6 times or more',
             'full_m_prism': 'Used a prism of the Full Moon',
             'new_m_prism': 'Used a prism of the New Moon'
             }

    prefix = {'plev': 'Reached player level %s',
              'dlev': 'Reached dungeon level %s',
              'dead_': 'Killed by %s',
              'moon_': 'Played on a %s moon'
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
              'pep': 'Used No-Doz pills at least %s times',
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

def main():

    w = 80
    h = 25

    diggr._inputs = []

    font = 'font.png' #'terminal10x16_gs_ro.png'
    libtcod.console_set_custom_font(font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(w, h, 'Diggr game replayer tool', False, libtcod.RENDERER_SDL)
    libtcod.sys_set_fps(30)

    libtcod.console_set_color_control(libtcod.COLCTRL_1, libtcod.white, libtcod.black)
    libtcod.console_set_color_control(libtcod.COLCTRL_2, libtcod.darker_green, libtcod.black)
    libtcod.console_set_color_control(libtcod.COLCTRL_3, libtcod.yellow, libtcod.black)
    libtcod.console_set_color_control(libtcod.COLCTRL_4, libtcod.red, libtcod.black)
    libtcod.console_set_color_control(libtcod.COLCTRL_5, libtcod.gray, libtcod.black)

    _c1 = libtcod.COLCTRL_1
    _c2 = libtcod.COLCTRL_2
    _c3 = libtcod.COLCTRL_3
    _c4 = libtcod.COLCTRL_4
    _c5 = libtcod.COLCTRL_5


    def input_name():
        name = ''
        while 1:
            k3 = diggr.draw_window(['Enter filename: ' + name], w, h)
            if k3 in '\n\r':
                break
            elif k3 in string.ascii_letters or k3 in string.digits or k3 in '.':
                name += k3
            elif ord(k3) == 8 or ord(k3) == 127:
                if len(name) > 0:
                    name = name[:-1]

        return name


    n = 0
    limit = 9

    conn = sqlite3.connect('highscore.db')
    c = conn.cursor()

    mode = 1
    achievement = None

    tbl_games = 'Games%s' % diggr._version.replace('.', '')
    tbl_achievements = 'Achievements%s' % diggr._version.replace('.', '')



    while 1:
        if libtcod.console_is_window_closed():
            break

        if mode == 1:
            if achievement:
                c.execute('select id, seed, score from %s join %s on (game_id = id) '
                          ' where achievement = ? order by seed desc'
                          ' limit %d offset %d' % (tbl_games, tbl_achievements, limit, n),
                          (achievement,))
            else:
                c.execute('select id, seed, score from %s order by seed desc '
                          'limit %d offset %d' % (tbl_games, limit, n))

        elif mode == 2:
            if achievement:
                c.execute('select id, seed, score from %s join %s on (game_id = id) '
                          ' where achievement = ? order by score desc'
                          ' limit %d offset %d' % (tbl_games, tbl_achievements, limit, n),
                          (achievement,))
            else:
                c.execute('select id, seed, score from %s order by score desc '
                          'limit %d offset %d' % (tbl_games, limit, n))


        qq = 0
        choice = {}
        s = []

        for gameid,seed,score in c.fetchall():
            chh = chr(97+qq)
            s.append('')
            s.append('%c%c)%c  Game #%c%d%c at %s, score %c%d%c' % \
                     (_c1, chh, _c2, _c1, gameid, _c5,
                      time.ctime(seed), _c1, score, _c5))
            qq += 1
            choice[chh] = (gameid, score)

        s.append('')
        s.append(":  Left and right keys to scroll entries")
        s.append(":  Type its letter to select an entry")
        s.append(":  %c'?'%c for help; Other keys: %cs%c, %cw%c, %cz%c, %cq%c" % \
                 (_c1, _c5, _c1, _c5, _c1, _c5, _c1, _c5, _c1, _c5))
        s.append('')
        s.append('*WARNING*: Only games from the _same_ version of Diggr will replay correctly!')

        k = diggr.draw_window(s, w, h, True)

        if k == 'h':
            n -= limit
            if n < 0:
                n = 0

        elif k == 'l':
            if len(choice) > 0:
                n += limit

        elif k == '?':
            s = ['',
                 'Left and right keys to scroll entries.',
                 'Type its letter to select an entry.',
                 ''
                 ' s : Switch sorting mode between "date" and "score".',
                 ' w : Filter scores by achievement.',
                 ' z : Load scores from another file on disk.',
                 ' q : Quit.'
                 '']
            diggr.draw_window(s, w, h)


        elif k == 's':
            if mode == 1:
                mode = 2
            else:
                mode = 1
            n = 0

        elif k == 'w':

            n2 = 0
            limit2 = 9

            while 1:
                c.execute('select achievement, count(*) from %s join %s '
                          'on (game_id = id) group by 1 order by 2 desc '
                          ' limit %d offset %d' % (tbl_games, tbl_achievements, limit2, n2))

                s = []
                qq = 0
                choices2 = {}
                for aach,cnt in c.fetchall():
                    aach = aach.encode('ascii')
                    chh = chr(97+qq)
                    achtext = ach_tag_to_text(aach)
                    s.append('')
                    s.append('%c%c%c) %c%s%c: %s%d games' % \
                             (_c1, chh, _c5, _c1, achtext, _c5, ' '*(max(0, 50-len(achtext))), cnt))
                    qq += 1
                    choices2[chh] = aach

                k2 = diggr.draw_window(s, w, h, True)

                if k2 == 'h':
                    n2 -= limit
                    if n2 < 0:
                        n2 = 0

                elif k2 == 'l':
                    if len(choices2) > 0:
                        n2 += limit

                elif k2 in choices2:
                    achievement = choices2[k2]
                    n = 0
                    break

                else:
                    achievement = None
                    n = 0
                    break

        elif k in choice:
            gameid, score = choice[k]

            s2 = ['',
                  'Do what?',
                  '  a) replay this game',
                  '  b) save this game to a file on disk',
                  '']

            c.execute('select sum(score >= %d),count(*) from %s' % (score, tbl_games))

            place,total = c.fetchone()

            s2.extend(['Game score: %d    (#%c%d%c/%d)' % (score, _c1, place, _c5, total),
                      '',
                      'Achievements of this game:',
                      ''])

            c.execute('select achievement from %s where game_id = %d' % (tbl_achievements, gameid))

            for aach in c.fetchall():
                aach = aach[0].encode('ascii')
                c.execute('select sum(score >= %d),count(*) from %s join %s on (game_id = id) where achievement = ?' % \
                          (score, tbl_games, tbl_achievements), (aach,))
                place,total = c.fetchone()
                aach = ach_tag_to_text(aach)
                s2.append('    %c%s%c: %s%c%d%c/%d' % (_c1, aach, _c5, '.'*max(0,50-len(aach)), _c1, place, _c5, total))

            k2 = diggr.draw_window(s2, w, h, True)

            if k2 == 'a':
                c.execute('select seed, inputs, bones from %s where id = %d' % \
                          (tbl_games, gameid))

                seed,inputs,bones = c.fetchone()
                inputs = cPickle.loads(str(inputs))
                bones = cPickle.loads(str(bones))

                diggr.main(diggr.Config(False),
                           replay=(seed,inputs,bones))

                if len(diggr._inputqueue) != 0:
                    raise Exception('Malformed replay file.')
                diggr._inputqueue = None

            elif k2 == 'b':
                name = input_name()

                if len(name) > 0:

                    name = os.path.join('replays', name)
                    conn2 = sqlite3.connect(name)
                    c2 = conn2.cursor()

                    c2.execute('create table if not exists ' + tbl_games + \
                               ' (id INTEGER PRIMARY KEY, seed int, score int, bones blob, inputs blob)')
                    c2.execute('create table if not exists ' + tbl_achievements + \
                               ' (achievement text, game_id int)')

                    c.execute('select seed, score, bones, inputs from %s where id = %d' % \
                              (tbl_games, gameid))

                    for seed,score,bones,inputs in c.fetchall():
                        c2.execute('insert into ' + tbl_games + '(id, seed, score, bones, inputs) values (NULL, ?, ?, ?, ?)',
                                   (seed, score, bones, inputs))
                        gameid2 = c2.lastrowid
                        c.execute('select achievement from %s where game_id = %d' % (tbl_achievements, gameid))
                        for ach in c.fetchall():
                            ach = ach[0]
                            c2.execute('insert into ' + tbl_achievements + '(achievement, game_id) values (?, ?)',
                                       (ach, gameid2))

                    conn2.commit()
                    c2.close()
                    conn2.close()
                    diggr.draw_window(['Saved to "%s".' % name,
                                       'Press any key to continue.'], w, h)



        elif k == 'z':
            name = input_name()

            if len(name) > 0:
                name = os.path.join('replays', name)

                ok = True
                try:
                    os.stat(name)
                except:
                    diggr.draw_window(['File not found: "%s".' % name,
                                       'Press any key to continue.'], w, h)
                    ok = False

                if ok:
                    c.close()
                    conn.close()
                    conn = sqlite3.connect(name)
                    c = conn.cursor()
                    n = 0
            else:
                c.close()
                conn.close()
                conn = sqlite3.connect('highscore.db')
                c = conn.cursor()
                n = 0


        elif k == 'q':
            break



if __name__ == '__main__':
    main()
