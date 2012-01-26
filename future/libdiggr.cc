
#include "serialize.h"
#include "neighbors.h"
#include "celauto.h"
#include "render.h"
#include "random.h"
#include "grid.h"


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
    celauto::get().step(cbon, cboff);
}

extern "C" void dg_celauto_get_state(unsigned int x, unsigned int y, size_t* id, unsigned int* age) {
    celauto::get().get_state(celauto::pt(x,y), *id, *age);
}


extern "C" void dg_state_save(const char* filename) {
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


extern "C" void dg_render_init(unsigned int w, unsigned int h) {
    grender::get().init(w, h);
}

// python ctypes and/or libffi is severly broken. This is why struct passed by each individual field.


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

extern "C" bool dg_render_draw(TCOD_map_t map, unsigned int t,
			       unsigned int px, unsigned int py, 
			       unsigned int hlx, unsigned int hly,
			       unsigned int rmin, unsigned int rmax,
			       unsigned int lr) {

    return grender::get().draw(map, t, px, py, hlx, hly, rmin, rmax, lr);
}

extern "C" void dg_random_init(long seed) {
    rnd::get().init(seed);
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
