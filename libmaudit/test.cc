
#include <iostream>

#include "io.h"
#include "screen.h"


maudit::glyph draw(size_t x, size_t y, size_t w, size_t h) {

    maudit::glyph ret;

    if (x == w/2) {

        if (y == h/2) {
            ret.text = "*";
            ret.fore = maudit::color::bright_white;
        } else {
            ret.text = "|";
            ret.fore = maudit::color::bright_blue;
        }

        ret.back = maudit::color::dim_black;

    } else if (y == h/2) {
        ret.text = "-";

        ret.fore = maudit::color::bright_blue;
        ret.back = maudit::color::dim_black;

    } else {
        ret.text = " ";
        ret.fore = maudit::color::none;
        ret.back = maudit::color::dim_black;
    }

    return ret;
}

int main(int argc, char** argv) {

    maudit::stdin_stdout io;
    maudit::screen<maudit::stdin_stdout> s(io);

    while (1) {
        if (!s.refresh(draw))
            break;

        int key;
        if (!s.wait_key(key))
            break;

        if (key == 'q') 
            break;
    }

    return 0;
}
