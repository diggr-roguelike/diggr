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

    nm = 'scsynth'
    sui = None

    if os.name == 'nt':
        nm += '.exe'
        sui = subprocess.STARTUPINFO()
        sui.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    try:
        p = subprocess.Popen([os.path.join(wd, nm),
                             '-u', '55500', '-U', plugindir],
                             #stdout=open('qq','w'),
                             env=env,
                             cwd=wd, startupinfo=sui)
        print 'OK'
        return p, synthdir
    except:
        print 'ERR'
        return None, synthdir


class Player:
    def __init__(self, synthdir):

        self.repl = OSC.OSCServer(("127.0.0.1", 55501))
        self.repl.addMsgHandler('default', self._ok)

        self.s = OSC.OSCClient(server=self.repl)
        self.s.connect(("127.0.0.1", 55500))
        self.n = 1000

        # HACK
        # Ugly Python code follows, eyebleach danger ahead!

        self.cmd_ok = False
        self.timeout_n = 1

        self.repl.handle_timeout = self.handle_timeout

        while not self.cmd_ok:
            self.s.send(OSC.OSCMessage("/d_loadDir", [synthdir]))
            self.repl.handle_request()
            if self.timeout_n > 3:
                raise Exception('No reply from OSC server')

    def handle_timeout(self):
        self.timeout_n += 1
        #print 'timeout!',self.timeout_n

    def _ok(self, *f):
        #print f
        if f[0] == '/done':
            self.cmd_ok = True

    def play(self, name, **args):

        m = OSC.OSCMessage("/s_new", [name, self.n, 0, 0])
        for k,v in args.iteritems():
            m.extend([k, v])
        #print m

        self.s.send(m)
        ret = self.n
        self.n += 1
        return ret

    def set(self, n, **args):
        m = OSC.OSCMessage("/n_set", [n])
        for k,v in args.iteritems():
            m.extend([k, v])

        self.s.send(m)

    def free(self, n):
        self.s.send(OSC.OSCMessage("/n_free", [n]))

    def quit(self):
        self.s.send(OSC.OSCMessage("/quit"))

class Engine:
    def __init__(self, enabled=True):
        self.mute = False
        self.process = None

        synthdir = None
        if enabled:
            self.process, synthdir = start_server()

        if self.process:
            try:
                self.p = Player(synthdir)
            except Exception as e:
                print e
                self.p = None

    def __del__(self):
        if self.process:
            if self.p:
                self.p.quit()
            self.process.kill()

    def play(self, name, **args):
        if not self.mute and self.process and self.p:
            try:
                return self.p.play(name, **args)
            except:
                self.p.quit()
                self.process.kill()
                self.process = None
        return -1

    def set(self, n, **args):
        if not self.mute and self.process and self.p:
            try:
                self.p.set(n, **args)
            except:
                self.p.quit()
                self.process.kill()
                self.process = None

    def stop(self, n):
        if self.process and self.p:
            try:
                self.p.free(n)
            except:
                self.p.quit()
                self.process.kill()
                self.process = None

    def toggle_mute(self):
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
