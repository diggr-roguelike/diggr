#ifndef __RENDER_H
#define __RENDER_H

#include <math.h>

#include "celauto.h"

#include "libtcod.h"

#include <sys/time.h>
#include <iostream>


namespace grender {



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

	gridpoint() : back(TCOD_black), is_lit(0), in_fov(false) {}
    };

    unsigned int w;
    unsigned int h;

    std::vector<gridpoint> grid;

    TCOD_color_t env_color;
    double env_intensity;

    Grid() : w(0), h(0), env_intensity(0) {}

    void init(unsigned int _w, unsigned int _h) {
	w = _w;
	h = _h;
	grid.clear();
	grid.resize(w*h);
	std::cout<<"INIT! "<<w<<" "<<h<<std::endl;
    }

    void set_env(const TCOD_color_t& color, double intensity) {
	env_color = color;
	env_intensity = intensity;
    }

    void set_back(unsigned int x, unsigned int y, const TCOD_color_t& color) {
	grid[y*h+x].back = color;
    }

    void set_is_lit(unsigned int x, unsigned int y, bool is_lit) {
	unsigned int& il = grid[y*h+x].is_lit;

	if (!is_lit) {
	    if (il > 0) --il;
	} else {
	    ++il;
	}
    }

    void push_skin(unsigned int x, unsigned int y,
		   const TCOD_color_t& fore, unsigned char c,
		   const TCOD_color_t& fore2, int fore_interp,
		   bool is_terrain) {

	std::vector<skin>& skins = grid[y*h+x].skins; 

	skins.emplace_back(fore, c, fore2, fore_interp, is_terrain);
    }

    void set_skin(unsigned int x, unsigned int y,
		  TCOD_color_t fore, unsigned char c,
		  TCOD_color_t fore2, int fore_interp,
		  bool is_terrain) {

	std::vector<skin>& skins = grid[y*h+x].skins; 

	if (skins.size() == 0) {
	    skins.emplace_back(fore, c, fore2, fore_interp, is_terrain);
	} else {
	    skin& sk = skins.back();
	    sk = skin(fore, c, fore2, fore_interp, is_terrain);
	}
    }

    void pop_skin(unsigned int x, unsigned int y) {
	std::vector<skin>& skins = grid[y*h+x].skins;

	if (skins.size() > 0)
	    skins.pop_back();
    }


    bool is_in_fov(unsigned int x, unsigned int y) {
	return grid[y*h+x].in_fov;
    }


    bool draw(TCOD_map_t map, unsigned int t,
	      unsigned int px, unsigned int py,
	      unsigned int hlx, unsigned int hly,
	      unsigned int rangemin, unsigned int rangemax,
	      unsigned int lightradius) {

	static double _sparkleinterp[10];
	static bool did_init = false;

	if (!did_init) {
	    for (int i = 0; i < 10; ++i) {
		_sparkleinterp[i] = pow(sin(i/M_PI), 2);
	    }
	    did_init = true;
	}

	bool ret = false;

	TCOD_map_compute_fov(map, px, py, lightradius, true, FOV_SHADOW);

	double othertotal = 0;

	benchmark bm0;
	bm0.start();

	for (int x = 0; x < w; ++x) {
	    for (int y = 0; y < h; ++y) {
		benchmark bm;

		bool in_fov = TCOD_map_is_in_fov(map, x, y);

		unsigned int tmpx = abs(x - px);
		unsigned int tmpy = abs(y - py);
		double d = sqrt(tmpx*tmpx + tmpy*tmpy);

		/// 
		//bm.start();
		//func(&p, x, y, in_fov, d);
		//othertotal += bm.end();

		gridpoint& gp = grid[y*h+x];
		const std::vector<skin>& skins = gp.skins;

		gp.in_fov = in_fov;

		if (skins.size() == 0)
		    continue;

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

		    if (in_fov) {
			ret = true;
		    }
		}

		TCOD_console_put_char_ex(NULL, x, y, c, fore, back);
	    }
	}
    
	std::cout<<"**Interp time:"<<othertotal<<std::endl;
	std::cout<<"**Tottime:"<<bm0.end()<<std::endl;
	return ret;
    }
};


inline Grid& get() {
    static Grid ret;
    return ret;
}

}


#endif
