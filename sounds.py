#!/usr/bin/env python

import subprocess
import os
import os.path
import time

import sound.OSC as OSC


def start_server():
    cwd = os.getcwd()
    wd = os.path.join(cwd, 'sound')
    synthdir = os.path.join(wd, 'synths')
    plugindir = os.path.join(wd, 'plugins')

    env = dict(os.environ)
    env['SC_SYNTHDEF_PATH'] = synthdir
    env['LD_LIBRARY_PATH'] = wd

    try:
        p = subprocess.Popen([os.path.join(wd, 'scsynth.exe'),
                             '-u', '55500', '-U', plugindir],
                             stdout=open('qq','w'),
                             env=env,
                             cwd=wd)
        print 'OK'
        return p
    except:
        print 'ERR'
        return None


class Player:
    def __init__(self):
        #time.sleep(1)

        #self.repl = OSC.OSCServer(("127.0.0.1", 55501))
        #self.repl.addMsgHandler("/done", self._ok)

        self.s = OSC.OSCClient() #server=self.repl)
        self.s.connect(("127.0.0.1", 55500))
        self.n = 1000

        #self.cmd_ok = False
        #self.s.send(OSC.OSCMessage("/d_loadDir", [synthdir]))
        #
        #while not self.cmd_ok:
        #    self.repl.handle_request()

    #def _ok(self, *f):
    #    self.cmd_ok = True

    def play(self, name, **args):

        m = OSC.OSCMessage("/s_new", [name, self.n, 0, 0])
        for k,v in args.iteritems():
            m.extend([k, v])
        print m

        self.s.send(m)
        ret = self.n
        self.n += 1
        return ret

    def free(self, n):
        self.s.send(OSC.OSCMessage("/n_free", [n]))


class Engine:
    def __init__(self):
        self.mute = False
        self.process = start_server()

        if self.process:
            self.p = Player()

    def __del__(self):
        if self.process:
            self.process.kill()

    def play(self, name, **args):
        if not self.mute and self.process:
            try:
                self.p.play(name, **args)
            except:
                self.process.kill()
                self.process = None

    def mute(self):
        self.mute = not self.mute

def main():
    e = Engine()
    time.sleep(1)
    e.play("plang")
    time.sleep(0.1)
    e.play("wobble")
    for x in xrange(4):
        e.play("plang", out=x%2)
        time.sleep(1)


if __name__ == '__main__':
    main()
