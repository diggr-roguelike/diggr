#ifndef __RENDER_H
#define __RENDER_H

#include <math.h>
#include <stdlib.h>

#include "celauto.h"

#include "libtcod.h"

#include <iostream>


namespace serialize {

template <>
struct reader<TCOD_color_t> {
    void read(Source& s, TCOD_color_t& v) {
	reader<unsigned char>().read(s, v.r);
	reader<unsigned char>().read(s, v.g);
	reader<unsigned char>().read(s, v.b);
    }
};

template <>
struct writer<TCOD_color_t> {
    void write(Sink& s, const TCOD_color_t& v) {
	writer<unsigned char>().write(s, v.r);
	writer<unsigned char>().write(s, v.g);
	writer<unsigned char>().write(s, v.b);
    }
};

}


namespace grender {


/*
struct benchmark {
    timeval ts;
    timeval te;
    benchmark() {}
    void start() {
	gettimeofday(&ts, NULL);
    }
    double end() {
	gettimeofday(&te, NULL);
	return (double)((te.tv_sec*1000000+te.tv_usec) - (ts.tv_sec*1000000+ts.tv_usec)) / 1e6;
    }
};
*/

struct Grid {

    struct skin {
	TCOD_color_t fore;
	unsigned char c;
	TCOD_color_t fore2;
	int fore_interp;
	bool is_terrain;

	skin() : c(' '), fore_interp(0), is_terrain(false)
	    {
		fore = TCOD_black;
	    }

	skin(const TCOD_color_t& _fore, unsigned char _c,
	     const TCOD_color_t& _fore2, int _fore_interp, bool _is_terrain) :
	    fore(_fore), c(_c), fore2(_fore2), fore_interp(_fore_interp), 
	    is_terrain(_is_terrain) {}
	     
    };

    struct gridpoint {
	std::vector<skin> skins;
	TCOD_color_t back;
	unsigned int is_lit;
	bool in_fov;
        bool is_transparent;

	gridpoint() : back(TCOD_black), is_lit(0), in_fov(false), is_transparent(false) {}
    };

    struct keypress {
        int vk;
        char c;
        keypress(int _vk=0, char _c=0) : vk(_vk), c(_c) {}
    };

    unsigned int w;
    unsigned int h;

    std::vector<gridpoint> grid;

    TCOD_color_t env_color;
    double env_intensity;

    TCOD_map_t tcodmap;

    std::string font;
    std::string title;
    bool fullscreen;
    bool has_console;

    std::vector<keypress> keylog;


    Grid() : w(0), h(0), env_intensity(0), 
             tcodmap(TCOD_map_new(0, 0)), 
             fullscreen(false), has_console(false)
        {}

    ~Grid() {
        TCOD_map_delete(tcodmap);
    }

    void init(unsigned int _w, unsigned int _h, 
              const std::string& _font, const std::string& _title, bool _fullscreen) {

        bool do_console = false;

        if (w != _w || h != _h) {

            w = _w;
            h = _h;

            grid.clear();
            grid.resize(w*h);

            TCOD_map_delete(tcodmap);
            tcodmap = TCOD_map_new(w, h);
            TCOD_map_clear(tcodmap, false, false);

            do_console = true;
        }

        if (font != _font || !has_console || do_console) {

            font = _font;
            title = _title;
            fullscreen = _fullscreen;

            if (has_console) {
                TCOD_console_delete(NULL);
            }

            TCOD_console_set_custom_font(font.c_str(), 
                                         TCOD_FONT_TYPE_GREYSCALE | TCOD_FONT_LAYOUT_ASCII_INROW, 0, 0);
            TCOD_console_init_root(w, h, title.c_str(), fullscreen, TCOD_RENDERER_SDL);
            TCOD_sys_set_fps(30);
            
            TCOD_console_set_color_control(TCOD_COLCTRL_1, TCOD_white, TCOD_black);
            TCOD_console_set_color_control(TCOD_COLCTRL_2, TCOD_darker_green, TCOD_black);
            TCOD_console_set_color_control(TCOD_COLCTRL_3, TCOD_yellow, TCOD_black);
            TCOD_console_set_color_control(TCOD_COLCTRL_4, TCOD_red, TCOD_black);
            TCOD_console_set_color_control(TCOD_COLCTRL_5, TCOD_gray, TCOD_black);

            has_console = true;

            return;
        }

        if (fullscreen != _fullscreen) {
            fullscreen = _fullscreen;
            TCOD_console_set_fullscreen(fullscreen);
        }

        if (title != _title) {
            title = _title;
            TCOD_console_set_window_title(title.c_str());
        }
    }

    void clear() {
        grid.clear();
        grid.resize(w*h);
        TCOD_map_clear(tcodmap, false, false);
    }


    gridpoint& _get(unsigned int x, unsigned int y) {
	return grid[y*w+x];
    }

    void set_env(const TCOD_color_t& color, double intensity) {
	env_color = color;
	env_intensity = intensity;
    }

    void set_back(unsigned int x, unsigned int y, const TCOD_color_t& color) {
	_get(x,y).back = color;
    }

    void set_is_lit(unsigned int x, unsigned int y, bool is_lit) {
	unsigned int& il = _get(x,y).is_lit;

	if (!is_lit) {
	    if (il > 0) --il;
	} else {
	    ++il;
	}
    }

    void set_transparent(unsigned int x, unsigned int y, bool t) {
	_get(x,y).is_transparent = t;
        TCOD_map_set_properties(tcodmap, x, y, t, t);
    }

    void push_skin(unsigned int x, unsigned int y,
		   const TCOD_color_t& fore, unsigned char c,
		   const TCOD_color_t& fore2, int fore_interp,
		   bool is_terrain) {

	std::vector<skin>& skins = _get(x,y).skins; 

	skins.emplace_back(fore, c, fore2, fore_interp, is_terrain);
    }

    void set_skin(unsigned int x, unsigned int y,
		  TCOD_color_t fore, unsigned char c,
		  TCOD_color_t fore2, int fore_interp,
		  bool is_terrain) {

	std::vector<skin>& skins = _get(x,y).skins; 

	if (skins.size() == 0) {
	    skins.emplace_back(fore, c, fore2, fore_interp, is_terrain);
	} else {
	    skin& sk = skins.back();
	    sk = skin(fore, c, fore2, fore_interp, is_terrain);
	}
    }

    void pop_skin(unsigned int x, unsigned int y) {
	std::vector<skin>& skins = _get(x,y).skins;

	if (skins.size() > 0)
	    skins.pop_back();
    }


    bool is_in_fov(unsigned int x, unsigned int y) {
        const gridpoint& gp = _get(x,y);
        return (gp.in_fov || gp.is_lit > 0);
    }


    bool draw(unsigned int t,
	      unsigned int px, unsigned int py,
	      unsigned int hlx, unsigned int hly,
	      unsigned int rangemin, unsigned int rangemax,
	      unsigned int lightradius) {

	static double _sparkleinterp[10];
	static bool did_init = false;
	static double pi = 3.14159265358979323846;

	if (!did_init) {
	    for (int i = 0; i < 10; ++i) {
		_sparkleinterp[i] = pow(sin(i/pi), 2);
	    }
	    did_init = true;
	}

	bool ret = false;

	TCOD_map_compute_fov(tcodmap, px, py, lightradius, true, FOV_SHADOW);

	for (int y = 0; y < h; ++y) {
	    for (int x = 0; x < w; ++x) {

		bool in_fov = TCOD_map_is_in_fov(tcodmap, x, y);

		unsigned int tmpx = abs(x - px);
		unsigned int tmpy = abs(y - py);
		double d = sqrt(tmpx*tmpx + tmpy*tmpy);

		gridpoint& gp = _get(x,y);
		const std::vector<skin>& skins = gp.skins;

		gp.in_fov = in_fov;

		if (skins.size() == 0) {
		    continue;
		}

		const skin& sk = skins.back();

		TCOD_color_t fore = sk.fore;
		TCOD_color_t back = gp.back;
		unsigned char c = sk.c;

		if (sk.fore_interp) {
                    double i = _sparkleinterp[(x * y + t) % 10];
		    fore = TCOD_color_lerp(fore, sk.fore2, i);
		}

		size_t caid;
		unsigned int caage;
		celauto::get().get_state(celauto::pt(x,y), caid, caage);

		if (caid) {
		    unsigned int maxage = celauto::get().rules[caid]->age;
		    double intrp = (double)caage / (maxage*2.0);
		    back = TCOD_color_lerp(back, TCOD_black, intrp);
		}

		if (gp.is_lit == 0) {

		    if (!in_fov) {
			back = TCOD_black;
			fore = TCOD_black;
			c = ' ';

		    } else {

			double d1 = d/lightradius;

			if (d < rangemin || d > rangemax) {
			    fore = TCOD_darkest_gray;
			    back = TCOD_black;

			} else {
			    if (sk.is_terrain) {
				fore = TCOD_color_lerp(TCOD_white, fore, std::min(d1*2.0, 1.0));
			    }

			    fore = TCOD_color_lerp(fore, TCOD_black, std::min(d1, 1.0));

			    if (env_intensity > 0) {
				fore = TCOD_color_lerp(env_color, fore, env_intensity);
			    }

			    back = TCOD_color_lerp(back, TCOD_black, std::min(d1, 1.0));
			}
		    }
		}

		if (x == hlx && y == hly) {
		    back = TCOD_white;

		    if (in_fov || gp.is_lit > 0) {
			ret = true;
		    }
		}

		TCOD_console_put_char_ex(NULL, x, y, c, fore, back);
	    }
	}

	return ret;
    }

    void wait_for_anykey() {
        TCOD_console_flush();
        TCOD_sys_wait_for_event(TCOD_EVENT_KEY_PRESS, NULL, NULL, true);
    }

    void skip_input(unsigned int delay=0) {
        TCOD_console_flush();

        if (delay != 0) {
            TCOD_sys_sleep_milli(delay);
        }

        TCOD_sys_check_for_event(TCOD_EVENT_KEY_PRESS, NULL, NULL);
    }

    keypress wait_for_key() {
        TCOD_console_flush();

        if (TCOD_console_is_window_closed()) {
            keypress ret(0, 1);
            keylog.push_back(ret);
            return ret;
        }


        TCOD_key_t ktmp;

        while (1) {
            TCOD_sys_wait_for_event(TCOD_EVENT_KEY_PRESS, &ktmp, NULL, false);
            if (ktmp.vk == TCODK_SHIFT ||
                ktmp.vk == TCODK_ALT ||
                ktmp.vk == TCODK_CONTROL)
                continue;
            break;
        }

        keypress ret(ktmp.vk, ktmp.c);
        keylog.push_back(ret);
        return ret;
    }


    void recompute_fov(unsigned int x, unsigned int y, unsigned int radius) {

	TCOD_map_compute_fov(tcodmap, x, y, radius, false, FOV_SHADOW);

	for (int y = 0; y < h; ++y) {
	    for (int x = 0; x < w; ++x) {

		bool in_fov = TCOD_map_is_in_fov(tcodmap, x, y);
		gridpoint& gp = _get(x,y);

                gp.in_fov = in_fov;
            }
        }
    }


    //***  ***//

    inline void write(serialize::Sink& s) {
	serialize::write(s, w);
	serialize::write(s, h);

        serialize::write(s, font);
        serialize::write(s, title);
        serialize::write(s, fullscreen);

	serialize::write(s, env_color);
	serialize::write(s, env_intensity);

        for (const auto& t : grid) {

            serialize::write(s, t.skins.size());
	    for (const auto& u : t.skins) {
		serialize::write(s, u.fore);
		serialize::write(s, u.c);
		serialize::write(s, u.fore2);
		serialize::write(s, u.fore_interp);
		serialize::write(s, u.is_terrain);
	    }

            serialize::write(s, t.back);
            serialize::write(s, t.is_lit);
            serialize::write(s, t.in_fov);
            serialize::write(s, t.is_transparent);
        }

	serialize::write(s, keylog.size());
        for (const auto& k : keylog) {
            serialize::write(s, k.vk);
            serialize::write(s, k.c);
        }
    }

    inline void read(serialize::Source& s) {
        unsigned int _w;
        unsigned int _h;

        serialize::read(s, _w);
        serialize::read(s, _h);

        serialize::read(s, font);
        serialize::read(s, title);
        serialize::read(s, fullscreen);
        has_console = false;

	serialize::read(s, env_color);
	serialize::read(s, env_intensity);

        init(_w, _h, font, title, fullscreen);

	for (size_t i = 0; i < grid.size(); ++i) {
	    size_t sks;
            serialize::read(s, sks);

	    gridpoint& p = grid[i];

	    p.skins.resize(sks);

	    for (size_t j = 0; j < sks; ++j) {
		skin& tmp = p.skins[j];
		serialize::read(s, tmp.fore);
		serialize::read(s, tmp.c);
		serialize::read(s, tmp.fore2);
		serialize::read(s, tmp.fore_interp);
		serialize::read(s, tmp.is_terrain);
	    }

            serialize::read(s, p.back);
            serialize::read(s, p.is_lit);
            serialize::read(s, p.in_fov);
            serialize::read(s, p.is_transparent);

            TCOD_map_set_properties(tcodmap, i % w, i / w, p.is_transparent, p.is_transparent);
        }

        size_t keylog_size;
	serialize::read(s, keylog_size);

        keylog.resize(keylog_size);

        for (size_t i = 0; i < keylog_size; ++i) {
            keypress& k = keylog[i];
            serialize::read(s, k.vk);
            serialize::read(s, k.c);
        }
    }

};


inline Grid& get() {
    static Grid ret;
    return ret;
}

}


#endif
