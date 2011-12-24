
from ctypes import *
import os

if os.name == 'nt':
    _dg = CDLL('./libdiggr.dll')
else:
    _dg = CDLL('./libdiggr.so')


def neighbors_init(w, h):
    _dg.dg_neighbors_init(c_uint(w), c_uint(h))

def celauto_init():
    print '*** ca_init'
    _dg.dg_celauto_init();

def celauto_make_rule(i, s, b, a):
    print '*** ca_make_rule',i,s,b,a
    _dg.dg_celauto_make_rule(c_ulong(i), c_char_p(s), c_char_p(b), c_uint(a))

def celauto_seed(x, y, ri):
    _dg.dg_celauto_seed(c_uint(x), c_uint(y), c_ulong(ri))

CELAUTOFUNC = CFUNCTYPE(None, c_uint, c_uint, c_ulong)

def celauto_clear(x, y, cb):
    _dg.dg_celauto_clear(c_uint(x), c_uint(y), CELAUTOFUNC(cb))

def celauto_step(cbon, cboff):
    _dg.dg_celauto_step(CELAUTOFUNC(cbon), CELAUTOFUNC(cboff))

def celauto_get_state(x, y):
    id = c_ulong()
    age = c_uint()
    _dg.dg_celauto_get_state(c_uint(x), c_uint(y), byref(id), byref(age))
    return id.value, age.value

def state_save(fn):
    print '// saving state', fn
    _dg.dg_state_save(c_char_p(fn))

def state_load(fn):
    print '// loading state', fn
    _dg.dg_state_load(c_char_p(fn))



