#ifndef __PICCOL_H
#define __PICCOL_H


#include "../piccol/piccol_vm.h"

namespace piccol {

struct Piccol0 : public Piccol {

    Piccol0() :
        Piccol(piccol::load_file("../piccol/macrolan.metal"),
               piccol::load_file("../piccol/piccol_lex.metal"),
               piccol::load_file("../piccol/piccol_morph.metal"),
               piccol::load_file("../piccol/piccol_emit.metal"),
               piccol::load_file("../piccol/prelude.piccol"))
        {
            Piccol::init();
        }
};

}

#endif
