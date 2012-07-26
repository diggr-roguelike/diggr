
#include <iostream>

#include <thread>

#include "io.h"
#include "server.h"
#include "screen.h"

struct context {

    int px;
    int py;
    bool done;

    context() : px(-1), py(-1), done(false) {}
    
    maudit::glyph draw(size_t x, size_t y, size_t w, size_t h) {
        
        if (px < 0) px = w/2;
        if (py < 0) py = h/2;

        maudit::glyph ret;

        if (x == px) {
            
            if (y == py) {
                ret.text = "*";
                ret.fore = maudit::color::bright_white;
            } else {
                ret.text = "|";
                ret.fore = maudit::color::bright_blue;
            }

            ret.back = maudit::color::dim_black;

        } else if (y == py) {
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

    void handle_key(const maudit::keypress& key) {

        if (key.letter == 'q') {
            done = true;
        }
            
        switch (key.key) {
        case maudit::keycode::left:  px--; break;
        case maudit::keycode::right: px++; break;
        case maudit::keycode::up:    py--; break;
        case maudit::keycode::down:  py++; break;
        default: break;
        }
    }
};

void client_mainloop(int client_fd) {

    try {

        maudit::client_socket client(client_fd);
        maudit::screen<maudit::client_socket> screen(client);

        context ctx;

        while (1) {
            if (!screen.refresh(
                    [&ctx](size_t x, size_t y, size_t w, size_t h) { 
                        return ctx.draw(x, y, w, h); 
                    })) {

                break;
            }

            maudit::keypress key;
            if (!screen.wait_key(key)) {
                break;
            }

            ctx.handle_key(key);

            if (ctx.done)
                break;
        }

    } catch (...) {
    }
}

int main(int argc, char** argv) {

    maudit::server_socket server("0.0.0.0", 20020);

    while (1) {

        int client = server.accept();

        std::cout << "Starting thread..." << std::endl;
        std::thread thr(client_mainloop, client);
        std::cout << "Detaching thread..." << std::endl;
        thr.detach();
        std::cout << "OK thread..." << std::endl;
    }

    return 0;
}
