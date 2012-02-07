
import libtcodpy as libtcod

import sounds

_version = '12.02.05'
_inputs = []
_inputqueue = None
_inputdelay = 100


class fakekey:
    def __init__(self, c, vk):
        self.c = c
        self.vk = vk

class Config:
    def __init__(self, sound_enabled=True):
        self.fullscreen = False
        self.sound_enabled = sound_enabled
        self.music_enabled = True

        self.cfgfile = {}
        self.load()

        self.sound = sounds.Engine(self.sound_enabled)
        self.music_n = None

    
    def load(self):
        try:
            self.cfgfile = eval(open('diggr.cfg').read())
        except:
            pass

        if 'fullscreen' in self.cfgfile:
            self.fullscreen = bool(self.cfgfile['fullscreen'])

        if 'sound' in self.cfgfile:
            self.sound_enabled = bool(self.cfgfile['sound'])

        if 'music' in self.cfgfile:
            self.music_enabled = bool(self.cfgfile['music'])



def console_wait_for_keypress():

    if _inputqueue is not None:

        if len(_inputqueue) == 0:
            raise Exception('Malformed replay file.')

        c, vk = _inputqueue.pop(0)

        if _inputdelay < 1000:
            tmp = libtcod.console_check_for_keypress()
        else:
            tmp = libtcod.console_wait_for_keypress(False)

        if tmp.vk == libtcod.KEY_RIGHT and _inputdelay > 20:
            _inputdelay -= (20 if _inputdelay <= 200 else 200)
        elif tmp.vk == libtcod.KEY_LEFT and _inputdelay < 1000:
            _inputdelay += (20 if _inputdelay < 200 else 200)
        elif tmp.c == 32: # space
            globals()['_inputdelay'] = 1000

        if _inputdelay < 1000:
            libtcod.sys_sleep_milli(_inputdelay)

        return fakekey(c, vk)

    k = libtcod.console_wait_for_keypress(False)
    _inputs.append((k.c, k.vk))

    return k
