
#include <thread>

#include <sstream>

#include "maudit.h"
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

    void handle_input(size_t& ticks, bool& done, bool& dead, maudit::keypress k) {

        bool regen = false;
        bool redraw = false;

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

        screen_t screen(client);

        mainloop::Main<Game, screen_t> main(screen);

        main.mainloop("_minisave.tmp", ::time(NULL));

    } catch (...) {
    }
}


int main(int argc, char** argv) {

    maudit::server_socket server("0.0.0.0", 20020);

    while (1) {

        int client = server.accept();

        std::thread thr(client_mainloop, client);
        thr.detach();
    }

    return 0;
}
