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


struct drawing_context_t {
    unsigned int px;
    unsigned int py;
    unsigned int lightradius;
    unsigned int hlx;
    unsigned int hly;
    unsigned int rangemin;
    unsigned int rangemax;
    bool do_hud;

    drawing_context_t() :
        px(0), py(0), lightradius(1000), 
        hlx(std::numeric_limits<unsigned int>::max()), 
        hly(hlx),
        rangemin(0),
        rangemax(hlx),
        do_hud(true)
        {}
};


template <typename GAME>
struct Main {

    GAME game;

    size_t ticks;

    Main() : ticks(1) {}



    bool load(const std::string& filename) {
        try {
            serialize::Source s(filename);

            rnd::get().read(s);
            neighbors::get().read(s);
            grid::get().read(s);
            grender::get().read(s);
            celauto::get().read(s);
            moon::get().read(s);

            serialize::read(s, ticks);

            game.load(s);

        } catch (std::exception& e) {
            return false;
        }
        return true;
    }

    void save(const std::string& filename) {

        serialize::Sink s(filename);

        rnd::get().write(s);
        neighbors::get().write(s);
        grid::get().write(s);
        grender::get().write(s);
        celauto::get().write(s);
        moon::get().write(s);

        serialize::write(s, ticks);

        game.save(s);
    }

    void clobber_savefile(const std::string& filename) {
        serialize::Sink s(filename);
    }


    bool start(const std::string& savefile,
               long seed,
               unsigned int _w, unsigned int _h, 
               unsigned int _w2, unsigned int _h2,
               const std::string& _font, 
               const std::string& _title, 
               bool _fullscreen) {

        if (load(savefile)) {
            return false;
        }


        rnd::get().init(seed);
        neighbors::get().init(_w, _h);
        grid::get().init(_w, _h);
        grender::get().init(_w2, _h2, _font, _title, _fullscreen);
        grender::get().keylog.clear();
        celauto::get().init();
        moon::get().init();

        ticks = 1;

        game.init();
        game.generate();

        return true;
    }

    void draw() {

        drawing_context_t ctx;
        game.drawing_context(ctx);

        if (ctx.do_hud) {
            game.draw_hud();
        }
        
        grender::get().draw(ticks, ctx.px, ctx.py, ctx.hlx, ctx.hly,
                            ctx.rangemin, ctx.rangemax, ctx.lightradius, 
                            ctx.do_hud);

    }

    void process(size_t& oldticks, bool& done, bool& dead, bool& need_input) {

        if (ticks == oldticks) {
            need_input = true;
            return;
        }

        oldticks = ticks;

        game.process_world(ticks, done, dead, need_input);

    }

    void pump_event(bool need_input, bool& done, bool& dead) {

        if (need_input) {

            grender::Grid::keypress k = grender::get().wait_for_key();
            game.handle_input(ticks, done, dead, k.vk, k.c);

        } else {
            grender::get().skip_input();
        }
    }

    bool check_done(bool done, bool dead, const std::string& savefile) {

        if (done) {
                
            if (dead) {

                game.endgame();

                clobber_savefile(savefile);

            } else {
                save(savefile);
            }

            grender::get().wait_for_anykey();
            return true;
        }

        return false;
    }

    bool mainloop(const std::string& savefile,
                  long seed,
                  unsigned int _w, unsigned int _h, 
                  unsigned int _w2, unsigned int _h2,
                  const std::string& _font, 
                  const std::string& _title, 
                  bool _fullscreen) {


        start(savefile, seed, _w, _h, _w2, _h2, _font, _title, _fullscreen);

        size_t oldticks = 0;

        draw();

        bool done = false;
        bool dead = false;

        while (1) {

            bool need_input = false;

            process(oldticks, done, dead, need_input);

            draw();

            if (check_done(done, dead, savefile)) 
                return dead;

            pump_event(need_input, done, dead);

            if (check_done(done, dead, savefile)) {

                draw();
                return dead;
            }
        }
    }
    

};


}

#endif
