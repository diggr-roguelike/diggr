
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
    var r = Ringz.ar(Dust2.ar(3), 1800, 3) * Line.ar(0.5 * mul, 0, 3, doneAction: 2);
    Out.ar(0, [r, r]); }).store();

Synth("bells", [\mul, 0.5]);

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

Synth("wizard", [\mul, 1]);

SynthDef("cthulhu", 
   { | mul = 1 |
     var basefreq = (WhiteNoise.ar(1)*10) + 30;
     var noiz = { 
         var ph = TIRand.ar(0, pi, Impulse.ar(1));
         BPF.ar(Saw.ar(basefreq), (SinOsc.ar(0.5, ph)*50)+440, 0.1); };
     Out.ar(0, [ noiz.value(), noiz.value() ] * mul * EnvGen.ar(Env.sine, timeScale: 4, doneAction: 2));
 }).store

Synth("cthulhu", [\mul, 1.0]);


SynthDef("hooves", 
  { | mul = 1 |
    var base = [ 1200, 900, 800 ];
    var rnd = TIRand.kr(0, 2, Impulse.kr(50));
    var cl = BPF.ar(WhiteNoise.ar(1), [Select.kr(rnd, base), 100, 2200], [0.1, 0.3, 0.7], [1, 0.5, 0.25]).sum;
    var rhythm = (Impulse.ar(2) + Impulse.ar(2, 0.79));
    var clk = cl * EnvGen.ar(Env.perc(0.05, 0.1), rhythm) * Line.ar(mul, 0, 2, doneAction: 2);
    Out.ar(0, [FreeVerb.ar(clk, 0.2, 0.5, 0.1), FreeVerb.ar(clk, 0.2, 0.5, 0.1)]);
 }).store

Synth("hooves");


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

{ Klank.ar(`[[800, 1071, 1353, 1723], nil, [1, 1, 1, 1]], Dust.ar(8, 0.1)) }.play; 
{ Klank.ar(`[[200, 671, 1153, 1723], nil, [1, 1, 1, 1]], Impulse.ar(1), 0.15) }.play; 

/* Credits go to: http://sccode.org/1-V */

/* "Air" */

SynthDef("air",
 { | mul = 1 |
  var a = PinkNoise.ar([1, 1]);
  27.do { a = BBandStop.ar(a, LFNoise1.kr(0.05.rand).exprange(40,15000), exprand(0.1,2)) };
  Out.ar(0, LPF.ar(a,1e5) * EnvGen.ar(Env.sine, timeScale: 3, doneAction: 2) * mul) }).store;

Synth("air");

/* "Earthquake" */

SynthDef("quake", 
 { | mul = 1| 
   var ff = { var p = PinkNoise.ar([1, 1]);
     var f = FreeVerb2.ar(*LPF.ar(p + 0.01*Dust.ar(6), 60) ++ [1,1,0.2,1e4]).tanh;
     Line.ar(mul, 0, 3, doneAction: 2) * f; };
   Out.ar(0, [ff.value, ff.value]);
}).store



(
~formants = {
		var table = IdentityDictionary.new;
		table.put(\sopranoA, [[800, 1150, 2900, 3900, 4950], [0, -6, -32, -20, -50].dbamp, [80, 90, 120, 130, 140]]);
		table.put(\sopranoE, [[350, 2000, 2800, 3600, 4950], [0, -20, -15, -40, -56].dbamp, [60, 100, 120, 150, 200]]);
		table.put(\sopranoI, [[270, 2140, 2950, 3900, 4950], [0, -12, -26, -26, -44].dbamp, [60, 90, 100, 120, 120]]);
		table.put(\sopranoO, [[450, 800, 2830, 3800, 4950], [0, -11, -22, -22, -50].dbamp, [70, 80 ,100, 130, 135]]);
		table.put(\sopranoU, [[325, 700, 2700, 3800, 4950], [0, -16, -35, -40, -60].dbamp, [50, 60, 170, 180, 200]]);
		table.put(\altoA, [[800, 1150, 2800, 3500, 4950], [0, -4, -20, -36, -60].dbamp, [80, 90, 120, 130, 140]]);
		table.put(\altoE, [[400, 1600, 2700, 3300, 4950], [0, -24, -30, -35, -60].dbamp, [60, 80, 120, 150, 200]]);
		table.put(\altoI, [[350, 1700, 2700, 3700, 4950], [0, -20, -30, -36, -60].dbamp, [50, 100, 120, 150, 200]]);
		table.put(\altoO, [[450, 800, 2830, 3500, 4950], [0, -9, -16, -28, -55].dbamp, [70, 80, 100, 130, 135]]);
		table.put(\altoU, [[325, 700, 2530, 3500, 4950], [0, -12, -30, -40, -64].dbamp, [50, 60, 170, 180, 200]]);
		table.put(\counterTenorA, [[660, 1120, 2750, 3000, 3350], [0, -6, -23, -24, -38].dbamp, [80, 90, 120, 130, 140]]);
		table.put(\counterTenorE, [[440, 1800, 2700, 3000, 3300], [0, -14, -18, -20, -20].dbamp, [70, 80, 100, 120, 120]]);
		table.put(\counterTenorI, [[270, 1850, 2900, 3350, 3590], [0, -24, -24, -36, -36].dbamp, [40, 90, 100, 120, 120]]);
		table.put(\counterTenorO, [[430, 820, 2700, 3000, 3300], [0, -10, -26, -22, -34].dbamp, [40, 80, 100, 120, 120]]);
		table.put(\counterTenorU, [[370, 630, 2750, 3000, 3400], [0, -20, -23, -30, -34].dbamp, [40, 60, 100, 120, 120]]);
		table.put(\tenorA, [[650, 1080, 2650, 2900, 3250], [0, -6, -7, -8, -22].dbamp, [80, 90, 120, 130, 140]]);
		table.put(\tenorE, [[400, 1700, 2600, 3200, 3580], [0, -14, -12, -14, -20].dbamp, [70, 80, 100, 120, 120]]);
		table.put(\tenorI, [[290, 1870, 2800, 3250, 3540], [0, -15, -18, -20, -30].dbamp, [40, 90, 100, 120, 120]]);
		table.put(\tenorO, [[400, 800, 2600, 2800, 3000], [0, -10, -12, -12, -26].dbamp, [40, 80, 100, 120, 120]]);
		table.put(\tenorU, [[350, 600, 2700, 2900, 3300], [0, -20, -17, -14, -26].dbamp, [40, 60, 100, 120, 120]]);
		table.put(\bassA, [[600, 1040, 2250, 2450, 2750], [0, -7, -9, -9, -20].dbamp, [60, 70, 110, 120, 130]]);
		table.put(\bassE, [[400, 1620, 2400, 2800, 3100], [0, -12, -9, -12, -18].dbamp, [40, 80, 100, 120, 120]]);
		table.put(\bassI, [[250, 1750, 2600, 3050, 3340], [0, -30, -16, -22, -28].dbamp, [60, 90, 100, 120, 120]]);
		table.put(\bassO, [[400, 750, 2400, 2600, 2900], [0, -11, -21, -20, -40].dbamp, [40, 80, 100, 120, 120]]);
		table.put(\bassU, [[350, 600, 2400, 2675, 2950], [0, -20, -32, -28, -36].dbamp, [40, 80, 100, 120, 120]]);
		
		// convert bandwidth to 1/q
		/*
		table.keysDo({ arg key;
			table[key][0].do({ arg center, i;
				table[key][2][i] = table[key][2][i] / center;
			});
		});
		*/
		table;
}
)

 // !

{ 
  var f, a, w;
  #f, a, w = ~formants.value[\bassA];
  [f, w, a].flop.collect{ | args | Formant.ar(120, *args); }.sum;
}.play




{ var f = [350, 600, 2400, 2675, 2950];
var a = [0, -20, -32, -28, -36].dbamp;
var w = [40, 80, 100, 120, 120]; 
Formant.ar(220, f, w, a).sum * EnvGen.ar(Env.perc(0.1, 0.3)) }.play

Synth("vowel1");
20.midicps

Pbind( \instrument, "vowel1",
  \vowl, Pxrand([0, 1, 2, 3, 4], 5),
  \freq, Pseq([31, 30, 29, 27].midicps, 5),
  \delta, Pseq([0.1, 0.2, 0.3, 0.4, 0.5]*2, 5),
  \dur, Pseq([0.1, 0.2, 0.3, 0.4, 0.5]*3, 5)
).play;



{a=LFTri.ar(1);20.do{a=BAllPass.ar(a,80,1);a=((a+0.02)*LFNoise0.kr(1/2)*8).tanh;a=LeakDC.ar(a,0.995)};a*0.1!2}.play// #supercollider

p={|f,a=1|LFPulse.ar(f)*a*[1,1.01]};{p.(p.(100-p.(1/16,20))+p.(2,1+p.(1/4))-0.5*200)+p.(100-p.(1/8,20),p.(8))*0.1}.play// #supercollider

f=0;Routine({inf.do{|i|f=i/12+f%[4,3];{Formant.ar(2**f*100,2**(i%8*f*0.2)*100,100)*Line.kr(0.1,0,1)}.play;0.25.wait;}}).play//#supercollider

{LocalOut.ar(a=CombN.ar(BPF.ar(LocalIn.ar(2)*7.5+Saw.ar([32,33],0.2),2**LFNoise0.kr(4/3,4)*300,0.1).distort,2,2,40));a}.play

d={|l,h,f,p|({Ringz.ar(LFPulse.ar(f,p,0.01),exprand(l,h),0.5)}!20).sum};{d.(50,100,2,[0,1/4])+d.(3e3,1e4,4,0)+d.(2e2,3e3,1,0.5)*3e-4!2}.play

 // !
d= { |l,h,f,p,n|
    sum( { Ringz.ar( LFPulse.ar(f, p, 0.01), exprand(l,h).round(n), 1.5) } ! 20) };
{ d.(50, 200, [2,1,1], [0,1/4,3/4],[1,40,20])*3e-4!2 }.play;


x=LFPulse;d={|l,h,f,p,n|sum({Ringz.ar(x.ar(f,p,0.01),exprand(l,h).round(n),0.6)}!40)};{d.(30,150,2,[0,0.3],[1,x.kr(1/8)*10+40])*3e-4!2}.play

n={|r,f,d=1|2**LFNoise0.kr(1!d,r)*f};{p=n.(4,1e3);CombN.ar(Ringz.ar(LFPulse.ar(1,0,0.01),n.(2,p,80),0.6).sum,8/5,8/5,60)*4e-4!2}.play

n={|r,f,n=0,d=1|round(r**LFNoise0.ar([4,1,8,2]!d)*f,n)};play{Splay.ar(d=n.(3,0.6);Ringz.ar(d*0.01,n.(2,n.(20,400),40,20),d).mean.tanh)}

p={|f,a=5|GVerb.ar(LFPulse.ar(f)*a)+f};play{tanh(HPF.ar(p.(99-p.(1/2,20)*(1+p.(2,1/5))+p.(4+p.(1/2)),0.5),80,XLine.kr(4e-4,1/8,61,1,0,2)))}

x=0;Pbind(*[type:\set,id:{|freq=10|LFTri.ar(freq.lag(0.1))!2}.play.nodeID,freq:Pfunc{x=x+32%355;x%12+1*40},dur:1/6]).play// #supercollider

x=0;Pbind(*[type:\set,id:{|freq=10|f=freq;LPF.ar(Saw.ar(f),f.lag(1)*3)!2}.play.nodeID,freq:Pfunc{x=x+32%35;x%12+1*40},dur:1/6]).play

play{ 
  p = PinkNoise.ar([1, 1]);
//  BRF.ar(p+Blip.ar(p+2,400),150,2,0.1) + 
//  LPF.ar(
   FreeVerb2.ar(*LPF.ar(p + 0.01*Dust.ar(1), 60) ++ [1,1,0.2,1e4]).tanh
//, 2000)
}

Ndef('x',{Normalizer.ar(FreqShift.ar(Rotate2.ar(*Ndef('x').ar++1/8).tanh,20*[-3,0.995])+Dust.ar(1!2,0.005),1,0.5)}).play// #supercollider

  // !
Ndef(\x,{DelayN.ar(BRF.ar(Saw.ar(20!2)*0.01+Rotate2.ar(*(Ndef(\x).ar*2).tanh++0.1),20**LFNoise1.kr(0.6)*500,1),1,1)}).play// #supercollider

b=Buffer.read(s,"sounds/a11wlk01.wav");play{t=Impulse.kr(5);PlayBuf.ar(1,b,1,t,Demand.kr(t,0,Dseq(1e3*[103,41,162,15,141,52,124,190],4)))!2}

Ndef('x',{x=(Ndef('x').ar*1.8).tanh;BPF.ar(x+[0.01,0.1],12**Latch.ar(x.mean,Impulse.ar(3)).lag(0.1)*200)})// tin whistle #supercollider

Ndef('x',{x=Ndef('x').ar+0.01;a=BPF.ar(x,6**Latch.ar(x,Dust.ar(x))*200,0.1).sin;9.do{a=AllpassN.ar(a,0.2,{0.2.rand}!2,9)};a+a.mean}).play;

f=g=0;Routine({loop{g=g+1e-3;f=f+g%1;play{l=Line.kr(1,0,3,doneAction:2);h=2**f*100;e=Pluck.ar(CuspL.ar,1,i=1/h,i,2,0.3)!2};0.15.wait}}).play

a=1@2;f=1;w=Window().front.drawHook_({900.do{Pen.line(a*200,(a=(a*(f=f+2e-6)).y.cos+1@a.x)*200)};Pen.stroke});AppClock.play{w.refresh;0.01}

p={|f,a=5|GVerb.ar(LFPulse.ar(f)*a)+f};play{tanh(HPF.ar(p.(99-p.(1/2,20)*(1+p.(2,1/5))+p.(4+p.(1/2)),0.5),80,XLine.kr(4e-4,1/8,61,1,0,2)))}

n={|r,f,n=0,d=1|round(r**LFNoise0.ar([4,1,8,2]!d)*f,n)};play{Splay.ar(d=n.(3,0.6);Ringz.ar(d*0.01,n.(2,n.(20,400),40,20),d).mean.tanh)}

x=0;Pbind(*[type:\set,id:{|freq=10|LFTri.ar(freq.lag(0.1))!2}.play.nodeID,freq:Pfunc{x=x+32%355;x%12+1*40},dur:1/6]).play// #supercollider

play{p=PinkNoise.ar(1!2);BRF.ar(p+Blip.ar(p+2,400),150,2,0.1)+LPF.ar(FreeVerb2.ar(*LPF.ar(p+0.2*Dust.ar(0.1),60)++[1,1,0.2,1e4]).tanh,2000)}

Ndef('x',{Normalizer.ar(FreqShift.ar(Rotate2.ar(*Ndef('x').ar++1/8).tanh,20*[-3,0.995])+Dust.ar(1!2,0.005),1,0.5)}).play// #supercollider

b=Buffer.read(s,"sounds/a11wlk01.wav");play{t=Impulse.kr(5);PlayBuf.ar(1,b,1,t,Demand.kr(t,0,Dseq(1e3*[103,41,162,15,141,52,124,190],4)))!2}
b=Buffer.read(s,"sounds/a11wlk01.wav");play{t=Impulse.kr(6);BufGrain.ar(t,0.3,b,1,Demand.kr(t,0,Dseq([26,8,11,42,44,3,5,37,4,32,45]/50,4)))}

Ndef('x',{x=Ndef('x').ar+0.01;a=BPF.ar(x,6**Latch.ar(x,Dust.ar(x))*200,0.1).sin;9.do{a=AllpassN.ar(a,0.2,{0.2.rand}!2,9)};a+a.mean}).play;

a=1@2;f=1;w=Window().front.drawHook_({900.do{Pen.line(a*200,(a=(a*(f=f+2e-6)).y.cos+1@a.x)*200)};Pen.stroke});AppClock.play{w.refresh;0.01}

Ndef(\,{LPF.ar(x=DelayN.ar(LeakDC.ar(Ndef(\).ar,1-2e-6)*0.99,1,0.01)+Dust.ar(0.5!2);x+(Trig1.ar(x<(x.mean.lag(30)),4e-3)*0.05),800)}).play

Ndef(\,{x=DelayL.ar(n=Ndef(\);n.ar,2,LFNoise0.kr(0.03*_!20)+1)+Blip.ar(0.5);LeakDC.ar(LPF.ar(x+x.mean*0.15,4e3)).sin});play{Splay.ar(n.ar)}

play{w=LFSaw;a=w.ar(-3,1)+1/2;f=Sweep.ar(0,3).floor;f=(f**3+f%8+4)*(f%3+3)%49*3;CombN.ar(RLPF.ar(w.ar(f)*a,f**a*30,0.3).tanh,5/6,5/6,6)!2}

play{PitchShift.ar(CombN.ar(Formant.ar(101,4**LFNoise1.kr(0.5)*450,200),1,0.5,99),1,Duty.kr(4,0,Dseq([[6,8,10],[6,7.2,7]]/8,inf))).sum/25!2}

Ndef(\,{x=DelayN.ar(LeakDC.ar(Ndef(\).ar),1,z=1e-2);LPF.ar(Trig1.ar(Amplitude.kr(x,5,120)*1.5+x+z-Dust.ar(2),4e-3)*0.1+x*0.99,1200)}).play

play{b=LocalBuf(1e5,2).clear;x=BufRd.ar(2,b,Phasor.ar(0,1,0,1e5))*0.6;BufWr.ar(Blip.ar([1,1.01],10)/5+x,b,LFNoise1.ar(0.2)+1*5e4);x}// #sc

play{b=LocalBuf(4e5,2).clear;BufCombL.ar(b,LeakDC.ar(BufRd.ar(2,b,LFNoise1.ar(0.25)+1*2e5)*0.98)+Blip.ar(2!2,10),2,20)/10}// #supercollider

play{b=LocalBuf(4e5,2).clear;BufCombL.ar(b,LeakDC.ar(LPF.ar(PlayBuf.ar(2,b,16/15,0,0,1),300))+Blip.ar([20,21],1),2,40)/20}// #supercollider
play{b=LocalBuf(2*SampleRate.ir,2);BufCombL.ar(b,LeakDC.ar(RLPF.ar(Limiter.ar(PlayBuf.ar(2,b,0.4,0,0,1),0.5)+Dust.ar(0.1),5e3,0.03)),1,10)}
play{({|i|x=Dbufrd(b=LocalBuf(5).clear,i);x=x**x-LFNoise0.ar(1/(2**i),50).floor%16;Pulse.ar(Duty.ar(1/8,0,Dbufwr(x,b,i))*20)}!5).mean!2}

play{x=Splay.ar({|i|RLPF.ar(0.6**i*40*Impulse.ar(2**i/32,1/2),4**LFNoise0.kr(1/16)*300,5e-3).sin}!8);2.do{x=FreeVerb2.ar(*x++[0.1,1,1])};x}

play{Splay.ar({|i|f=1.9**i/128;BPF.ar(PinkNoise.ar(1!2),4**LFNoise2.kr(1.2**i/16)*300,0.15)*(5**LFNoise2.ar(f)/(i+8)*20)}!15)}

  // ! robot
play{x=Saw.ar([50,50.1]);8.do{|i|f=2**(8-i);x=BRF.ar(AllpassN.ar(x,1,0.1/(12-i),2),80**TRand.ar(0,1,Impulse.ar(f/32,1/2)).lag(1/f)*80,2)};x}

p=Impulse;play{mean({|i|Pluck.ar(LFSaw.ar([102,101]),x=p.ar(1,i/10)+p.ar(0),1,1/Latch.ar(1.015**Sweep.ar(0,1)*64%1+1*200,x),4,0.2)}!10)}

p=SCImage(n=300);n.do{|i|n.do{|j|z=c=Complex(i-240,j-150)/n*2.5;{(r=rho(z=z*z+c)/8)>1&&{z=0}}!200;p.setColor(Color.hsv(r,1,1),i,j)}};p.plot

x=Ndef(\x,Pbind(\freq,Pseq(a=(3..5);a/.x a*.x[40,80],8)));Ndef(\,{Limiter ar:GVerb.ar(PitchShift.ar(Ndef ar:\,1,2,0,0.1),30,9)/4+x.ar}).play

x=Ndef(\x,Pbind(\freq,Pseq(a=(3..5);a*.x a*.x[4,8],8)));Ndef(\,{Limiter ar:GVerb.ar(PitchShift.ar(Ndef ar:\,1,2,0,0.1),20,20)/4+x.ar}).play

play{GVerb.ar(LFTri.ar(Duty.ar(Dseq([3,1]/12,inf),0,Dseq(x=(3..6);allTuples(x/.t x).flat*[100,200,400]++0))),25,5)/5} // #supercollider

play{GVerb.ar(Saw.ar(Duty.ar(1/8,0,Dseq(x=[5,2,9,3];1/(flat(allTuples(x/.t x).reject(any(_,{|i|i%1==0}))/.-1 x)%1)*30++0))),165,5)/5}

play{GVerb.ar(Saw.ar(Duty.ar(1/8,0,Dseq(x=[5,2,[9,7],3];1/(flat(allTuples(x/.t x).reject(any(_,{|i|i%1==0}))/.-1 x)%1)*30++0))),165,1)/5}

play{GVerb.ar(Pulse.ar(Duty.ar(1/8,0,Dseq(x=[5,2,7,3];1/flat(allTuples(x/.t x).reject(any(_,{|i|i%1==0}))%1)*.x[1,3,2,6]*40++0))),165,7)/5}

t={|u,d,a|u.ar(Duty.ar(d/5,0,Dseq(a++0))*300)};play{t.(Saw,1,x=[6,5,9,8];flat(y=allTuples(x/.t x)[(127..1)+[0,127]]%1))+t.(LFTri,4,y*2)!2/6} 

play{GVerb.ar(VarSaw.ar(Duty.ar(1/5,0,Dseq(x=[[4,4.5],[2,3,5,6]];flat(x*.x allTuples(x*.x x)*4).clump(2)++0)),0,0.9)*LFPulse.ar(5),99,5)/5}

f=0;{inf.do{|i|f=f+log2(2*i%6+1+floor(f)/(i%5+1))%2;play{SyncSaw.ar(2**f*99+[0,1],i%8+2*52)*Line.kr(0.1,0,1,1,0,2)};0.3.wait}}.r.play
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               