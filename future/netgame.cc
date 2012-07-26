
#include <thread>

#include <sstream>

#include <iostream>
#include <sys/time.h>
struct bm {
    struct timeval b;
    std::string msg;
    bm(const std::string& s) : msg(s) {
        gettimeofday(&b, NULL);
    }
    ~bm() {
        struct timeval e;
        gettimeofday(&e, NULL);
        size_t a = (e.tv_sec*1e6 + e.tv_usec);
        size_t q = (b.tv_sec*1e6 + b.tv_usec);
        std::cout << msg << ": " << ((double)a-(double)q)/1e6 << std::endl;
    }
};

struct bm_s {
    struct timeval b;
    double& _s;
    bm_s(double& s) : _s(s) {
        gettimeofday(&b, NULL);
    }
    ~bm_s() {
        struct timeval e;
        gettimeofday(&e, NULL);
        size_t a = (e.tv_sec*1e6 + e.tv_usec);
        size_t q = (b.tv_sec*1e6 + b.tv_usec);
        _s += ((double)a-(double)q)/1e6;
    }
};


#include "maudit.h"
#include "mainloop_net.h"




struct Game {

    unsigned int px;
    unsigned int py;

    Game() : px(0), py(0) {}

    void make_screen(mainloop::screen_params_t& sp) {

        sp.w = 1024;
        sp.h = 1024;
        sp.w2 = sp.w;
        sp.h2 = sp.h;
    }

    void init() {}

    void generate() {
        std::cout << "Generating..." << std::endl;
        grid::get().generate(0);
        std::cout << "Generating OK" << std::endl;

        grid::pt xy;
        if (!grid::get().one_of_floor(xy))
            throw std::runtime_error("Failed to generate grid");

        px = xy.first;
        py = xy.second;
    }

    void set_skin(unsigned int x, unsigned int y) {

        bool walkable = grid::get().is_walk(x, y);
        bool water = grid::get().is_water(x, y);

        grender::get().set_is_viewblock(x, y, 0, !walkable);
        grender::get().set_is_walkblock(x, y, 0, !walkable);

        grender::Grid::skin s;

        if (walkable) {
            if (water) {
                s = grender::Grid::skin("-", maudit::color::dim_blue, maudit::color::bright_black);
            } else {
                s = grender::Grid::skin(".", maudit::color::dim_white, maudit::color::bright_black);
            }

        } else {
            if (water) {
                s = grender::Grid::skin("#", maudit::color::dim_blue, maudit::color::bright_black);
            } else {
                s = grender::Grid::skin("#", maudit::color::bright_white, maudit::color::bright_black);
            }
        }

        grender::get().set_skin(x, y, 0, s);

        if (x == px && y == py) {

            s = grender::Grid::skin("@", maudit::color::bright_white, maudit::color::bright_black);
            grender::get().set_skin(x, y, 1, s);
        }
    }

    void endgame() {}

    template <typename SINK>
    void save(SINK& s) {}

    template <typename SOURCE>
    void load(SOURCE& s) {}

    void drawing_context(mainloop::drawing_context_t& ctx) {

        ctx.voff_x = 0;
        ctx.voff_y = 0;
        ctx.px = px;
        ctx.py = py;
        ctx.lightradius = 8;
    }

    void draw_hud() {

        grender::get().push_hud_line("Foo", maudit::color::bright_yellow, 
                                     4, '+', maudit::color::bright_green);

        grender::get().push_hud_line("Bump", maudit::color::bright_red, 
                                     -2, '-', '+', maudit::color::bright_blue, maudit::color::dim_red);
    }

    void process_world(size_t& ticks, bool& done, bool& dead, bool& need_input) {
        
        ticks++;
        need_input = true;
    }

    void move(int dx, int dy) {
        int nx = px + dx;
        int ny = py + dy;

        if (nx < 0 || ny < 0) 
            return;

        if (!neighbors::get().linked(neighbors::pt(px, py), neighbors::pt(nx, ny)) ||
            !grid::get().is_walk(nx, ny)) {

            return;
        }

        grender::get().unset_skin(px, py, 1);

        px = nx;
        py = ny;

        grender::get().set_skin(px, py, 1, 
                                grender::Grid::skin("@", maudit::color::bright_white, 
                                                    maudit::color::bright_black));
    }

    void handle_input(size_t& ticks, bool& done, bool& dead, maudit::keypress k) {

        bool regen = false;
        bool redraw = false;


        switch (k.letter) {
        case 'Q':
            done = true;
            dead = true;
            break;
        case 'h':
            move(-1, 0);
            break;
        case 'j':
            move(0, 1);
            break;
        case 'k':
            move(0, -1);
            break;
        case 'l':
            move(1, 0);
            break;
        }

        if (regen) {
            generate();

        } else if (redraw) {
            grender::get().clear();
        }
    }
};


void client_mainloop(int client_fd) {

    try {

        maudit::client_socket client(client_fd);

        typedef maudit::screen<maudit::client_socket> screen_t;

        std::cout << "Making screen..." << std::endl;
        screen_t screen(client);

        mainloop::Main<Game, screen_t> main(screen);

        std::cout << "Starting mainloop..." << std::endl;
        main.mainloop("_ngsave.tmp", ::time(NULL));

    } catch (std::exception& e) {
        std::cout << "Caught error: " << e.what() << std::endl;

    } catch (...) {
    }
}


int main(int argc, char** argv) {

    maudit::server_socket server("0.0.0.0", 20020);

    while (1) {

        std::cout << "Accepting..." << std::endl;
        int client = server.accept();

        std::cout << "Making thread..." << std::endl;
        std::thread thr(client_mainloop, client);
        thr.detach();
    }

    return 0;
}
