
import cPickle
import time
import string

import libtcodpy as libtcod

import diggr

Item = diggr.Item

def main():

    w = 80
    h = 25

    diggr._inputs = []

    font = 'terminal10x16_gs_ro.png'
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



    hss = []
    try:
        hsf = open('highscore', 'r')
        hss = cPickle.load(hsf)
    except:
        passs

    if len(hss) < 3:
        n = 0
    else:
        n = len(hss)-3

    while 1:
        if libtcod.console_is_window_closed():
            break

        s = []
        end = False
        if len(hss)-n < 3:
            n2 = len(hss)
            end = True
        else:
            n2 = n + 3

        ni = n
        print n, n+3, len(hss)
        for v in hss[n:n+3]:
            s.append('')
            s.append('%c%c)%c  %s%c: #%c%d%c/%d:' % \
                    (_c1, chr(97+ni-n), _c2, time.ctime(v['seed']), _c5,
                     _c1, ni+1, _c5, len(hss)))

            score = (v['plev'] * 5) + (v['dlev'] * 5) + len(v['kills'])
            s.append('%c    Player level %c%d%c, with a total score of %c%d%c.' % \
                     (_c5, _c1, v['plev'], _c5, _c3, score, _c5))
            pad = ''
            reason = v['reason']
            if len(reason) < 30:
                pad = pad + (' ' * (20 - len(reason)))
            s.append('    Died on dungeon level %c%d%c, killed by %c%s%c.%s' % \
                     (_c1, v['dlev'], _c5, _c1, reason, _c5, pad))
            ni += 1

        s.append('')
        s.append('')
        s.append(":  Left and right keys to scroll")
        s.append(":  Type a letter to select entry")
        s.append(":  'q' to quit")
        s.append(":  'z' to replay a game from a file on disk.")
        s.append('')
        s.append('*WARNING*: Only games from the _same_ version of Diggr will replay correctly!')

        k = diggr.draw_window(s, w, h, True)

        if k == 'h':
            n -= 3
            if n < 0:
                n = len(hss)+n
        elif k == 'l':
            n += 3
            if n >= len(hss):
                n -= len(hss)

        elif k == 'z':
            name = input_name()
            diggr.main(replay=0, highscorefilename=name)

        elif k in 'abc':
            thisn = n + (ord(k)-97)

            s2 = ['',
                  'Do what?',
                  '  a) replay this game',
                  '  b) save this game to a file on disk']

            k2 = diggr.draw_window(s2, w, h, True)

            if k2 == 'a':
                diggr.main(replay=thisn)
            elif k2 == 'b':
                name = input_name()
                if len(name) > 0:
                    namef = open(name, 'w')
                    minihs = [hss[thisn]]
                    cPickle.dump(minihs, namef)
                    namef.close()

        elif k == 'q':
            break



if __name__ == '__main__':
    main()
