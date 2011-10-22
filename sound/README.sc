
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
 var w = SinOsc.ar(freq + (freqrange * SinOsc.ar(5, 0, 0.5)), 0, 1.0) * EnvGen.kr(Env.perc, timeScale: dur, doneAction: 2);
 Out.ar(0, [w, w]); 
}).store();

Synth("wobble", [\dur, 0.5]);

/* "Player damaged" */

SynthDef("windnoise",
 { | dur |
   f = { 
   var muln = TRand.kr(0.1, 0.9, Dust2.kr(1));
   var freqn = TRand.kr(-1, 1, Dust2.kr(1));
   var noise = LPF.ar(BrownNoise.ar(muln), 440 + (220 * freqn));
   Lag.ar(noise, 0.01) * EnvGen.ar(Env.perc(0.05, dur), doneAction: 2);
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
    s = s * EnvGen.ar(Env.perc(0.1, 2), doneAction: 2) * mul;
    Out.ar(0, [s, s]) }).store();

Synth("nintendo", [\mul, 0.5]);

/* "Tinkling bells" */

SynthDef("bells", 
  { | mul |
    var r = Ringz.ar(Dust2.ar(3), 1800, 3) * Line.ar(0.5 * mul, 0, 3, doneAction: 2) * 0.25;
    Out.ar(0, [r, r]); }).store();

Synth("bells", [\mul, 0.3]);

SynthDef("wizard", { | dur = 3.5, freq = 25.9565, n = 0.5, mul = 1 | 
  var formants = [
  [[600, 1040, 2250, 2450, 2750], [0, -7, -9, -9, -20].dbamp, [60, 70, 110, 120, 130]],
  [[400, 1620, 2400, 2800, 3100], [0, -12, -9, -12, -18].dbamp, [40, 80, 100, 120, 120]],
  [[250, 1750, 2600, 3050, 3340], [0, -30, -16, -22, -28].dbamp, [60, 90, 100, 120, 120]],
  [[400, 750, 2400, 2600, 2900], [0, -11, -21, -20, -40].dbamp, [40, 80, 100, 120, 120]],
  [[350, 600, 2400, 2675, 2950], [0, -20, -32, -28, -36].dbamp, [40, 80, 100, 120, 120]]
  ];

  var f, a, w;
  var bpf;
  var in = WhiteNoise.ar(1) * Saw.ar(freq);

  var vowl = TIRand.ar(0, 4, Impulse.ar(1));
  #f, a, w = Select.kr(vowl, formants);
  bpf = [f, (w).reciprocal, a].flop.collect{ | args | BPF.ar(in, *args); }.sum;
  bpf = bpf * EnvGen.ar(Env.perc(dur*(1-n), dur*n), doneAction: 2) * 4 * mul;
  Out.ar(0, bpf!2);
}).store

Synth("wizard", [\mul, 0.3]);

SynthDef("cthulhu", 
   { | mul = 1 |
     var basefreq = (WhiteNoise.ar(1)*10) + 30;
     var noiz = { 
         var ph = TIRand.ar(0, pi, Impulse.ar(1));
         BPF.ar(Saw.ar(basefreq), (SinOsc.ar(0.5, ph)*50)+440, 0.1); };
     Out.ar(0, [ noiz.value(), noiz.value() ] * mul * EnvGen.ar(Env.sine, timeScale: 4, doneAction: 2));
 }).store

Synth("cthulhu", [\mul, 0.3]);


SynthDef("hooves", 
  { | mul = 1 |
    var base = [ 1200, 900, 800 ];
    var rnd = TIRand.kr(0, 2, Impulse.kr(50));
    var cl = BPF.ar(WhiteNoise.ar(1), [Select.kr(rnd, base), 100, 2200], [0.1, 0.3, 0.7], [1, 0.5, 0.25]).sum;
    var rhythm = (Impulse.ar(2) + Impulse.ar(2, 0.79));
    var clk = cl * EnvGen.ar(Env.perc(0.05, 0.1), rhythm) * Line.ar(mul, 0, 2, doneAction: 2);
    Out.ar(0, [FreeVerb.ar(clk, 0.2, 0.5, 0.1), FreeVerb.ar(clk, 0.2, 0.5, 0.1)]);
 }).store

Synth("hooves", [\mul, 0.3]);


SynthDef("slither",
  { | mul = 1 |
    var v = BPF.ar(WhiteNoise.ar(1), [2800, 2000, 160], [0.1, 0.1, 0.2], [SinOsc.ar(0.1), 0.3, SinOsc.ar(0.1, pi/2)]).sum;
    Out.ar(0, v!2 * mul * EnvGen.ar(Env.sine, doneAction: 2, timeScale: 4)) }).store;

Synth("slither", [\mul, 0.6])

SynthDef("robot",
{ | mul = 1 |
  var klank = Klank.ar(`[[800, 1071, 1153, 2723], [1, 1, 1, 0.1], [2, 1, 0.7, 0.5]], Impulse.ar(1.5));
  var grind = BPF.ar(BrownNoise.ar(1), 110, 0.1);
  var beep = SinOsc.ar(1440) * EnvGen.ar(Env.sine, Impulse.ar(2.5), timeScale: 0.1) * 0.1;
  klank = grind * klank;
  Out.ar(0, Mix([grind*3, klank, beep])!2 * EnvGen.ar(Env.sine, doneAction: 2, timeScale: 5));
 }).store

Synth("robot", [\mul, 1])


/* Roar. */

SynthDef("roar", 
 { | mul = 1 | 
   var e = EnvGen.ar(Env.perc(0.25, 1.5), doneAction:2);
   var r = LFNoise1.ar(600+(e*400))*e; 
   Out.ar(0, (mul * FreeVerb.ar(r, 0.5, 0.7, 0.1, 2))!2); }).store;

Synth("roar", [\mul, 0.3]);


/* Wings flapping. */

SynthDef("wings", 
 { | mul = 1 | 
   var e = EnvGen.ar(Env.perc(0.1, 0.6), Impulse.ar(2));
   var n = Lag.ar(PinkNoise.ar(1), 1/1000);
   var w = LPF.ar(n, 110 + (e * 900)) * e * Line.ar(2, 0, 2, doneAction:2); 
   Out.ar(0, (mul * w)!2); }).store

Synth("wings", [\mul, 0.8])


SynthDef("laugh",
 { | mul = 1 |
  var n = (WhiteNoise.ar(0.75) + SinOsc.ar(340, 0, 0.25)) * LFSaw.ar(1 + SinOsc.ar(0.25)*3); 
  var k = BPF.ar(n, [340, 1400, 2800, 4000], [1/50, 1/100, 1/50, 1/50], [1, 0.7, 0.5, 0.5]).sum;
  var v = Vibrato.ar(k, 64, 0.2, 0, 0.05, 0.5, 0.25) * Line.ar(1, 0, 5, doneAction:2);
  Out.ar(0, (v*5*mul)!2);
}).store;


Synth("laugh", [\mul, 0.3]) 

SynthDef("boom", 
 { | mul = 1 |
  var v = Impulse.ar(1);
  var k = Klank.ar(`[[70, 80, 90], nil, [10, 1, 1]], v);
  k = Line.kr(1, 0, 3.5, doneAction:2) * Lag.ar(k, 0.05, 7);
  Out.ar(0, (k*mul*2)!2); }).store;

Synth("boom", [\mul, 0.4]);


SynthDef("mutter", 
{ | mul = 1|
  var f = [Dwhite(100, 400, inf), Dwhite(40, 180, inf)];
  var q = [Dwhite(1/2, 1/300, inf), Dwhite(1/30, 1/150, inf)];
  var a = [Dwhite(1, 1, inf), Dwhite(1, 1, inf)];
  var b;
  var trig = Dust.kr(15);
  #f, q, a = [f, q, a].collect{|i| Demand.kr(trig, 0, i)};
  b = Lag.ar(BrownNoise.ar(0.75), 0.02) * EnvGen.ar(Env.perc(0.05), Dust.kr(5));
  b = BPF.ar(b, f, q, a).sum * 15;
  b = Limiter.ar(b, 1, 0.1) * EnvGen.ar(Env.perc(0.05, 0.2), Dust2.ar(25)); 
  Out.ar(0, (b!2) * mul * Line.kr(1, 0, 4.5, doneAction:2)); }).store;

Synth("mutter", [\mul, 0.2]);


/* Credits go to: http://sccode.org/1-V */

/* "Air" */

SynthDef("air",
 { | mul = 1 |
  var a = PinkNoise.ar([1, 1]);
  27.do { a = BBandStop.ar(a, LFNoise1.kr(0.05.rand).exprange(40,15000), exprand(0.1,2)) };
  Out.ar(0, LPF.ar(a,1e5) * EnvGen.ar(Env.sine, timeScale: 3, doneAction: 2) * mul) }).store;

Synth("air", [\mul, 0.2]);

/* "Earthquake" */

SynthDef("quake", 
 { | mul = 1| 
   var ff = { var p = PinkNoise.ar([1, 1]);
     var f = FreeVerb2.ar(*LPF.ar(p + 0.01*Dust.ar(6), 60) ++ [1,1,0.2,1e4]).tanh;
     Line.ar(mul, 0, 3, doneAction: 2) * f; };
   Out.ar(0, [ff.value, ff.value]);
}).store














SynthDef("music", {
 | rate = 2.5 | 
 var bjorklund = { |k, n|
   var run = { |arr|
      var index = arr.indexOfEqual(arr[arr.size-1]);

      var a = arr.copyRange(0, index-1);
      var b = arr.copyRange(index, arr.size-1);

      if (b.size > 1 and: {a.size > 0}, {
         run.value(a.collect{|x, i| x++b[i]}++b.copyRange(a.size, b.size-1));
      }, {
         (a++b).flat;
      });
   };

   var arr = [1].dup(k)++[0].dup(n-k);
   arr = arr.collect{|x| x.asCollection};
   run.value(arr);
 };

  var rhythms = [bjorklund.value(3, 8),
	          bjorklund.value(2, 8),
	          bjorklund.value(5, 8)];

  var scales = [[0, 2, 4, 7, 9],
                [0, 3, 5, 7, 10]];
 
  var driver = Impulse.kr(1/(rate*20));
  var musicswitch = Demand.kr(driver, 0, 
                 [ Diwhite(0, rhythms.size-1, inf), 
                   Diwhite(0, rhythms.size-1, inf), 
                   Diwhite(0, rhythms.size-1, inf), 
                   Diwhite(0, scales.size-1, inf),
                   Diwhite(0, 4, inf),
                   Diwhite(0, 3, inf),
                   Diwhite(0, 3, inf)]);

  var fader = EnvGen.kr(Env.sine, driver, timeScale: rate*20);

  var seq = Dxrand((Select.kr(musicswitch[3], scales) + (musicswitch[4] * 12) + 48).midicps, inf);
  var rhythm1 = Dseq(Select.kr(musicswitch[0], rhythms), inf);
  var rhythm2 = Dseq(Select.kr(musicswitch[1], rhythms), inf);
  var rhythm3 = Dseq(Select.kr(musicswitch[2], rhythms), inf);

  var trig1, trig2, trig3, note;
  var r1, r2, g;

  trig1 = Demand.kr(Impulse.kr(rate), 0, rhythm1);
  trig2 = Demand.kr(Impulse.kr(rate, 0.5), 0, rhythm2);
  #trig3, note = Demand.kr(Impulse.kr(rate*2, 0), 0, [rhythm3, seq]);

  r1 = Ringz.ar(K2A.ar(trig1), ((musicswitch[5] * 12) + 24).midicps, 0.05) * 0.05;
  r2 = Ringz.ar(K2A.ar(trig2), ((musicswitch[6] * 12) + 36).midicps, 0.07) * 0.05;
  //r2 = PinkNoise.ar(1) * EnvGen.kr(Env.perc, trig2);
  g = Pluck.ar(WhiteNoise.ar(0.5), trig3, 0.1, note.reciprocal, 5) * 0.7;

  //Out.ar(0, ((Mix([r1, r2, g])*fader)!2).clip(0, 0.2));
  g = ((Mix([r1, r2, g])*fader)!2);
  Out.ar(0, Limiter.ar(g, 0.5, 1));
  }).store;


s = Synth("music");
s.set("rate", 10);

                                                                    