
#include <sstream>

#include "mainloop_net.h"




struct Game {

    Game() {}

    void make_screen(mainloop::screen_params_t& sp) {}

    void init() {}

    void generate() {}

    void set_skin(unsigned int x, unsigned int y) {}

    void endgame() {}

    template <typename SINK>
    void save(SINK& s) {}

    template <typename SOURCE>
    void load(SOURCE& s) {}

    void drawing_context(mainloop::drawing_context_t& ctx) {}

    void draw_hud() {}

    void process_world(size_t& ticks, bool& done, bool& dead, bool& need_input) {}

    void handle_input(size_t& ticks, bool& done, bool& dead, int vk, char c) {

        bool regen = false;
        bool redraw = false;

        if (regen) {
            generate();

        } else if (redraw) {
            grender::get().clear();
        }
    }
};

int main(int argc, char** argv) {

    mainloop::Main<Game> main;

    main.mainloop("_minisave.tmp", ::time(NULL));

    return 0;
}
