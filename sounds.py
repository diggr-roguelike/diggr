#!/usr/bin/env python

from ctypes import *
import os
import time
import sys

if os.name == 'nt':
    _sound = CDLL('./libsound.dll')
else:
    _sound = CDLL('./libsound.so')

_sound.sound_play.restype = c_int
_sound.sound_toggle_mute.restype = c_int



class Engine:
    def __init__(self, enabled=True):

        if not enabled:
            return
 
        exe = 'scsynth'
        cwd = os.getcwd()
        wd = os.path.join(cwd, 'sound')
        exedir = os.path.join(wd, '')
        synthdir = os.path.join(wd, 'synths')
        plugindir = os.path.join(wd, 'plugins')

        if os.name == 'nt':
            exe += '.exe'

        _sound.sound_init(exe, exedir, synthdir, plugindir)


    def __del__(self):
        _sound.sound_stop()

    def play(self, name, **args):
        k,v = args.items()[0]
        return _sound.sound_play(name, k, c_float(v))

    def set(self, n, **args):
        k,v = args.items()[0]
        _sound.sound_set(n, k, c_float(v))

    def stop(self, n):
        _sound.sound_free(n)

    def toggle_mute(self):
        return _sound.sound_toggle_mute()

def main():
    e = Engine()
    time.sleep(1)
    e.play("plang")
    time.sleep(0.1)
    e.play("wobble")
    for x in xrange(4):
        e.play("plang", out=x%2)
        time.sleep(1)


if __name__ == '__main__':
    main()
