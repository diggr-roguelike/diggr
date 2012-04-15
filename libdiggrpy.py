
from ctypes import *
import os


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


def render_init(w, h, fontfile, title, fullscreen):
    _dg.dg_render_init(c_uint(w), c_uint(h), c_char_p(fontfile), c_char_p(title), c_bool(fullscreen))

def render_clear():
    _dg.dg_render_clear()

def render_wait_for_anykey():
    _dg.dg_render_wait_for_anykey()

def render_skip_input(delay=0):
    _dg.dg_render_skip_input(c_uint(delay))

def render_wait_for_key():
    vk = c_int()
    c = c_char()
    _dg.dg_render_wait_for_key(byref(vk), byref(c))
    return (vk.value, c.value)

def render_draw_window(msg):
    n = len(msg)
    strp_t = c_char_p * n
    strp = strp_t()

    for i in xrange(n):
        strp[i] = msg[i]

    vk = c_int()
    c = c_char()
    _dg.dg_render_draw_window(strp, n, byref(vk), byref(c))
    return (vk.value, c.value)

_dg.dg_render_get_keylog_size.restype = c_ulong

def render_get_keylog_size():
    return _dg.dg_render_get_keylog_size()

_dg.dg_render_get_keylog_entry.restype = c_bool

def render_get_keylog_entry(i):
    vk = c_int()
    c = c_char()
    ret = _dg.dg_render_get_keylog_entry(c_ulong(i), byref(vk), byref(c))

    if not ret:
        return None
    return (vk.value, c.value)

def render_clear_keylog():
    _dg.dg_render_clear_keylog()

def render_push_replay_keypress(kp):
    _dg.dg_render_push_replay_keypress(c_int(kp[0]), c_char(kp[1]))

def render_stop_keypress_replay():
    return _dg.dg_render_stop_keypress_replay()

def render_set_env(color, intensity):
    _dg.dg_render_set_env(c_ubyte(color.r), c_ubyte(color.g), c_ubyte(color.b), c_double(intensity))

def render_set_back(x, y, z, back):
    _dg.dg_render_set_back(c_uint(x), c_uint(y), c_uint(z), c_ubyte(back.r), c_ubyte(back.g), c_ubyte(back.b))

def render_set_is_lit(x, y, z, is_lit):
    _dg.dg_render_set_is_lit(c_uint(x), c_uint(y), c_uint(z), c_bool(is_lit))

def render_set_is_viewblock(x, y, z, t):
    _dg.dg_render_set_is_viewblock(c_uint(x), c_uint(y), c_uint(z), c_bool(t))

def render_set_is_walkblock(x, y, z, t):
    _dg.dg_render_set_is_walkblock(c_uint(x), c_uint(y), c_uint(z), c_bool(t))

def render_set_skin(x, y, z, fore, c, fore2, fore_i, is_terrain):
    if type(c) == type(1):
        c = chr(c)
    _dg.dg_render_set_skin(c_uint(x), c_uint(y), c_uint(z),
                           c_ubyte(fore.r), c_ubyte(fore.g), c_ubyte(fore.b), 
                           c_char(c), 
                           c_ubyte(fore2.r), c_ubyte(fore2.g), c_ubyte(fore2.b), 
                           c_int(fore_i), 
                           c_bool(is_terrain))

def render_unset_skin(x, y, z):
    _dg.dg_render_unset_skin(c_uint(x), c_uint(y), c_uint(z))


_dg.dg_render_is_in_fov.restype = c_bool

def render_is_in_fov(x, y):
    return _dg.dg_render_is_in_fov(c_uint(x), c_uint(y))

_dg.dg_render_draw.restype = c_bool

def render_draw(t, px, py, hlx, hly, rmin, rmax, lr, do_hud):
    _dg.dg_render_draw(c_uint(t), c_uint(px), c_uint(py),
                       c_uint(hlx), c_uint(hly), c_uint(rmin), c_uint(rmax),
                       c_uint(lr), c_bool(do_hud))

def render_push_hud_line(label, labelcolor, signed, npips, style):
    _dg.dg_render_push_hud_line(c_char_p(label), 
                                c_ubyte(labelcolor.r), c_ubyte(labelcolor.g), c_ubyte(labelcolor.b), 
                                c_bool(signed), c_int(npips),
                                c_char(style[0][0]), 
                                c_ubyte(style[0][1].r), c_ubyte(style[0][1].g), c_ubyte(style[0][1].b), 
                                c_char(style[1][0]), 
                                c_ubyte(style[1][1].r), c_ubyte(style[1][1].g), c_ubyte(style[1][1].b))

DRAWDOFUNC = CFUNCTYPE(None, c_uint, c_uint)
DRAWCHECKFUNC = CFUNCTYPE(c_bool, c_uint, c_uint)

def render_draw_circle(x, y, r, col, func):
    if not col:
        _dg.dg_render_draw_circle(c_uint(x), c_uint(y), c_uint(r), c_bool(False),
                                  c_ubyte(0), c_ubyte(0), c_ubyte(0),
                                  c_ubyte(0), c_ubyte(0), c_ubyte(0),
                                  DRAWDOFUNC(func))
    else:
        _dg.dg_render_draw_circle(c_uint(x), c_uint(y), c_uint(r), c_bool(True),
                                  c_ubyte(col[0].r), c_ubyte(col[0].g), c_ubyte(col[0].b),
                                  c_ubyte(col[1].r), c_ubyte(col[1].g), c_ubyte(col[1].b),
                                  DRAWDOFUNC(func))

def render_draw_fov_circle(x, y, r, col, func):
    if not col:
        _dg.dg_render_draw_fov_circle(c_uint(x), c_uint(y), c_uint(r), c_bool(False),
                                      c_ubyte(0), c_ubyte(0), c_ubyte(0),
                                      c_ubyte(0), c_ubyte(0), c_ubyte(0),
                                      DRAWDOFUNC(func))
    else:
        _dg.dg_render_draw_fov_circle(c_uint(x), c_uint(y), c_uint(r), c_bool(True),
                                      c_ubyte(col[0].r), c_ubyte(col[0].g), c_ubyte(col[0].b),
                                      c_ubyte(col[1].r), c_ubyte(col[1].g), c_ubyte(col[1].b),
                                      DRAWDOFUNC(func))

def render_draw_floodfill(x, y, col, func):
    if not col:
        _dg.dg_render_draw_floodfill(c_uint(x), c_uint(y), c_bool(False),
                                     c_ubyte(0), c_ubyte(0), c_ubyte(0),
                                     c_ubyte(0), c_ubyte(0), c_ubyte(0),
                                     DRAWCHECKFUNC(func))
    else:
        _dg.dg_render_draw_floodfill(c_uint(x), c_uint(y), c_bool(True),
                                     c_ubyte(col[0].r), c_ubyte(col[0].g), c_ubyte(col[0].b),
                                     c_ubyte(col[1].r), c_ubyte(col[1].g), c_ubyte(col[1].b),
                                     DRAWCHECKFUNC(func))

def render_draw_line(x0, y0, x1, y1, col, func):
    if not col:
        _dg.dg_render_draw_line(c_uint(x0), c_uint(y0), c_uint(x1), c_uint(y1), c_bool(False),
                                c_ubyte(0), c_ubyte(0), c_ubyte(0),
                                c_ubyte(0), c_ubyte(0), c_ubyte(0),
                                DRAWCHECKFUNC(func))
    else:
        _dg.dg_render_draw_line(c_uint(x0), c_uint(y0), c_uint(x1), c_uint(y1), c_bool(True),
                                c_ubyte(col[0].r), c_ubyte(col[0].g), c_ubyte(col[0].b),
                                c_ubyte(col[1].r), c_ubyte(col[1].g), c_ubyte(col[1].b),
                                DRAWCHECKFUNC(func))

def render_message(msg, important):
    _dg.dg_render_message(c_char_p(msg), c_bool(important))

def render_draw_messages_window():
    _dg.dg_render_draw_messages_window()

_dg.dg_render_path_walk.restype = c_bool

def render_path_walk(x0, y0, x1, y1, n, cutoff):
    xo = c_uint()
    yo = c_uint()
    r = _dg.dg_render_path_walk(c_uint(x0), c_uint(y0), c_uint(x1), c_uint(y1),
                                c_uint(n), c_uint(cutoff), byref(xo), byref(yo))
    if not r:
        return (None, None)
    return (xo.value, yo.value)

def random_init(seed):
    _dg.dg_random_init(c_long(seed))

_dg.dg_random_range.restype = c_int

def random_range(a, b):
    return _dg.dg_random_range(c_int(a), c_int(b))

_dg.dg_random_n.restype = c_uint

def random_n(n):
    return _dg.dg_random_n(c_uint(n))

_dg.dg_random_gauss.restype = c_double

def random_gauss(m, s):
    return _dg.dg_random_gauss(c_double(m), c_double(s))

_dg.dg_random_uniform.restype = c_double

def random_uniform(a, b):
    return _dg.dg_random_uniform(c_double(a), c_double(b))

_dg.dg_random_geometric.restype = c_uint

def random_geometric(p):
    return _dg.dg_random_geometric(c_double(p))

_dg.dg_random_biased_gauss.restype = c_double

def random_biased_gauss(m, s, b, f):
    return _dg.dg_random_biased_gauss(c_double(m), c_double(s), c_double(b), c_double(f))

def grid_init(w, h):
    _dg.dg_grid_init(c_uint(w), c_uint(h))

def grid_generate(type):
    _dg.dg_grid_generate(c_int(type))

def grid_set_height(x, y, h):
    _dg.dg_grid_set_height(c_uint(x), c_uint(y), c_double(h))

_dg.dg_grid_get_height.restype = c_double

def grid_get_height(x, y):
    return _dg.dg_grid_get_height(c_uint(x), c_uint(y))

_dg.dg_grid_is_walk.restype = c_bool
_dg.dg_grid_is_water.restype = c_bool

def grid_is_walk(x, y):
    return _dg.dg_grid_is_walk(c_uint(x), c_uint(y))

def grid_is_water(x, y):
    return _dg.dg_grid_is_water(c_uint(x), c_uint(y))

def grid_set_walk(x, y, v):
    _dg.dg_grid_set_walk(c_uint(x), c_uint(y), c_bool(v))

def grid_set_water(x, y, v):
    _dg.dg_grid_set_water(c_uint(x), c_uint(y), c_bool(v))

def grid_add_nogen(x, y):
    _dg.dg_grid_add_nogen(c_uint(x), c_uint(y))

def grid_one_of_floor():
    x = c_uint()
    y = c_uint()
    ret = _dg.dg_grid_one_of_floor(byref(x), byref(y))
    if not ret:
        return (None, None)
    return x.value, y.value

def grid_one_of_water():
    x = c_uint()
    y = c_uint()
    ret = _dg.dg_grid_one_of_water(byref(x), byref(y))
    if not ret:
        return (None, None)
    return x.value, y.value

def grid_one_of_walk():
    x = c_uint()
    y = c_uint()
    ret = _dg.dg_grid_one_of_walk(byref(x), byref(y))
    if not ret:
        return (None, None)
    return x.value, y.value
