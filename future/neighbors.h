#ifndef __NEIGHBORS_H
#define __NEIGHBORS_H

#include <vector>
#include <map>


namespace neighbors {

typedef std::pair<unsigned int, unsigned int> pt;


struct Neighbors {
    
    typedef std::map<pt, std::vector<pt> > ns_t;
    ns_t nbmap;

    void init(unsigned int w, unsigned int h) {

        nbmap.clear();

        for (unsigned int x = 0; x < w; x++) {
            for (unsigned int y = 0; y < h; y++) {

                std::vector<pt>& v = nbmap[std::make_pair(x, y)];

                for (int xi = -1; xi <= 1; xi++) {
                    for (int yi = -1; yi <= 1; yi++) { 

                        if (xi == 0 && yi == 0) continue;

                        pt tmp(x+xi, y+yi);

                        if (tmp.first < 0 || tmp.first >= w || tmp.second < 0 || tmp.second >= h)
                            continue;

                        v.push_back(tmp);
                    }
                }
            }
        }
    }

    const std::vector<pt>& operator()(const pt& xy) const {
        static std::vector<pt> empty;

        ns_t::const_iterator i = nbmap.find(xy);

        if (i != nbmap.end()) {
            return i->second;
	}
        
        return empty;
    }
};


inline Neighbors& get() {
    static Neighbors ret;
    return ret;
}


}

#endif
