#ifndef __MAINLOOP_H
#define __MAINLOOP_H

#include "serialize.h"
#include "neighbors.h"
#include "celauto.h"
#include "render.h"
#include "random.h"
#include "grid.h"

#include "moon.h"


namespace mainloop {

template <typename GENERATE,
          typename DRAWING_CONTEXT,
          typename DRAW_HUD,
          typename PROCESS,
          typename HANDLE_INPUT,
          typename ENDGAME>
struct Main {

    GENERATE generate;
    DRAWING_CONTEXT drawing_context;
    DRAW_HUD draw_hud;
    PROCESS process;
    HANDLE_INPUT handle_input;
    ENDGAME endgame;

    size_t ticks;

    Main() : ticks(1) {}



    bool load(const std::string& filename) {
        try {
            serialize::Source s(filename);

            rnd::get().read(s);
            celauto::get().read(s);
            grender::get().read(s);
            grid::get().read(s);
            neighbors::get().read(s);
            moon::get().read(s);

            serialize::read(s, tick);

        } catch (std::exception& e) {
            return false;
        }
        return true;
    }

    void save(const std::string& filename) {

        serialize::Sink s(filename);

        rnd::get().write(s);
        celauto::get().write(s);
        grender::get().write(s);
        grid::get().write(s);
        neighbors::get().write(s);
        moon::get().write(s);

        serialize::write(s, tick);
    }

    void clobber_savefile(const std::string& filename) {
        serialize::Sink s(filename);
    }


    bool start(const std::string& _savefile,
               long seed,
               unsigned int _w, unsigned int _h, 
               unsigned int _w2, unsigned int _h2,
               const std::string& _font, 
               const std::string& _title, 
               bool _fullscreen) {

        savefile = _savefile;

        if (load(savefile)) {
            return false;
        }


        rnd::get().init(seed);
        celauto::get().init();
        grid::get().init(_w, _h);
        grender::get().init(_w2, _h2, _font, _title, _fullscreen);
        grender::get().keylog.clear();
        neighbors::get().init(_w, _h);
        moon::get().init();

        ticks = 1;

        generate();
        return true;
    }


    void draw() {

        unsigned int px;
        unsigned int py;
        unsigned int lightradius;
        unsigned int hlx;
        unsigned int hly;
        unsigned int rangemin;
        unsigned int rangemax;
        bool do_hud;
        
        drawing_context(px, py, lightradius, hlx, hly, rangemin, rangemax, do_hud);

        if (do_hud) {
            draw_hud();
        }
        
        grender::get().draw(ticks, px, py, hlx, hly,
                            rangemin, rangemax, lightradius, do_hud);

    }

    void process(bool done, bool need_input) {
        static size_t oldticks = 0;

        if (ticks == oldticks)
            return;

        oldticks = ticks;

        process(ticks, done, need_input);

    }

    void pump_event(bool need_input) {

        if (need_input) {

            grender::Grid::keypress_t k = grender::get().wait_for_key();
            handle_input(k.vk, k.c);

        } else {
            grender::get().skip_input();
        }
    }
    

    bool mainloop(const std::string& savefile) {

        init(savefile);

        while (1) {

            draw();

            bool done;
            bool dead;
            bool need_input;

            process(done, need_input);

            if (done) {
                draw();
                
                if (dead) {
                    endgame();
                    clobber_savefile(savefile);
                } else {
                    save(savefile);
                }

                grender::get().wait_for_anykey();
                return dead;
            }

            pump_event(need_input);
        }
    }
    

};


}

#endif
