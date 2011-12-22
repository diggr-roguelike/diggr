
from ctypes import *

if os.name == 'nt':
    _dg = CDLL('./libdiggr.dll')
else:
    _dg = CDLL('./libdiggr.so')


def neighbors_init(w, h):
    _dg.dg_neighbors_init(c_uint(w), c_uint(h))

def celauto_init():
    _dg.dg_celauto_init();

def celauto_make_rule(i, s, b, a):
    _dg.dg_celauto_make_rule(c_ulong(i), c_char_p(s), c_char_p(b), c_uint(a))

def celauto_seed(x, y, ri):
    _dg.dg_celauto_seed(c_uint(x), c_uint(y), c_ulong(ri))

CELAUTOFUNC = CFUNCTYPE(c_uint, c_uint, c_ulong)

def celauto_clear(x, y, cb):
    _dg.dg_celauto_clear(c_uint(x), c_uint(y), CELAUTOFUNC(cb))

def celauto_step(cbon, cboff):
    _dg.dg_celauto_step(CELAUTOFUNC(cbon), CELAUTOFUNC(cboff))

