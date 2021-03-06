#ifndef __SCRIPT_H
#define __SCRIPT_H

#include <unordered_map>

#include "../piccol/piccol_modulum.h"
#include "../piccol/structures.h"
#include "../piccol/sequencers.h"

#include "tcod_colors.h"


#define CALLBACK const nanom::Shapes& shapes, const nanom::Shape& shape, \
        const nanom::Shape& shapeto, const nanom::Struct& struc, nanom::Struct& ret


using namespace std::placeholders;

namespace serialize {

template <>
struct writer<nanom::Val> {
    void write(Sink& s, const nanom::Val& v) {
        serialize::write(s, v.uint);
    }
};

template <>
struct reader<nanom::Val> {
    void read(Source& s, nanom::Val& v) {
        serialize::read(s, v.uint);
    }
};

template <>
struct writer<nanom::Struct> {
    void write(Sink& s, const nanom::Struct& v) {
        serialize::write(s, v.v);
    }
};


template <>
struct reader<nanom::Struct> {
    void read(Source& s, nanom::Struct& v) {
        serialize::read(s, v.v);
    }
};

}

namespace scripting {


/****/

struct Player;
struct Dungeon;

struct FeatStock;
struct PropStock;
struct MonsterStock;
struct ItemStock;

struct FeatMap;
struct MonsterMap;
struct MonsterMapScratch;
struct ItemMap;

struct Inventory;

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

inline bool dg_random_uniform(CALLBACK) {
    nanom::Real v = rnd::get().uniform(struc.v[0].real, struc.v[1].real);
    ret.v.push_back(v);
    return true;
}

inline bool dg_random_geometric(CALLBACK) {
    nanom::UInt v = rnd::get().geometric(struc.v[0].real);
    ret.v.push_back(v);
    return true;
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

inline bool dg_render_is_valid(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    ret.v.push_back((nanom::UInt)grender::get().is_valid(x, y));
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

inline bool dg_grid_add_nogen_expand(CALLBACK) {

    nanom::UInt x = struc.v[0].uint;
    nanom::UInt y = struc.v[1].uint;
    grid::get().add_nogen_expand(x, y, struc.v[2].uint);
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
    
    grid::pt xy;
    bool r = grid::get().one_of_floor(xy);

    if (r) {
        ret.v.push_back((nanom::UInt)xy.first);
        ret.v.push_back((nanom::UInt)xy.second);
    }
    return r;
}

inline bool dg_grid_one_of_water(CALLBACK) {
    
    grid::pt xy;
    bool r = grid::get().one_of_water(xy);

    if (r) {
        ret.v.push_back((nanom::UInt)xy.first);
        ret.v.push_back((nanom::UInt)xy.second);
    }
    return r;
}

inline bool dg_grid_one_of_walk(CALLBACK) {
    
    grid::pt xy;
    bool r = grid::get().one_of_walk(xy);

    if (r) {
        ret.v.push_back((nanom::UInt)xy.first);
        ret.v.push_back((nanom::UInt)xy.second);
    }
    return r;
}

inline bool dg_neighbors_linked(CALLBACK) {
    
    ret.v.push_back((nanom::UInt)neighbors::get().linked(neighbors::pt(struc.v[0].uint, struc.v[1].uint),
                                                         neighbors::pt(struc.v[2].uint, struc.v[3].uint)));
    return true;
}

inline bool dg_current_moon(CALLBACK) {
    ret.v.push_back(metalan::symtab().get(moon::get().pi.phase_str));
    return true;
}

inline bool dg_render_message(CALLBACK) {
    grender::get().do_message(metalan::symtab().get(struc.v[0].uint), struc.v[1].uint);
    return true;
}

inline bool dg_render_path_walk(CALLBACK) {
    unsigned int xo;
    unsigned int yo;
    bool r = grender::get().path_walk(struc.v[0].uint, struc.v[1].uint,
                                      struc.v[2].uint, struc.v[3].uint,
                                      struc.v[4].uint, struc.v[5].uint,
                                      xo, yo);
    if (r) {
        ret.v.push_back((nanom::UInt)xo);
        ret.v.push_back((nanom::UInt)yo);
    }
    return r;
}

inline bool dg_render_push_hud_line_uint(CALLBACK) {
    const std::string& label = metalan::symtab().get(struc.v[0].uint);
    TCOD_color_t labelcolor = colorsyms::color(struc.v[1].uint);
    nanom::UInt npips = struc.v[2].uint;
    char style[2] = { metalan::symtab().get(struc.v[3].uint)[0], '\0'};
    TCOD_color_t cols[2]  = { colorsyms::color(struc.v[4].uint), TCOD_black };
       
    grender::get().push_hud_line(label, labelcolor, false, npips, style, cols);
    return true;
}

inline bool dg_render_push_hud_line_int(CALLBACK) {
    const std::string& label = metalan::symtab().get(struc.v[0].uint);
    TCOD_color_t labelcolor = colorsyms::color(struc.v[1].uint);
    nanom::Int npips = struc.v[2].inte;
    char style[2] = { metalan::symtab().get(struc.v[3].uint)[0], metalan::symtab().get(struc.v[4].uint)[0] };
    TCOD_color_t cols[2]  = { colorsyms::color(struc.v[5].uint), colorsyms::color(struc.v[6].uint) };
       
    grender::get().push_hud_line(label, labelcolor, true, npips, style, cols);
    return true;
}


inline bool dg_dist(CALLBACK) {
    nanom::UInt a = struc.v[0].uint, b = struc.v[1].uint, c = struc.v[2].uint, d = struc.v[3].uint;

    nanom::Int ac = ((nanom::Int)a - (nanom::Int)c);
    nanom::Int bd = ((nanom::Int)b - (nanom::Int)d);
    nanom::Real dist = sqrt((nanom::Real)(ac * ac) + (nanom::Real)(bd * bd));

    ret.v.push_back(dist);
    return true;
}

inline bool dg_upcase(CALLBACK) {
    const std::string& s = metalan::symtab().get(struc.v[0].uint);

    if (s.size() > 0) {
        std::string s2 = s;
        s2[0] = ::toupper(s2[0]);
        ret.v.push_back((nanom::UInt)metalan::symtab().get(s2));
    } else {
        ret.v.push_back(struc.v[0].uint);
    }
    return true;
}

inline bool dg_uint_to_char(CALLBACK) {
    ret.v.push_back(metalan::symtab().get(std::string(1, (unsigned char)struc.v[0].uint)));
    return true;
}


/*** ***/

struct window_buff {
    std::vector<std::string> data;
};

inline void __feed_void(window_buff& w, const nanom::Shapes& shapes, const nanom::Shape& shape, 
                        const nanom::Struct& struc) {
}

inline void dg_render_draw_window_feed(window_buff& w, const nanom::Shapes& shapes, const nanom::Shape& shape, 
                                       const nanom::Struct& struc) {

    w.data.push_back(metalan::symtab().get(struc.v[0].uint));
}

inline bool dg_render_draw_window(window_buff& w, const nanom::Shapes& shapes, const nanom::Shape& shapeto, 
                                  nanom::Struct& ret) {

    grender::Grid::keypress k = grender::get().draw_window(w.data);

    ret.v.push_back((nanom::UInt)k.vk);
    char cc[2] = { k.c, 0 };
    ret.v.push_back((nanom::Sym)metalan::symtab().get(cc));

    return true;
}

inline bool dg_render_draw_window_paste(CALLBACK) {

    window_buff& w = piccol::seqholder<window_buff>().top();
    const std::string& str = metalan::symtab().get(struc.v[0].uint);

    size_t oldi = 0;

    while (1) {
        size_t i = str.find('\n', oldi);

        if (i == std::string::npos) {
            w.data.push_back(str.substr(oldi));
            break;
        } else {
            w.data.push_back(str.substr(oldi, i-oldi));
            oldi = i + 1;
        }
    }
    return true;
}

inline bool dg_render_draw_splashscreen(CALLBACK) {

    const std::string& str = metalan::symtab().get(struc.v[2].uint);
    std::vector<std::string> lines;

    size_t oldi = 0;

    while (1) {
        size_t i = str.find('\n', oldi);

        if (i == std::string::npos) {
            lines.push_back(str.substr(oldi));
            break;
        } else {
            lines.push_back(str.substr(oldi, i-oldi));
            oldi = i + 1;
        }
    }
    
    grender::get().draw_splashscreen(struc.v[0].uint, struc.v[1].uint, lines);    

    return true;
}


struct Vm {

    piccol::Modules vm;

    Vm(const std::string& sysdir, 
       const std::string& appdir, bool verbose = false) : vm(sysdir, appdir, "game.modules", verbose) {

        piccol::register_map<FeatStock>(vm,    "Sym",           "Feat");
        piccol::register_map<PropStock>(vm,    "Sym",           "Props");
        piccol::register_map<FeatMap>(vm,      "[ UInt UInt ]", "Feat");

        piccol::register_map<MonsterStock>(vm,  "Sym",        "Monster");
        piccol::register_pool<MonsterStock>(vm, "MonsterKey", "Sym");

        piccol::register_map<MonsterMap>(vm,    "[ UInt UInt ]", "MonsterVal");

        piccol::register_map<MonsterMapScratch>(vm, "[ UInt UInt ]", "MonsterVal", "_scratch");

        piccol::register_map<ItemStock>(vm,  "Sym", "Item");
        piccol::register_pool<ItemStock>(vm, "ItemKey", "Sym");

        piccol::register_stack<ItemMap>(vm,    "[ UInt UInt ]", "ItemVal");

        piccol::register_map<Inventory>(vm, "Sym", "ItemVal");
            
        piccol::register_global<Player>(vm,  "Player");
        piccol::register_global<Dungeon>(vm, "Dungeon");

        //////

        vm.register_callback("dg_random_range", "[ Int Int ]", "Int", dg_random_range);
        vm.register_callback("dg_random_pos_gauss", "[ Real Real Real ]", "Real", dg_random_pos_gauss);
        vm.register_callback("dg_random_neg_gauss", "[ Real Real Real ]", "Real", dg_random_neg_gauss);
        vm.register_callback("dg_random_nat_pos_gauss", "[ Real Real Real UInt ]", "UInt", 
                             dg_random_nat_pos_gauss);
        vm.register_callback("dg_random_nat_neg_gauss", "[ Real Real Real UInt ]", "UInt", 
                             dg_random_nat_neg_gauss);

        vm.register_callback("dg_random_uniform",   "[ Real Real ]", "Real", dg_random_uniform);
        vm.register_callback("dg_random_geometric", "Real",          "UInt", dg_random_geometric);
        
        vm.register_callback("dg_render_set_is_lit",    "[ UInt UInt UInt Bool ]",  "Void", dg_render_set_is_lit);
        vm.register_callback("dg_render_set_back",      "[ UInt UInt UInt Sym ]",  "Void", dg_render_set_back);

        vm.register_callback("dg_render_set_is_viewblock", "[ UInt UInt UInt Bool ]", 
                             "Void", dg_render_set_is_viewblock);
        vm.register_callback("dg_render_set_is_walkblock", "[ UInt UInt UInt Bool ]", 
                             "Void", dg_render_set_is_walkblock);

        vm.register_callback("dg_render_is_viewblock", "[ UInt UInt ]", "Bool", dg_render_is_viewblock);
        vm.register_callback("dg_render_is_walkblock", "[ UInt UInt ]", "Bool", dg_render_is_walkblock);
        vm.register_callback("dg_render_is_valid",     "[ UInt UInt ]", "Bool", dg_render_is_valid);

        vm.register_callback("dg_render_set_skin", "[ UInt UInt UInt Skin ]", "Void", dg_render_set_skin);

        vm.register_callback("dg_render_set_env", "[ Sym Real ]", "Void", dg_render_set_env);

        vm.register_callback("dg_grid_set_walk",        "[ UInt UInt Bool ]", "Void", dg_grid_set_walk);
        vm.register_callback("dg_grid_set_water",       "[ UInt UInt Bool ]", "Void", dg_grid_set_water);
        vm.register_callback("dg_grid_set_height",      "[ UInt UInt Real ]", "Void", dg_grid_set_height);

        vm.register_callback("dg_grid_is_walk",    "[ UInt UInt ]", "Bool", dg_grid_is_walk);
        vm.register_callback("dg_grid_is_water",   "[ UInt UInt ]", "Bool", dg_grid_is_water);
        vm.register_callback("dg_grid_get_height", "[ UInt UInt ]", "Real", dg_grid_get_height);

        vm.register_callback("dg_grid_add_nogen",         "[ UInt UInt ]",      "Void", dg_grid_add_nogen);
        vm.register_callback("dg_grid_add_nogen_expand",  "[ UInt UInt UInt ]", "Void", dg_grid_add_nogen_expand);
       
        vm.register_callback("dg_grid_generate", "Int", "Void", dg_grid_generate);

        vm.register_callback("dg_grid_one_of_floor", "Void", "[ UInt UInt ]", dg_grid_one_of_floor);
        vm.register_callback("dg_grid_one_of_water", "Void", "[ UInt UInt ]", dg_grid_one_of_water);
        vm.register_callback("dg_grid_one_of_walk",  "Void", "[ UInt UInt ]", dg_grid_one_of_walk);

        vm.register_callback("dg_neighbors_linked", "[ UInt UInt UInt UInt ]", "Bool", dg_neighbors_linked);

        vm.register_callback("dg_current_moon", "Void", "Sym", dg_current_moon);

        vm.register_callback("dg_render_message", "[ Sym Bool ]", "Void", dg_render_message);

        vm.register_callback("dg_render_path_walk", 
                             "[ UInt UInt UInt UInt UInt UInt ]", "[ UInt UInt ]",
                             dg_render_path_walk);

        vm.register_callback("dg_render_push_hud_line", "IntHudLine",  "Void", dg_render_push_hud_line_int);
        vm.register_callback("dg_render_push_hud_line", "UIntHudLine", "Void", dg_render_push_hud_line_uint);

        vm.register_callback("dg_dist", "[ UInt UInt UInt UInt ]", "Real", dg_dist);
        vm.register_callback("dg_upcase", "Sym", "Sym", dg_upcase);
        vm.register_callback("dg_uint_to_char", "UInt", "Sym", dg_uint_to_char);

        vm.register_callback("dg_render_draw_window_paste",
                             "Sym", "Void", dg_render_draw_window_paste);

        vm.register_callback("dg_render_draw_splashscreen",
                             "[ UInt UInt Sym ]", "Void", dg_render_draw_splashscreen);

        piccol::register_sequencer<window_buff>(vm, "dg_render_draw_window")
            .feed("Sym", dg_render_draw_window_feed)
            .feed("Void", __feed_void)
            .end("[ Int Sym ]", dg_render_draw_window);

        piccol::register_fmt_sequencer(vm);
        piccol::register_print_sequencer(vm);

        ////// 

        vm.required("make_screen", "Void", "ScreenParams");
        vm.required("init", "Void", "Void");

        vm.required("remove_monster",     "[ [ UInt UInt ] MonsterVal ]", "Void");
        vm.required("move_monster",       "[ [ UInt UInt ] MonsterVal ]", "Void");

        vm.required("remove_item", "[ [ UInt UInt ] UInt ItemVal ]", "Void");
        vm.required("generate", "Void", "Void");
        vm.required("set_skin", "[ UInt UInt ]", "Void");
        vm.required("drawing_context", "Void", "DrawingContext");
        vm.required("handle_input", "InState", "OutState");
        vm.required("draw_hud", "Void", "Void");
        vm.required("process_world", "UInt", "OutState");

        vm.init();

        vm.check_type("ScreenParams",
                      {nanom::UINT, nanom::UINT, nanom::UINT, nanom::UINT, nanom::UINT, nanom::UINT,
                       nanom::SYMBOL, nanom::SYMBOL, nanom::BOOL});

        vm.check_type("Skin", 
                      {nanom::SYMBOL, nanom::SYMBOL, nanom::SYMBOL, nanom::BOOL, nanom::BOOL});

        vm.check_type("InState",
                      {nanom::UINT, nanom::INT, nanom::SYMBOL});

        vm.check_type("OutState",
                      {nanom::UINT, nanom::BOOL, nanom::BOOL, nanom::BOOL, nanom::BOOL, nanom::BOOL});

        vm.check_type("DrawingContext", 
                      {nanom::INT, nanom::INT,
                       nanom::UINT, nanom::UINT, nanom::UINT, nanom::UINT, nanom::UINT, nanom::UINT, nanom::UINT, 
                       nanom::BOOL });

        vm.check_type("IntHudLine", 
                      {nanom::SYMBOL, nanom::SYMBOL, nanom::INT,
                       nanom::SYMBOL, nanom::SYMBOL, nanom::SYMBOL, nanom::SYMBOL });

        vm.check_type("UIntHudLine", 
                      {nanom::SYMBOL, nanom::SYMBOL, nanom::UINT,
                       nanom::SYMBOL, nanom::SYMBOL });

    }        

    void run(const std::string& name, const std::string& from, const std::string& to, 
             const nanom::Struct& inp, nanom::Struct& out) {

        bool ret = vm.run(name, from, to, inp, out);
        if (!ret) {
            throw std::runtime_error("Calling " + name + " " + from + "->" + to + " failed");
        }
    }

    void make_screen(mainloop::screen_params_t& sp) {
        nanom::Struct out;
        nanom::Struct inp;

        run("make_screen", "Void", "ScreenParams", inp, out);

        sp.w = out.v[0].uint;
        sp.h = out.v[1].uint;
        sp.w2 = out.v[2].uint;
        sp.h2 = out.v[3].uint;
        sp.view_w = out.v[4].uint;
        sp.view_h = out.v[5].uint;
        sp.font = metalan::symtab().get(out.v[6].uint);
        sp.title = metalan::symtab().get(out.v[7].uint);
        sp.fullscreen = out.v[8].uint;
    }

    void init() {
        nanom::Struct out;
        nanom::Struct inp;
        run("init", "Void", "Void", inp, out);
    }

    void draw_hud() {
        nanom::Struct out;
        nanom::Struct inp;
        run("draw_hud", "Void", "Void", inp, out);
    }

    void generate() {
        nanom::Struct out;
        nanom::Struct inp;

        celauto::get().clear();
        grid::get().clear();
        neighbors::get().clear();
        grender::get().clear();

        forall_monsters("remove_monster");
        forall_items("remove_item");

        piccol::structmap<FeatMap>().clear();
        piccol::structmap<MonsterMap>().clear();
        piccol::structstack<ItemMap>().clear();

        run("generate", "Void", "Void", inp, out);
    }

    void set_skin(unsigned int x, unsigned int y) {
        nanom::Struct out;
        nanom::Struct inp;
        inp.v.push_back((nanom::UInt)x);
        inp.v.push_back((nanom::UInt)y);
        run("set_skin", "[ UInt UInt ]", "Void", inp, out);
    }

    void drawing_context(mainloop::drawing_context_t& ctx) {
        nanom::Struct out;
        nanom::Struct inp;

        run("drawing_context", "Void", "DrawingContext", inp, out);

        ctx.voff_x = out.v[0].inte;
        ctx.voff_y = out.v[1].inte;
        ctx.px = out.v[2].uint;
        ctx.py = out.v[3].uint;
        ctx.lightradius = out.v[4].uint;
        ctx.hlx = out.v[5].uint;
        ctx.hly = out.v[6].uint;
        ctx.rangemin = out.v[7].uint;
        ctx.rangemax = out.v[8].uint;
        ctx.do_hud = out.v[9].uint;
    }

    void handle_input(size_t& ticks, int vk, char c, bool& done, bool& dead, bool& regen, bool& redraw) {
        nanom::Struct out;
        nanom::Struct inp;
        inp.v.push_back((nanom::UInt)ticks);
        inp.v.push_back((nanom::Int)vk);
        char cc[2] = { c, 0 };
        inp.v.push_back((nanom::Sym)metalan::symtab().get(cc));

        run("handle_input", "InState", "OutState", inp, out);

        ticks = out.v[0].uint;
        done = out.v[1].uint;
        dead = out.v[2].uint;
        regen = out.v[3].uint;
        redraw = out.v[4].uint;
    }

    void process_world(size_t& ticks, bool& done, bool& dead, bool& need_input) {

        piccol::StructMap::map_t tmpmap;

        std::unordered_set<nanom::Struct> changed_coords;

        forall_monsters("move_monster");
        
        auto& mapm2 = piccol::structmap<MonsterMapScratch>().map;
        auto& mapm1 = piccol::structmap<MonsterMap>().map;

        for (const auto& kv : mapm1) {
            changed_coords.insert(kv.first);
        }

        for (const auto& kv : mapm2) {
            changed_coords.insert(kv.first);
        }

        mapm1.swap(mapm2);
        mapm2.clear();

        nanom::Struct out;

        for (const auto& k : changed_coords) {
            run("set_skin", "[ UInt UInt ]", "Void", k, out);
        }

        nanom::Struct inp;
        inp.v.push_back((nanom::UInt)ticks);

        run("process_world", "UInt", "OutState", inp, out);

        ticks = out.v[0].uint;
        done = out.v[1].uint;
        dead = out.v[2].uint;
        need_input = out.v[5].uint;
    }

    void forall_monsters(const std::string& func) {
        piccol::Struct tmp;

        piccol::structmap<MonsterMap>().set_readonly(true);

        for (const auto& kv : piccol::structmap<MonsterMap>().map) {
            piccol::Struct s;
            s.v.insert(s.v.end(), kv.first.v.begin(), kv.first.v.end());
            s.v.insert(s.v.end(), kv.second.v.begin(), kv.second.v.end());

            run(func, "[ [ UInt UInt ] MonsterVal ]", "Void", s, tmp);
        }

        piccol::structmap<MonsterMap>().set_readonly(false);
    }

    void forall_items(const std::string& func) {
        piccol::Struct tmp;

        for (const auto& kv : piccol::structstack<ItemMap>().map) {

            size_t n = kv.second.size()-1;

            for (const auto& v : kv.second) {
                piccol::Struct s;
                s.v.insert(s.v.end(), kv.first.v.begin(), kv.first.v.end());
                s.v.push_back((piccol::UInt)n);
                s.v.insert(s.v.end(), v.v.begin(), v.v.end());

                run(func, "[ [ UInt UInt ] UInt ItemVal ]", "Void", s, tmp);
                --n;
            }
        }
    }
    

    template <typename SINK>
    void save(SINK& s) {

        metalan::symtab().save(
            [&s](nanom::Sym sn, const std::string& ss) {
                serialize::write(s, sn);
                serialize::write(s, ss);
            }
            );

        serialize::write(s, piccol::structmap<FeatStock>().map);
        serialize::write(s, piccol::structmap<PropStock>().map);
        serialize::write(s, piccol::structmap<FeatMap>().map);
        serialize::write(s, piccol::structmap<MonsterStock>().map);
        serialize::write(s, piccol::structpool<MonsterStock>().map);
        serialize::write(s, piccol::structmap<MonsterMap>().map);
        serialize::write(s, piccol::structmap<ItemStock>().map);
        serialize::write(s, piccol::structpool<ItemStock>().map);
        serialize::write(s, piccol::structstack<ItemMap>().map);
        serialize::write(s, piccol::structmap<Inventory>().map);

        const piccol::GlobalStruct& p = piccol::globalstruct<Player>();
        const piccol::GlobalStruct& d = piccol::globalstruct<Dungeon>();

        serialize::write(s, p.init);
        serialize::write(s, p.obj);
        serialize::write(s, d.init);
        serialize::write(s, d.obj);
    }

    template <typename SOURCE>
    void load(SOURCE& s) {

        while (1) {
            nanom::Sym sn;
            std::string ss;
            serialize::read(s, sn);
            serialize::read(s, ss);

            if (!metalan::symtab().load(sn, ss))
                break;
        }

        serialize::read(s, piccol::structmap<FeatStock>().map);
        serialize::read(s, piccol::structmap<PropStock>().map);
        serialize::read(s, piccol::structmap<FeatMap>().map);
        serialize::read(s, piccol::structmap<MonsterStock>().map);
        serialize::read(s, piccol::structpool<MonsterStock>().map);
        serialize::read(s, piccol::structmap<MonsterMap>().map);
        serialize::read(s, piccol::structmap<ItemStock>().map);
        serialize::read(s, piccol::structpool<ItemStock>().map);
        serialize::read(s, piccol::structstack<ItemMap>().map);
        serialize::read(s, piccol::structmap<Inventory>().map);

        piccol::GlobalStruct& p = piccol::globalstruct<Player>();
        piccol::GlobalStruct& d = piccol::globalstruct<Dungeon>();

        serialize::read(s, p.init);
        serialize::read(s, p.obj);
        serialize::read(s, d.init);
        serialize::read(s, d.obj);
    }

};


}

#undef CALLBACK

#endif

