#ifndef __SC_OSC_H
#define __SC_OSC_H

#include <stdio.h>
#include <stdlib.h>

#ifdef _WIN32

#include <windows.h>

#else

#include <unistd.h>
#include <sys/wait.h>

#endif

#include "lo/lo.h"

#include <string>
//#include <iostream>


namespace sc_osc {

void _error(int num, const char* msg, const char* path) {
    printf("liblo server error %d in path %s: %s\n", num, path, msg);
}

int _handler(const char* path, const char* types, lo_arg** argv,
             int argc, void* data, void* user_data);


struct SC_OSC {

    lo_address server_send;
    lo_server server_reply;

    bool active;
    bool mute;
    unsigned int m_n;

    SC_OSC(bool _ok, const std::string& synthdir) : active(false), mute(false), m_n(1000) {

        server_send = lo_address_new(NULL, "55500");
        server_reply = lo_server_new("55501", _error);
        lo_server_add_method(server_reply, NULL, NULL, _handler, this);

        if (!_ok)
            return;

        bool ok = false;

        for (int i = 0; i < 5; ++i) {

            fprintf(stdout, "Waiting for sound server to start...\n");
            int r = lo_send_from(server_send, server_reply, LO_TT_IMMEDIATE, 
                                 "/notify", "i", 1);

            if (r < 0) {
#ifdef _WIN32
                Sleep(1000);
#else
                sleep(1);
#endif
                continue;
            }

            if (lo_server_recv_noblock(server_reply, 1000)) {
                ok = true;
                break;
            }

#ifdef _WIN32
            // Hack for Windows. :(
            Sleep(1000);
#endif
        }

        if (!ok) {
            fprintf(stderr, "Did not get reply from a /notify command, turning off sound.\n");
            return;
        }

        lo_send_from(server_send, server_reply, LO_TT_IMMEDIATE,
                     "/d_loadDir", "s", synthdir.c_str());

        if (lo_server_recv_noblock(server_reply, 4000) == 0) {
            fprintf(stderr, "Did not get reply from a /d_loadDir command, turning off sound.\n");
            return;
        }
	
        active = true;
    }

    ~SC_OSC() {
        lo_address_free(server_send);
        lo_server_free(server_reply);
    }

    unsigned int play(const std::string& synth, const std::string& param, float p) {
        if (!active || mute) return 0;

        lo_send(server_send, "/s_new", "siiisf", 
                synth.c_str(), m_n, 0, 0, param.c_str(), p);

	//std::cout << "!!" << m_n << " " << synth << " " << param << " " << p << std::endl;
        return m_n++;
    }

    void set(unsigned int synthn, const std::string& param, float p) {
        if (!active || mute) return;

        lo_send(server_send, "/n_set", "isf", 
                synthn, param.c_str(), p);
    }

    void free(unsigned int synthn) {
        if (!active) return;

        lo_send(server_send, "/n_free", "i", synthn);
    }

    void quit() {
        if (!active) return;

        lo_send_from(server_send, server_reply, LO_TT_IMMEDIATE, "/quit", "");

        lo_server_recv_noblock(server_reply, 2000);
    }

    bool toggle_mute() {
        mute = !mute;
        return (active && !mute);
    }
};

int _handler(const char* path, const char* types, lo_arg** argv,
             int argc, void* data, void* user_data) {
    return 0;
}


struct Engine {

    bool active;

#ifdef _WIN32
    HANDLE child;

    Engine(const std::string& exe,
           const std::string& execdir,
           const std::string& synthdir, 
           const std::string& plugindir) : active(false) {

        std::string tmp3 = execdir+exe;

        std::string tmp4;
        tmp4 += exe;
        tmp4 += " -u 55500 -U \"";
        tmp4 += plugindir;
        tmp4 += "\"";

        STARTUPINFO si;
        PROCESS_INFORMATION pi;
        DWORD tstat;

        GetStartupInfo(&si);
        si.dwFlags = STARTF_USESHOWWINDOW;
        si.wShowWindow = SW_HIDE;

        BOOL res = SetEnvironmentVariable("SC_SYNTHDEF_PATH", synthdir.c_str());

        if (!res) return;

        res = CreateProcess(tmp3.c_str(), 
                            (char*)tmp4.c_str(),
                            NULL,        // Default process security attributes
                            NULL,        // Default thread security attributes
                            FALSE,      // Don't inherit handles from the parent
                            CREATE_NO_WINDOW,        // 
			    NULL,        // Use the same environment as the parent
                            execdir.c_str(),
                            &si,        // Startup Information
                            &pi);        // Process information stored upon return

        if (!res) return;

        child = pi.hProcess;
        active = true;
    }


    void wait() {
        if (!active) return;
        WaitForSingleObject(child, 2000);
    }


#else

    pid_t child;

    Engine(const std::string& exe,
           const std::string& execdir,
           const std::string& synthdir, 
           const std::string& plugindir) : active(false), child(1) {

        int ch = fork();

        if (ch < 0) {
            fprintf(stderr, "Could not fork().\n");
            return;

        } else if (ch == 0) {

            setenv("SC_SYNTHDEF_PATH", synthdir.c_str(), 1);
            setenv("LD_LIBRARY_PATH", execdir.c_str(), 1);
	    setenv("SC_JACK_DEFAULT_OUTPUTS", "system:playback_1,system:playback_2", 1);
	    setenv("SC_JACK_DEFAULT_INPUTS", "system:capture_1,system:capture_2", 1);

            chdir(execdir.c_str());
            
            std::string tmp3 = execdir+exe;

            if (execl(tmp3.c_str(), exe.c_str(), 
                      "-u", "55500", "-U", plugindir.c_str(), NULL) < 0) {
                
                fprintf(stderr, "Could not execle(): %s%s -u 55500 -U %s\n",
                        execdir.c_str(), exe.c_str(), plugindir.c_str());
                _exit(1);
            }

        } else {
            active = true;
            child = ch;
        }
    }

    void wait() {
        if (!active) return;
        int tmp;
        waitpid(child, &tmp, 0);
    }

#endif

};


struct Sound {
    Engine en;
    SC_OSC osc;

    Sound(const std::string& exe,
          const std::string& execdir,
          const std::string& synthdir, 
          const std::string& plugindir) : 
        en(exe, execdir, synthdir, plugindir), osc(en.active, synthdir)
        {}

    ~Sound() {
        osc.quit();
        en.wait();
    }
};


}


#endif
