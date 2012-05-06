
#include "serialize.h"
#include "neighbors.h"
#include "celauto.h"
#include "render.h"
#include "random.h"
#include "grid.h"


#ifdef __MINGW32__
#define EXPORT extern "C" __declspec(dllexport)
#else
#define EXPORT extern "C"
#endif


EXPORT void dg_neighbors_init(unsigned int w, unsigned int h) {
    neighbors::get().init(w, h);
}

EXPORT void dg_celauto_init() {
    celauto::get().init();
}

EXPORT void dg_celauto_make_rule(size_t i, const char* s, const char* b, unsigned int a) {
    celauto::get().make_rule(i, s, b, a);
}

EXPORT void dg_celauto_seed(unsigned int x, unsigned int y, size_t ri) {
    celauto::CaMap& ca = celauto::get();
    std::shared_ptr<celauto::rule> r = ca.get_rule(ri);

    if (r) {
        ca.seed(celauto::pt(x,y), r);
    }
}

typedef void (*dg_celauto_callback)(unsigned int, unsigned int, size_t);

EXPORT void dg_celauto_clear(unsigned int x, unsigned int y, dg_celauto_callback cb) {
    celauto::get().clear(celauto::pt(x,y), cb);
}

EXPORT void dg_celauto_step(dg_celauto_callback cbon, dg_celauto_callback cboff) {
    celauto::get().step(cbon, cboff);
}

EXPORT void dg_celauto_get_state(unsigned int x, unsigned int y, size_t* id, unsigned int* age) {
    celauto::get().get_state(celauto::pt(x,y), *id, *age);
}


EXPORT void dg_state_save(const char* filename) {
    serialize::Sink s(filename);
    celauto::get().write(s);
    grender::get().write(s);
    grid::get().write(s);
}

EXPORT void dg_state_load(const char* filename) {
    serialize::Source s(filename);
    celauto::get().read(s);
    grender::get().read(s);
    grid::get().read(s);
}


EXPORT void dg_render_init(unsigned int w, unsigned int h, 
                           const char* fontfile, const char* title, bool fullscreen) {
    grender::get().init(w, h, w, h, fontfile, title, fullscreen);
}

EXPORT void dg_render_clear() {
    grender::get().clear();
}

EXPORT void dg_render_wait_for_anykey() {
    return grender::get().wait_for_anykey();
}

EXPORT void dg_render_skip_input(unsigned int delay) {
    return grender::get().skip_input(delay);
}

EXPORT void dg_render_wait_for_key(int* vk, char* c) {
    grender::Grid::keypress k = grender::get().wait_for_key();
    *vk = k.vk;
    *c = k.c;
}

EXPORT void dg_render_draw_window(const char** _msg, size_t n, int* vk, char* c) {
    std::vector<std::string> msg;
    for (size_t i = 0; i < n; ++i) {
        msg.push_back(_msg[i]);
    }
    grender::Grid::keypress k = grender::get().draw_window(msg);
    *vk = k.vk;
    *c = k.c;
}

EXPORT unsigned long dg_render_get_keylog_size() {
    return grender::get().keylog.size();
}

EXPORT bool dg_render_get_keylog_entry(unsigned long i, int* vk, char* c) {

    if (i >= grender::get().keylog.size())
        return false;

    const grender::Grid::keypress& k = grender::get().keylog[i];
    *vk = k.vk;
    *c = k.c;
    return true;
}

EXPORT void dg_render_clear_keylog() {
    grender::get().keylog.clear();
}

EXPORT void dg_render_push_replay_keypress(int vk, char c) {
    grender::get().push_replay_keypress(grender::Grid::keypress(vk, c));
}

EXPORT void dg_render_stop_keypress_replay() {
    grender::get().stop_keypress_replay();
}

// python ctypes and/or libffi is severly broken. This is why struct are passed by each individual field.


EXPORT void dg_render_set_env(uint8 r, uint8 g, uint8 b, double intensity) {
    TCOD_color_t color;
    color.r = r;
    color.g = g;
    color.b = b;
    grender::get().set_env(color, intensity);
}

EXPORT void dg_render_set_back(unsigned int x, unsigned int y, unsigned int z, uint8 r, uint8 g, uint8 b) {
    TCOD_color_t back;
    back.r = r;
    back.g = g;
    back.b = b;
    grender::get().set_back(x, y, z, back);
}

EXPORT void dg_render_set_is_lit(unsigned int x, unsigned int y, unsigned int z, bool is_lit) {
    grender::get().set_is_lit(x, y, z, is_lit);
}

EXPORT void dg_render_set_skin(unsigned int x, unsigned int y, unsigned int z,
                               uint8 fr, uint8 fg, uint8 fb, 
                               unsigned char c,
                               uint8 f2r, uint8 f2g, uint8 f2b, 
                               int fore_interp, bool is_terrain) {
    TCOD_color_t fore;
    TCOD_color_t fore2;
    fore.r = fr;
    fore.g = fg;
    fore.b = fb;
    fore2.r = f2r;
    fore2.g = f2g;
    fore2.b = f2b;
    grender::get().set_skin(x, y, z, fore, c, fore2, fore_interp, is_terrain);
}

EXPORT void dg_render_unset_skin(unsigned int x, unsigned int y, unsigned int z) {
    grender::get().unset_skin(x, y, z);
}

EXPORT bool dg_render_is_in_fov(unsigned int x, unsigned int y) {
    return grender::get().is_in_fov(x, y);
}

EXPORT void dg_render_set_is_viewblock(unsigned int x, unsigned int y, unsigned int z, bool t) {
    grender::get().set_is_viewblock(x, y, z, t);
}

EXPORT void dg_render_set_is_walkblock(unsigned int x, unsigned int y, unsigned int z, bool t) {
    grender::get().set_is_walkblock(x, y, z, t);
}

EXPORT void dg_render_draw(unsigned int t,
                           unsigned int px, unsigned int py, 
                           unsigned int hlx, unsigned int hly,
                           unsigned int rmin, unsigned int rmax,
                           unsigned int lr, bool do_hud) {
    grender::get().draw(t, 0, 0, px, py, hlx, hly, rmin, rmax, lr, do_hud);
}

EXPORT void dg_render_push_hud_line(char* label, uint8 lr, uint8 lg, uint8 lb,
                                        bool signd, int npips, 
                                        char s1, uint8 r1, uint8 g1, uint8 b1,
                                        char s2, uint8 r2, uint8 g2, uint8 b2) {

    char style[2] = { s1, s2 };
    TCOD_color_t cols[2] = { TCOD_color_RGB(r1, g1, b1), TCOD_color_RGB(r2, g2, b2) };
    grender::get().push_hud_line(label, TCOD_color_RGB(lr, lg, lb), signd, npips, style, cols);
}

typedef void (*dg_draw_do_callback)(unsigned int, unsigned int);
typedef bool (*dg_draw_check_callback)(unsigned int, unsigned int);

EXPORT void dg_render_draw_circle(unsigned int x, unsigned int y, unsigned int r, 
                                  bool do_draw, 
                                  uint8 rf, uint8 gf, uint8 bf,
                                  uint8 rb, uint8 gb, uint8 bb,
                                  dg_draw_do_callback func) {

    TCOD_color_t fore = TCOD_color_RGB(rf, gf, bf);
    TCOD_color_t back = TCOD_color_RGB(rb, gb, bb);

    grender::get().draw_circle(0, 0, x, y, r, do_draw, fore, back, func);
}

EXPORT void dg_render_draw_fov_circle(unsigned int x, unsigned int y, unsigned int rad, 
                                      bool do_draw, 
                                      uint8 rf, uint8 gf, uint8 bf,
                                      uint8 rb, uint8 gb, uint8 bb,
                                      dg_draw_do_callback func) {

    TCOD_color_t fore = TCOD_color_RGB(rf, gf, bf);
    TCOD_color_t back = TCOD_color_RGB(rb, gb, bb);

    grender::get().draw_fov_circle(0, 0, x, y, rad, do_draw, fore, back, func);
}

EXPORT void dg_render_draw_floodfill(unsigned int x, unsigned int y, 
                                         bool do_draw, 
                                         uint8 rf, uint8 gf, uint8 bf,
                                         uint8 rb, uint8 gb, uint8 bb,
                                         dg_draw_check_callback func) {


    TCOD_color_t fore = TCOD_color_RGB(rf, gf, bf);
    TCOD_color_t back = TCOD_color_RGB(rb, gb, bb);

    grender::get().draw_floodfill(0, 0, x, y, do_draw, fore, back, func);
}

EXPORT void dg_render_draw_line(unsigned int x0, unsigned int y0, 
                                unsigned int x1, unsigned int y1, 
                                bool do_draw, 
                                uint8 rf, uint8 gf, uint8 bf,
                                uint8 rb, uint8 gb, uint8 bb,
                                dg_draw_check_callback func) {

    TCOD_color_t fore = TCOD_color_RGB(rf, gf, bf);
    TCOD_color_t back = TCOD_color_RGB(rb, gb, bb);

    grender::get().draw_line(0, 0, x0, y0, x1, y1, do_draw, fore, back, func);
}

EXPORT void dg_render_message(char* msg, bool important) {
    grender::get().do_message(msg, important);
}

EXPORT void dg_render_draw_messages_window() {
    grender::get().draw_messages_window();
}

EXPORT bool dg_render_path_walk(unsigned int x0, unsigned int y0, unsigned int x1, unsigned int y1,
                                    unsigned int n, unsigned int cutoff, 
                                    unsigned int* xo, unsigned int* yo) {
    return grender::get().path_walk(x0, y0, x1, y1, n, cutoff, *xo, *yo);
}

EXPORT void dg_random_init(long seed) {
    rnd::get().init(seed);
}

EXPORT int dg_random_range(int a, int b) {
    return rnd::get().range(a, b);
}

EXPORT unsigned int dg_random_n(unsigned int n) {
    return rnd::get().n(n);
}

EXPORT double dg_random_gauss(double m, double s) {
    return rnd::get().gauss(m, s);
}

EXPORT double dg_random_uniform(double a, double b) {
    return rnd::get().uniform(a, b);
}

EXPORT unsigned int dg_random_geometric(double p) {
    return rnd::get().geometric(p);
}

EXPORT double dg_random_biased_gauss(double mean, double stddev, double bias, double factor) {
    return rnd::get().biased_gauss(mean, stddev, bias, factor);
}

EXPORT void dg_grid_init(unsigned int w, unsigned int h) {
    grid::get().init(w, h);
}

EXPORT void dg_grid_generate(int type) {
    grid::get().generate(type);
}

EXPORT void dg_grid_set_height(unsigned int x, unsigned int y, double h) {
    grid::get().set_height(x, y, h);
}

EXPORT double dg_grid_get_height(unsigned int x, unsigned int y) {
    return grid::get().get_height(x, y);
}

EXPORT bool dg_grid_is_walk(unsigned int x, unsigned int y) {
    return grid::get().is_walk(x, y);
}

EXPORT bool dg_grid_is_water(unsigned int x, unsigned int y) {
    return grid::get().is_water(x, y);
}

EXPORT void dg_grid_set_walk(unsigned int x, unsigned int y, bool v) {
    return grid::get().set_walk(x, y, v);
}

EXPORT void dg_grid_set_water(unsigned int x, unsigned int y, bool v) {
    return grid::get().set_water(x, y, v);
}

EXPORT void dg_grid_add_nogen(unsigned int x, unsigned int y) {
    grid::get().add_nogen(x, y);
}

EXPORT bool dg_grid_one_of_floor(unsigned int* x, unsigned int* y) {
    grid::pt xy; 
    bool ret = grid::get().one_of_floor(xy);
    *x = xy.first;
    *y = xy.second;
    return ret;
}

EXPORT bool dg_grid_one_of_water(unsigned int* x, unsigned int* y) {
    grid::pt xy;
    bool ret = grid::get().one_of_water(xy);
    *x = xy.first;
    *y = xy.second;
    return ret;
}

EXPORT bool dg_grid_one_of_walk(unsigned int* x, unsigned int* y) {
    grid::pt xy;
    bool ret = grid::get().one_of_walk(xy);
    *x = xy.first;
    *y = xy.second;
    return ret;
}
