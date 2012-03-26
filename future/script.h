#ifndef __SCRIPTS_H
#define __SCRIPTS_H

#include <unordered_map>

#include "piccol.h"

namespace feats {

using nanom::Sym;
typedef nanom::Struct Obj;

struct Featstock {

    typedef std::unordered_map< Sym, std::pair<int,Obj> > stock_t;

    stock_t feats;

    void _add_feat(Sym s, const Obj& o, int t) { 
        auto i = feats.find(s);
        if (i != feats.end())
            throw std::runtime_error("Adding new Feature: duplicate tag, '" + metalan::symtab().get(s) + "'");
        feats[s] = std::make_pair(t, o);
    }

    void add_feat(Sym s, const Obj& o)        { _add_feat(s, o, 1); }
    void add_noskin_feat(Sym s, const Obj& o) { _add_feat(s, o, 2); }
    void add_gridprops(Sym s, const Obj& o)   { _add_feat(s, o, 3); }

    bool _get_feat(Sym s, Obj& o, int t) const {
        auto i = feats.find(s);
        if (i == feats.end() || i->second.first != t)
            return false;
        o = i->second.second;
        return true;
    }

    bool get_feat(Sym s, Obj& o) const        { return _get_feat(s, o, 1); }
    bool get_noskin_feat(Sym s, Obj& o) const { return _get_feat(s, o, 2); }
    bool get_gridprops(Sym s, Obj& o) const   { return _get_feat(s, o, 3); }

};

inline Featstock& featstock() {
    static Featstock ret;
    return ret;
}

inline bool featstock_set_1(const nanom::Shapes& shapes, const nanom::Shape& shape, const nanom::Shape& shapeto,
                            const nanom::Struct& struc, nanom::Struct& ret) {
    featstock().add_feat(struc.v[0].uint, struc.substruct(1, shape.size()-1));
    return true;
}

inline bool featstock_set_2(const nanom::Shapes& shapes, const nanom::Shape& shape, const nanom::Shape& shapeto,
                            const nanom::Struct& struc, nanom::Struct& ret) {
    featstock().add_noskin_feat(struc.v[0].uint, struc.substruct(1, shape.size()-1));
    return true;
}

inline bool featstock_set_3(const nanom::Shapes& shapes, const nanom::Shape& shape, const nanom::Shape& shapeto,
                            const nanom::Struct& struc, nanom::Struct& ret) {
    featstock().add_gridprops(struc.v[0].uint, struc.substruct(1, shape.size()-1));
    return true;
}


inline bool featstock_get_1(const nanom::Shapes& shapes, const nanom::Shape& shape, const nanom::Shape& shapeto,
                            const nanom::Struct& struc, nanom::Struct& ret) {
    return featstock().get_feat(struc.v[0].uint, ret);
}

inline bool featstock_get_2(const nanom::Shapes& shapes, const nanom::Shape& shape, const nanom::Shape& shapeto,
                            const nanom::Struct& struc, nanom::Struct& ret) {
    return featstock().get_noskin_feat(struc.v[0].uint, ret);
}

inline bool featstock_get_3(const nanom::Shapes& shapes, const nanom::Shape& shape, const nanom::Shape& shapeto,
                            const nanom::Struct& struc, nanom::Struct& ret) {
    return featstock().get_gridprops(struc.v[0].uint, ret);
}

struct FeatVm {

    piccol::Piccol0 vm;

    FeatVm() {
        vm.register_callback("featstock_set", "[ Sym Feat ]",       "Void", featstock_set_1);
        vm.register_callback("featstock_set", "[ Sym FeatNoSkin ]", "Void", featstock_set_2);
        vm.register_callback("featstock_set", "[ Sym Gridprops ]",  "Void", featstock_set_3);

        vm.register_callback("featstock_get", "Sym", "Feat",       featstock_get_1);
        vm.register_callback("featstock_set", "Sym", "FeatNoSkin", featstock_get_2);
        vm.register_callback("featstock_set", "Sym", "Gridprops",  featstock_get_3);

        vm.load(piccol::load_file("scripts/feats.piccol"));
    }        

    void init() {
        Obj out;
        vm.run("featstock_init", "Void", "Void", out);
    }
};

inline FeatVm& feats() {
    static FeatVm ret;
    return ret;
}

}


#endif
