#ifndef __GRID_H
#define __GRID_H

#include <math.h>
#include <stdlib.h>

#include "neighbors.h"
#include "random.h"

#include <algorithm>
#include <unordered_set>
#include <unordered_map>
#include <limits>

#include <iostream>


namespace std {

template <typename A, typename B>
struct hash< pair<A,B> > {
    size_t operator()(const pair<A,B>& p) const {
        return hash<A>()(p.first) ^ hash<B>()(p.second);
    }
};

}



namespace grid {

typedef std::pair<unsigned int, unsigned int> pt;


struct Map {

    unsigned int w;
    unsigned int h;

    std::vector<double> grid;
 
    std::unordered_set<pt> walkmap;
    std::unordered_set<pt> watermap;

    std::unordered_set<pt> nogens;

    void init(unsigned int _w, unsigned int _h) {
        w = _w;
        h = _h;

        grid.resize(w*h);
        walkmap.clear();
        watermap.clear();
        nogens.clear();

        for (int i = 0; i < w*h; ++i) {
            grid[i] = 10.0;
        }
    }

    double& _get(unsigned int x, unsigned int y) {
        return grid[y*w+x];
    }

    double& _get(const pt& xy) {
        return grid[xy.second*w+xy.first];
    }



    /*** *** *** *** *** ***/


    void subdivide_mapgen(unsigned int a, unsigned int b, 
                          unsigned int c, unsigned int d, bool domid) {

        unsigned int x = ((c - a) / 2) + a;
        unsigned int y = ((d - b) / 2) + b;

        if ((a == x || c == x) &&
            (b == y || d == y))
            return;

        //int s = std::max(c-a, d-b);
        int step = 0;
        int s = 1;

        double mid;

        if (!domid) {
            mid = _get(x, y);
            //std::cout << "!" << mid << std::endl;

        } else {

            mid = _get(a, b) + _get(c, b) + _get(a, d) + _get(c, d);
            mid = (mid / 4.0) - step + rnd::get().range(-s, s);
            //std::cout << " . " << mid << std::endl;

            _get(x, y) = mid;
        }

        double top = ((_get(a, b) + _get(c, b) + mid) / 3.0) - step + rnd::get().range(-s, s);
        _get(x, b) = top;

        double bot = ((_get(a, d) + _get(c, d) + mid) / 3.0) - step + rnd::get().range(-s, s);
        _get(x, d) = bot;

        double lef = ((_get(a, b) + _get(a, d) + mid) / 3.0) - step + rnd::get().range(-s, s);
        _get(a, y) = lef;

        double rig = ((_get(c, b) + _get(c, d) + mid) / 3.0) - step + rnd::get().range(-s, s);
        _get(c, y) = rig;

        subdivide_mapgen(a, b, x, y, true);
        subdivide_mapgen(x, b, c, y, true);
        subdivide_mapgen(a, y, x, d, true);
        subdivide_mapgen(x, y, c, d, true);
    }


    void normalize() {
        double avg = 0.0;
        double min = std::numeric_limits<double>::max();
        double max = std::numeric_limits<double>::min();

        for (double i : grid) {
            avg += i;
        }

        avg /= (w * h);

        for (double& i : grid) {
            i -= avg;
            if (i > max) max = i;
            else if (i < min) min = i;
        }

        double scale = (max - min) / 20.0;

        for (double& i : grid) {
            i = (i / scale);

            if (i > 10.0) i = 10.0;
            else if (i < -10.0) i = -10.0;
        }
    }

    void makegrid() {
        _get((w-1)/2, (h-1)/2) = -10;
        subdivide_mapgen(0, 0, w - 1, h - 1, false);
        normalize();
    }


    void flow(const pt& xy,
              std::unordered_set<pt>& out, 
              double n) {

        //std::cout << "  FLOW: " << xy.first << "," << xy.second << " " << n << std::endl;

        if (n < 1e-5)
            return;

        if (out.count(xy) != 0)
            return;

        out.insert(xy);

        double v0 = _get(xy);
        std::vector< std::pair<double, pt> > l;

        for (const auto& xy_ : neighbors::get()(xy)) {

            double v = _get(xy_);

            //if (out.count(xy_) == 0) {
            //    std::cout << "        " << v << " ~~ " << v0 << std::endl;
            //}

            if (out.count(xy_) == 0 && fabs(v - v0) <= 1.0) {
                l.push_back(std::make_pair(v, xy_));
            }
        }

        //std::cout << "    " << l.size() << " " << v0 << std::endl;

        if (l.size() == 0)
            return;

        std::sort(l.begin(), l.end());

        if (l.size() > 2) {
            l.resize(2);
        }

        double qq = n / (l.size() + 1);

        for (auto& i : l) {
            flow(i.second, out, qq);
        }
    }

    void makeflow(std::unordered_set<pt>& gout, 
                  std::unordered_map<pt, int>& watr,
                  double n, double q) {

        unsigned int x = rnd::get().range((unsigned int)0, w-1);
        unsigned int y = rnd::get().range((unsigned int)0, h-1);

        std::unordered_set<pt> out;
        flow(pt(x, y), out, n);

        std::cout << x << "," << y << " " << out.size() << std::endl;

        for (const pt& xy : out) {

            watr[xy] += 1;

            double& i = _get(xy);

            i -= q;
            if (i < -10.0) i = -10.0;
        }

        gout.insert(out.begin(), out.end());
    }

    void makerivers() {

        std::unordered_set<pt> gout;
        std::unordered_map<pt, int> watr;

        for (int y = 0; y < h; ++y) {
            for (int x = 0; x < w; ++x) {
                std::cout << (char)('A'+(int)_get(x, y));
            }
            std::cout << std::endl;
        }

        for (int i = 0; i < 50; ++i) {
            makeflow(gout, watr, 100.0, 1);
        }

        for (int y = 0; y < h; ++y) {
            for (int x = 0; x < w; ++x) {
                if (gout.count(pt(x,y)) != 0) {
                    std::cout << ' ';
                } else {
                    std::cout << (char)('A'+(int)_get(x, y));
                }
            }
            std::cout << std::endl;
        }


        for (const pt& xy : gout) {

            if (_get(xy) <= 0) {
                walkmap.insert(xy);
            }
        }
        
        std::vector< std::pair<int,pt> > watr_r;

        for (const auto& v : watr) {
            watr_r.push_back(std::make_pair(v.second, v.first));
        }

        std::sort(watr_r.begin(), watr_r.end());
        std::reverse(watr_r.begin(), watr_r.end());

        int pctwater = rnd::get().gauss(5.0, 1.0);
        if (pctwater <= 1) pctwater = 1;

        std::cout << "WATER: " << gout.size() << " " << walkmap.size() << " : " 
                  << watr_r.size() << " " << pctwater << " " << watermap.size() << std::endl;

        pctwater = watr_r.size() / pctwater;

        if (watr_r.size() > pctwater) {
            watr_r.resize(pctwater);
        }

        for (const auto& v : watr_r) {
            watermap.insert(v.second);
            std::cout << " !!! " << watermap.size() << " " << v.second.first << "," << v.second.second << std::endl;
        }

        std::cout << "W2: " << watr_r.size() << " " << pctwater << " " 
                  << watermap.size() << " " << walkmap.size() << std::endl;
    }

    void flatten_pass() {

        std::unordered_set<pt> towalk;
        std::unordered_set<pt> towater;

        for (int x = 0; x < w; ++x) {
            for (int y = 0; y < h; ++y) {

                int nwall = 0;
                int nwater = 0;

                pt xy(x, y);

                for (const auto& xy_ : neighbors::get()(xy)) {

                    if (walkmap.count(xy_) == 0)
                        nwall++;

                    if (watermap.count(xy_) != 0)
                        nwater++;
                }

                if (walkmap.count(xy) == 0 && nwall < 3) {
                    towalk.insert(xy);
                }

                if (watermap.count(xy) == 0 && nwater > 2) {
                    towater.insert(xy);
                }
            }
        }

        walkmap.insert(towalk.begin(), towalk.end());
        walkmap.insert(towater.begin(), towater.end());
        watermap.insert(towater.begin(), towater.end());
    }


    void unflow() {

        std::unordered_set<pt> unwater;

        for (const pt& xy : watermap) {
            int nwater = 0;

            for (const auto& xy_ : neighbors::get()(xy)) {

                if (watermap.count(xy_) != 0)
                    nwater++;
            }

            if (nwater < 5) {
                unwater.insert(xy);
            }
        }

        for (const pt& xy : unwater) {
            watermap.erase(xy);
        }
    }

    void flatten(int type) {
        std::cout << "FLATTEN: " << type << std::endl;

        if (type == 1) {
            for (int i = 0; i < 5; ++i) {
                flatten_pass();
            }

        } else if (type == -1) {
            unflow();
        }
    }

    void generate(int type) {
        makegrid();
        makerivers();
        flatten(type);
    }


    /*** *** *** *** ***/

    void set_height(unsigned int x, unsigned int y, double h) {
        _get(x, y) = h;
    }

    double get_height(unsigned int x, unsigned int y) {
        return _get(x, y);
    }

    bool is_walk(unsigned int x, unsigned int y) {
        return (walkmap.count(pt(x, y)) != 0);
    }

    bool is_water(unsigned int x, unsigned int y) {
        std::cout << "   \\> " << x << "," << y << ":" << watermap.count(pt(x, y)) << std::endl;
        return (watermap.count(pt(x, y)) != 0);
    }

    void set_walk(unsigned int x, unsigned int y, bool v) {
        if (v) {
            walkmap.insert(pt(x, y));
        } else {
            walkmap.erase(pt(x, y));
        }
    }

    void set_water(unsigned int x, unsigned int y, bool v) {
        std::cout << "   /> " << x << "," << y << ":" << v << std::endl;
        if (v) {
            watermap.insert(pt(x, y));
        } else {
            watermap.erase(pt(x, y));
        }
    }

    void add_nogen(unsigned int x, unsigned int y) {
        nogens.insert(pt(x, y));
    }


    pt _one_of(std::vector<pt>& tmp) {
        if (tmp.size() == 0) {
            return pt(rnd::get().range((unsigned int)0, w-1),
                      rnd::get().range((unsigned int)0, h-1));
        }

        std::sort(tmp.begin(), tmp.end());
        return tmp[rnd::get().range(0, (int)tmp.size()-1)];
    }

    pt one_of_floor() {
        std::vector<pt> tmp;

        for (const pt& v : walkmap) {
            if (watermap.count(v) != 0 ||
                nogens.count(v) != 0)
                continue;

            tmp.push_back(v);
        }

        return _one_of(tmp);
    }

    pt one_of_water() {
        std::vector<pt> tmp;

        for (const pt& v : watermap) {
            if (walkmap.count(v) == 0 ||
                nogens.count(v) != 0)
                continue;

            tmp.push_back(v);
        }

        return _one_of(tmp);
    }


    pt one_of_walk() {
        std::vector<pt> tmp;

        for (const pt& v : walkmap) {
            if (nogens.count(v) != 0)
                continue;

            tmp.push_back(v);
        }

        return _one_of(tmp);
    }


    inline void write(serialize::Sink& s) {
        serialize::write(s, w);
        serialize::write(s, h);
        serialize::write(s, grid);
        serialize::write(s, walkmap);
        serialize::write(s, watermap);
    }

    inline void read(serialize::Source& s) {
        serialize::read(s, w);
        serialize::read(s, h);
        serialize::read(s, grid);
        serialize::read(s, walkmap);
        serialize::read(s, watermap);
    }
};

Map& get() {
    static Map ret;
    return ret;
}


}

#endif
