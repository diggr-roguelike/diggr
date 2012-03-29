#ifndef __PICCOL_H
#define __PICCOL_H


#include "../piccol/piccol_vm.h"

namespace piccol {

struct Piccol0 : public Piccol {

    Piccol0(const std::string& sysdir) :
        Piccol(piccol::load_file(sysdir + "macrolan.metal"),
               piccol::load_file(sysdir + "piccol_lex.metal"),
               piccol::load_file(sysdir + "piccol_morph.metal"),
               piccol::load_file(sysdir + "piccol_emit.metal"),
               piccol::load_file(sysdir + "prelude.piccol"))
        {
            Piccol::init();
        }
};

}

#endif
