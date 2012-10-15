#ifndef __DESIGNS_H
#define __DESIGNS_H

#include <string>

#include "counters.h"

struct Design {

    std::string tag;
    std::string name;
    maudit::glyph skin;
    
    unsigned int level;
    unsigned int count;

    Design() : level(0), count(0) {}

    Design(const std::string& _tag, unsigned int _level, unsigned int _count,
           const std::string& _name, const std::string& _chr, maudit::color _fore) :

        tag(_tag), name(_name), skin(_chr, _fore, maudit::color::bright_black),
        level(_level), count(_count)
        {}
};

#endif