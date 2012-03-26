#ifndef __COLORSYMS_H
#define __COLORSYMS_H

namespace colorsyms {

struct ColorSyms {

    std::unordered_map<Sym,TCOD_color_t> colors;

    void add(const std::string& s, const TCOD_color_t& c) {
        colors[metalan::symtab().get(s)] = c;
    }

    const TCOD_color_t& get(Sym s) {
        auto i = colors.find(s);
        if (i == colors.end())
            throw std::runtime_error("Undefined color: " + metalan::symtab().get(s));
        return i->second;
    }

    ColorSyms() {
        add("black", TCOD_black);
        add("darkest_grey", TCOD_darkest_grey);
        add("darker_grey", TCOD_darker_grey);
        add("dark_grey", TCOD_dark_grey);
        add("grey", TCOD_grey);
        add("light_grey", TCOD_light_grey);
        add("lighter_grey", TCOD_lighter_grey);
        add("lightest_grey", TCOD_lightest_grey);
        add("darkest_gray", TCOD_darkest_gray);
        add("darker_gray", TCOD_darker_gray);
        add("dark_gray", TCOD_dark_gray);
        add("gray", TCOD_gray);
        add("light_gray", TCOD_light_gray);
        add("lighter_gray", TCOD_lighter_gray);
        add("lightest_gray", TCOD_lightest_gray);
        add("white", TCOD_white);
        add("darkest_sepia", TCOD_darkest_sepia);
        add("darker_sepia", TCOD_darker_sepia);
        add("dark_sepia", TCOD_dark_sepia);
        add("sepia", TCOD_sepia);
        add("light_sepia", TCOD_light_sepia);
        add("lighter_sepia", TCOD_lighter_sepia);
        add("lightest_sepia", TCOD_lightest_sepia);
        add("red", TCOD_red);
        add("flame", TCOD_flame);
        add("orange", TCOD_orange);
        add("amber", TCOD_amber);
        add("yellow", TCOD_yellow);
        add("lime", TCOD_lime);
        add("chartreuse", TCOD_chartreuse);
        add("green", TCOD_green);
        add("sea", TCOD_sea);
        add("turquoise", TCOD_turquoise);
        add("cyan", TCOD_cyan);
        add("sky", TCOD_sky);
        add("azure", TCOD_azure);
        add("blue", TCOD_blue);
        add("han", TCOD_han);
        add("violet", TCOD_violet);
        add("purple", TCOD_purple);
        add("fuchsia", TCOD_fuchsia);
        add("magenta", TCOD_magenta);
        add("pink", TCOD_pink);
        add("crimson", TCOD_crimson);
        add("dark_red", TCOD_dark_red);
        add("dark_flame", TCOD_dark_flame);
        add("dark_orange", TCOD_dark_orange);
        add("dark_amber", TCOD_dark_amber);
        add("dark_yellow", TCOD_dark_yellow);
        add("dark_lime", TCOD_dark_lime);
        add("dark_chartreuse", TCOD_dark_chartreuse);
        add("dark_green", TCOD_dark_green);
        add("dark_sea", TCOD_dark_sea);
        add("dark_turquoise", TCOD_dark_turquoise);
        add("dark_cyan", TCOD_dark_cyan);
        add("dark_sky", TCOD_dark_sky);
        add("dark_azure", TCOD_dark_azure);
        add("dark_blue", TCOD_dark_blue);
        add("dark_han", TCOD_dark_han);
        add("dark_violet", TCOD_dark_violet);
        add("dark_purple", TCOD_dark_purple);
        add("dark_fuchsia", TCOD_dark_fuchsia);
        add("dark_magenta", TCOD_dark_magenta);
        add("dark_pink", TCOD_dark_pink);
        add("dark_crimson", TCOD_dark_crimson);
        add("darker_red", TCOD_darker_red);
        add("darker_flame", TCOD_darker_flame);
        add("darker_orange", TCOD_darker_orange);
        add("darker_amber", TCOD_darker_amber);
        add("darker_yellow", TCOD_darker_yellow);
        add("darker_lime", TCOD_darker_lime);
        add("darker_chartreuse", TCOD_darker_chartreuse);
        add("darker_green", TCOD_darker_green);
        add("darker_sea", TCOD_darker_sea);
        add("darker_turquoise", TCOD_darker_turquoise);
        add("darker_cyan", TCOD_darker_cyan);
        add("darker_sky", TCOD_darker_sky);
        add("darker_azure", TCOD_darker_azure);
        add("darker_blue", TCOD_darker_blue);
        add("darker_han", TCOD_darker_han);
        add("darker_violet", TCOD_darker_violet);
        add("darker_purple", TCOD_darker_purple);
        add("darker_fuchsia", TCOD_darker_fuchsia);
        add("darker_magenta", TCOD_darker_magenta);
        add("darker_pink", TCOD_darker_pink);
        add("darker_crimson", TCOD_darker_crimson);
        add("darkest_red", TCOD_darkest_red);
        add("darkest_flame", TCOD_darkest_flame);
        add("darkest_orange", TCOD_darkest_orange);
        add("darkest_amber", TCOD_darkest_amber);
        add("darkest_yellow", TCOD_darkest_yellow);
        add("darkest_lime", TCOD_darkest_lime);
        add("darkest_chartreuse", TCOD_darkest_chartreuse);
        add("darkest_green", TCOD_darkest_green);
        add("darkest_sea", TCOD_darkest_sea);
        add("darkest_turquoise", TCOD_darkest_turquoise);
        add("darkest_cyan", TCOD_darkest_cyan);
        add("darkest_sky", TCOD_darkest_sky);
        add("darkest_azure", TCOD_darkest_azure);
        add("darkest_blue", TCOD_darkest_blue);
        add("darkest_han", TCOD_darkest_han);
        add("darkest_violet", TCOD_darkest_violet);
        add("darkest_purple", TCOD_darkest_purple);
        add("darkest_fuchsia", TCOD_darkest_fuchsia);
        add("darkest_magenta", TCOD_darkest_magenta);
        add("darkest_pink", TCOD_darkest_pink);
        add("darkest_crimson", TCOD_darkest_crimson);
        add("light_red", TCOD_light_red);
        add("light_flame", TCOD_light_flame);
        add("light_orange", TCOD_light_orange);
        add("light_amber", TCOD_light_amber);
        add("light_yellow", TCOD_light_yellow);
        add("light_lime", TCOD_light_lime);
        add("light_chartreuse", TCOD_light_chartreuse);
        add("light_green", TCOD_light_green);
        add("light_sea", TCOD_light_sea);
        add("light_turquoise", TCOD_light_turquoise);
        add("light_cyan", TCOD_light_cyan);
        add("light_sky", TCOD_light_sky);
        add("light_azure", TCOD_light_azure);
        add("light_blue", TCOD_light_blue);
        add("light_han", TCOD_light_han);
        add("light_violet", TCOD_light_violet);
        add("light_purple", TCOD_light_purple);
        add("light_fuchsia", TCOD_light_fuchsia);
        add("light_magenta", TCOD_light_magenta);
        add("light_pink", TCOD_light_pink);
        add("light_crimson", TCOD_light_crimson);
        add("lighter_red", TCOD_lighter_red);
        add("lighter_flame", TCOD_lighter_flame);
        add("lighter_orange", TCOD_lighter_orange);
        add("lighter_amber", TCOD_lighter_amber);
        add("lighter_yellow", TCOD_lighter_yellow);
        add("lighter_lime", TCOD_lighter_lime);
        add("lighter_chartreuse", TCOD_lighter_chartreuse);
        add("lighter_green", TCOD_lighter_green);
        add("lighter_sea", TCOD_lighter_sea);
        add("lighter_turquoise", TCOD_lighter_turquoise);
        add("lighter_cyan", TCOD_lighter_cyan);
        add("lighter_sky", TCOD_lighter_sky);
        add("lighter_azure", TCOD_lighter_azure);
        add("lighter_blue", TCOD_lighter_blue);
        add("lighter_han", TCOD_lighter_han);
        add("lighter_violet", TCOD_lighter_violet);
        add("lighter_purple", TCOD_lighter_purple);
        add("lighter_fuchsia", TCOD_lighter_fuchsia);
        add("lighter_magenta", TCOD_lighter_magenta);
        add("lighter_pink", TCOD_lighter_pink);
        add("lighter_crimson", TCOD_lighter_crimson);
        add("lightest_red", TCOD_lightest_red);
        add("lightest_flame", TCOD_lightest_flame);
        add("lightest_orange", TCOD_lightest_orange);
        add("lightest_amber", TCOD_lightest_amber);
        add("lightest_yellow", TCOD_lightest_yellow);
        add("lightest_lime", TCOD_lightest_lime);
        add("lightest_chartreuse", TCOD_lightest_chartreuse);
        add("lightest_green", TCOD_lightest_green);
        add("lightest_sea", TCOD_lightest_sea);
        add("lightest_turquoise", TCOD_lightest_turquoise);
        add("lightest_cyan", TCOD_lightest_cyan);
        add("lightest_sky", TCOD_lightest_sky);
        add("lightest_azure", TCOD_lightest_azure);
        add("lightest_blue", TCOD_lightest_blue);
        add("lightest_han", TCOD_lightest_han);
        add("lightest_violet", TCOD_lightest_violet);
        add("lightest_purple", TCOD_lightest_purple);
        add("lightest_fuchsia", TCOD_lightest_fuchsia);
        add("lightest_magenta", TCOD_lightest_magenta);
        add("lightest_pink", TCOD_lightest_pink);
        add("lightest_crimson", TCOD_lightest_crimson);
        add("desaturated_red", TCOD_desaturated_red);
        add("desaturated_flame", TCOD_desaturated_flame);
        add("desaturated_orange", TCOD_desaturated_orange);
        add("desaturated_amber", TCOD_desaturated_amber);
        add("desaturated_yellow", TCOD_desaturated_yellow);
        add("desaturated_lime", TCOD_desaturated_lime);
        add("desaturated_chartreuse", TCOD_desaturated_chartreuse);
        add("desaturated_green", TCOD_desaturated_green);
        add("desaturated_sea", TCOD_desaturated_sea);
        add("desaturated_turquoise", TCOD_desaturated_turquoise);
        add("desaturated_cyan", TCOD_desaturated_cyan);
        add("desaturated_sky", TCOD_desaturated_sky);
        add("desaturated_azure", TCOD_desaturated_azure);
        add("desaturated_blue", TCOD_desaturated_blue);
        add("desaturated_han", TCOD_desaturated_han);
        add("desaturated_violet", TCOD_desaturated_violet);
        add("desaturated_purple", TCOD_desaturated_purple);
        add("desaturated_fuchsia", TCOD_desaturated_fuchsia);
        add("desaturated_magenta", TCOD_desaturated_magenta);
        add("desaturated_pink", TCOD_desaturated_pink);
        add("desaturated_crimson", TCOD_desaturated_crimson);
        add("brass", TCOD_brass);
        add("copper", TCOD_copper);
        add("gold", TCOD_gold);
        add("silver", TCOD_silver);
        add("celadon", TCOD_celadon);
        add("peach", TCOD_peach);
    }
};

inline const TCOD_color_t& color(Sym s) {
    static ColorSyms ret;
    return ret.get(s);
}

}


#endif
