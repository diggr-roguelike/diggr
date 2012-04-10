#ifndef __SCRIPT_H
#define __SCRIPT_H

#include <unordered_map>

#include "../piccol/piccol_modulum.h"
#include "../piccol/structures.h"

#include "tcod_colors.h"


#define CALLBACK const nanom::Shapes& shapes, const nanom::Shape& shape, \
        const nanom::Shape& shapeto, const nanom::Struct& struc, nanom::Struct& ret

namespace scripting {


/****/

struct Player;
struct Dungeon;

struct FeatStock;
struct PropStock;
struct MonsterStock;

struct FeatMap;
struct MonsterMap;

/****/

inline bool dg_random_range(CALLBACK) {

    ret.v.push_back(rnd::get().range(struc.v[0].inte, struc.v[1].inte));
    return true;
}

inline bool random_gauss(const nanom::Struct& struc, nanom::Struct& ret, nanom::Real n) {
    nanom::Real mean = struc.v[0].real;
    nanom::Real stdd = struc.v[1].real;
    nanom::Real bias = struc.v[2].real;
    nanom::Real rt;

    if (bias == 0) {
        rt = rnd::get().gauss(mean, stdd);
    } else {
        rt = rnd::get().biased_gauss(mean, stdd, bias, n);
    }

    ret.v.push_back(rt);
    return true;
}

inline bool dg_random_neg_gauss(CALLBACK) {
    return random_gauss(struc, ret, -1.0);
}

inline bool dg_random_pos_gauss(CALLBACK) {
    return random_gauss(struc, ret, 1.0);
}

inline bool random_nat_gauss(const nanom::Struct& struc, nanom::Struct& ret, nanom::Real n) {
    bool rr = random_gauss(struc, ret, n);
    nanom::UInt m = struc.v[3].uint;
    nanom::UInt tmp = std::max((nanom::Int)round(ret.v[0].real), (nanom::Int)m);
    ret.v[0] = tmp;
    return rr;
}

inline bool dg_random_nat_neg_gauss(CALLBACK) {
    return random_nat_gauss(struc, ret, -1.0);
}

inline bool dg_random_nat_pos_gauss(CALLBACK) {
    return random_nat_gauss(struc, ret, 1.0);
}


inline bool dg_render_set_is_lit(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    nanom::UInt z = struc.v[2].uint;
    grender::get().set_is_lit(x, y, z, struc.v[3].uint);
    return true;
}

inline bool dg_render_set_back(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    nanom::UInt z = struc.v[2].uint;
    grender::get().set_back(x, y, z, colorsyms::color(struc.v[3].uint));
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

inline bool dg_render_is_viewblock(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    ret.v.push_back((nanom::UInt)grender::get().is_viewblock(x, y));
    return true;
}

inline bool dg_render_is_walkblock(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    ret.v.push_back((nanom::UInt)grender::get().is_walkblock(x, y));
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

inline bool dg_neighbors_linked(CALLBACK) {
    
    ret.v.push_back((nanom::UInt)neighbors::get().linked(neighbors::pt(struc.v[0].uint, struc.v[1].uint),
                                                         neighbors::pt(struc.v[2].inte, struc.v[3].inte)));
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

    piccol::structmap<FeatMap>().clear();
    piccol::structmap<MonsterMap>().clear();

    return true;
}

inline bool _print1(CALLBACK) {
    std::cout << struc.v[0].inte;
    return true;
}

inline bool _print2(CALLBACK) {
    std::cout << struc.v[0].uint;
    return true;
}

inline bool _print3(CALLBACK) {
    std::cout << metalan::symtab().get(struc.v[0].uint);
    return true;
}


struct Vm {

    piccol::Modules vm;

    typedef nanom::Struct Obj;

    Vm(const std::string& sysdir, 
       const std::string& appdir) : vm(sysdir, appdir, "game.modules") {

        piccol::register_map<FeatStock>(vm,    "Sym",           "Feat");
        piccol::register_map<PropStock>(vm,    "Sym",           "Props");
        piccol::register_map<FeatMap>(vm,      "[ UInt UInt ]", "Feat");

        piccol::register_map<MonsterStock>(vm,  "Sym",        "Monster");
        piccol::register_pool<MonsterStock>(vm, "MonsterKey", "Sym");

        piccol::register_map<MonsterMap>(vm,    "[ UInt UInt ]", "MonsterVal");
            
        piccol::register_global<Player>(vm,  "Player");
        piccol::register_global<Dungeon>(vm, "Dungeon");

        //////

        vm.register_callback("dg_random_range", "[ Int Int ]", "Int", dg_random_range);
        vm.register_callback("dg_random_pos_gauss", "[ Real Real Real ]", "Real", dg_random_pos_gauss);
        vm.register_callback("dg_random_neg_gauss", "[ Real Real Real ]", "Real", dg_random_neg_gauss);
        vm.register_callback("dg_random_nat_pos_gauss", "[ Real Real Real UInt ]", "UInt", dg_random_nat_pos_gauss);
        vm.register_callback("dg_random_nat_neg_gauss", "[ Real Real Real UInt ]", "UInt", dg_random_nat_neg_gauss);
        
        vm.register_callback("dg_render_set_is_lit",    "[ UInt UInt UInt Bool ]",  "Void", dg_render_set_is_lit);
        vm.register_callback("dg_render_set_back",      "[ UInt UInt UInt Sym ]",  "Void", dg_render_set_back);

        vm.register_callback("dg_render_set_is_viewblock", "[ UInt UInt UInt Bool ]", 
                             "Void", dg_render_set_is_viewblock);
        vm.register_callback("dg_render_set_is_walkblock", "[ UInt UInt UInt Bool ]", 
                             "Void", dg_render_set_is_walkblock);

        vm.register_callback("dg_render_is_viewblock", "[ UInt UInt ]", "Bool", dg_render_is_viewblock);
        vm.register_callback("dg_render_is_walkblock", "[ UInt UInt ]", "Bool", dg_render_is_walkblock);

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

        vm.register_callback("dg_neighbors_linked", "[ UInt UInt Int Int ]", "Bool", dg_neighbors_linked);

        vm.register_callback("dg_current_moon", "Void", "Sym", dg_current_moon);

        vm.register_callback("dg__clear_map", "Void", "Void", dg__clear_map);

        vm.register_callback("print", "UInt", "Void", _print1);
        vm.register_callback("print", "Int",  "Void", _print2);
        vm.register_callback("print", "Sym",  "Void", _print3);

        ////// 

        vm.required("init", "Void", "Void");
        vm.required("generate", "Void", "Void");
        vm.required("set_skin", "[ UInt UInt ]", "Void");
        vm.required("drawing_context", "Void", "[ UInt UInt ]");
        vm.required("handle_input", "InState", "OutState");

        vm.init();

        vm.check_type("InState",  {nanom::UINT, nanom::INT, nanom::SYMBOL});
        vm.check_type("OutState", {nanom::UINT, nanom::BOOL, nanom::BOOL});
    }        

    void run(const std::string& name, const std::string& from, const std::string& to, 
             nanom::Struct& inp, nanom::Struct& out) {

        bool ret = vm.run(name, from, to, inp, out);
        if (!ret) {
            throw std::runtime_error("Calling " + name + " " + from + "->" + to + " failed");
        }
    }

    void init() {
        Obj out;
        Obj inp;
        run("init", "Void", "Void", inp, out);
    }

    void generate() {
        Obj out;
        Obj inp;
        run("generate", "Void", "Void", inp, out);
    }

    void set_skin(unsigned int x, unsigned int y) {
        std::cout << "!!!! set_skin" << std::endl;
        Obj out;
        Obj inp;
        inp.v.push_back((nanom::UInt)x);
        inp.v.push_back((nanom::UInt)y);
        run("set_skin", "[ UInt UInt ]", "Void", inp, out);
    }

    void drawing_context(unsigned int& px, unsigned int& py) {
        Obj out;
        Obj inp;

        run("drawing_context", "Void", "[ UInt UInt ]", inp, out);

        px = out.v[0].uint;
        py = out.v[1].uint;
    }

    void handle_input(size_t& ticks, int vk, char c, bool& done, bool& dead) {
        Obj out;
        Obj inp;
        inp.v.push_back((nanom::UInt)ticks);
        inp.v.push_back((nanom::Int)vk);
        char cc[2] = { c, 0 };
        inp.v.push_back((nanom::Sym)metalan::symtab().get(cc));

        run("handle_input", "InState", "OutState", inp, out);

        ticks = out.v[0].uint;
        done = out.v[1].uint;
        dead = out.v[2].uint;
    }

};


}

#undef CALLBACK

#endif
