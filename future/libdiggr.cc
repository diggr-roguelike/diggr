
#include "neighbors.h"
#include "celauto.h"


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

