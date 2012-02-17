
#include "serialize.h"
#include "neighbors.h"
#include "celauto.h"
#include "render.h"
#include "random.h"
#include "grid.h"

struct _mark {
    grender::benchmark bm;
    std::string func;
    _mark(const std::string& s) : func(s) { bm.start(); }
    ~_mark() { std::cout << "  " << func << " " << bm.end() << std::endl; }
};

extern "C" void dg_neighbors_init(unsigned int w, unsigned int h) {
    neighbors::get().init(w, h);
}

extern "C" void dg_celauto_init() {
    celauto::get().init();
}

extern "C" void dg_celauto_make_rule(size_t i, const char* s, const char* b, unsigned int a) {
    celauto::get().make_rule(i, s, b, a);
}

extern "C" void dg_celauto_seed(unsigned int x, unsigned int y, size_t ri) {
    celauto::CaMap& ca = celauto::get();
    std::shared_ptr<celauto::rule> r = ca.get_rule(ri);

    if (r) {
        ca.seed(celauto::pt(x,y), r);
    }
}

typedef void (*dg_celauto_callback)(unsigned int, unsigned int, size_t);

extern "C" void dg_celauto_clear(unsigned int x, unsigned int y, dg_celauto_callback cb) {
    celauto::get().clear(celauto::pt(x,y), cb);
}

extern "C" void dg_celauto_step(dg_celauto_callback cbon, dg_celauto_callback cboff) {
    _mark __m(__func__);
    celauto::get().step(cbon, cboff);
}

extern "C" void dg_celauto_get_state(unsigned int x, unsigned int y, size_t* id, unsigned int* age) {
    celauto::get().get_state(celauto::pt(x,y), *id, *age);
}


extern "C" void dg_state_save(const char* filename) {
    _mark __m(__func__);
    serialize::Sink s(filename);
    celauto::get().write(s);
    grender::get().write(s);
    grid::get().write(s);
}

extern "C" void dg_state_load(const char* filename) {
    serialize::Source s(filename);
    celauto::get().read(s);
    grender::get().read(s);
    grid::get().read(s);
}


extern "C" void dg_render_init(unsigned int w, unsigned int h, 
                               const char* fontfile, const char* title, bool fullscreen) {
    _mark __m(__func__);
    grender::get().init(w, h, fontfile, title, fullscreen);
}

extern "C" void dg_render_clear() {
    grender::get().clear();
}

extern "C" void dg_render_wait_for_anykey() {
    return grender::get().wait_for_anykey();
}

extern "C" void dg_render_skip_input(unsigned int delay) {
    return grender::get().skip_input(delay);
}

extern "C" void dg_render_wait_for_key(int* vk, char* c) {
    grender::Grid::keypress k = grender::get().wait_for_key();
    *vk = k.vk;
    *c = k.c;
}

extern "C" void dg_render_draw_window(const char** _msg, size_t n, int* vk, char* c) {
    _mark __m(__func__);
    std::vector<std::string> msg;
    for (int i = 0; i < n; ++i) {
        msg.push_back(_msg[i]);
    }
    grender::Grid::keypress k = grender::get().draw_window(msg);
    *vk = k.vk;
    *c = k.c;
}

extern "C" unsigned long dg_render_get_keylog_size() {
    return grender::get().keylog.size();
}

extern "C" bool dg_render_get_keylog_entry(unsigned long i, int* vk, char* c) {

    if (i >= grender::get().keylog.size())
        return false;

    const grender::Grid::keypress& k = grender::get().keylog[i];
    *vk = k.vk;
    *c = k.c;
    return true;
}

extern "C" void dg_render_clear_keylog() {
    grender::get().keylog.clear();
}

extern "C" void dg_render_push_replay_keypress(int vk, char c) {
    grender::get().push_replay_keypress(grender::Grid::keypress(vk, c));
}

extern "C" void dg_render_stop_keypress_replay() {
    grender::get().stop_keypress_replay();
}

// python ctypes and/or libffi is severly broken. This is why struct are passed by each individual field.


extern "C" void dg_render_set_env(uint8 r, uint8 g, uint8 b, double intensity) {
    TCOD_color_t color;
    color.r = r;
    color.g = g;
    color.b = b;
    grender::get().set_env(color, intensity);
}

extern "C" void dg_render_set_back(unsigned int x, unsigned int y, uint8 r, uint8 g, uint8 b) {
    TCOD_color_t back;
    back.r = r;
    back.g = g;
    back.b = b;
    grender::get().set_back(x, y, back);
}

extern "C" void dg_render_set_is_lit(unsigned int x, unsigned int y, bool is_lit) {
    grender::get().set_is_lit(x, y, is_lit);
}

extern "C" void dg_render_push_skin(unsigned int x, unsigned int y,
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
    grender::get().push_skin(x, y, fore, c, fore2, fore_interp, is_terrain);
}

extern "C" void dg_render_set_skin(unsigned int x, unsigned int y,
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
    grender::get().set_skin(x, y, fore, c, fore2, fore_interp, is_terrain);
}

extern "C" void dg_render_pop_skin(unsigned int x, unsigned int y) {
    grender::get().pop_skin(x, y);
}

extern "C" bool dg_render_is_in_fov(unsigned int x, unsigned int y) {
    return grender::get().is_in_fov(x, y);
}

extern "C" void dg_render_set_is_viewblock(unsigned int x, unsigned int y, bool t) {
    grender::get().set_is_viewblock(x, y, t);
}

extern "C" void dg_render_set_is_walkblock(unsigned int x, unsigned int y, bool t) {
    grender::get().set_is_walkblock(x, y, t);
}

extern "C" bool dg_render_draw(unsigned int t,
			       unsigned int px, unsigned int py, 
			       unsigned int hlx, unsigned int hly,
			       unsigned int rmin, unsigned int rmax,
			       unsigned int lr, bool do_hud) {
    _mark __m(__func__);
    return grender::get().draw(t, px, py, hlx, hly, rmin, rmax, lr, do_hud);
}

extern "C" void dg_render_push_hud_line(char* label, uint8 lr, uint8 lg, uint8 lb,
                                        bool signd, int npips, 
                                        char s1, uint8 r1, uint8 g1, uint8 b1,
                                        char s2, uint8 r2, uint8 g2, uint8 b2) {

    char style[2] = { s1, s2 };
    TCOD_color_t cols[2] = { TCOD_color_RGB(r1, g1, b1), TCOD_color_RGB(r2, g2, b2) };
    grender::get().push_hud_line(label, TCOD_color_RGB(lr, lg, lb), signd, npips, style, cols);
}

typedef void (*dg_draw_do_callback)(unsigned int, unsigned int);
typedef bool (*dg_draw_check_callback)(unsigned int, unsigned int);

extern "C" void dg_render_draw_circle(unsigned int x, unsigned int y, unsigned int r, 
                                      bool do_draw, 
                                      uint8 rf, uint8 gf, uint8 bf,
                                      uint8 rb, uint8 gb, uint8 bb,
                                      dg_draw_do_callback func) {

    TCOD_color_t fore = TCOD_color_RGB(rf, gf, bf);
    TCOD_color_t back = TCOD_color_RGB(rb, gb, bb);

    grender::get().draw_circle(x, y, r, do_draw, fore, back, func);
}

extern "C" void dg_render_draw_fov_circle(unsigned int x, unsigned int y, unsigned int rad, 
                                          bool do_draw, 
                                          uint8 rf, uint8 gf, uint8 bf,
                                          uint8 rb, uint8 gb, uint8 bb,
                                          dg_draw_do_callback func) {

    TCOD_color_t fore = TCOD_color_RGB(rf, gf, bf);
    TCOD_color_t back = TCOD_color_RGB(rb, gb, bb);

    grender::get().draw_fov_circle(x, y, rad, do_draw, fore, back, func);
}

extern "C" void dg_render_draw_floodfill(unsigned int x, unsigned int y, 
                                         bool do_draw, 
                                         uint8 rf, uint8 gf, uint8 bf,
                                         uint8 rb, uint8 gb, uint8 bb,
                                         dg_draw_check_callback func) {


    TCOD_color_t fore = TCOD_color_RGB(rf, gf, bf);
    TCOD_color_t back = TCOD_color_RGB(rb, gb, bb);

    grender::get().draw_floodfill(x, y, do_draw, fore, back, func);
}

extern "C" void dg_render_draw_line(unsigned int x0, unsigned int y0, 
                                    unsigned int x1, unsigned int y1, 
                                    bool do_draw, 
                                    uint8 rf, uint8 gf, uint8 bf,
                                    uint8 rb, uint8 gb, uint8 bb,
                                    dg_draw_check_callback func) {
    _mark __m(__func__);
    TCOD_color_t fore = TCOD_color_RGB(rf, gf, bf);
    TCOD_color_t back = TCOD_color_RGB(rb, gb, bb);

    grender::get().draw_line(x0, y0, x1, y1, do_draw, fore, back, func);
}

extern "C" void dg_render_message(char* msg, bool important) {
    grender::get().do_message(msg, important);
}

extern "C" void dg_render_draw_messages_window() {
    grender::get().draw_messages_window();
}

extern "C" bool dg_render_path_walk(unsigned int x0, unsigned int y0, unsigned int x1, unsigned int y1,
                                    unsigned int n, unsigned int cutoff, 
                                    unsigned int* xo, unsigned int* yo) {
    return grender::get().path_walk(x0, y0, x1, y1, n, cutoff, *xo, *yo);
}

extern "C" void dg_random_init(long seed) {
    rnd::get().init(seed);
}

extern "C" int dg_random_range(int a, int b) {
    return rnd::get().range(a, b);
}

extern "C" unsigned int dg_random_n(unsigned int n) {
    return rnd::get().n(n);
}

extern "C" double dg_random_gauss(double m, double s) {
    return rnd::get().gauss(m, s);
}

extern "C" double dg_random_uniform(double a, double b) {
    return rnd::get().uniform(a, b);
}

extern "C" unsigned int dg_random_geometric(double p) {
    return rnd::get().geometric(p);
}

extern "C" double dg_random_biased_gauss(double mean, double stddev, double bias, double factor) {
    return rnd::get().biased_gauss(mean, stddev, bias, factor);
}

extern "C" void dg_grid_init(unsigned int w, unsigned int h) {
    grid::get().init(w, h);
}

extern "C" void dg_grid_generate(int type) {
    grid::get().generate(type);
}

extern "C" void dg_grid_set_height(unsigned int x, unsigned int y, double h) {
    grid::get().set_height(x, y, h);
}

extern "C" double dg_grid_get_height(unsigned int x, unsigned int y) {
    return grid::get().get_height(x, y);
}

extern "C" bool dg_grid_is_walk(unsigned int x, unsigned int y) {
    return grid::get().is_walk(x, y);
}

extern "C" bool dg_grid_is_water(unsigned int x, unsigned int y) {
    return grid::get().is_water(x, y);
}

extern "C" void dg_grid_set_walk(unsigned int x, unsigned int y, bool v) {
    return grid::get().set_walk(x, y, v);
}

extern "C" void dg_grid_set_water(unsigned int x, unsigned int y, bool v) {
    return grid::get().set_water(x, y, v);
}

extern "C" void dg_grid_add_nogen(unsigned int x, unsigned int y) {
    grid::get().add_nogen(x, y);
}

extern "C" void dg_grid_one_of_floor(unsigned int* x, unsigned int* y) {
    grid::pt xy = grid::get().one_of_floor();
    *x = xy.first;
    *y = xy.second;
}

extern "C" void dg_grid_one_of_water(unsigned int* x, unsigned int* y) {
    grid::pt xy = grid::get().one_of_water();
    *x = xy.first;
    *y = xy.second;
}

extern "C" void dg_grid_one_of_walk(unsigned int* x, unsigned int* y) {
    grid::pt xy = grid::get().one_of_walk();
    *x = xy.first;
    *y = xy.second;
}
