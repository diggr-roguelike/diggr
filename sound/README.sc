
// ./scsynth -u 55500 -U plugins/

/*
~ss = Server.new(\mine, NetAddr("127.0.0.1", 55500));
~ss.initTree;
~ss.notify;

~ss.queryAllNodes;

~ss.loadDirectory("foo", "hello");

Synth("plang", nil, ~ss);

Synth("plang", [\freq, 100], ~ss);
*/

// import OSC
// c = OSC.OSCClient()
// c.connect(("127.0.0.1", 55500))
// c.send(OSC.OSCMessage("/s_new", ["plang", 1000, 0, 0]))
 

//{ SinOsc.ar(440*SinOsc.ar(4, pi/2, 1)+880, 0, 1) * EnvGen.kr(Env.perc(0.125, 0.25, 1, -6)) }.play();

/* "Monster visible" */

SynthDef("wobble", {
 | freq = 200, freqrange = 200, dur = 0.5 |
 var w = SinOsc.ar(freq + (freqrange * SinOsc.ar(5, 0, 0.5)), 0, 1.0) * EnvGen.kr(Env.perc, timeScale: dur);
 Out.ar(0, [w, w]); 
}).store();

Synth("wobble");

/* "Player damaged" */

SynthDef("windnoise",
 { | dur |
   f = { 
   var muln = TRand.kr(0.1, 0.9, Dust2.kr(1));
   var freqn = TRand.kr(-1, 1, Dust2.kr(1));
   var noise = LPF.ar(BrownNoise.ar(muln), 440 + (220 * freqn));
   Lag.ar(noise, 0.01) * EnvGen.ar(Env.perc(0.05, dur)); //Line.ar(1, 0, dur, doneAction: 2)
   };
   Out.ar(0, f);
   Out.ar(1, f);
}).store();


Synth("windnoise", [\dur, 1.5]);

/* "Damage monster" */

SynthDef("klang1",
 { | mul |
   var k = Klank.ar(`[[80, 220, 900], [1.0, 0.2, 1], [3, 1, 0.1]], Impulse.ar(0.1, 0));
   DetectSilence.ar(k, doneAction: 2); 
   Out.ar(0, [k * mul, k * mul]); }).store();

Synth("klang1", [\mul, 0.75]);

/* "8-bit music" */

SynthDef("nintendo",
  { | mul |
    var notes = (TRand.kr(1, 8, Dust2.kr(10)) / 8);
    var s = Pulse.ar(440 * notes, 0.5) * Saw.ar(5.5, 0.5);
    s = s * EnvGen.ar(Env.perc(0.1, 2)) * mul;
    Out.ar(0, [s, s]) }).play();

Synth("nintendo", [\mul, 0.5]);

  