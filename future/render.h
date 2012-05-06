#ifndef __RENDER_H
#define __RENDER_H

#include <math.h>
#include <stdlib.h>

#include <list>
#include <stdexcept>

#include "celauto.h"

#include "libtcod.h"

#include <iostream>
#include <sys/time.h>


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


typedef std::pair<unsigned int, unsigned int> pt;


struct Grid {

    static const size_t replay_delay = 100;

    static const size_t skincount = 8;


    struct skin {
	TCOD_color_t fore;
	TCOD_color_t back;
	unsigned char c;
	TCOD_color_t fore2;
	int fore_interp;
	bool is_terrain;

	skin() : back(TCOD_black), c(0), fore_interp(0), is_terrain(false)
	    {
		fore = TCOD_black;
	    }

	skin(const TCOD_color_t& _fore, unsigned char _c,
	     const TCOD_color_t& _fore2, int _fore_interp, bool _is_terrain) :
	    fore(_fore), back(TCOD_black), c(_c), fore2(_fore2), fore_interp(_fore_interp), 
	    is_terrain(_is_terrain) {}
	     
    };

    struct gridpoint {
	std::vector<skin> skins;
	unsigned int is_lit;
	bool in_fov;
        unsigned int is_viewblock;
        unsigned int is_walkblock;

	gridpoint() : is_lit(0), in_fov(false), 
                      is_viewblock(0), is_walkblock(0) 
            {
                skins.resize(skincount);
            }
    };

    struct keypress {
        int vk;
        char c;
        keypress(int _vk=0, char _c=0) : vk(_vk), c(_c) {}
    };

    struct message {
        std::string text;
        bool important;
        unsigned int timestamp;

        message(const std::string& t = "", bool i = false, unsigned int ts = 0) :
            text(t), important(i), timestamp(ts) {}
    };

    struct hud_line {
        std::string label;
        TCOD_color_t labelcolor;
        enum numtype_t { SIGNED, UNSIGNED };
        numtype_t numtype;
        int npips;
        char pipstyle[2];
        TCOD_color_t pipcolor[2];

        hud_line(const std::string& l, TCOD_color_t lc,
                 numtype_t nt, int np,
                 char s[2],
                 TCOD_color_t c[2]) : 
            label(l), labelcolor(lc), numtype(nt), npips(np)
            {
                pipstyle[0] = s[0];
                pipstyle[1] = s[1];
                pipcolor[0] = c[0];
                pipcolor[1] = c[1];

                uint8 o1 = 1;

                labelcolor.r = std::max(labelcolor.r, o1);
                labelcolor.g = std::max(labelcolor.g, o1);
                labelcolor.b = std::max(labelcolor.b, o1);
                pipcolor[0].r = std::max(pipcolor[0].r, o1);
                pipcolor[0].g = std::max(pipcolor[0].g, o1);
                pipcolor[0].b = std::max(pipcolor[0].b, o1);
                pipcolor[1].r = std::max(pipcolor[1].r, o1);
                pipcolor[1].g = std::max(pipcolor[1].g, o1);
                pipcolor[1].b = std::max(pipcolor[1].b, o1);
            }
    };

    unsigned int w;
    unsigned int h;

    unsigned int view_w;
    unsigned int view_h;

    std::vector<gridpoint> grid;

    TCOD_color_t env_color;
    double env_intensity;

    // transient, not saved in dump.
    TCOD_map_t tcodmap;
    TCOD_path_t tcodpath;

    std::string font;
    std::string title;
    bool fullscreen;

    // transient, not saved in dump.
    bool has_console;

    std::vector<keypress> keylog;

    std::list<message> messages;

    // transient, not saved in dump.
    std::vector<hud_line> hud_pips;

    // transient, not saved in dump.
    bool keylog_do_replay;
    size_t keylog_index;

private:

    double _dist(const pt& a, const pt& b) {

        unsigned int dx = abs(a.first - b.first);
        unsigned int dy = abs(a.second - b.second);
        return sqrt(dx*dx + dy*dy);
    }

    bool _translate_v2g(int voff_x, int voff_y, const pt& vxy, pt& gxy) {

        int rx = (int)vxy.first + voff_x;
        int ry = (int)vxy.second + voff_y;

        if (rx < 0 || (unsigned int)rx >= w || ry < 0 || (unsigned int)ry >= h)
            return false;

        gxy.first = (unsigned int)rx;
        gxy.second = (unsigned int)ry;
        return true;
    }

    bool _translate_g2v(int voff_x, int voff_y, const pt& gxy, pt& vxy) {

        int rx = (int)gxy.first - voff_x;
        int ry = (int)gxy.second - voff_y;
        
        if (rx < 0 || (unsigned int)rx >= view_w || ry < 0 || (unsigned int)ry >= view_h)
            return false;
        
        vxy.first = (unsigned int)rx;
        vxy.second = (unsigned int)ry;
        return true;
    }



    template <typename FUNC1, typename FUNC2>
    void _draw_circle(int voff_x, int voff_y,
                      unsigned int x, unsigned int y, unsigned int r, 
                      bool do_draw, TCOD_color_t fore, TCOD_color_t back, 
                      FUNC1 f_chk, FUNC2 f_do) {

        unsigned int x0 = (x < r ? 0 : x - r);
        unsigned int y0 = (y < r ? 0 : y - r);

        unsigned int x1 = std::min(x + r + 1, w);
        unsigned int y1 = std::min(y + r + 1, h);

        std::vector<pt> pts;

        for (unsigned int _x = x0; _x < x1; ++_x) {
            for (unsigned int _y = y0; _y < y1; ++_y) {

                pt _xy(_x, _y);

                double d = _dist(pt(x,y), _xy);

                if (d <= r && f_chk(_x, _y)) {
                    pts.push_back(_xy);
                }
            }
        }

        if (do_draw) {
        
            std::vector<TCOD_color_t> cols;

            cols.push_back(fore);
            cols.push_back(TCOD_color_lerp(cols.back(), back, 0.5));
            cols.push_back(TCOD_color_lerp(cols.back(), back, 0.5));

            for (const auto& col : cols) {
                for (const auto& xy : pts) {

                    pt vxy;
                    if (!_translate_g2v(voff_x, voff_y, xy, vxy))
                        continue;

                    TCOD_console_put_char_ex(NULL, vxy.first, vxy.second, '*', col, back);
                }
                TCOD_console_flush();
                TCOD_sys_sleep_milli(100);
            }
        }

        for (const auto& xy : pts) {
            f_do(xy.first, xy.second);
        }
    }


    void _draw_messages(unsigned int x, unsigned int y, unsigned int t) {

        int i = 0;
        std::string m;
        auto li = messages.begin();

        while (i < 3 && li != messages.end()) {

            if (li != messages.begin())
                m += '\n';

            if (li->timestamp == 0 || li->timestamp >= t) {
                m += (char)(li->important ? TCOD_COLCTRL_3 : TCOD_COLCTRL_1);
                li->timestamp = t;

            } else {
                m += (char)TCOD_COLCTRL_5;
            }

            m += li->text;
            ++i;
            ++li;
        }

        TCOD_console_print_rect(NULL, x, y, TCOD_console_get_width(NULL) - 30, 3, m.c_str());
    } 


    void _draw_pipline(unsigned int x, unsigned int y, const hud_line& line) {

        std::string l;

        l += (char)TCOD_COLCTRL_FORE_RGB;
        l += (char)line.labelcolor.r;
        l += (char)line.labelcolor.g;
        l += (char)line.labelcolor.b;
        
        if (line.label.size() < 6)
            l += std::string(6 - line.label.size(), ' ');

        l += line.label;
        l += ": ";

        if (line.numtype == hud_line::UNSIGNED) {
            l += (char)TCOD_COLCTRL_FORE_RGB;
            l += (char)line.pipcolor[0].r;
            l += (char)line.pipcolor[0].g;
            l += (char)line.pipcolor[0].b;
            l += std::string(line.npips, line.pipstyle[0]);

        } else {
            if (line.npips < 0) {

                l += (char)TCOD_COLCTRL_FORE_RGB;
                l += (char)line.pipcolor[0].r;
                l += (char)line.pipcolor[0].g;
                l += (char)line.pipcolor[0].b;

                if (line.npips > -3) {
                    l += std::string(line.npips + 3, ' ');
                }
                l += std::string(-line.npips, line.pipstyle[0]);

            } else {
                l += (char)TCOD_COLCTRL_FORE_RGB;
                l += (char)line.pipcolor[1].r;
                l += (char)line.pipcolor[1].g;
                l += (char)line.pipcolor[1].b;

                l += "   ";
                l += std::string(line.npips, line.pipstyle[1]);
            }
        }

        TCOD_console_print(NULL, x, y, l.c_str());
    }


public:

    Grid() : w(0), h(0), view_w(w), view_h(h),
             env_intensity(0), 
             tcodmap(TCOD_map_new(0, 0)), 
             tcodpath(TCOD_path_new_using_map(tcodmap, 1.41)),
             fullscreen(false), has_console(false), 
             keylog_do_replay(false), keylog_index(0)
        {}

    ~Grid() {
        TCOD_map_delete(tcodmap);
        TCOD_path_delete(tcodpath);
    }

    void init(unsigned int _w, unsigned int _h, 
              unsigned int _view_w, unsigned int _view_h,
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

            TCOD_path_delete(tcodpath);
            tcodpath = TCOD_path_new_using_map(tcodmap, 1.41);

            do_console = true;
        }

        if (_view_w != view_w || _view_h != view_h) {
            view_w = _view_w;
            view_h = _view_h;

            do_console = true;
        }

        if (font != _font || !has_console || do_console) {

            font = _font;
            title = _title;
            fullscreen = _fullscreen;

            if (has_console) {
                TCOD_console_delete(NULL);
            } else {
                TCOD_sys_startup();
            }

            TCOD_console_set_custom_font(font.c_str(), 
                                         TCOD_FONT_TYPE_GREYSCALE | TCOD_FONT_LAYOUT_ASCII_INROW, 
                                         16, 16);
            TCOD_console_init_root(view_w, view_h, title.c_str(), fullscreen, TCOD_RENDERER_SDL);
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

    bool is_valid(unsigned int x, unsigned int y) {
        if (x < w && y < h) return true;
        return false;
    }

    gridpoint& _get(unsigned int x, unsigned int y) {
	return grid[y*w+x];
    }

    gridpoint& _get(const pt& xy) {
	return grid[xy.second*w+xy.first];
    }

    void set_env(const TCOD_color_t& color, double intensity) {
	env_color = color;
	env_intensity = intensity;
    }

    void set_back(unsigned int x, unsigned int y, unsigned int z, const TCOD_color_t& color) {
	_get(x,y).skins[z].back = color;
    }

    void set_is_lit(unsigned int x, unsigned int y, unsigned int z, bool is_lit) {
	unsigned int& il = _get(x,y).is_lit;

        if (is_lit) {
            il |= (1<<z);
	} else {
	    il &= ~(1<<z);
	}
    }

    void set_is_viewblock(unsigned int x, unsigned int y, unsigned int z, bool t) {
	gridpoint& g = _get(x,y);

        if (t) {
            g.is_viewblock |= (1<<z);
        } else {
            g.is_viewblock &= ~(1<<z);
        }

        TCOD_map_set_properties(tcodmap, x, y, (g.is_viewblock == 0), (g.is_walkblock == 0));
    }

    void set_is_walkblock(unsigned int x, unsigned int y, unsigned int z, bool t) {
	gridpoint& g = _get(x,y);

        if (t) {
            g.is_walkblock |= (1<<z);
        } else {
            g.is_walkblock &= ~(1<<z);
        }

        TCOD_map_set_properties(tcodmap, x, y, (g.is_viewblock == 0), (g.is_walkblock == 0));
    }

    bool is_walkblock(unsigned int x, unsigned int y) {
	gridpoint& g = _get(x,y);
        return g.is_walkblock;
    }

    bool is_viewblock(unsigned int x, unsigned int y) {
	gridpoint& g = _get(x,y);
        return g.is_viewblock;
    }

    void set_skin(unsigned int x, unsigned int y, unsigned int z,
                  const TCOD_color_t& fore, unsigned char c,
                  const TCOD_color_t& fore2, int fore_interp,
                  bool is_terrain) {

	std::vector<skin>& skins = _get(x,y).skins; 
        skin& s = skins[z];

        s.fore = fore;
        s.c = c;
        s.fore2 = fore2;
        s.fore_interp = fore_interp;
        s.is_terrain = is_terrain;
    }

    void unset_skin(unsigned int x, unsigned int y, unsigned int z) {
	std::vector<skin>& skins = _get(x,y).skins;

        skins[z].c = 0;
    }


    bool is_in_fov(unsigned int x, unsigned int y) {
        const gridpoint& gp = _get(x,y);
        return (gp.in_fov || gp.is_lit != 0);
    }


    void draw(unsigned int t,
              int voff_x, int voff_y,
	      unsigned int px, unsigned int py,
	      unsigned int hlx, unsigned int hly,
	      unsigned int rangemin, unsigned int rangemax,
	      unsigned int lightradius, bool do_hud) {

	static double _sparkleinterp[10];
	static bool did_init = false;
	static double pi = 3.14159265358979323846;

	if (!did_init) {
	    for (int i = 0; i < 10; ++i) {
		_sparkleinterp[i] = pow(sin(i/pi), 2);
	    }
	    did_init = true;
	}


	TCOD_map_compute_fov(tcodmap, px, py, lightradius, true, FOV_SHADOW);

	for (size_t _vy = 0; _vy < view_h; ++_vy) {
	    for (size_t _vx = 0; _vx < view_w; ++_vx) {

                pt xy;
                bool is_ok = _translate_v2g(voff_x, voff_y, pt(_vx, _vy), xy);

                if (!is_ok) {
                    TCOD_console_put_char_ex(NULL, _vx, _vy, ' ', TCOD_black, TCOD_black);
                    continue;
                }

                unsigned int x = xy.first;
                unsigned int y = xy.second;

		bool in_fov = TCOD_map_is_in_fov(tcodmap, x, y);

                double d = _dist(xy, pt(px, py));

		gridpoint& gp = _get(xy);
		const std::vector<skin>& skins = gp.skins;

		gp.in_fov = in_fov;

		TCOD_color_t back = TCOD_black;

                auto skin_i = skins.rbegin();
                auto skin_c = skin_i;
                bool found_s = false;
                bool found_b = false;

                while (skin_c != skins.rend()) {

                    if (!found_s && skin_c->c != 0) {
                        found_s = true;
                        skin_i = skin_c;
                    }

                    if (!found_b && !TCOD_color_equals(skin_c->back, TCOD_black)) {
                        found_b = true;
                        back = skin_c->back;
                    }

                    if (found_s && found_b) break;

                    ++skin_c;
                }


                if (!found_s) {
		    continue;
		}

		const skin& sk = *skin_i;

		TCOD_color_t fore = sk.fore;
		unsigned char c = sk.c;

		if (sk.fore_interp) {
                    double i = _sparkleinterp[(x * y + t) % 10];
		    fore = TCOD_color_lerp(fore, sk.fore2, i);
		}

		size_t caid;
		unsigned int caage;
		celauto::get().get_state(xy, caid, caage);

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
		}

		TCOD_console_put_char_ex(NULL, _vx, _vy, c, fore, back);
	    }
	}

        if (do_hud) {
            unsigned int hl = 0;
            unsigned int hpx = (px > view_w / 2 ? 0 : view_w - 14);

            for (const auto& hudline : hud_pips) {
                _draw_pipline(hpx, hl, hudline);
                ++hl;
            }

            if (py > h / 2) {
                _draw_messages(15, 0, t);
            } else {
                _draw_messages(15, view_h - 3, t);
            }
        }

        hud_pips.clear();
    }

    void push_hud_line(const std::string& label, TCOD_color_t labelcolor,
                       bool signd, int npips,
                       char style[2], TCOD_color_t color[2]) {

        hud_pips.emplace_back(label, labelcolor, 
                              (signd ? hud_line::SIGNED : hud_line::UNSIGNED), npips,
                              style, color);
    }


    //////


    void wait_for_anykey() {
        TCOD_console_flush();

        if (keylog_do_replay) {
            TCOD_sys_sleep_milli(replay_delay);
            return;
        }

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

        if (keylog_do_replay) {

            if (keylog_index >= keylog.size())
                throw std::runtime_error("Malformed replay file: premature end-of-keylog.");

            TCOD_sys_check_for_event(TCOD_EVENT_KEY_PRESS, NULL, NULL);
            TCOD_sys_sleep_milli(replay_delay);
            return keylog[keylog_index++];
        }

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

    void push_replay_keypress(const keypress& kp) {

        if (!keylog_do_replay) {
            keylog_do_replay = true;
            keylog_index = keylog.size();
        }

        keylog.push_back(kp);
    }

    void stop_keypress_replay() {
        if (keylog_index < keylog.size())
            throw std::runtime_error("Malformed replay file: not all keypresses were consumed.");
        keylog_do_replay = false;
    }

    /////


    keypress draw_window(const std::vector<std::string>& msg) {
        unsigned int _w = view_w;
        unsigned int _h = view_h;

        size_t maxl = 0;
        std::string s;

        for (const auto& l : msg) {
            maxl = std::max(l.size(), maxl);

            if (s.empty()) {
                s += (char)TCOD_COLCTRL_1;
            } else {
                s += '\n';
            }

            s += l;
        }

        unsigned int l = msg.size();

        unsigned int x0 = _w - maxl - 4;

        if (maxl > _w || _w - maxl < 4)
            x0 = 0;

        unsigned int y0 = std::min(l + 2, _h);

        TCOD_console_set_default_background(NULL, TCOD_darkest_blue);
        TCOD_console_rect(NULL, x0, 0, _w - x0, y0, true, TCOD_BKGND_SET);
        TCOD_console_print_rect(NULL, x0 + 2, 1, _w - x0 - 2, y0 - 1, s.c_str());
        TCOD_console_set_default_background(NULL, TCOD_black);

        TCOD_console_flush();
        keypress ret = wait_for_key();

        TCOD_console_rect(NULL, x0, 0, _w - x0, y0, true, TCOD_BKGND_DEFAULT);
        TCOD_console_flush();

        return ret;
    }

    template <typename FUNC>
    void draw_circle(int voff_x, int voff_y, 
                     unsigned int x, unsigned int y, unsigned int r, 
                     bool do_draw, TCOD_color_t fore, TCOD_color_t back, 
                     FUNC func) {

        _draw_circle(voff_x, voff_y, x, y, r, 
                     /*true, TCOD_yellow, TCOD_darkest_red, */
                     do_draw, fore, back,
                     [](unsigned int, unsigned int) { return true; },
                     func);
    }

    template <typename FUNC>
    void draw_fov_circle(int voff_x, int voff_y,
                         unsigned int x, unsigned int y, unsigned int r, 
                         bool do_draw, TCOD_color_t fore, TCOD_color_t back,
                         FUNC func) {

	TCOD_map_compute_fov(tcodmap, x, y, r, false, FOV_SHADOW);

        _draw_circle(voff_x, voff_y, x, y, r, do_draw, fore, back, //TCOD_darkest_blue,
                     [this](unsigned int x, unsigned int y) { return TCOD_map_is_in_fov(tcodmap, x, y); },
                     func);
    }


    template <typename FUNC>
    void draw_floodfill(int voff_x, int voff_y,
                        unsigned int x, unsigned int y, 
                        bool do_draw, TCOD_color_t fore, TCOD_color_t back,
                        FUNC func) {

        std::set<pt> procd;
        std::set<pt> toproc;

        toproc.insert(pt(x,y));

        while (1) {

            pt xy = *(toproc.begin());
            toproc.erase(toproc.begin());

            for (const auto& xyi : neighbors::get()(xy)) {

                if (procd.count(xyi) != 0) 
                    continue;

                procd.insert(xyi);

                if (func(xyi.first, xyi.second)) {
                    toproc.insert(xyi);
                }
            }

            if (toproc.empty()) {
                break;
            }
        }

        if (do_draw) {
            std::vector<TCOD_color_t> cols;
            //TCOD_color_t back = TCOD_darkest_red;

            cols.push_back(fore); //TCOD_yellow);
            cols.push_back(TCOD_color_lerp(cols.back(), back, 0.5));
            cols.push_back(TCOD_color_lerp(cols.back(), back, 0.5));

            for (const auto& col : cols) {
                for (const auto& xy : procd) {

                    pt vxy;
                    if (!_translate_g2v(voff_x, voff_y, xy, vxy))
                        continue;

                    TCOD_console_put_char_ex(NULL, vxy.first, vxy.second, '*', col, back);
                }
                TCOD_console_flush();
                TCOD_sys_sleep_milli(100);
            }
        }
    }

    template <typename FUNC>
    void draw_line(int voff_x, int voff_y,
                   unsigned int x0, unsigned int y0, unsigned int x1, unsigned int y1, 
                   bool do_draw, TCOD_color_t fore, TCOD_color_t back,
                   FUNC func) {
        
        TCOD_line_init(x0, y0, x1, y1);

        std::vector<pt> pts;

        unsigned int x = x0;
        unsigned int y = y0;
        while (1) {
            if (!func(x, y))
                break;

            pts.push_back(pt(x, y));

            bool ret = TCOD_line_step((int*)&x, (int*)&y);
            if (ret)
                break;
        }

        if (do_draw) {
            for (const auto& xy : pts) {

                pt vxy;
                if (!_translate_g2v(voff_x, voff_y, xy, vxy))
                    continue;

                TCOD_console_put_char_ex(NULL, xy.first, xy.second, '*', fore, back);
                TCOD_console_flush();
                TCOD_sys_sleep_milli(50);
            }
        }
    }



    void do_message(const std::string& msg, bool important) {
        if (!messages.empty()) {
            message& m = messages.front();

            if (m.text == msg) {
                m.timestamp = 0;
                return;
            }
        }

        messages.emplace_front(msg, important, 0);
    }

    void draw_messages_window() {
        unsigned int i = 0;
        std::list<message>::const_iterator li = messages.begin();
        std::vector<std::string> lines;

        while (i < 23 && li != messages.end()) {
            lines.emplace_back();
            std::string& m = lines.back();

            if (li->important) {
                m += (char)TCOD_COLCTRL_3;
            } else if (li == messages.begin()) {
                m += (char)TCOD_COLCTRL_1;
            } else {
                m += (char)TCOD_COLCTRL_5;
            }

            m += li->text;
            ++i;
            ++li;
        }

        draw_window(lines);
    }

    bool path_walk(unsigned int x0, unsigned int y0, unsigned int x1, unsigned int y1,
                   unsigned int n, unsigned int cutoff, 
                   unsigned int& xo, unsigned int& yo) {

        bool tmp = TCOD_path_compute(tcodpath, x0, y0, x1, y1, cutoff);

        if (!tmp) return false;

        for (unsigned int i = 0; i < n; ++i) {
            if (!TCOD_path_walk(tcodpath, (int*)&xo, (int*)&yo, true, cutoff))
                return false;
        }
        return true;
    }



    //***  ***//

    inline void write(serialize::Sink& s) {
	serialize::write(s, w);
	serialize::write(s, h);

        serialize::write(s, view_w);
        serialize::write(s, view_h);

        serialize::write(s, font);
        serialize::write(s, title);
        serialize::write(s, fullscreen);

	serialize::write(s, env_color);
	serialize::write(s, env_intensity);

        for (const auto& t : grid) {

            serialize::write(s, t.skins.size());
	    for (const auto& u : t.skins) {
		serialize::write(s, u.fore);
                serialize::write(s, u.back);
		serialize::write(s, u.c);
		serialize::write(s, u.fore2);
		serialize::write(s, u.fore_interp);
		serialize::write(s, u.is_terrain);
	    }

            serialize::write(s, t.is_lit);
            serialize::write(s, t.in_fov);
            serialize::write(s, t.is_viewblock);
            serialize::write(s, t.is_walkblock);
        }

	serialize::write(s, keylog.size());
        for (const auto& k : keylog) {
            serialize::write(s, k.vk);
            serialize::write(s, k.c);
        }

        serialize::write(s, messages.size());
        for (const auto& m : messages) {
            serialize::write(s, m.text);
            serialize::write(s, m.important);
            serialize::write(s, m.timestamp);
        }
    }

    inline void read(serialize::Source& s) {
        unsigned int _w;
        unsigned int _h;
        unsigned int _view_w;
        unsigned int _view_h;

        serialize::read(s, _w);
        serialize::read(s, _h);

        serialize::read(s, _view_w);
        serialize::read(s, _view_h);

        serialize::read(s, font);
        serialize::read(s, title);
        serialize::read(s, fullscreen);

	serialize::read(s, env_color);
	serialize::read(s, env_intensity);

        init(_w, _h, _view_w, _view_h, font, title, fullscreen);

	for (size_t i = 0; i < grid.size(); ++i) {
	    size_t sks;
            serialize::read(s, sks);

	    gridpoint& p = grid[i];

	    p.skins.resize(sks);

	    for (size_t j = 0; j < sks; ++j) {
		skin& tmp = p.skins[j];
		serialize::read(s, tmp.fore);
                serialize::read(s, tmp.back);
		serialize::read(s, tmp.c);
		serialize::read(s, tmp.fore2);
		serialize::read(s, tmp.fore_interp);
		serialize::read(s, tmp.is_terrain);
	    }

            serialize::read(s, p.is_lit);
            serialize::read(s, p.in_fov);
            serialize::read(s, p.is_viewblock);
            serialize::read(s, p.is_walkblock);

            TCOD_map_set_properties(tcodmap, i % w, i / w, 
                                    (p.is_viewblock == 0), (p.is_walkblock == 0));
        }

        size_t keylog_size;
	serialize::read(s, keylog_size);

        keylog.resize(keylog_size);

        for (size_t i = 0; i < keylog_size; ++i) {
            keypress& k = keylog[i];
            serialize::read(s, k.vk);
            serialize::read(s, k.c);
        }

        size_t messages_size;
        serialize::read(s, messages_size);

        messages.clear();

        for (size_t i = 0; i < messages_size; ++i) {
            messages.emplace_back();
            message& m = messages.back();
            serialize::read(s, m.text);
            serialize::read(s, m.important);
            serialize::read(s, m.timestamp);
        }
    }

};


inline Grid& get() {
    static Grid ret;
    return ret;
}

}


#endif
