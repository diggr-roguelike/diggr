#ifndef __MAINLOOP_H
#define __MAINLOOP_H

namespace mainloop {

struct Main {

    size_t ticks;

    Main() : ticks(1) {}



    bool load(const std::string& filename) {
        try {
            serialize::Source s(filename);
            celauto::get().read(s);
            grender::get().read(s);
            grid::get().read(s);

        } catch (std::exception& e) {
            return false;
        }
        return true;
    }


    bool start(const std::string& savefile,
               long seed,
               unsigned int _w, unsigned int _h, 
               unsigned int _w2, unsigned int _h2,
               const std::string& _font, 
               const std::string& _title, 
               bool _fullscreen) {

        bool ret = false;

        if (!load(savefile)) {

            celauto::get().init();
            grid::get().init(_w, _h);
            grender::get().init(_w2, _h2, _font, _title, _fullscreen);
            grender::get().keylog.clear();

            ret = true;
        }

        rnd::get().init(seed);
        return ret;
    }


    void draw() {

        unsigned int lightradius = get_lightradius();
        bool do_hud = draw_hud();

        push_skins();

        if (do_hud) {
            draw_hud();
        }
        
        grender::get().draw(ticks, px, py, hlx, hly,
                            rangemin, rangemax, lightradius, do_hud);

        pop_skins();

        return did_hl;
    }

    void process() {
        static size_t oldticks = 0;

        if (ticks == oldticks)
            return;

        process(ticks);

        oldticks = ticks;
    }

    void pump_event() {
    }
    

    void mainloop() {

        while (1) {

            draw();

            process();

            if (done()) {
                draw();
                return;
            }

            pump_event();
        }
    }
    

};


}

#endif
