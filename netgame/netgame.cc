
#include <thread>

#include <sstream>

#include <iostream>

#include "maudit.h"

#include "debug_benchmark.h"

////

#include "species.h"
#include "species_bank.h"

#include "mainloop_net.h"



void init_statics() {

    init_species("moss1", 0, 300, "pond scum", "x", maudit::color::bright_green, Species::habitat_t::shoreline);
    init_species("moss2", 1, 280, "lichen", "x", maudit::color::dim_white, Species::habitat_t::corner);
}


struct Game {

    unsigned int px;
    unsigned int py;

    int worldx;
    int worldy;
    int worldz;

    static const unsigned int GRID_W = 256;
    static const unsigned int GRID_H = 256;


    Game() : px(0), py(0), worldx(0), worldy(0), worldz(0) {}

    void make_screen(mainloop::screen_params_t& sp) {

        sp.w = GRID_W;
        sp.h = GRID_H;
        sp.w2 = sp.w;
        sp.h2 = sp.h;
    }

    void init() {}

    void make_map(mainloop::GameState& state,
                  uint64_t gridseed, const std::string& cached_grid) {

        state.rng.init(gridseed);

        unsigned int nflatten = std::max(8 - (::abs(worldx) + ::abs(worldy)), 0);
        unsigned int nunflow = std::min(std::max(0, worldz), 8);

        //nflatten = 0;

        std::cout << "Generating... " << gridseed << " " 
                  << nflatten << " " << nunflow << std::endl;

        state.grid.generate(state.neigh, state.rng, nflatten, nunflow);

        std::cout << "Generating OK" << std::endl;

        for (unsigned int x = 0; x < GRID_W; ++x) {
            state.grid.set_walk(state.neigh, x, 0, false);
            state.grid.set_walk(state.neigh, x, GRID_H-1, false);
        }

        for (unsigned int y = 1; y < GRID_H-1; ++y) {
            state.grid.set_walk(state.neigh, 0, y, false);
            state.grid.set_walk(state.neigh, GRID_W-1, y, false);
        }

        std::cout << "Writing grid... " << cached_grid << std::endl;

        serialize::Sink sink(cached_grid);
        state.grid.write(sink);

        std::cout << "Writing OK" << std::endl;
    }

    void generate(mainloop::GameState& state) {

        // Read or generate cached map.

        std::ostringstream cached_grid;

        cached_grid << "_level_" << worldx << "_" << worldy << "_" << worldz << ".dat";

        uint64_t gridseed = (((uint64_t)worldx) ^ 
                             ((uint64_t)worldy << 16) ^
                             ((uint64_t)worldz << 32)) + 1;

        try {

            std::cout << "Reading grid... " << cached_grid.str() << std::endl;

            serialize::Source source(cached_grid.str());
            state.grid.read(source);

            std::cout << "Reading grid OK" << std::endl;

        } catch (std::exception& e) {

            make_map(state, gridseed, cached_grid.str());
        }

        // Place the player on the same starting point every time.

        state.rng.init(gridseed);

        grid::pt xy;
        if (!state.grid.one_of_floor(state.rng, xy))
            throw std::runtime_error("Failed to generate grid");

        px = xy.first;
        py = xy.second;

        state.grid.add_nogen(px, py);

        // Place some random monsters.

        state.rng.init(::time(NULL));

        unsigned int moncount = ::fabs(state.rng.gauss(150.0, 30.0));

        bm _z("monster generation");
        state.monsters.generate(state.rng, state.grid, state.species_counts, 
                                ::abs(worldz), moncount);
    }

    maudit::color floor_color(mainloop::GameState& state, unsigned int x, unsigned int y) {
        double z = state.grid._get(x, y);

        if (z <= -9) {
            return maudit::color::dim_red;
        } else if (z <= -8) {
            return maudit::color::bright_red;
        } else if (z <= -7) {
            return maudit::color::dim_green;
        } else if (z <= -6) {
            return maudit::color::bright_green;
        } else if (z <= -5) {
            return maudit::color::dim_yellow;
        } else if (z <= -4) {
            return maudit::color::bright_yellow;
        } else if (z <= -3) {
            return maudit::color::dim_white;
        }

        return maudit::color::bright_white;
    }

    void set_skin(mainloop::GameState& state, unsigned int x, unsigned int y) {

        bool walkable = state.grid.is_walk(x, y);
        bool water = state.grid.is_water(x, y);

        state.render.set_is_viewblock(x, y, 0, !walkable);
        state.render.set_is_walkblock(x, y, 0, !walkable);

        grender::Grid::skin s;

        if (walkable) {
            if (water) {
                s = grender::Grid::skin("-", maudit::color::bright_blue, maudit::color::bright_black);
            } else {
                s = grender::Grid::skin(".", floor_color(state, x, y), maudit::color::bright_black);
            }

        } else {
            if (water) {
                s = grender::Grid::skin("#", maudit::color::bright_blue, maudit::color::bright_black);
            } else {
                s = grender::Grid::skin("#", maudit::color::bright_white, maudit::color::bright_black);
            }
        }

        state.render.set_skin(x, y, 0, s);

        if (x == px && y == py) {

            s = grender::Grid::skin("@", maudit::color::bright_white, maudit::color::bright_black);
            state.render.set_skin(x, y, 1, s);
        }

        monsters::Monster mon;
        if (state.monsters.get(x, y, mon)) {

            const Species& s = species().get(mon.tag);
            state.render.set_skin(x, y, 1, s.skin);
        }
    }

    void endgame() {}

    template <typename SINK>
    void save(SINK& s) {}

    template <typename SOURCE>
    void load(SOURCE& s) {}

    void drawing_context(mainloop::drawing_context_t& ctx) {

        //unsigned int view_x = (px / 20) * 20;
        //unsigned int view_y = (py / 20) * 20;

        unsigned int grid_x = ctx.view_w / 4;
        unsigned int grid_y = ctx.view_h / 4;

        if (grid_x > 1) {
            ctx.voff_off_x = -(px % grid_x) + (grid_x / 2);
        } else {
            ctx.voff_off_x = 0;
        }

        if (grid_y > 1) {
            ctx.voff_off_y = -(py % grid_y) + (grid_y / 2);
        } else {
            ctx.voff_off_y = 0;
        }

        ctx.px = px;
        ctx.py = py;
        ctx.lightradius = 8;
    }

    void draw_hud(mainloop::GameState& state) {

        state.render.push_hud_line("Foo", maudit::color::bright_yellow, 
                                   4, '+', maudit::color::bright_green);

        state.render.push_hud_line("Bump", maudit::color::bright_red, 
                                   -2, '-', '+', maudit::color::bright_blue, maudit::color::dim_red);
    }

    void process_world(size_t& ticks, bool& done, bool& dead, bool& need_input) {
        
    }

    bool attack(mainloop::GameState& state, monsters::Monster& mon) {

        const Species& s = species().get(mon.tag);

        state.render.do_message("You see " + s.name, false);
        return true;
    }

    void move(mainloop::GameState& state, int dx, int dy, size_t& ticks) {
        int nx = px + dx;
        int ny = py + dy;

        if (nx < 0 || ny < 0) 
            return;

        if (!state.neigh.linked(neighbors::pt(px, py), neighbors::pt(nx, ny)) ||
            !state.grid.is_walk(nx, ny)) {

            return;
        }

        monsters::Monster mon;
        if (state.monsters.get(nx, ny, mon)) {

            if (attack(state, mon)) {
                ++ticks;
            }

            return;
        }

        ++ticks;

        state.render.unset_skin(px, py, 1);

        px = nx;
        py = ny;

        state.render.set_skin(px, py, 1, 
                              grender::Grid::skin("@", maudit::color::bright_white, 
                                                  maudit::color::bright_black));
    }

    void rest(mainloop::GameState& state, size_t& ticks) {

        std::ostringstream s;
        //s << "Turn no.: " << ticks;
        s << "[" << px << "," << py << "] : " << state.grid._get(px, py);

        state.render.do_message(s.str(), false);

        ++ticks;
    }

    void handle_input(mainloop::GameState& state,
                      size_t& ticks, bool& done, bool& dead, maudit::keypress k) {

        bool regen = false;
        bool redraw = false;

        switch (k.letter) {
        case 'Q':
            done = true;
            dead = true;
            break;

        case 'S':
            done = true;
            dead = false;
            break;

        case 'h':
            move(state, -1, 0, ticks);
            break;
        case 'j':
            move(state, 0, 1, ticks);
            break;
        case 'k':
            move(state, 0, -1, ticks);
            break;
        case 'l':
            move(state, 1, 0, ticks);
            break;
        case 'y':
            move(state, -1, -1, ticks);
            break;
        case 'u':
            move(state, 1, -1, ticks);
            break;
        case 'b':
            move(state, -1, 1, ticks);
            break;
        case 'n':
            move(state, 1, 1, ticks);
            break;

        case '.':
            rest(state, ticks);
            break;
        }

        switch (k.key) {
        case maudit::keycode::up:
            move(state, 0, -1, ticks);
            break;
        case maudit::keycode::left:
            move(state, -1, 0, ticks);
            break;
        case maudit::keycode::right:
            move(state, 1, 0, ticks);
            break;
        case maudit::keycode::down:
            move(state, 0, 1, ticks);
            break;
        default:
            break;
        }            

        if (regen) {
            generate(state);

        } else if (redraw) {
            state.render.clear();
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

    init_statics();

    while (1) {

        std::cout << "Accepting..." << std::endl;
        int client = server.accept();

        std::cout << "Making thread..." << std::endl;
        std::thread thr(client_mainloop, client);
        thr.detach();
    }

    return 0;
}