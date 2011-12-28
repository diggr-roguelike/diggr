
from ctypes import *
import os

import libtcodpy


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
    _dg.dg_state_save(c_char_p(fn))

def state_load(fn):
    _dg.dg_state_load(c_char_p(fn))


def render_init(w, h):
    _dg.dg_render_init(c_uint(w), c_uint(h))

def render_set_env(color, intensity):
    _dg.dg_render_set_env(c_ubyte(color.r), c_ubyte(color.g), c_ubyte(color.b), c_double(intensity))

def render_set_back(x, y, back):
    _dg.dg_render_set_back(c_uint(x), c_uint(y), c_ubyte(back.r), c_ubyte(back.g), c_ubyte(back.b))

def render_set_is_lit(x, y, is_lit):
    _dg.dg_render_set_is_lit(c_uint(x), c_uint(y), c_bool(is_lit))


def render_push_skin(x, y, fore, c, fore2, fore_i, is_terrain):
    if type(c) == type(1):
        c = chr(c)
    _dg.dg_render_push_skin(c_uint(x), c_uint(y), c_ubyte(fore.r), c_ubyte(fore.g), c_ubyte(fore.b), 
                            c_char(c), 
                            c_ubyte(fore2.r), c_ubyte(fore2.g), c_ubyte(fore2.b), 
                            c_int(fore_i), 
                            c_bool(is_terrain))

def render_set_skin(x, y, fore, c, fore2, fore_i, is_terrain):
    if type(c) == type(1):
        c = chr(c)
    _dg.dg_render_set_skin(c_uint(x), c_uint(y), c_ubyte(fore.r), c_ubyte(fore.g), c_ubyte(fore.b), 
                           c_char(c), 
                           c_ubyte(fore2.r), c_ubyte(fore2.g), c_ubyte(fore2.b), 
                           c_int(fore_i), 
                           c_bool(is_terrain))

def render_pop_skin(x, y):
    _dg.dg_render_pop_skin(c_uint(x), c_uint(y))


_dg.dg_render_is_in_fov.restype = c_bool

def render_is_in_fov(x, y):
    return _dg.dg_render_is_in_fov(c_uint(x), c_uint(y))

_dg.dg_render_draw.restype = c_bool

def render_draw(map, t, px, py, hlx, hly, rmin, rmax, lr):
    return _dg.dg_render_draw(c_void_p(map), c_uint(t), c_uint(px), c_uint(py),
                              c_uint(hlx), c_uint(hly), c_uint(rmin), c_uint(rmax),
                              c_uint(lr))


