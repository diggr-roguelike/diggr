
from ctypes import *
import os

sound = CDLL('./libsound.so')

dir = os.path.join(os.getcwd(), 'sound')

sound.sound_init('scsynth',
                 os.path.join(dir, ''),
                 os.path.join(dir, 'synths'), os.path.join(dir, 'plugins'))

sound.sound_play("wobble", "dur", c_double(1.5))

sound.sound_stop()

