
#include "sc_osc.h"


static sc_osc::Sound* _sound = NULL;

extern "C" void sound_init(const char* exe,
                           const char* execdir,
                           const char* synthdir,
                           const char* plugindir) {

    if (_sound) {
        delete _sound;
    }

    _sound = new sc_osc::Sound(exe, execdir, synthdir, plugindir);
}

extern "C" void sound_stop() __attribute__((destructor));

void sound_stop() {
    if (_sound) {
        delete _sound;
        _sound = NULL;
    }
}

extern "C" void sound_toggle_mute() {
    if (_sound) _sound->osc.toggle_mute();
}

extern "C" void sound_free(unsigned int s) {
    if (_sound) _sound->osc.free(s);
}

extern "C" void sound_set(unsigned int s, const char* p, double pd) {
    if (_sound) _sound->osc.set(s, p, pd);
}

extern "C" void sound_play(const char* s, const char* p, double pd) {
    if (_sound) _sound->osc.play(s, p, pd);
}

