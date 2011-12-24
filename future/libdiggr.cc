
#include "serialize.h"
#include "neighbors.h"
#include "celauto.h"
#include <sys/time.h>


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
    struct timeval t1;
    struct timeval t2;
    gettimeofday(&t1, NULL);
    celauto::get().step(cbon, cboff);
    gettimeofday(&t2, NULL);
    size_t n1 = (t1.tv_sec*1000000) + t1.tv_usec;
    size_t n2 = (t2.tv_sec*1000000) + t2.tv_usec;
    std::cout << "steptime:"<<(double)(n2-n1)/1e6<<std::endl;
}

extern "C" void dg_celauto_get_state(unsigned int x, unsigned int y, size_t* id, unsigned int* age) {
    celauto::get().get_state(celauto::pt(x,y), *id, *age);
}


extern "C" void dg_state_save(const char* filename) {
    serialize::Sink s(filename);
    celauto::get().write(s);
}

extern "C" void dg_state_load(const char* filename) {
    serialize::Source s(filename);
    celauto::get().read(s);
}


