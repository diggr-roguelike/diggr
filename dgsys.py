
import libdiggrpy as dg

import sounds

_version = '12.02.05'
_inputqueue = None
_inputdelay = 500


class Config:
    def __init__(self, cfg=None):
        self.fullscreen = False
        self.sound_enabled = True
        self.music_enabled = True
        self.fontfile = "font.png"

        if cfg is None:
            self.cfgfile = {}
            self.load()
        else:
            self.cfgfile = cfg

        self._apply()

        self.sound = sounds.Engine(self.sound_enabled)
        self.music_n = None

    
    def load(self):
        try:
            self.cfgfile = eval(open('diggr.cfg').read())
        except:
            pass

    def _apply(self):
        if 'fullscreen' in self.cfgfile:
            self.fullscreen = bool(self.cfgfile['fullscreen'])

        if 'sound' in self.cfgfile:
            self.sound_enabled = bool(self.cfgfile['sound'])

        if 'music' in self.cfgfile:
            self.music_enabled = bool(self.cfgfile['music'])

        if 'fontfile' in self.cfgfile:
            self.fontfile = str(self.cfgfile['fontfile'])


class keypress:
    def __init__(self, vk, c):
        self.c = c
        self.vk = vk


def console_wait_for_keypress():

    if _inputqueue is not None:

        if len(_inputqueue) == 0:
            raise Exception('Malformed replay file.')

        vk, c = _inputqueue.pop(0)
        dg.render_skip_input(_inputdelay)
        return keypress(vk, c)


    vk, c = dg.render_wait_for_key()
    return keypress(vk, c)
