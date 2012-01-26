#ifndef __GRID_H
#define __GRID_H

#include <math.h>
#include <stdlib.h>

#include "neighbors.h"
#include "random.h"

#include <algorithm>
#include <unordered_set>
#include <unordered_map>
#include <numeric_limits>


namespace grid {

typedef std::pair<unsigned int, unsigned int> pt;


struct Map {

    unsigned int w;
    unsigned int h;

    std::vector<double> grid;
 
    std::unordered_set<pt> walkmap;
    std::unordered_set<pt> watermap;

    void init(unsigned int _w, unsigned int _h) {
        w = _w;
        h = _h;

        grid.resize(w*h);
        walkmap.clear();
        watermap.clear();

        for (int i = 0; i < w*h; ++i) {
            grid[i] = 10.0;
        }
    }

    double& _get(unsigned int x, unsigned int y) {
        return grid[y*w+x];
    }

    double& _get(const pt& xy) {
        return grid[pt.second*w+pt.first];
    }



    /*** *** *** *** *** ***/


    void subdivide_mapgen(unsigned int a, unsigned int b, 
                          unsigned int c, unsigned int d,
                          double mid) {

        unsigned int x = ((c - a) / 2) + a;
        unsigned int y = ((d - b) / 2) + b;

        if ((a == x || c == x) &&
            (b == y || d == y))
            return;

        //unsigned int s = std::max(c-a, d-b);
        unsigned int step = 0;
        unsigned int s = 1;

        if (mid == std::numeric_limits<int>::max()) {
            mid = _get(a, b) + _get(c, b) + _get(a, d) + _get(c, d);
            mid = (mid / 4.0) - step + random::get().range(-s, s);
        }

        _get(x, y) = mid;

        double top = ((_get(a, b) + _get(c, b) + mid) / 3) - step + random::get().range(-s, s);
        _get(x, b) = top;

        double bot = ((_get(a, d) + _get(c, d) + mid) / 3) - step + random::get().range(-s, s);
        _get(x, d) = bot;

        double lef = ((_get(a, b) + _get(a, d) + mid) / 3) - step + random::get().range(-s, s);
        _get(a, y) = lef;

        double rig = ((_get(c, b) + _get(c, d) + mid) / 3) - step + random::get().range(-s, s);
        _get(c, y) = rig;

        double none = std::numeric_limits<int>::max();
        subdivide_mapgen(a, b, x, y, none);
        subdivide_mapgen(x, b, c, y, none);
        subdivide_mapgen(a, y, x, d, none);
        subdivide_mapgen(x, y, c, d, none);
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
            if (i < min) min = i;
        }

        double scale = (max - min) / 20.0;

        for (double& i : grid) {
            i /= scale;

            if (i > 10.0) i = 10.0;
            else if (i < -10.0) i = -10.0;
        }
    }

    void makegrid() {
        subdivide_mapgen(0, 0, w - 1, h - 1, -10);        
        normalize();
    }


    void flow(const pt& xy,
              std::unordered_set<pt>& out, 
              double n) {

        if (n < 1e-5)
            return;

        if (out.count(xy) != 0)
            return;

        out.insert(xy);

        double v0 = _get(xy);
        std::vector< std::pair<double, pt> > l;

        for (const auto& xy_ : neighbors::get()(xy)) {

            double v = _get(xy_);

            if (out.count(xy_) == 0 && v <= v0) {
                l.push_back(std::make_pair(v, xy_));
            }
        }

        if (l.size() == 0)
            return;

        std::sort(l.begin(), l.end());

        if (l.size() > 2) {
            l.resize(2);
        }

        double qq = n / (l.size() + 1);

        for (auto& i : l) {
            flow(i.second.first, i.second.second, out, qq);
        }
    }

    void makeflow(std::unordered_set<pt>& gout, 
                  std::unordered_map<pt, int>& watr,
                  double n, double q) {

        unsigned int x = random::get().range(0, w-1);
        unsigned int y = random::get().range(0, h-1);

        std::unordered_set<pt> out;
        flow(x, y, out, n);

        for (pt& xy : out) {

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

        for (int i = 0; i < 50; ++i) {
            makeflow(gout, watr, 100.0, 1);
        }

        for (const pt& xy : gout) {

            if (_get(xy) <= 0) {
                walkmap.insert(pt);
            }
        }
        
        std::vector< std::pair<int,pt> > watr_r;

        for (const auto& v : watr) {
            watr_r.push_back(std::make_pair(v.second, v.first));
        }

        std::sort(watr_r.begin(), watr_r.end());
        std::reverse(watr_r.begin(), watr_r.end());

        int pctwater = random::get().gauss(5, 1);
        if (pctwater <= 1) pctwater = 1;

        pctwater = watr_r.size() / pctwater;

        if (watr_r.size() > pctwater) {
            watr_r.resize(pctwater);
        }

        for (const auto& v : watr_r) {
            watermap.insert(v.second);
        }
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
        if (v) {
            watermap.insert(pt(x, y));
        } else {
            watermap.erase(pt(x, y));
        }
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
