#ifndef __SCRIPTS_H
#define __SCRIPTS_H

#include <unordered_map>

#include "../piccol/piccol_modulum.h"

#include "tcod_colors.h"


#define CALLBACK const nanom::Shapes& shapes, const nanom::Shape& shape, \
        const nanom::Shape& shapeto, const nanom::Struct& struc, nanom::Struct& ret

namespace scripting {

using nanom::Sym;
typedef nanom::Struct Obj;

struct SymMap {

    typedef std::unordered_map<Sym,Obj> stock_t;

    stock_t objs;

    void add(Sym s, const Obj& o) { 
        auto i = objs.find(s);
        if (i != objs.end())
            throw std::runtime_error("Adding new object to stock: duplicate tag, '" + metalan::symtab().get(s) + "'");
        objs[s] = o;
    }

    bool get(Sym s, Obj& o) const {
        auto i = objs.find(s);
        if (i == objs.end())
            return false;
        o = i->second;
        return true;
    }
};


template <typename T>
inline T& symmap() {
    static T ret;
    return ret;
}

template <typename T>
inline bool symmap_set(CALLBACK) {
    symmap<T>().add(struc.v[0].uint, struc.substruct(1, shape.size()-1));
    return true;
}

template <typename T>
inline bool symmap_get(CALLBACK) {
    return symmap<T>().get(struc.v[0].uint, ret);
}


/*** *** ***/


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

inline Featmap& featmap() {
    static Featmap ret;
    return ret;
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

struct GlobalVar {
    Obj v;
};

template <typename T>
inline T& global() {
    static T ret;
    return ret;
}

template <typename T>
inline bool global_set(CALLBACK) {
    global<T>().v = struc;
    return true;
}

template <typename T>
inline bool global_get(CALLBACK) {
    Obj& v = global<T>().v;

    if (v.v.size() != shapeto.size()) {
        v.v.resize(shapeto.size());
    }

    ret = v;
    return true;
}


/****/

struct Player : public GlobalVar {};
struct Dungeon : public GlobalVar {};

struct FeatStock : public SymMap {};
struct PropStock : public SymMap {};


/****/

inline bool dg_random_range(CALLBACK) {

    ret.v.push_back(rnd::get().range(struc.v[0].inte, struc.v[1].inte));
    return true;
}

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

inline bool dg_grid_add_nogen(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    grid::get().add_nogen(x, y);
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

inline bool dg_render_set_env(CALLBACK) {
    
    grender::get().set_env(colorsyms::color(struc.v[0].uint), struc.v[1].real);
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

inline bool dg_current_moon(CALLBACK) {
    ret.v.push_back(metalan::symtab().get(moon::get().pi.phase_str));
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

    piccol::Modules vm;

    Vm(const std::string& sysdir, 
       const std::string& appdir) : vm(sysdir, appdir, "game.modules") {
            
        vm.register_callback("featstock_set", "[ Sym Feat ]",   "Void", symmap_set<FeatStock>);
        vm.register_callback("featstock_set", "[ Sym Props ]",  "Void", symmap_set<PropStock>);

        vm.register_callback("featstock_get", "Sym", "Feat",   symmap_get<FeatStock>);
        vm.register_callback("featstock_get", "Sym", "Props",  symmap_get<PropStock>);

        vm.register_callback("featmap_set",   "[ UInt UInt Feat ]", "Void", featmap_set);
        vm.register_callback("featmap_unset", "[ UInt UInt ]",      "Void", featmap_unset);

        vm.register_callback("get", "Void",   "Player", global_get<Player>);
        vm.register_callback("set", "Player", "Void",   global_set<Player>);

        vm.register_callback("get", "Void",    "Dungeon", global_get<Dungeon>);
        vm.register_callback("set", "Dungeon", "Void",    global_set<Dungeon>);

        //////

        vm.register_callback("dg_random_range", "[ Int Int ]", "Int", dg_random_range);
        
        vm.register_callback("dg_render_set_is_lit",    "[ UInt UInt Bool ]", "Void", dg_render_set_is_lit);
        vm.register_callback("dg_render_set_back",      "[ UInt UInt Sym ]",  "Void", dg_render_set_back);

        vm.register_callback("dg_render_set_is_viewblock", "[ UInt UInt Bool UInt ]", 
                             "Void", dg_render_set_is_viewblock);
        vm.register_callback("dg_render_set_is_walkblock", "[ UInt UInt Bool UInt ]", 
                             "Void", dg_render_set_is_walkblock);

        vm.register_callback("dg_render_set_skin", 
                             "[ UInt UInt UInt Sym Sym Sym Bool Bool ]", "Void", dg_render_set_skin);

        vm.register_callback("dg_render_set_env", "[ Sym Real ]", "Void", dg_render_set_env);

        vm.register_callback("dg_grid_set_walk",        "[ UInt UInt Bool ]", "Void", dg_grid_set_walk);
        vm.register_callback("dg_grid_set_water",       "[ UInt UInt Bool ]", "Void", dg_grid_set_water);
        vm.register_callback("dg_grid_set_height",      "[ UInt UInt Real ]", "Void", dg_grid_set_height);

        vm.register_callback("dg_grid_is_walk",    "[ UInt UInt ]", "Bool", dg_grid_is_walk);
        vm.register_callback("dg_grid_is_water",   "[ UInt UInt ]", "Bool", dg_grid_is_water);
        vm.register_callback("dg_grid_get_height", "[ UInt UInt ]", "Real", dg_grid_get_height);

        vm.register_callback("dg_grid_add_nogen",  "[ UInt UInt ]", "Void", dg_grid_add_nogen);
       
        vm.register_callback("dg_grid_generate", "Int", "Void", dg_grid_generate);

        vm.register_callback("dg_grid_one_of_floor", "Void", "[ UInt UInt ]", dg_grid_one_of_floor);
        vm.register_callback("dg_grid_one_of_water", "Void", "[ UInt UInt ]", dg_grid_one_of_water);
        vm.register_callback("dg_grid_one_of_walk",  "Void", "[ UInt UInt ]", dg_grid_one_of_walk);

        vm.register_callback("dg_current_moon", "Void", "Sym", dg_current_moon);

        vm.register_callback("dg__clear_map", "Void", "Void", dg__clear_map);

        vm.required("init", "Void", "Void");
        vm.required("generate", "Void", "Void");
        vm.required("set_skin", "[ UInt UInt ]", "Void");
        vm.required("drawing_context", "Void", "[ UInt UInt ]");

        vm.init();
    }        

    void init() {
        Obj out;
        Obj inp;
        vm.run("init", "Void", "Void", inp, out);
    }

    void generate() {
        Obj out;
        Obj inp;
        vm.run("generate", "Void", "Void", inp, out);
    }

    void set_skin(unsigned int x, unsigned int y) {
        Obj out;
        Obj in;
        in.v.push_back((nanom::UInt)x);
        in.v.push_back((nanom::UInt)y);
        vm.run("set_skin", "[ UInt UInt ]", "Void", in, out);
    }

    void drawing_context(unsigned int& px, unsigned int& py) {
        Obj out;
        Obj inp;

        vm.run("drawing_context", "Void", "[ UInt UInt ]", inp, out);

        px = out.v[0].uint;
        py = out.v[1].uint;
    }
};


}


#endif
