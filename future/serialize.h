#ifndef __SERIALIZE_H
#define __SERIALIZE_H

#include <iostream>
#include <fstream>

#include <vector>
#include <map>

namespace serialize {

struct Sink {
    std::ofstream out;

    Sink(const std::string& name) {

	out.exceptions(std::ofstream::failbit|std::ofstream::badbit);
	out.open(name, std::ios::out|/*std::ios::app|*/std::ios::binary|std::ios::trunc);
    }

    template <typename T>
    void operator<<(const T& t) {
        out << t << "\n";
    }
};

struct Source {
    std::ifstream inp;
    
    Source(const std::string& name) {
	inp.exceptions(std::ifstream::failbit|std::ifstream::badbit);
	inp.open(name, std::ios::in|std::ios::binary);
    }

    template <typename T>
    void operator>>(T& t) {
        inp >> t;
    }
};


template <typename T> 
struct writer {
    void write(Sink& s, const T& t) {
        s<<t;
    }
};

template <typename T> 
struct reader {
    void read(Source& s, T& t) {
        s>>t;
    }
};


template <typename T1, typename T2>
struct writer< std::pair<T1,T2> > {
    void write(Sink& s, const std::pair<T1,T2>& v) {
        writer<T1>().write(s, v.first);
        writer<T2>().write(s, v.second);
    }
};

template <typename T1, typename T2>
struct reader< std::pair<T1,T2> > {
    void read(Source& s, std::pair<T1,T2>& v) {
        reader<T1>().read(s, v.first);
        reader<T2>().read(s, v.second);
    }
};


template <typename T>
inline void write_stl(Sink& s, const T& v) {
    s<<v.size();
    for (const T& i : v) {
        writer<T>().write(s, i);
    }
}


template <typename T>
struct remove_constpair { typedef T type; };

template <typename T1, typename T2>
struct remove_constpair< std::pair<const T1, T2> > { typedef std::pair<T1, T2> type; };


template <typename T>
inline void read_stl(Source& s, T& v) {
    size_t sz;
    s>>sz;
    for (size_t i = 0; i < sz; ++i) {
        typename remove_constpair<typename T::value_type>::type vv;
        reader<decltype(vv)>().read(s, vv);
        v.insert(v.end(), vv);
    }
}


template <typename T>
struct writer< std::vector<T> > {
    void write(Sink& s, const std::vector<T>& v) {
        write_stl(s, v);
    }
};

template <typename K,typename V>
struct writer< std::map<K,V> > {
    void write(Sink& s, const std::map<K,V>& v) {
        write_stl(s, v);
    }
};


template <typename T>
struct reader< std::vector<T> > {
    void read(Source& s, std::vector<T>& v) {
        read_stl(s, v);
    }
};

template <typename K,typename V>
struct reader< std::map<K,V> > {
    void read(Source& s, std::map<K,V>& v) {
        read_stl(s, v);
    }
};


template <typename T>
inline void write(Sink& s, const T& t) {
    writer<T>().write(s, t);
}

template <typename T>
inline void read(Source& s, T& t) {
    reader<T>().read(s, t);
}


}


#endif
