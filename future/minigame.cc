
#include <sstream>

#include "mainloop.h"

#include "script.h"


struct Game {

    scripting::Vm vm;

    grid::pt pxy;

    Game() : vm("piccol/", "future/scripts/") {}

    void generate() {

        vm.generate();

        unsigned int gw = grender::get().w;
        unsigned int gh = grender::get().h;

        for (unsigned int y = 0; y < gh; ++y) {
            for (unsigned int x = 0; x < gw; ++x) {
                vm.set_skin(x, y);
            }
        }

        pxy = grid::get().one_of_floor();
    }

    void endgame() {
        std::cout << "Done!" << std::endl;
    }

    template <typename SINK>
    void save(SINK& s) {
        serialize::write(s, pxy);
    }

    template <typename SOURCE>
    void load(SOURCE& s) {
        serialize::read(s, pxy);
    }

    void drawing_context(mainloop::drawing_context_t& ctx) {
        ctx.px = pxy.first;
        ctx.py = pxy.second;
    }

    void draw_hud() {
        char style[2] = { '-', '+' };
        TCOD_color_t color[2] = { TCOD_red, TCOD_green };
        grender::get().push_hud_line("Test", TCOD_yellow, true, 2, style, color);
    }

    void process_world(size_t& ticks, bool& done, bool& dead, bool& need_input) {

        std::ostringstream ss;
        ss << "Turn " << ticks;

        grender::get().do_message(ss.str(), false);

        need_input = true;
    }

    void handle_input(size_t& ticks, bool& done, bool& dead, int vk, char c) {

        std::cout << "!" << ticks << " " << vk << " [" << c << "]" << std::endl;

        if (c == 'Q') {
            dead = true;
            done = true;

        } else if (c == 'S') {
            done = true;

        } else if (c == '.') {
            ticks++;
        }
    }
};

int main(int argc, char** argv) {

    mainloop::Main<Game> main;

    main.mainloop("_minisave.tmp", ::time(NULL),
                  80, 25, 80, 25, 
                  "font.png", "Minigame", false);

    return 0;
}
