#ifndef __SCRIPTS_H
#define __SCRIPTS_H

#include <unordered_map>

#include "piccol.h"

#include "tcod_colors.h"


#define CALLBACK const nanom::Shapes& shapes, const nanom::Shape& shape, \
        const nanom::Shape& shapeto, const nanom::Struct& struc, nanom::Struct& ret

namespace scripting {

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
    void add_gridprops(Sym s, const Obj& o)   { _add_feat(s, o, 2); }

    bool _get_feat(Sym s, Obj& o, int t) const {
        auto i = feats.find(s);
        if (i == feats.end() || i->second.first != t)
            return false;
        o = i->second.second;
        return true;
    }

    bool get_feat(Sym s, Obj& o) const        { return _get_feat(s, o, 1); }
    bool get_gridprops(Sym s, Obj& o) const   { return _get_feat(s, o, 2); }

};

struct Featmap {

    typedef std::unordered_map< std::pair<unsigned int, unsigned int>, Obj > fmap_t;

    fmap_t feats;
    
    void set(unsigned int x, unsigned int y, const Obj& o) {
        feats[std::make_pair(x, y)] = o;
    }

    void unset(unsigned int x, unsigned int y) {
        feats.erase(std::make_pair(x, y));
    }

    bool get(unsigned int x, unsigned int y, Obj& o) const {
        auto i = feats.find(std::make_pair(x, y));
        if (i == feats.end())
            return false;
        o = i->second;
        return true;
    }

    void clear() {
        feats.clear();
    }
};

inline Featstock& featstock() {
    static Featstock ret;
    return ret;
}

inline Featmap& featmap() {
    static Featmap ret;
    return ret;
}

inline bool featstock_set_1(CALLBACK) {
    featstock().add_feat(struc.v[0].uint, struc.substruct(1, shape.size()-1));
    return true;
}

inline bool featstock_set_2(CALLBACK) {
    featstock().add_gridprops(struc.v[0].uint, struc.substruct(1, shape.size()-1));
    return true;
}


inline bool featstock_get_1(CALLBACK) {
    return featstock().get_feat(struc.v[0].uint, ret);
}

inline bool featstock_get_2(CALLBACK) {
    return featstock().get_gridprops(struc.v[0].uint, ret);
}


inline bool featmap_set(CALLBACK) {
    featmap().set(struc.v[0].uint, 
                  struc.v[1].uint, struc.substruct(2, shape.size()-1));
    return true;
}

inline bool featmap_unset(CALLBACK) {
    featmap().unset(struc.v[0].uint, struc.v[1].uint);
    return true;
}


/****/

struct Player {
    Obj p;
};

inline Player& player() {
    static Player ret;
    return ret;
}

inline bool player_set(CALLBACK) {
    player().p = struc;
    return true;
}

inline bool player_get(CALLBACK) {
    Obj& p = player().p;

    if (p.v.size() != shapeto.size()) {
        p.v.resize(shapeto.size());
    }

    ret = p;
    return true;
}

/****/

inline bool dg_render_set_is_lit(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    grender::get().set_is_lit(x, y, struc.v[2].uint);
    return true;
}

inline bool dg_render_set_back(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    grender::get().set_back(x, y, colorsyms::color(struc.v[2].uint));
    return true;
}

inline bool dg_render_set_is_viewblock(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    grender::get().set_is_viewblock(x, y, struc.v[2].uint, struc.v[3].uint);
    return true;
}

inline bool dg_render_set_is_walkblock(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    grender::get().set_is_walkblock(x, y, struc.v[2].uint, struc.v[3].uint);
    return true;
}

inline bool dg_grid_set_walk(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    grid::get().set_walk(x, y, struc.v[2].uint);
    return true;
}

inline bool dg_grid_set_height(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    grid::get().set_height(x, y, struc.v[2].inte);
    return true;
}

inline bool dg_grid_set_water(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    grid::get().set_height(x, y, struc.v[2].real);
    return true;
}

inline bool dg_grid_is_walk(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    bool r = grid::get().is_walk(x, y);
    ret.v.push_back((nanom::UInt)r);
    return true;
}

inline bool dg_grid_is_water(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    bool r = grid::get().is_water(x, y);
    ret.v.push_back((nanom::UInt)r);
    return true;
}

inline bool dg_grid_get_height(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    nanom::Real r = grid::get().get_height(x, y);
    ret.v.push_back(r);
    return true;
}

inline bool dg_render_set_skin(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;

    grender::get().set_skin(x, y, struc.v[2].uint,
                            colorsyms::color(struc.v[3].uint),
                            metalan::symtab().get(struc.v[4].uint)[0],
                            colorsyms::color(struc.v[5].uint),
                            struc.v[6].uint,
                            struc.v[7].uint);
    return true;
}

inline bool dg_grid_generate(CALLBACK) {

    grid::get().generate(struc.v[0].inte);
    return true;
}

inline bool dg_grid_one_of_floor(CALLBACK) {
    
    grid::pt xy = grid::get().one_of_floor();
    ret.v.push_back((nanom::UInt)xy.first);
    ret.v.push_back((nanom::UInt)xy.second);
    return true;
}

inline bool dg_grid_one_of_water(CALLBACK) {
    
    grid::pt xy = grid::get().one_of_water();
    ret.v.push_back((nanom::UInt)xy.first);
    ret.v.push_back((nanom::UInt)xy.second);
    return true;
}

inline bool dg_grid_one_of_walk(CALLBACK) {
    
    grid::pt xy = grid::get().one_of_walk();
    ret.v.push_back((nanom::UInt)xy.first);
    ret.v.push_back((nanom::UInt)xy.second);
    return true;
}

inline bool dg__clear_map(CALLBACK) {

    celauto::get().clear();
    grid::get().clear();
    neighbors::get().clear();
    grender::get().clear();
    return true;
}

struct Vm {

    piccol::Piccol0 vm;

    Vm(const std::string& sysdir, 
       const std::string& appdir) : vm(sysdir) {
            
        vm.register_callback("featstock_set", "[ Sym Feat ]",       "Void", featstock_set_1);
        vm.register_callback("featstock_set", "[ Sym Gridprops ]",  "Void", featstock_set_2);

        vm.register_callback("featstock_get", "Sym", "Feat",       featstock_get_1);
        vm.register_callback("featstock_get", "Sym", "Gridprops",  featstock_get_2);

        vm.register_callback("featmap_set",   "[ UInt UInt Feat ]", "Void", featmap_set);
        vm.register_callback("featmap_unset", "[ UInt UInt ]",      "Void", featmap_unset);

        vm.register_callback("get", "Void", "Player", player_get);
        vm.register_callback("set", "Player", "Void", player_set);

        vm.register_callback("dg_render_set_is_lit",    "[ UInt UInt Bool ]", "Void", dg_render_set_is_lit);
        vm.register_callback("dg_render_set_back",      "[ UInt UInt Sym ]",  "Void", dg_render_set_back);

        vm.register_callback("dg_render_set_is_viewblock", "[ UInt UInt Bool UInt ]", 
                             "Void", dg_render_set_is_viewblock);
        vm.register_callback("dg_render_set_is_walkblock", "[ UInt UInt Bool UInt ]", 
                             "Void", dg_render_set_is_walkblock);

        vm.register_callback("dg_render_set_skin", 
                             "[ UInt UInt UInt Sym Sym Sym Bool Bool ]", "Void", dg_render_set_skin);

        vm.register_callback("dg_grid_set_walk",        "[ UInt UInt Bool ]", "Void", dg_grid_set_walk);
        vm.register_callback("dg_grid_set_water",       "[ UInt UInt Bool ]", "Void", dg_grid_set_water);
        vm.register_callback("dg_grid_set_height",      "[ UInt UInt Real ]", "Void", dg_grid_set_height);

        vm.register_callback("dg_grid_is_walk",    "[ UInt UInt ]", "Bool", dg_grid_is_walk);
        vm.register_callback("dg_grid_is_water",   "[ UInt UInt ]", "Bool", dg_grid_is_water);
        vm.register_callback("dg_grid_get_height", "[ UInt UInt ]", "Real", dg_grid_get_height);
       
        vm.register_callback("dg_grid_generate", "Int", "Void", dg_grid_generate);

        vm.register_callback("dg_grid_one_of_floor", "Void", "[ UInt UInt ]", dg_grid_one_of_floor);
        vm.register_callback("dg_grid_one_of_water", "Void", "[ UInt UInt ]", dg_grid_one_of_water);
        vm.register_callback("dg_grid_one_of_walk",  "Void", "[ UInt UInt ]", dg_grid_one_of_walk);

        vm.register_callback("dg__clear_map", "Void", "Void", dg__clear_map);

        vm.load(piccol::load_file(appdir + "common.piccol"));
        vm.load(piccol::load_file(appdir + "generate.piccol"));
    }        


    void generate() {
        Obj out;
        vm.run("generate", "Void", "Void", out);
    }

    void set_skin(unsigned int x, unsigned int y) {
        Obj out;
        Obj in;
        in.v.push_back((nanom::UInt)x);
        in.v.push_back((nanom::UInt)y);
        vm.run("set_skin", "[ UInt UInt ]", "Void", in, out);
    }

    void init() {
        //Obj out;
        //vm.run("featstock_init", "Void", "Void", out);
    }
};

/*
inline Vm& vm() {
    static Vm ret;
    return ret;
}
*/

}


#endif
