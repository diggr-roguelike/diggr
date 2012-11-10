
#line 1 "configparser.rl"
#ifndef __CONFIGPARSER_H
#define __CONFIGPARSER_H

// This file needs to be preprocessed with the 'ragel' tool.
// Run it like this:
//
//   ragel -G2 configparser.rl -o configparser.h
//

#include <string>
#include <stdexcept>
#include <iostream>

#include <string.h>
#include <stdio.h>

#include "maudit.h"
#include "species.h"
#include "species_bank.h"

namespace configparser {

struct ragel_state {

    /** Ragel scanner cruft. **/

    // Iterators for start and end of buffer data.
    char* p;
    char* pe;

    // Iterator for 'end of file'.
    char* eof;

    // Iterator for start and end of token.
    char* ts;
    char* te;

    // Internal state and rollback variables.
    int cs, act;

    // Stack for ragel machine states.
    int stack[32];
    int top;

    // Not part of ragel's variables; this is a buffer to hold the current match.
    std::string match;
};

inline void init_species(const Species& s) {
    init_species_copy(s);
}

inline void init_design(const Design& d) {
    init_design_copy(d);
}

inline void init_terrain(const Terrain& t) {
    init_terrain_copy(t);
}

inline void init_levelskin_(const Levelskin& l) {
    init_levelskin(l);
}

inline void add_color(maudit::color& c, unsigned int i) {
    c = (maudit::color)((uint32_t)c + i);
}

inline int toint(const std::string& s) {
    return ::atoi(s.c_str());
}

inline double toreal(const std::string& s) {
    return ::atof(s.c_str());
}

void parse_config(const std::string& filename) {

    /** File reading cruft. **/

    char buf[4096];

    FILE* fn = ::fopen(filename.c_str(), "r");

    if (fn == NULL) {
        throw std::runtime_error("Could not open: \"" + filename + "\"");
    }

    ragel_state state;

    Species spe;
    Design des;
    Terrain ter;
    Levelskin lev;

    maudit::glyph skin;

    
#line 376 "configparser.rl"

/*

*/

    
#line 109 "configparser.h"
static const int ConfigParser_start = 1;
static const int ConfigParser_first_final = 1351;
static const int ConfigParser_error = 0;

static const int ConfigParser_en_strchar_escape = 47;
static const int ConfigParser_en_one_species = 48;
static const int ConfigParser_en_one_design = 335;
static const int ConfigParser_en_one_terrain = 483;
static const int ConfigParser_en_one_levelskin = 628;
static const int ConfigParser_en_main = 1;


#line 382 "configparser.rl"
    
#line 124 "configparser.h"
	{
	 state.cs = ConfigParser_start;
	 state.top = 0;
	}

#line 383 "configparser.rl"

    bool done = false;
    int have = 0;

    while (!done) {
        int space = sizeof(buf) - have;
        if (space == 0) {
            throw std::runtime_error("Token too big!");
        }

        state.p = buf + have;
        int len = ::fread(state.p, 1, space, fn);
        
        state.pe = state.p + len;
        state.eof = 0;
        
        if (len == 0) {
            state.eof = state.pe;
            done = true;
        }

        
#line 153 "configparser.h"
	{
	if ( ( state.p) == ( state.pe) )
		goto _test_eof;
	goto _resume;

_again:
	switch (  state.cs ) {
		case 1: goto st1;
		case 0: goto st0;
		case 2: goto st2;
		case 3: goto st3;
		case 4: goto st4;
		case 5: goto st5;
		case 6: goto st6;
		case 7: goto st7;
		case 8: goto st8;
		case 9: goto st9;
		case 10: goto st10;
		case 11: goto st11;
		case 12: goto st12;
		case 1351: goto st1351;
		case 1352: goto st1352;
		case 13: goto st13;
		case 14: goto st14;
		case 15: goto st15;
		case 16: goto st16;
		case 17: goto st17;
		case 18: goto st18;
		case 19: goto st19;
		case 20: goto st20;
		case 21: goto st21;
		case 22: goto st22;
		case 23: goto st23;
		case 24: goto st24;
		case 1353: goto st1353;
		case 25: goto st25;
		case 26: goto st26;
		case 27: goto st27;
		case 28: goto st28;
		case 29: goto st29;
		case 30: goto st30;
		case 31: goto st31;
		case 32: goto st32;
		case 33: goto st33;
		case 34: goto st34;
		case 35: goto st35;
		case 36: goto st36;
		case 1354: goto st1354;
		case 37: goto st37;
		case 38: goto st38;
		case 39: goto st39;
		case 40: goto st40;
		case 41: goto st41;
		case 42: goto st42;
		case 43: goto st43;
		case 44: goto st44;
		case 45: goto st45;
		case 46: goto st46;
		case 1355: goto st1355;
		case 47: goto st47;
		case 1356: goto st1356;
		case 48: goto st48;
		case 49: goto st49;
		case 50: goto st50;
		case 51: goto st51;
		case 52: goto st52;
		case 53: goto st53;
		case 54: goto st54;
		case 55: goto st55;
		case 56: goto st56;
		case 57: goto st57;
		case 58: goto st58;
		case 59: goto st59;
		case 60: goto st60;
		case 61: goto st61;
		case 62: goto st62;
		case 63: goto st63;
		case 64: goto st64;
		case 65: goto st65;
		case 66: goto st66;
		case 1357: goto st1357;
		case 67: goto st67;
		case 68: goto st68;
		case 69: goto st69;
		case 70: goto st70;
		case 71: goto st71;
		case 72: goto st72;
		case 73: goto st73;
		case 74: goto st74;
		case 75: goto st75;
		case 76: goto st76;
		case 77: goto st77;
		case 78: goto st78;
		case 79: goto st79;
		case 80: goto st80;
		case 81: goto st81;
		case 82: goto st82;
		case 83: goto st83;
		case 84: goto st84;
		case 85: goto st85;
		case 86: goto st86;
		case 87: goto st87;
		case 88: goto st88;
		case 89: goto st89;
		case 90: goto st90;
		case 91: goto st91;
		case 92: goto st92;
		case 93: goto st93;
		case 94: goto st94;
		case 95: goto st95;
		case 96: goto st96;
		case 97: goto st97;
		case 98: goto st98;
		case 99: goto st99;
		case 100: goto st100;
		case 101: goto st101;
		case 102: goto st102;
		case 103: goto st103;
		case 104: goto st104;
		case 105: goto st105;
		case 106: goto st106;
		case 107: goto st107;
		case 108: goto st108;
		case 109: goto st109;
		case 110: goto st110;
		case 111: goto st111;
		case 112: goto st112;
		case 113: goto st113;
		case 114: goto st114;
		case 115: goto st115;
		case 116: goto st116;
		case 117: goto st117;
		case 118: goto st118;
		case 119: goto st119;
		case 120: goto st120;
		case 121: goto st121;
		case 122: goto st122;
		case 123: goto st123;
		case 124: goto st124;
		case 125: goto st125;
		case 126: goto st126;
		case 127: goto st127;
		case 128: goto st128;
		case 129: goto st129;
		case 130: goto st130;
		case 131: goto st131;
		case 132: goto st132;
		case 133: goto st133;
		case 134: goto st134;
		case 135: goto st135;
		case 136: goto st136;
		case 137: goto st137;
		case 138: goto st138;
		case 139: goto st139;
		case 140: goto st140;
		case 141: goto st141;
		case 142: goto st142;
		case 143: goto st143;
		case 144: goto st144;
		case 145: goto st145;
		case 146: goto st146;
		case 147: goto st147;
		case 148: goto st148;
		case 149: goto st149;
		case 150: goto st150;
		case 151: goto st151;
		case 152: goto st152;
		case 153: goto st153;
		case 154: goto st154;
		case 155: goto st155;
		case 156: goto st156;
		case 157: goto st157;
		case 158: goto st158;
		case 159: goto st159;
		case 160: goto st160;
		case 161: goto st161;
		case 162: goto st162;
		case 163: goto st163;
		case 164: goto st164;
		case 165: goto st165;
		case 166: goto st166;
		case 167: goto st167;
		case 168: goto st168;
		case 169: goto st169;
		case 170: goto st170;
		case 171: goto st171;
		case 172: goto st172;
		case 173: goto st173;
		case 174: goto st174;
		case 175: goto st175;
		case 176: goto st176;
		case 177: goto st177;
		case 178: goto st178;
		case 179: goto st179;
		case 180: goto st180;
		case 181: goto st181;
		case 182: goto st182;
		case 183: goto st183;
		case 184: goto st184;
		case 185: goto st185;
		case 186: goto st186;
		case 187: goto st187;
		case 188: goto st188;
		case 189: goto st189;
		case 190: goto st190;
		case 191: goto st191;
		case 192: goto st192;
		case 193: goto st193;
		case 194: goto st194;
		case 195: goto st195;
		case 196: goto st196;
		case 197: goto st197;
		case 198: goto st198;
		case 199: goto st199;
		case 200: goto st200;
		case 201: goto st201;
		case 202: goto st202;
		case 203: goto st203;
		case 204: goto st204;
		case 205: goto st205;
		case 206: goto st206;
		case 207: goto st207;
		case 208: goto st208;
		case 209: goto st209;
		case 210: goto st210;
		case 211: goto st211;
		case 212: goto st212;
		case 213: goto st213;
		case 214: goto st214;
		case 215: goto st215;
		case 216: goto st216;
		case 217: goto st217;
		case 218: goto st218;
		case 219: goto st219;
		case 220: goto st220;
		case 221: goto st221;
		case 222: goto st222;
		case 223: goto st223;
		case 224: goto st224;
		case 225: goto st225;
		case 226: goto st226;
		case 227: goto st227;
		case 228: goto st228;
		case 229: goto st229;
		case 230: goto st230;
		case 231: goto st231;
		case 232: goto st232;
		case 233: goto st233;
		case 234: goto st234;
		case 235: goto st235;
		case 236: goto st236;
		case 237: goto st237;
		case 238: goto st238;
		case 239: goto st239;
		case 240: goto st240;
		case 241: goto st241;
		case 242: goto st242;
		case 243: goto st243;
		case 244: goto st244;
		case 245: goto st245;
		case 246: goto st246;
		case 247: goto st247;
		case 248: goto st248;
		case 249: goto st249;
		case 250: goto st250;
		case 251: goto st251;
		case 252: goto st252;
		case 253: goto st253;
		case 254: goto st254;
		case 255: goto st255;
		case 256: goto st256;
		case 257: goto st257;
		case 258: goto st258;
		case 259: goto st259;
		case 260: goto st260;
		case 261: goto st261;
		case 262: goto st262;
		case 263: goto st263;
		case 264: goto st264;
		case 265: goto st265;
		case 266: goto st266;
		case 267: goto st267;
		case 268: goto st268;
		case 269: goto st269;
		case 270: goto st270;
		case 271: goto st271;
		case 272: goto st272;
		case 273: goto st273;
		case 274: goto st274;
		case 275: goto st275;
		case 276: goto st276;
		case 277: goto st277;
		case 278: goto st278;
		case 279: goto st279;
		case 280: goto st280;
		case 281: goto st281;
		case 282: goto st282;
		case 283: goto st283;
		case 284: goto st284;
		case 285: goto st285;
		case 286: goto st286;
		case 287: goto st287;
		case 288: goto st288;
		case 289: goto st289;
		case 290: goto st290;
		case 291: goto st291;
		case 292: goto st292;
		case 293: goto st293;
		case 294: goto st294;
		case 295: goto st295;
		case 296: goto st296;
		case 297: goto st297;
		case 298: goto st298;
		case 299: goto st299;
		case 300: goto st300;
		case 301: goto st301;
		case 302: goto st302;
		case 303: goto st303;
		case 304: goto st304;
		case 305: goto st305;
		case 306: goto st306;
		case 307: goto st307;
		case 308: goto st308;
		case 309: goto st309;
		case 310: goto st310;
		case 311: goto st311;
		case 312: goto st312;
		case 313: goto st313;
		case 314: goto st314;
		case 315: goto st315;
		case 316: goto st316;
		case 317: goto st317;
		case 318: goto st318;
		case 319: goto st319;
		case 320: goto st320;
		case 321: goto st321;
		case 322: goto st322;
		case 323: goto st323;
		case 324: goto st324;
		case 325: goto st325;
		case 326: goto st326;
		case 327: goto st327;
		case 328: goto st328;
		case 329: goto st329;
		case 330: goto st330;
		case 331: goto st331;
		case 332: goto st332;
		case 333: goto st333;
		case 334: goto st334;
		case 335: goto st335;
		case 336: goto st336;
		case 337: goto st337;
		case 338: goto st338;
		case 339: goto st339;
		case 340: goto st340;
		case 341: goto st341;
		case 342: goto st342;
		case 343: goto st343;
		case 344: goto st344;
		case 345: goto st345;
		case 1358: goto st1358;
		case 346: goto st346;
		case 347: goto st347;
		case 348: goto st348;
		case 349: goto st349;
		case 350: goto st350;
		case 351: goto st351;
		case 352: goto st352;
		case 353: goto st353;
		case 354: goto st354;
		case 355: goto st355;
		case 356: goto st356;
		case 357: goto st357;
		case 358: goto st358;
		case 359: goto st359;
		case 360: goto st360;
		case 361: goto st361;
		case 362: goto st362;
		case 363: goto st363;
		case 364: goto st364;
		case 365: goto st365;
		case 366: goto st366;
		case 367: goto st367;
		case 368: goto st368;
		case 369: goto st369;
		case 370: goto st370;
		case 371: goto st371;
		case 372: goto st372;
		case 373: goto st373;
		case 374: goto st374;
		case 375: goto st375;
		case 376: goto st376;
		case 377: goto st377;
		case 378: goto st378;
		case 379: goto st379;
		case 380: goto st380;
		case 381: goto st381;
		case 382: goto st382;
		case 383: goto st383;
		case 384: goto st384;
		case 385: goto st385;
		case 386: goto st386;
		case 387: goto st387;
		case 388: goto st388;
		case 389: goto st389;
		case 390: goto st390;
		case 391: goto st391;
		case 392: goto st392;
		case 393: goto st393;
		case 394: goto st394;
		case 395: goto st395;
		case 396: goto st396;
		case 397: goto st397;
		case 398: goto st398;
		case 399: goto st399;
		case 400: goto st400;
		case 401: goto st401;
		case 402: goto st402;
		case 403: goto st403;
		case 404: goto st404;
		case 405: goto st405;
		case 406: goto st406;
		case 407: goto st407;
		case 408: goto st408;
		case 409: goto st409;
		case 410: goto st410;
		case 411: goto st411;
		case 412: goto st412;
		case 413: goto st413;
		case 414: goto st414;
		case 415: goto st415;
		case 416: goto st416;
		case 417: goto st417;
		case 418: goto st418;
		case 419: goto st419;
		case 420: goto st420;
		case 421: goto st421;
		case 422: goto st422;
		case 423: goto st423;
		case 424: goto st424;
		case 425: goto st425;
		case 426: goto st426;
		case 427: goto st427;
		case 428: goto st428;
		case 429: goto st429;
		case 430: goto st430;
		case 431: goto st431;
		case 432: goto st432;
		case 433: goto st433;
		case 434: goto st434;
		case 435: goto st435;
		case 436: goto st436;
		case 437: goto st437;
		case 438: goto st438;
		case 439: goto st439;
		case 440: goto st440;
		case 441: goto st441;
		case 442: goto st442;
		case 443: goto st443;
		case 444: goto st444;
		case 445: goto st445;
		case 446: goto st446;
		case 447: goto st447;
		case 448: goto st448;
		case 449: goto st449;
		case 450: goto st450;
		case 451: goto st451;
		case 452: goto st452;
		case 453: goto st453;
		case 454: goto st454;
		case 455: goto st455;
		case 456: goto st456;
		case 457: goto st457;
		case 458: goto st458;
		case 459: goto st459;
		case 460: goto st460;
		case 461: goto st461;
		case 462: goto st462;
		case 463: goto st463;
		case 464: goto st464;
		case 465: goto st465;
		case 466: goto st466;
		case 467: goto st467;
		case 468: goto st468;
		case 469: goto st469;
		case 470: goto st470;
		case 471: goto st471;
		case 472: goto st472;
		case 473: goto st473;
		case 474: goto st474;
		case 475: goto st475;
		case 476: goto st476;
		case 477: goto st477;
		case 478: goto st478;
		case 479: goto st479;
		case 480: goto st480;
		case 481: goto st481;
		case 482: goto st482;
		case 483: goto st483;
		case 484: goto st484;
		case 485: goto st485;
		case 486: goto st486;
		case 487: goto st487;
		case 488: goto st488;
		case 489: goto st489;
		case 490: goto st490;
		case 491: goto st491;
		case 1359: goto st1359;
		case 492: goto st492;
		case 493: goto st493;
		case 494: goto st494;
		case 495: goto st495;
		case 496: goto st496;
		case 497: goto st497;
		case 498: goto st498;
		case 499: goto st499;
		case 500: goto st500;
		case 501: goto st501;
		case 502: goto st502;
		case 503: goto st503;
		case 504: goto st504;
		case 505: goto st505;
		case 506: goto st506;
		case 507: goto st507;
		case 508: goto st508;
		case 509: goto st509;
		case 510: goto st510;
		case 511: goto st511;
		case 512: goto st512;
		case 513: goto st513;
		case 514: goto st514;
		case 515: goto st515;
		case 516: goto st516;
		case 517: goto st517;
		case 518: goto st518;
		case 519: goto st519;
		case 520: goto st520;
		case 521: goto st521;
		case 522: goto st522;
		case 523: goto st523;
		case 524: goto st524;
		case 525: goto st525;
		case 526: goto st526;
		case 527: goto st527;
		case 528: goto st528;
		case 529: goto st529;
		case 530: goto st530;
		case 531: goto st531;
		case 532: goto st532;
		case 533: goto st533;
		case 534: goto st534;
		case 535: goto st535;
		case 536: goto st536;
		case 537: goto st537;
		case 538: goto st538;
		case 539: goto st539;
		case 540: goto st540;
		case 541: goto st541;
		case 542: goto st542;
		case 543: goto st543;
		case 544: goto st544;
		case 545: goto st545;
		case 546: goto st546;
		case 547: goto st547;
		case 548: goto st548;
		case 549: goto st549;
		case 550: goto st550;
		case 551: goto st551;
		case 552: goto st552;
		case 553: goto st553;
		case 554: goto st554;
		case 555: goto st555;
		case 556: goto st556;
		case 557: goto st557;
		case 558: goto st558;
		case 559: goto st559;
		case 560: goto st560;
		case 561: goto st561;
		case 562: goto st562;
		case 563: goto st563;
		case 564: goto st564;
		case 565: goto st565;
		case 566: goto st566;
		case 567: goto st567;
		case 568: goto st568;
		case 569: goto st569;
		case 570: goto st570;
		case 571: goto st571;
		case 572: goto st572;
		case 573: goto st573;
		case 574: goto st574;
		case 575: goto st575;
		case 576: goto st576;
		case 577: goto st577;
		case 578: goto st578;
		case 579: goto st579;
		case 580: goto st580;
		case 581: goto st581;
		case 582: goto st582;
		case 583: goto st583;
		case 584: goto st584;
		case 585: goto st585;
		case 586: goto st586;
		case 587: goto st587;
		case 588: goto st588;
		case 589: goto st589;
		case 590: goto st590;
		case 591: goto st591;
		case 592: goto st592;
		case 593: goto st593;
		case 594: goto st594;
		case 595: goto st595;
		case 596: goto st596;
		case 597: goto st597;
		case 598: goto st598;
		case 599: goto st599;
		case 600: goto st600;
		case 601: goto st601;
		case 602: goto st602;
		case 603: goto st603;
		case 604: goto st604;
		case 605: goto st605;
		case 606: goto st606;
		case 607: goto st607;
		case 608: goto st608;
		case 609: goto st609;
		case 610: goto st610;
		case 611: goto st611;
		case 612: goto st612;
		case 613: goto st613;
		case 614: goto st614;
		case 615: goto st615;
		case 616: goto st616;
		case 617: goto st617;
		case 618: goto st618;
		case 619: goto st619;
		case 620: goto st620;
		case 621: goto st621;
		case 622: goto st622;
		case 623: goto st623;
		case 624: goto st624;
		case 625: goto st625;
		case 626: goto st626;
		case 627: goto st627;
		case 628: goto st628;
		case 629: goto st629;
		case 630: goto st630;
		case 631: goto st631;
		case 632: goto st632;
		case 633: goto st633;
		case 634: goto st634;
		case 635: goto st635;
		case 636: goto st636;
		case 637: goto st637;
		case 638: goto st638;
		case 639: goto st639;
		case 640: goto st640;
		case 641: goto st641;
		case 642: goto st642;
		case 643: goto st643;
		case 644: goto st644;
		case 645: goto st645;
		case 646: goto st646;
		case 647: goto st647;
		case 648: goto st648;
		case 649: goto st649;
		case 650: goto st650;
		case 651: goto st651;
		case 652: goto st652;
		case 653: goto st653;
		case 654: goto st654;
		case 655: goto st655;
		case 1360: goto st1360;
		case 656: goto st656;
		case 657: goto st657;
		case 658: goto st658;
		case 659: goto st659;
		case 660: goto st660;
		case 661: goto st661;
		case 662: goto st662;
		case 663: goto st663;
		case 664: goto st664;
		case 665: goto st665;
		case 666: goto st666;
		case 667: goto st667;
		case 668: goto st668;
		case 669: goto st669;
		case 670: goto st670;
		case 671: goto st671;
		case 672: goto st672;
		case 673: goto st673;
		case 674: goto st674;
		case 675: goto st675;
		case 676: goto st676;
		case 677: goto st677;
		case 678: goto st678;
		case 679: goto st679;
		case 680: goto st680;
		case 681: goto st681;
		case 682: goto st682;
		case 683: goto st683;
		case 684: goto st684;
		case 685: goto st685;
		case 686: goto st686;
		case 687: goto st687;
		case 688: goto st688;
		case 689: goto st689;
		case 690: goto st690;
		case 691: goto st691;
		case 692: goto st692;
		case 693: goto st693;
		case 694: goto st694;
		case 695: goto st695;
		case 696: goto st696;
		case 697: goto st697;
		case 698: goto st698;
		case 699: goto st699;
		case 700: goto st700;
		case 701: goto st701;
		case 702: goto st702;
		case 703: goto st703;
		case 704: goto st704;
		case 705: goto st705;
		case 706: goto st706;
		case 707: goto st707;
		case 708: goto st708;
		case 709: goto st709;
		case 710: goto st710;
		case 711: goto st711;
		case 712: goto st712;
		case 713: goto st713;
		case 714: goto st714;
		case 715: goto st715;
		case 716: goto st716;
		case 717: goto st717;
		case 718: goto st718;
		case 719: goto st719;
		case 720: goto st720;
		case 721: goto st721;
		case 722: goto st722;
		case 723: goto st723;
		case 724: goto st724;
		case 725: goto st725;
		case 726: goto st726;
		case 727: goto st727;
		case 728: goto st728;
		case 729: goto st729;
		case 730: goto st730;
		case 731: goto st731;
		case 732: goto st732;
		case 733: goto st733;
		case 734: goto st734;
		case 735: goto st735;
		case 736: goto st736;
		case 737: goto st737;
		case 738: goto st738;
		case 739: goto st739;
		case 740: goto st740;
		case 741: goto st741;
		case 742: goto st742;
		case 743: goto st743;
		case 744: goto st744;
		case 745: goto st745;
		case 746: goto st746;
		case 747: goto st747;
		case 748: goto st748;
		case 749: goto st749;
		case 750: goto st750;
		case 751: goto st751;
		case 752: goto st752;
		case 753: goto st753;
		case 754: goto st754;
		case 755: goto st755;
		case 756: goto st756;
		case 757: goto st757;
		case 758: goto st758;
		case 759: goto st759;
		case 760: goto st760;
		case 761: goto st761;
		case 762: goto st762;
		case 763: goto st763;
		case 764: goto st764;
		case 765: goto st765;
		case 766: goto st766;
		case 767: goto st767;
		case 768: goto st768;
		case 769: goto st769;
		case 770: goto st770;
		case 771: goto st771;
		case 772: goto st772;
		case 773: goto st773;
		case 774: goto st774;
		case 775: goto st775;
		case 776: goto st776;
		case 777: goto st777;
		case 778: goto st778;
		case 779: goto st779;
		case 780: goto st780;
		case 781: goto st781;
		case 782: goto st782;
		case 783: goto st783;
		case 784: goto st784;
		case 785: goto st785;
		case 786: goto st786;
		case 787: goto st787;
		case 788: goto st788;
		case 789: goto st789;
		case 790: goto st790;
		case 791: goto st791;
		case 792: goto st792;
		case 793: goto st793;
		case 794: goto st794;
		case 795: goto st795;
		case 796: goto st796;
		case 797: goto st797;
		case 798: goto st798;
		case 799: goto st799;
		case 800: goto st800;
		case 801: goto st801;
		case 802: goto st802;
		case 803: goto st803;
		case 804: goto st804;
		case 805: goto st805;
		case 806: goto st806;
		case 807: goto st807;
		case 808: goto st808;
		case 809: goto st809;
		case 810: goto st810;
		case 811: goto st811;
		case 812: goto st812;
		case 813: goto st813;
		case 814: goto st814;
		case 815: goto st815;
		case 816: goto st816;
		case 817: goto st817;
		case 818: goto st818;
		case 819: goto st819;
		case 820: goto st820;
		case 821: goto st821;
		case 822: goto st822;
		case 823: goto st823;
		case 824: goto st824;
		case 825: goto st825;
		case 826: goto st826;
		case 827: goto st827;
		case 828: goto st828;
		case 829: goto st829;
		case 830: goto st830;
		case 831: goto st831;
		case 832: goto st832;
		case 833: goto st833;
		case 834: goto st834;
		case 835: goto st835;
		case 836: goto st836;
		case 837: goto st837;
		case 838: goto st838;
		case 839: goto st839;
		case 840: goto st840;
		case 841: goto st841;
		case 842: goto st842;
		case 843: goto st843;
		case 844: goto st844;
		case 845: goto st845;
		case 846: goto st846;
		case 847: goto st847;
		case 848: goto st848;
		case 849: goto st849;
		case 850: goto st850;
		case 851: goto st851;
		case 852: goto st852;
		case 853: goto st853;
		case 854: goto st854;
		case 855: goto st855;
		case 856: goto st856;
		case 857: goto st857;
		case 858: goto st858;
		case 859: goto st859;
		case 860: goto st860;
		case 861: goto st861;
		case 862: goto st862;
		case 863: goto st863;
		case 864: goto st864;
		case 865: goto st865;
		case 866: goto st866;
		case 867: goto st867;
		case 868: goto st868;
		case 869: goto st869;
		case 870: goto st870;
		case 871: goto st871;
		case 872: goto st872;
		case 873: goto st873;
		case 874: goto st874;
		case 875: goto st875;
		case 876: goto st876;
		case 877: goto st877;
		case 878: goto st878;
		case 879: goto st879;
		case 880: goto st880;
		case 881: goto st881;
		case 882: goto st882;
		case 883: goto st883;
		case 884: goto st884;
		case 885: goto st885;
		case 886: goto st886;
		case 887: goto st887;
		case 888: goto st888;
		case 889: goto st889;
		case 890: goto st890;
		case 891: goto st891;
		case 892: goto st892;
		case 893: goto st893;
		case 894: goto st894;
		case 895: goto st895;
		case 896: goto st896;
		case 897: goto st897;
		case 898: goto st898;
		case 899: goto st899;
		case 900: goto st900;
		case 901: goto st901;
		case 902: goto st902;
		case 903: goto st903;
		case 904: goto st904;
		case 905: goto st905;
		case 906: goto st906;
		case 907: goto st907;
		case 908: goto st908;
		case 909: goto st909;
		case 910: goto st910;
		case 911: goto st911;
		case 912: goto st912;
		case 913: goto st913;
		case 914: goto st914;
		case 915: goto st915;
		case 916: goto st916;
		case 917: goto st917;
		case 918: goto st918;
		case 919: goto st919;
		case 920: goto st920;
		case 921: goto st921;
		case 922: goto st922;
		case 923: goto st923;
		case 924: goto st924;
		case 925: goto st925;
		case 926: goto st926;
		case 927: goto st927;
		case 928: goto st928;
		case 929: goto st929;
		case 930: goto st930;
		case 931: goto st931;
		case 932: goto st932;
		case 933: goto st933;
		case 934: goto st934;
		case 935: goto st935;
		case 936: goto st936;
		case 937: goto st937;
		case 938: goto st938;
		case 939: goto st939;
		case 940: goto st940;
		case 941: goto st941;
		case 942: goto st942;
		case 943: goto st943;
		case 944: goto st944;
		case 945: goto st945;
		case 946: goto st946;
		case 947: goto st947;
		case 948: goto st948;
		case 949: goto st949;
		case 950: goto st950;
		case 951: goto st951;
		case 952: goto st952;
		case 953: goto st953;
		case 954: goto st954;
		case 955: goto st955;
		case 956: goto st956;
		case 957: goto st957;
		case 958: goto st958;
		case 959: goto st959;
		case 960: goto st960;
		case 961: goto st961;
		case 962: goto st962;
		case 963: goto st963;
		case 964: goto st964;
		case 965: goto st965;
		case 966: goto st966;
		case 967: goto st967;
		case 968: goto st968;
		case 969: goto st969;
		case 970: goto st970;
		case 971: goto st971;
		case 972: goto st972;
		case 973: goto st973;
		case 974: goto st974;
		case 975: goto st975;
		case 976: goto st976;
		case 977: goto st977;
		case 978: goto st978;
		case 979: goto st979;
		case 980: goto st980;
		case 981: goto st981;
		case 982: goto st982;
		case 983: goto st983;
		case 984: goto st984;
		case 985: goto st985;
		case 986: goto st986;
		case 987: goto st987;
		case 988: goto st988;
		case 989: goto st989;
		case 990: goto st990;
		case 991: goto st991;
		case 992: goto st992;
		case 993: goto st993;
		case 994: goto st994;
		case 995: goto st995;
		case 996: goto st996;
		case 997: goto st997;
		case 998: goto st998;
		case 999: goto st999;
		case 1000: goto st1000;
		case 1001: goto st1001;
		case 1002: goto st1002;
		case 1003: goto st1003;
		case 1004: goto st1004;
		case 1005: goto st1005;
		case 1006: goto st1006;
		case 1007: goto st1007;
		case 1008: goto st1008;
		case 1009: goto st1009;
		case 1010: goto st1010;
		case 1011: goto st1011;
		case 1012: goto st1012;
		case 1013: goto st1013;
		case 1014: goto st1014;
		case 1015: goto st1015;
		case 1016: goto st1016;
		case 1017: goto st1017;
		case 1018: goto st1018;
		case 1019: goto st1019;
		case 1020: goto st1020;
		case 1021: goto st1021;
		case 1022: goto st1022;
		case 1023: goto st1023;
		case 1024: goto st1024;
		case 1025: goto st1025;
		case 1026: goto st1026;
		case 1027: goto st1027;
		case 1028: goto st1028;
		case 1029: goto st1029;
		case 1030: goto st1030;
		case 1031: goto st1031;
		case 1032: goto st1032;
		case 1033: goto st1033;
		case 1034: goto st1034;
		case 1035: goto st1035;
		case 1036: goto st1036;
		case 1037: goto st1037;
		case 1038: goto st1038;
		case 1039: goto st1039;
		case 1040: goto st1040;
		case 1041: goto st1041;
		case 1042: goto st1042;
		case 1043: goto st1043;
		case 1044: goto st1044;
		case 1045: goto st1045;
		case 1046: goto st1046;
		case 1047: goto st1047;
		case 1048: goto st1048;
		case 1049: goto st1049;
		case 1050: goto st1050;
		case 1051: goto st1051;
		case 1052: goto st1052;
		case 1053: goto st1053;
		case 1054: goto st1054;
		case 1055: goto st1055;
		case 1056: goto st1056;
		case 1057: goto st1057;
		case 1058: goto st1058;
		case 1059: goto st1059;
		case 1060: goto st1060;
		case 1061: goto st1061;
		case 1062: goto st1062;
		case 1063: goto st1063;
		case 1064: goto st1064;
		case 1065: goto st1065;
		case 1066: goto st1066;
		case 1067: goto st1067;
		case 1068: goto st1068;
		case 1069: goto st1069;
		case 1070: goto st1070;
		case 1071: goto st1071;
		case 1072: goto st1072;
		case 1073: goto st1073;
		case 1074: goto st1074;
		case 1075: goto st1075;
		case 1076: goto st1076;
		case 1077: goto st1077;
		case 1078: goto st1078;
		case 1079: goto st1079;
		case 1080: goto st1080;
		case 1081: goto st1081;
		case 1082: goto st1082;
		case 1083: goto st1083;
		case 1084: goto st1084;
		case 1085: goto st1085;
		case 1086: goto st1086;
		case 1087: goto st1087;
		case 1088: goto st1088;
		case 1089: goto st1089;
		case 1090: goto st1090;
		case 1091: goto st1091;
		case 1092: goto st1092;
		case 1093: goto st1093;
		case 1094: goto st1094;
		case 1095: goto st1095;
		case 1096: goto st1096;
		case 1097: goto st1097;
		case 1098: goto st1098;
		case 1099: goto st1099;
		case 1100: goto st1100;
		case 1101: goto st1101;
		case 1102: goto st1102;
		case 1103: goto st1103;
		case 1104: goto st1104;
		case 1105: goto st1105;
		case 1106: goto st1106;
		case 1107: goto st1107;
		case 1108: goto st1108;
		case 1109: goto st1109;
		case 1110: goto st1110;
		case 1111: goto st1111;
		case 1112: goto st1112;
		case 1113: goto st1113;
		case 1114: goto st1114;
		case 1115: goto st1115;
		case 1116: goto st1116;
		case 1117: goto st1117;
		case 1118: goto st1118;
		case 1119: goto st1119;
		case 1120: goto st1120;
		case 1121: goto st1121;
		case 1122: goto st1122;
		case 1123: goto st1123;
		case 1124: goto st1124;
		case 1125: goto st1125;
		case 1126: goto st1126;
		case 1127: goto st1127;
		case 1128: goto st1128;
		case 1129: goto st1129;
		case 1130: goto st1130;
		case 1131: goto st1131;
		case 1132: goto st1132;
		case 1133: goto st1133;
		case 1134: goto st1134;
		case 1135: goto st1135;
		case 1136: goto st1136;
		case 1137: goto st1137;
		case 1138: goto st1138;
		case 1139: goto st1139;
		case 1140: goto st1140;
		case 1141: goto st1141;
		case 1142: goto st1142;
		case 1143: goto st1143;
		case 1144: goto st1144;
		case 1145: goto st1145;
		case 1146: goto st1146;
		case 1147: goto st1147;
		case 1148: goto st1148;
		case 1149: goto st1149;
		case 1150: goto st1150;
		case 1151: goto st1151;
		case 1152: goto st1152;
		case 1153: goto st1153;
		case 1154: goto st1154;
		case 1155: goto st1155;
		case 1156: goto st1156;
		case 1157: goto st1157;
		case 1158: goto st1158;
		case 1159: goto st1159;
		case 1160: goto st1160;
		case 1161: goto st1161;
		case 1162: goto st1162;
		case 1163: goto st1163;
		case 1164: goto st1164;
		case 1165: goto st1165;
		case 1166: goto st1166;
		case 1167: goto st1167;
		case 1168: goto st1168;
		case 1169: goto st1169;
		case 1170: goto st1170;
		case 1171: goto st1171;
		case 1172: goto st1172;
		case 1173: goto st1173;
		case 1174: goto st1174;
		case 1175: goto st1175;
		case 1176: goto st1176;
		case 1177: goto st1177;
		case 1178: goto st1178;
		case 1179: goto st1179;
		case 1180: goto st1180;
		case 1181: goto st1181;
		case 1182: goto st1182;
		case 1183: goto st1183;
		case 1184: goto st1184;
		case 1185: goto st1185;
		case 1186: goto st1186;
		case 1187: goto st1187;
		case 1188: goto st1188;
		case 1189: goto st1189;
		case 1190: goto st1190;
		case 1191: goto st1191;
		case 1192: goto st1192;
		case 1193: goto st1193;
		case 1194: goto st1194;
		case 1195: goto st1195;
		case 1196: goto st1196;
		case 1197: goto st1197;
		case 1198: goto st1198;
		case 1199: goto st1199;
		case 1200: goto st1200;
		case 1201: goto st1201;
		case 1202: goto st1202;
		case 1203: goto st1203;
		case 1204: goto st1204;
		case 1205: goto st1205;
		case 1206: goto st1206;
		case 1207: goto st1207;
		case 1208: goto st1208;
		case 1209: goto st1209;
		case 1210: goto st1210;
		case 1211: goto st1211;
		case 1212: goto st1212;
		case 1213: goto st1213;
		case 1214: goto st1214;
		case 1215: goto st1215;
		case 1216: goto st1216;
		case 1217: goto st1217;
		case 1218: goto st1218;
		case 1219: goto st1219;
		case 1220: goto st1220;
		case 1221: goto st1221;
		case 1222: goto st1222;
		case 1223: goto st1223;
		case 1224: goto st1224;
		case 1225: goto st1225;
		case 1226: goto st1226;
		case 1227: goto st1227;
		case 1228: goto st1228;
		case 1229: goto st1229;
		case 1230: goto st1230;
		case 1231: goto st1231;
		case 1232: goto st1232;
		case 1233: goto st1233;
		case 1234: goto st1234;
		case 1235: goto st1235;
		case 1236: goto st1236;
		case 1237: goto st1237;
		case 1238: goto st1238;
		case 1239: goto st1239;
		case 1240: goto st1240;
		case 1241: goto st1241;
		case 1242: goto st1242;
		case 1243: goto st1243;
		case 1244: goto st1244;
		case 1245: goto st1245;
		case 1246: goto st1246;
		case 1247: goto st1247;
		case 1248: goto st1248;
		case 1249: goto st1249;
		case 1250: goto st1250;
		case 1251: goto st1251;
		case 1252: goto st1252;
		case 1253: goto st1253;
		case 1254: goto st1254;
		case 1255: goto st1255;
		case 1256: goto st1256;
		case 1257: goto st1257;
		case 1258: goto st1258;
		case 1259: goto st1259;
		case 1260: goto st1260;
		case 1261: goto st1261;
		case 1262: goto st1262;
		case 1263: goto st1263;
		case 1264: goto st1264;
		case 1265: goto st1265;
		case 1266: goto st1266;
		case 1267: goto st1267;
		case 1268: goto st1268;
		case 1269: goto st1269;
		case 1270: goto st1270;
		case 1271: goto st1271;
		case 1272: goto st1272;
		case 1273: goto st1273;
		case 1274: goto st1274;
		case 1275: goto st1275;
		case 1276: goto st1276;
		case 1277: goto st1277;
		case 1278: goto st1278;
		case 1279: goto st1279;
		case 1280: goto st1280;
		case 1281: goto st1281;
		case 1282: goto st1282;
		case 1283: goto st1283;
		case 1284: goto st1284;
		case 1285: goto st1285;
		case 1286: goto st1286;
		case 1287: goto st1287;
		case 1288: goto st1288;
		case 1289: goto st1289;
		case 1290: goto st1290;
		case 1291: goto st1291;
		case 1292: goto st1292;
		case 1293: goto st1293;
		case 1294: goto st1294;
		case 1295: goto st1295;
		case 1296: goto st1296;
		case 1297: goto st1297;
		case 1298: goto st1298;
		case 1299: goto st1299;
		case 1300: goto st1300;
		case 1301: goto st1301;
		case 1302: goto st1302;
		case 1303: goto st1303;
		case 1304: goto st1304;
		case 1305: goto st1305;
		case 1306: goto st1306;
		case 1307: goto st1307;
		case 1308: goto st1308;
		case 1309: goto st1309;
		case 1310: goto st1310;
		case 1311: goto st1311;
		case 1312: goto st1312;
		case 1313: goto st1313;
		case 1314: goto st1314;
		case 1315: goto st1315;
		case 1316: goto st1316;
		case 1317: goto st1317;
		case 1318: goto st1318;
		case 1319: goto st1319;
		case 1320: goto st1320;
		case 1321: goto st1321;
		case 1322: goto st1322;
		case 1323: goto st1323;
		case 1324: goto st1324;
		case 1325: goto st1325;
		case 1326: goto st1326;
		case 1327: goto st1327;
		case 1328: goto st1328;
		case 1329: goto st1329;
		case 1330: goto st1330;
		case 1331: goto st1331;
		case 1332: goto st1332;
		case 1333: goto st1333;
		case 1334: goto st1334;
		case 1335: goto st1335;
		case 1336: goto st1336;
		case 1337: goto st1337;
		case 1338: goto st1338;
		case 1339: goto st1339;
		case 1340: goto st1340;
		case 1341: goto st1341;
		case 1342: goto st1342;
		case 1343: goto st1343;
		case 1344: goto st1344;
		case 1345: goto st1345;
		case 1346: goto st1346;
		case 1347: goto st1347;
		case 1348: goto st1348;
		case 1349: goto st1349;
		case 1350: goto st1350;
	default: break;
	}

	if ( ++( state.p) == ( state.pe) )
		goto _test_eof;
_resume:
	switch (  state.cs )
	{
st1:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1;
case 1:
	switch( (*( state.p)) ) {
		case 13: goto st1;
		case 32: goto st1;
		case 100: goto st2;
		case 108: goto st13;
		case 115: goto st25;
		case 116: goto st37;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1;
	goto st0;
st0:
 state.cs = 0;
	goto _out;
tr2068:
#line 285 "configparser.rl"
	{ init_design(des); }
	goto st2;
tr2074:
#line 366 "configparser.rl"
	{ init_levelskin_(lev); }
	goto st2;
tr2079:
#line 247 "configparser.rl"
	{ init_species(spe); }
	goto st2;
tr2084:
#line 327 "configparser.rl"
	{ init_terrain(ter); }
	goto st2;
st2:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof2;
case 2:
#line 1568 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st3;
	goto st0;
st3:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof3;
case 3:
	if ( (*( state.p)) == 115 )
		goto st4;
	goto st0;
st4:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof4;
case 4:
	if ( (*( state.p)) == 105 )
		goto st5;
	goto st0;
st5:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof5;
case 5:
	if ( (*( state.p)) == 103 )
		goto st6;
	goto st0;
st6:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof6;
case 6:
	if ( (*( state.p)) == 110 )
		goto st7;
	goto st0;
st7:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof7;
case 7:
	switch( (*( state.p)) ) {
		case 13: goto tr11;
		case 32: goto tr11;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr11;
	goto st0;
tr11:
#line 282 "configparser.rl"
	{ des = Design(); }
	goto st8;
st8:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof8;
case 8:
#line 1619 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st8;
		case 32: goto st8;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr13;
	} else if ( (*( state.p)) >= 9 )
		goto st8;
	goto st0;
tr13:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st9;
tr15:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st9;
st9:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof9;
case 9:
#line 1650 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr14;
		case 32: goto tr14;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr15;
	} else if ( (*( state.p)) >= 9 )
		goto tr14;
	goto st0;
tr14:
#line 275 "configparser.rl"
	{ des.level = toint(state.match); }
	goto st10;
st10:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof10;
case 10:
#line 1669 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st10;
		case 32: goto st10;
		case 95: goto tr17;
	}
	if ( (*( state.p)) < 48 ) {
		if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
			goto st10;
	} else if ( (*( state.p)) > 57 ) {
		if ( (*( state.p)) > 90 ) {
			if ( 97 <= (*( state.p)) && (*( state.p)) <= 122 )
				goto tr17;
		} else if ( (*( state.p)) >= 65 )
			goto tr17;
	} else
		goto tr17;
	goto st0;
tr17:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st11;
tr19:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st11;
st11:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof11;
case 11:
#line 1707 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr18;
		case 32: goto tr18;
		case 95: goto tr19;
		case 123: goto tr20;
	}
	if ( (*( state.p)) < 48 ) {
		if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
			goto tr18;
	} else if ( (*( state.p)) > 57 ) {
		if ( (*( state.p)) > 90 ) {
			if ( 97 <= (*( state.p)) && (*( state.p)) <= 122 )
				goto tr19;
		} else if ( (*( state.p)) >= 65 )
			goto tr19;
	} else
		goto tr19;
	goto st0;
tr18:
#line 278 "configparser.rl"
	{ des.tag = state.match; }
	goto st12;
st12:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof12;
case 12:
#line 1734 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st12;
		case 32: goto st12;
		case 123: goto tr22;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st12;
	goto st0;
tr20:
#line 278 "configparser.rl"
	{ des.tag = state.match; }
#line 284 "configparser.rl"
	{{ state.stack[ state.top++] = 1351; goto st335;}}
	goto st1351;
tr22:
#line 284 "configparser.rl"
	{{ state.stack[ state.top++] = 1351; goto st335;}}
	goto st1351;
st1351:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1351;
case 1351:
#line 1757 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr2067;
		case 32: goto tr2067;
		case 100: goto tr2068;
		case 108: goto tr2069;
		case 115: goto tr2070;
		case 116: goto tr2071;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr2067;
	goto st0;
tr2067:
#line 285 "configparser.rl"
	{ init_design(des); }
	goto st1352;
tr2073:
#line 366 "configparser.rl"
	{ init_levelskin_(lev); }
	goto st1352;
tr2078:
#line 247 "configparser.rl"
	{ init_species(spe); }
	goto st1352;
tr2083:
#line 327 "configparser.rl"
	{ init_terrain(ter); }
	goto st1352;
st1352:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1352;
case 1352:
#line 1789 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st1352;
		case 32: goto st1352;
		case 100: goto st2;
		case 108: goto st13;
		case 115: goto st25;
		case 116: goto st37;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1352;
	goto st0;
tr2069:
#line 285 "configparser.rl"
	{ init_design(des); }
	goto st13;
tr2075:
#line 366 "configparser.rl"
	{ init_levelskin_(lev); }
	goto st13;
tr2080:
#line 247 "configparser.rl"
	{ init_species(spe); }
	goto st13;
tr2085:
#line 327 "configparser.rl"
	{ init_terrain(ter); }
	goto st13;
st13:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof13;
case 13:
#line 1821 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st14;
	goto st0;
st14:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof14;
case 14:
	if ( (*( state.p)) == 118 )
		goto st15;
	goto st0;
st15:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof15;
case 15:
	if ( (*( state.p)) == 101 )
		goto st16;
	goto st0;
st16:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof16;
case 16:
	if ( (*( state.p)) == 108 )
		goto st17;
	goto st0;
st17:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof17;
case 17:
	if ( (*( state.p)) == 115 )
		goto st18;
	goto st0;
st18:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof18;
case 18:
	if ( (*( state.p)) == 107 )
		goto st19;
	goto st0;
st19:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof19;
case 19:
	if ( (*( state.p)) == 105 )
		goto st20;
	goto st0;
st20:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof20;
case 20:
	if ( (*( state.p)) == 110 )
		goto st21;
	goto st0;
st21:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof21;
case 21:
	switch( (*( state.p)) ) {
		case 13: goto tr31;
		case 32: goto tr31;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr31;
	goto st0;
tr31:
#line 363 "configparser.rl"
	{ lev = Levelskin(); }
	goto st22;
st22:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof22;
case 22:
#line 1893 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st22;
		case 32: goto st22;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr33;
	} else if ( (*( state.p)) >= 9 )
		goto st22;
	goto st0;
tr33:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st23;
tr35:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st23;
st23:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof23;
case 23:
#line 1924 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr34;
		case 32: goto tr34;
		case 123: goto tr36;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr35;
	} else if ( (*( state.p)) >= 9 )
		goto tr34;
	goto st0;
tr34:
#line 359 "configparser.rl"
	{ lev.level = toint(state.match); }
	goto st24;
st24:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof24;
case 24:
#line 1944 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st24;
		case 32: goto st24;
		case 123: goto tr38;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st24;
	goto st0;
tr36:
#line 359 "configparser.rl"
	{ lev.level = toint(state.match); }
#line 365 "configparser.rl"
	{{ state.stack[ state.top++] = 1353; goto st628;}}
	goto st1353;
tr38:
#line 365 "configparser.rl"
	{{ state.stack[ state.top++] = 1353; goto st628;}}
	goto st1353;
st1353:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1353;
case 1353:
#line 1967 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr2073;
		case 32: goto tr2073;
		case 100: goto tr2074;
		case 108: goto tr2075;
		case 115: goto tr2076;
		case 116: goto tr2077;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr2073;
	goto st0;
tr2070:
#line 285 "configparser.rl"
	{ init_design(des); }
	goto st25;
tr2076:
#line 366 "configparser.rl"
	{ init_levelskin_(lev); }
	goto st25;
tr2081:
#line 247 "configparser.rl"
	{ init_species(spe); }
	goto st25;
tr2086:
#line 327 "configparser.rl"
	{ init_terrain(ter); }
	goto st25;
st25:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof25;
case 25:
#line 1999 "configparser.h"
	if ( (*( state.p)) == 112 )
		goto st26;
	goto st0;
st26:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof26;
case 26:
	if ( (*( state.p)) == 101 )
		goto st27;
	goto st0;
st27:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof27;
case 27:
	if ( (*( state.p)) == 99 )
		goto st28;
	goto st0;
st28:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof28;
case 28:
	if ( (*( state.p)) == 105 )
		goto st29;
	goto st0;
st29:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof29;
case 29:
	if ( (*( state.p)) == 101 )
		goto st30;
	goto st0;
st30:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof30;
case 30:
	if ( (*( state.p)) == 115 )
		goto st31;
	goto st0;
st31:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof31;
case 31:
	switch( (*( state.p)) ) {
		case 13: goto tr45;
		case 32: goto tr45;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr45;
	goto st0;
tr45:
#line 244 "configparser.rl"
	{ spe = Species(); }
	goto st32;
st32:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof32;
case 32:
#line 2057 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st32;
		case 32: goto st32;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr47;
	} else if ( (*( state.p)) >= 9 )
		goto st32;
	goto st0;
tr47:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st33;
tr49:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st33;
st33:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof33;
case 33:
#line 2088 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr48;
		case 32: goto tr48;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr49;
	} else if ( (*( state.p)) >= 9 )
		goto tr48;
	goto st0;
tr48:
#line 237 "configparser.rl"
	{ spe.level = toint(state.match); }
	goto st34;
st34:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof34;
case 34:
#line 2107 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st34;
		case 32: goto st34;
		case 95: goto tr51;
	}
	if ( (*( state.p)) < 48 ) {
		if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
			goto st34;
	} else if ( (*( state.p)) > 57 ) {
		if ( (*( state.p)) > 90 ) {
			if ( 97 <= (*( state.p)) && (*( state.p)) <= 122 )
				goto tr51;
		} else if ( (*( state.p)) >= 65 )
			goto tr51;
	} else
		goto tr51;
	goto st0;
tr51:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st35;
tr53:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st35;
st35:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof35;
case 35:
#line 2145 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr52;
		case 32: goto tr52;
		case 95: goto tr53;
		case 123: goto tr54;
	}
	if ( (*( state.p)) < 48 ) {
		if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
			goto tr52;
	} else if ( (*( state.p)) > 57 ) {
		if ( (*( state.p)) > 90 ) {
			if ( 97 <= (*( state.p)) && (*( state.p)) <= 122 )
				goto tr53;
		} else if ( (*( state.p)) >= 65 )
			goto tr53;
	} else
		goto tr53;
	goto st0;
tr52:
#line 240 "configparser.rl"
	{ spe.tag = state.match; }
	goto st36;
st36:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof36;
case 36:
#line 2172 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st36;
		case 32: goto st36;
		case 123: goto tr56;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st36;
	goto st0;
tr54:
#line 240 "configparser.rl"
	{ spe.tag = state.match; }
#line 246 "configparser.rl"
	{{ state.stack[ state.top++] = 1354; goto st48;}}
	goto st1354;
tr56:
#line 246 "configparser.rl"
	{{ state.stack[ state.top++] = 1354; goto st48;}}
	goto st1354;
st1354:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1354;
case 1354:
#line 2195 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr2078;
		case 32: goto tr2078;
		case 100: goto tr2079;
		case 108: goto tr2080;
		case 115: goto tr2081;
		case 116: goto tr2082;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr2078;
	goto st0;
tr2071:
#line 285 "configparser.rl"
	{ init_design(des); }
	goto st37;
tr2077:
#line 366 "configparser.rl"
	{ init_levelskin_(lev); }
	goto st37;
tr2082:
#line 247 "configparser.rl"
	{ init_species(spe); }
	goto st37;
tr2087:
#line 327 "configparser.rl"
	{ init_terrain(ter); }
	goto st37;
st37:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof37;
case 37:
#line 2227 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st38;
	goto st0;
st38:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof38;
case 38:
	if ( (*( state.p)) == 114 )
		goto st39;
	goto st0;
st39:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof39;
case 39:
	if ( (*( state.p)) == 114 )
		goto st40;
	goto st0;
st40:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof40;
case 40:
	if ( (*( state.p)) == 97 )
		goto st41;
	goto st0;
st41:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof41;
case 41:
	if ( (*( state.p)) == 105 )
		goto st42;
	goto st0;
st42:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof42;
case 42:
	if ( (*( state.p)) == 110 )
		goto st43;
	goto st0;
st43:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof43;
case 43:
	switch( (*( state.p)) ) {
		case 13: goto tr63;
		case 32: goto tr63;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr63;
	goto st0;
tr63:
#line 324 "configparser.rl"
	{ ter = Terrain(); }
	goto st44;
st44:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof44;
case 44:
#line 2285 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st44;
		case 32: goto st44;
		case 95: goto tr65;
	}
	if ( (*( state.p)) < 48 ) {
		if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
			goto st44;
	} else if ( (*( state.p)) > 57 ) {
		if ( (*( state.p)) > 90 ) {
			if ( 97 <= (*( state.p)) && (*( state.p)) <= 122 )
				goto tr65;
		} else if ( (*( state.p)) >= 65 )
			goto tr65;
	} else
		goto tr65;
	goto st0;
tr65:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st45;
tr67:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st45;
st45:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof45;
case 45:
#line 2323 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr66;
		case 32: goto tr66;
		case 95: goto tr67;
		case 123: goto tr68;
	}
	if ( (*( state.p)) < 48 ) {
		if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
			goto tr66;
	} else if ( (*( state.p)) > 57 ) {
		if ( (*( state.p)) > 90 ) {
			if ( 97 <= (*( state.p)) && (*( state.p)) <= 122 )
				goto tr67;
		} else if ( (*( state.p)) >= 65 )
			goto tr67;
	} else
		goto tr67;
	goto st0;
tr66:
#line 320 "configparser.rl"
	{ ter.tag = state.match; }
	goto st46;
st46:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof46;
case 46:
#line 2350 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st46;
		case 32: goto st46;
		case 123: goto tr70;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st46;
	goto st0;
tr68:
#line 320 "configparser.rl"
	{ ter.tag = state.match; }
#line 326 "configparser.rl"
	{{ state.stack[ state.top++] = 1355; goto st483;}}
	goto st1355;
tr70:
#line 326 "configparser.rl"
	{{ state.stack[ state.top++] = 1355; goto st483;}}
	goto st1355;
st1355:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1355;
case 1355:
#line 2373 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr2083;
		case 32: goto tr2083;
		case 100: goto tr2084;
		case 108: goto tr2085;
		case 115: goto tr2086;
		case 116: goto tr2087;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr2083;
	goto st0;
st47:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof47;
case 47:
	switch( (*( state.p)) ) {
		case 34: goto tr71;
		case 92: goto tr72;
		case 110: goto tr73;
	}
	goto st0;
tr71:
#line 136 "configparser.rl"
	{ state.match += '"';  { state.cs =  state.stack[-- state.top];goto _again;} }
	goto st1356;
tr72:
#line 138 "configparser.rl"
	{ state.match += '\\'; { state.cs =  state.stack[-- state.top];goto _again;} }
	goto st1356;
tr73:
#line 137 "configparser.rl"
	{ state.match += '\n'; { state.cs =  state.stack[-- state.top];goto _again;} }
	goto st1356;
st1356:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1356;
case 1356:
#line 2411 "configparser.h"
	goto st0;
st48:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof48;
case 48:
	switch( (*( state.p)) ) {
		case 13: goto st48;
		case 32: goto st48;
		case 97: goto st49;
		case 99: goto st67;
		case 100: goto st131;
		case 104: goto st154;
		case 105: goto st189;
		case 109: goto st207;
		case 110: goto st231;
		case 114: goto st238;
		case 115: goto st245;
		case 125: goto tr84;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st48;
	goto st0;
st49:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof49;
case 49:
	switch( (*( state.p)) ) {
		case 105: goto st50;
		case 116: goto st325;
	}
	goto st0;
st50:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof50;
case 50:
	switch( (*( state.p)) ) {
		case 13: goto st51;
		case 32: goto st51;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st51;
	goto st0;
st51:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof51;
case 51:
	switch( (*( state.p)) ) {
		case 13: goto st51;
		case 32: goto st51;
		case 105: goto st52;
		case 110: goto st304;
		case 114: goto st308;
		case 115: goto st314;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st51;
	goto st0;
st52:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof52;
case 52:
	if ( (*( state.p)) == 110 )
		goto st53;
	goto st0;
st53:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof53;
case 53:
	if ( (*( state.p)) == 114 )
		goto st54;
	goto st0;
st54:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof54;
case 54:
	if ( (*( state.p)) == 97 )
		goto st55;
	goto st0;
st55:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof55;
case 55:
	if ( (*( state.p)) == 110 )
		goto st56;
	goto st0;
st56:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof56;
case 56:
	if ( (*( state.p)) == 103 )
		goto st57;
	goto st0;
st57:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof57;
case 57:
	if ( (*( state.p)) == 101 )
		goto st58;
	goto st0;
st58:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof58;
case 58:
	if ( (*( state.p)) == 95 )
		goto st59;
	goto st0;
st59:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof59;
case 59:
	if ( (*( state.p)) == 114 )
		goto st60;
	goto st0;
st60:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof60;
case 60:
	if ( (*( state.p)) == 97 )
		goto st61;
	goto st0;
st61:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof61;
case 61:
	if ( (*( state.p)) == 110 )
		goto st62;
	goto st0;
st62:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof62;
case 62:
	if ( (*( state.p)) == 100 )
		goto st63;
	goto st0;
st63:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof63;
case 63:
	if ( (*( state.p)) == 111 )
		goto st64;
	goto st0;
st64:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof64;
case 64:
	if ( (*( state.p)) == 109 )
		goto st65;
	goto st0;
st65:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof65;
case 65:
	switch( (*( state.p)) ) {
		case 13: goto tr105;
		case 32: goto tr105;
		case 59: goto tr106;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr105;
	goto st0;
tr84:
#line 231 "configparser.rl"
	{ { state.cs =  state.stack[-- state.top];goto _again;} }
	goto st66;
tr105:
#line 179 "configparser.rl"
	{ spe.ai = Species::ai_t::inrange_random; }
	goto st66;
tr146:
#line 222 "configparser.rl"
	{ spe.cast_cloud.back().name = state.match; }
	goto st66;
tr166:
#line 204 "configparser.rl"
	{ spe.clumpsize.deviation = toreal(state.match); }
	goto st66;
tr190:
#line 209 "configparser.rl"
	{ spe.companion.back().chance = toreal(state.match); }
	goto st66;
tr198:
#line 191 "configparser.rl"
	{ spe.count = toint(state.match); }
	goto st66;
tr212:
#line 200 "configparser.rl"
	{ spe.defense = toreal(state.match); }
	goto st66;
tr229:
#line 214 "configparser.rl"
	{ spe.drop.back().chance = toreal(state.match); }
	goto st66;
tr249:
#line 172 "configparser.rl"
	{ spe.habitat = Species::habitat_t::corner; }
	goto st66;
tr255:
#line 170 "configparser.rl"
	{ spe.habitat = Species::habitat_t::floor; }
	goto st66;
tr265:
#line 173 "configparser.rl"
	{ spe.habitat = Species::habitat_t::shoreline; }
	goto st66;
tr271:
#line 169 "configparser.rl"
	{ spe.habitat = Species::habitat_t::walk; }
	goto st66;
tr275:
#line 171 "configparser.rl"
	{ spe.habitat = Species::habitat_t::water; }
	goto st66;
tr289:
#line 182 "configparser.rl"
	{ spe.idle_ai = Species::idle_ai_t::none; }
	goto st66;
tr296:
#line 183 "configparser.rl"
	{ spe.idle_ai = Species::idle_ai_t::random; }
	goto st66;
tr308:
#line 186 "configparser.rl"
	{ spe.move = Species::move_t::any; }
	goto st66;
tr315:
#line 189 "configparser.rl"
	{ spe.move = Species::move_t::corner; }
	goto st66;
tr321:
#line 187 "configparser.rl"
	{ spe.move = Species::move_t::floor; }
	goto st66;
tr327:
#line 188 "configparser.rl"
	{ spe.move = Species::move_t::water; }
	goto st66;
tr337:
#line 192 "configparser.rl"
	{ spe.name = state.match; }
	goto st66;
tr345:
#line 198 "configparser.rl"
	{ spe.range = toint(state.match); }
	goto st66;
tr388:
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st66;
tr391:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st66;
tr396:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st66;
tr402:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st66;
tr410:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st66;
tr414:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st66;
tr420:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st66;
tr427:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st66;
tr445:
#line 176 "configparser.rl"
	{ spe.ai = Species::ai_t::none; }
	goto st66;
tr452:
#line 178 "configparser.rl"
	{ spe.ai = Species::ai_t::random; }
	goto st66;
tr464:
#line 177 "configparser.rl"
	{ spe.ai = Species::ai_t::seek_player; }
	goto st66;
tr474:
#line 199 "configparser.rl"
	{ spe.attack = toreal(state.match); }
	goto st66;
st66:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof66;
case 66:
#line 2722 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st66;
		case 32: goto st66;
		case 59: goto st1357;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st66;
	goto st0;
tr106:
#line 179 "configparser.rl"
	{ spe.ai = Species::ai_t::inrange_random; }
	goto st1357;
tr147:
#line 222 "configparser.rl"
	{ spe.cast_cloud.back().name = state.match; }
	goto st1357;
tr168:
#line 204 "configparser.rl"
	{ spe.clumpsize.deviation = toreal(state.match); }
	goto st1357;
tr192:
#line 209 "configparser.rl"
	{ spe.companion.back().chance = toreal(state.match); }
	goto st1357;
tr200:
#line 191 "configparser.rl"
	{ spe.count = toint(state.match); }
	goto st1357;
tr214:
#line 200 "configparser.rl"
	{ spe.defense = toreal(state.match); }
	goto st1357;
tr231:
#line 214 "configparser.rl"
	{ spe.drop.back().chance = toreal(state.match); }
	goto st1357;
tr250:
#line 172 "configparser.rl"
	{ spe.habitat = Species::habitat_t::corner; }
	goto st1357;
tr256:
#line 170 "configparser.rl"
	{ spe.habitat = Species::habitat_t::floor; }
	goto st1357;
tr266:
#line 173 "configparser.rl"
	{ spe.habitat = Species::habitat_t::shoreline; }
	goto st1357;
tr272:
#line 169 "configparser.rl"
	{ spe.habitat = Species::habitat_t::walk; }
	goto st1357;
tr276:
#line 171 "configparser.rl"
	{ spe.habitat = Species::habitat_t::water; }
	goto st1357;
tr290:
#line 182 "configparser.rl"
	{ spe.idle_ai = Species::idle_ai_t::none; }
	goto st1357;
tr297:
#line 183 "configparser.rl"
	{ spe.idle_ai = Species::idle_ai_t::random; }
	goto st1357;
tr309:
#line 186 "configparser.rl"
	{ spe.move = Species::move_t::any; }
	goto st1357;
tr316:
#line 189 "configparser.rl"
	{ spe.move = Species::move_t::corner; }
	goto st1357;
tr322:
#line 187 "configparser.rl"
	{ spe.move = Species::move_t::floor; }
	goto st1357;
tr328:
#line 188 "configparser.rl"
	{ spe.move = Species::move_t::water; }
	goto st1357;
tr338:
#line 192 "configparser.rl"
	{ spe.name = state.match; }
	goto st1357;
tr347:
#line 198 "configparser.rl"
	{ spe.range = toint(state.match); }
	goto st1357;
tr389:
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st1357;
tr392:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st1357;
tr397:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st1357;
tr403:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st1357;
tr411:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st1357;
tr415:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st1357;
tr421:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st1357;
tr428:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 193 "configparser.rl"
	{ spe.skin = skin; }
	goto st1357;
tr446:
#line 176 "configparser.rl"
	{ spe.ai = Species::ai_t::none; }
	goto st1357;
tr453:
#line 178 "configparser.rl"
	{ spe.ai = Species::ai_t::random; }
	goto st1357;
tr465:
#line 177 "configparser.rl"
	{ spe.ai = Species::ai_t::seek_player; }
	goto st1357;
tr476:
#line 199 "configparser.rl"
	{ spe.attack = toreal(state.match); }
	goto st1357;
st1357:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1357;
case 1357:
#line 2877 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st48;
		case 32: goto st48;
		case 97: goto st49;
		case 99: goto st67;
		case 100: goto st131;
		case 104: goto st154;
		case 105: goto st189;
		case 109: goto st207;
		case 110: goto st231;
		case 114: goto st238;
		case 115: goto st245;
		case 125: goto tr84;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st48;
	goto st0;
st67:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof67;
case 67:
	switch( (*( state.p)) ) {
		case 97: goto st68;
		case 108: goto st92;
		case 111: goto st110;
	}
	goto st0;
st68:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof68;
case 68:
	if ( (*( state.p)) == 115 )
		goto st69;
	goto st0;
st69:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof69;
case 69:
	if ( (*( state.p)) == 116 )
		goto st70;
	goto st0;
st70:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof70;
case 70:
	if ( (*( state.p)) == 95 )
		goto st71;
	goto st0;
st71:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof71;
case 71:
	if ( (*( state.p)) == 99 )
		goto st72;
	goto st0;
st72:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof72;
case 72:
	if ( (*( state.p)) == 108 )
		goto st73;
	goto st0;
st73:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof73;
case 73:
	if ( (*( state.p)) == 111 )
		goto st74;
	goto st0;
st74:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof74;
case 74:
	if ( (*( state.p)) == 117 )
		goto st75;
	goto st0;
st75:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof75;
case 75:
	if ( (*( state.p)) == 100 )
		goto st76;
	goto st0;
st76:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof76;
case 76:
	switch( (*( state.p)) ) {
		case 13: goto tr120;
		case 32: goto tr120;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr120;
	goto st0;
tr120:
#line 217 "configparser.rl"
	{ spe.cast_cloud.push_back(Species::cloud_t()); }
	goto st77;
st77:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof77;
case 77:
#line 2980 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st77;
		case 32: goto st77;
		case 45: goto tr122;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr123;
	} else if ( (*( state.p)) >= 9 )
		goto st77;
	goto st0;
tr122:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st78;
st78:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof78;
case 78:
#line 3006 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr124;
	goto st0;
tr123:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st79;
tr124:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st79;
st79:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof79;
case 79:
#line 3030 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr125;
		case 32: goto tr125;
		case 46: goto tr126;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr124;
	} else if ( (*( state.p)) >= 9 )
		goto tr125;
	goto st0;
tr125:
#line 218 "configparser.rl"
	{ spe.cast_cloud.back().chance = toreal(state.match); }
	goto st80;
st80:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof80;
case 80:
#line 3050 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st80;
		case 32: goto st80;
		case 34: goto tr128;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st80;
	goto st0;
tr129:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st81;
tr128:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st81;
tr131:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 81; goto st47;}}
	goto st81;
st81:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof81;
case 81:
#line 3079 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st82;
		case 92: goto tr131;
	}
	goto tr129;
st82:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof82;
case 82:
	switch( (*( state.p)) ) {
		case 13: goto tr132;
		case 32: goto tr132;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr132;
	goto st0;
tr132:
#line 219 "configparser.rl"
	{ spe.cast_cloud.back().terraintag = state.match; }
	goto st83;
st83:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof83;
case 83:
#line 3104 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st83;
		case 32: goto st83;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr134;
	} else if ( (*( state.p)) >= 9 )
		goto st83;
	goto st0;
tr134:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st84;
tr136:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st84;
st84:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof84;
case 84:
#line 3135 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr135;
		case 32: goto tr135;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr136;
	} else if ( (*( state.p)) >= 9 )
		goto tr135;
	goto st0;
tr135:
#line 220 "configparser.rl"
	{ spe.cast_cloud.back().radius = toint(state.match); }
	goto st85;
st85:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof85;
case 85:
#line 3154 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st85;
		case 32: goto st85;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr138;
	} else if ( (*( state.p)) >= 9 )
		goto st85;
	goto st0;
tr138:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st86;
tr140:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st86;
st86:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof86;
case 86:
#line 3185 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr139;
		case 32: goto tr139;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr140;
	} else if ( (*( state.p)) >= 9 )
		goto tr139;
	goto st0;
tr139:
#line 221 "configparser.rl"
	{ spe.cast_cloud.back().turns = toint(state.match); }
	goto st87;
st87:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof87;
case 87:
#line 3204 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st87;
		case 32: goto st87;
		case 34: goto tr142;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st87;
	goto st0;
tr143:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st88;
tr142:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st88;
tr145:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 88; goto st47;}}
	goto st88;
st88:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof88;
case 88:
#line 3233 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st89;
		case 92: goto tr145;
	}
	goto tr143;
st89:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof89;
case 89:
	switch( (*( state.p)) ) {
		case 13: goto tr146;
		case 32: goto tr146;
		case 59: goto tr147;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr146;
	goto st0;
tr126:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st90;
st90:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof90;
case 90:
#line 3261 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr148;
	goto st0;
tr148:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st91;
st91:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof91;
case 91:
#line 3275 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr125;
		case 32: goto tr125;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr148;
	} else if ( (*( state.p)) >= 9 )
		goto tr125;
	goto st0;
st92:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof92;
case 92:
	if ( (*( state.p)) == 117 )
		goto st93;
	goto st0;
st93:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof93;
case 93:
	if ( (*( state.p)) == 109 )
		goto st94;
	goto st0;
st94:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof94;
case 94:
	if ( (*( state.p)) == 112 )
		goto st95;
	goto st0;
st95:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof95;
case 95:
	if ( (*( state.p)) == 115 )
		goto st96;
	goto st0;
st96:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof96;
case 96:
	if ( (*( state.p)) == 105 )
		goto st97;
	goto st0;
st97:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof97;
case 97:
	if ( (*( state.p)) == 122 )
		goto st98;
	goto st0;
st98:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof98;
case 98:
	if ( (*( state.p)) == 101 )
		goto st99;
	goto st0;
st99:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof99;
case 99:
	switch( (*( state.p)) ) {
		case 13: goto st100;
		case 32: goto st100;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st100;
	goto st0;
st100:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof100;
case 100:
	switch( (*( state.p)) ) {
		case 13: goto st100;
		case 32: goto st100;
		case 45: goto tr157;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr158;
	} else if ( (*( state.p)) >= 9 )
		goto st100;
	goto st0;
tr157:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st101;
st101:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof101;
case 101:
#line 3375 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr159;
	goto st0;
tr158:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st102;
tr159:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st102;
st102:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof102;
case 102:
#line 3399 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr160;
		case 32: goto tr160;
		case 46: goto tr161;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr159;
	} else if ( (*( state.p)) >= 9 )
		goto tr160;
	goto st0;
tr160:
#line 203 "configparser.rl"
	{ spe.clumpsize.mean = toreal(state.match); }
	goto st103;
st103:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof103;
case 103:
#line 3419 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st103;
		case 32: goto st103;
		case 45: goto tr163;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr164;
	} else if ( (*( state.p)) >= 9 )
		goto st103;
	goto st0;
tr163:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st104;
st104:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof104;
case 104:
#line 3445 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr165;
	goto st0;
tr164:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st105;
tr165:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st105;
st105:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof105;
case 105:
#line 3469 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr166;
		case 32: goto tr166;
		case 46: goto tr167;
		case 59: goto tr168;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr165;
	} else if ( (*( state.p)) >= 9 )
		goto tr166;
	goto st0;
tr167:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st106;
st106:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof106;
case 106:
#line 3492 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr169;
	goto st0;
tr169:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st107;
st107:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof107;
case 107:
#line 3506 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr166;
		case 32: goto tr166;
		case 59: goto tr168;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr169;
	} else if ( (*( state.p)) >= 9 )
		goto tr166;
	goto st0;
tr161:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st108;
st108:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof108;
case 108:
#line 3528 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr170;
	goto st0;
tr170:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st109;
st109:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof109;
case 109:
#line 3542 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr160;
		case 32: goto tr160;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr170;
	} else if ( (*( state.p)) >= 9 )
		goto tr160;
	goto st0;
st110:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof110;
case 110:
	switch( (*( state.p)) ) {
		case 109: goto st111;
		case 117: goto st126;
	}
	goto st0;
st111:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof111;
case 111:
	if ( (*( state.p)) == 112 )
		goto st112;
	goto st0;
st112:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof112;
case 112:
	if ( (*( state.p)) == 97 )
		goto st113;
	goto st0;
st113:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof113;
case 113:
	if ( (*( state.p)) == 110 )
		goto st114;
	goto st0;
st114:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof114;
case 114:
	if ( (*( state.p)) == 105 )
		goto st115;
	goto st0;
st115:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof115;
case 115:
	if ( (*( state.p)) == 111 )
		goto st116;
	goto st0;
st116:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof116;
case 116:
	if ( (*( state.p)) == 110 )
		goto st117;
	goto st0;
st117:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof117;
case 117:
	switch( (*( state.p)) ) {
		case 13: goto tr179;
		case 32: goto tr179;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr179;
	goto st0;
tr179:
#line 207 "configparser.rl"
	{ spe.companion.push_back(Species::companion_t()); }
	goto st118;
st118:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof118;
case 118:
#line 3623 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st118;
		case 32: goto st118;
		case 34: goto tr181;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st118;
	goto st0;
tr182:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st119;
tr181:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st119;
tr184:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 119; goto st47;}}
	goto st119;
st119:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof119;
case 119:
#line 3652 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st120;
		case 92: goto tr184;
	}
	goto tr182;
st120:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof120;
case 120:
	switch( (*( state.p)) ) {
		case 13: goto tr185;
		case 32: goto tr185;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr185;
	goto st0;
tr185:
#line 208 "configparser.rl"
	{ spe.companion.back().tag = state.match; }
	goto st121;
st121:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof121;
case 121:
#line 3677 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st121;
		case 32: goto st121;
		case 45: goto tr187;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr188;
	} else if ( (*( state.p)) >= 9 )
		goto st121;
	goto st0;
tr187:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st122;
st122:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof122;
case 122:
#line 3703 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr189;
	goto st0;
tr188:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st123;
tr189:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st123;
st123:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof123;
case 123:
#line 3727 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr190;
		case 32: goto tr190;
		case 46: goto tr191;
		case 59: goto tr192;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr189;
	} else if ( (*( state.p)) >= 9 )
		goto tr190;
	goto st0;
tr191:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st124;
st124:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof124;
case 124:
#line 3750 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr193;
	goto st0;
tr193:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st125;
st125:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof125;
case 125:
#line 3764 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr190;
		case 32: goto tr190;
		case 59: goto tr192;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr193;
	} else if ( (*( state.p)) >= 9 )
		goto tr190;
	goto st0;
st126:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof126;
case 126:
	if ( (*( state.p)) == 110 )
		goto st127;
	goto st0;
st127:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof127;
case 127:
	if ( (*( state.p)) == 116 )
		goto st128;
	goto st0;
st128:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof128;
case 128:
	switch( (*( state.p)) ) {
		case 13: goto st129;
		case 32: goto st129;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st129;
	goto st0;
st129:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof129;
case 129:
	switch( (*( state.p)) ) {
		case 13: goto st129;
		case 32: goto st129;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr197;
	} else if ( (*( state.p)) >= 9 )
		goto st129;
	goto st0;
tr197:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st130;
tr199:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st130;
st130:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof130;
case 130:
#line 3835 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr198;
		case 32: goto tr198;
		case 59: goto tr200;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr199;
	} else if ( (*( state.p)) >= 9 )
		goto tr198;
	goto st0;
st131:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof131;
case 131:
	switch( (*( state.p)) ) {
		case 101: goto st132;
		case 114: goto st143;
	}
	goto st0;
st132:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof132;
case 132:
	if ( (*( state.p)) == 102 )
		goto st133;
	goto st0;
st133:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof133;
case 133:
	if ( (*( state.p)) == 101 )
		goto st134;
	goto st0;
st134:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof134;
case 134:
	if ( (*( state.p)) == 110 )
		goto st135;
	goto st0;
st135:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof135;
case 135:
	if ( (*( state.p)) == 115 )
		goto st136;
	goto st0;
st136:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof136;
case 136:
	if ( (*( state.p)) == 101 )
		goto st137;
	goto st0;
st137:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof137;
case 137:
	switch( (*( state.p)) ) {
		case 13: goto st138;
		case 32: goto st138;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st138;
	goto st0;
st138:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof138;
case 138:
	switch( (*( state.p)) ) {
		case 13: goto st138;
		case 32: goto st138;
		case 45: goto tr209;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr210;
	} else if ( (*( state.p)) >= 9 )
		goto st138;
	goto st0;
tr209:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st139;
st139:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof139;
case 139:
#line 3931 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr211;
	goto st0;
tr210:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st140;
tr211:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st140;
st140:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof140;
case 140:
#line 3955 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr212;
		case 32: goto tr212;
		case 46: goto tr213;
		case 59: goto tr214;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr211;
	} else if ( (*( state.p)) >= 9 )
		goto tr212;
	goto st0;
tr213:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st141;
st141:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof141;
case 141:
#line 3978 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr215;
	goto st0;
tr215:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st142;
st142:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof142;
case 142:
#line 3992 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr212;
		case 32: goto tr212;
		case 59: goto tr214;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr215;
	} else if ( (*( state.p)) >= 9 )
		goto tr212;
	goto st0;
st143:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof143;
case 143:
	if ( (*( state.p)) == 111 )
		goto st144;
	goto st0;
st144:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof144;
case 144:
	if ( (*( state.p)) == 112 )
		goto st145;
	goto st0;
st145:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof145;
case 145:
	switch( (*( state.p)) ) {
		case 13: goto tr218;
		case 32: goto tr218;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr218;
	goto st0;
tr218:
#line 212 "configparser.rl"
	{ spe.drop.push_back(Species::drop_t()); }
	goto st146;
st146:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof146;
case 146:
#line 4037 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st146;
		case 32: goto st146;
		case 34: goto tr220;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st146;
	goto st0;
tr221:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st147;
tr220:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st147;
tr223:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 147; goto st47;}}
	goto st147;
st147:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof147;
case 147:
#line 4066 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st148;
		case 92: goto tr223;
	}
	goto tr221;
st148:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof148;
case 148:
	switch( (*( state.p)) ) {
		case 13: goto tr224;
		case 32: goto tr224;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr224;
	goto st0;
tr224:
#line 213 "configparser.rl"
	{ spe.drop.back().tag = state.match; }
	goto st149;
st149:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof149;
case 149:
#line 4091 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st149;
		case 32: goto st149;
		case 45: goto tr226;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr227;
	} else if ( (*( state.p)) >= 9 )
		goto st149;
	goto st0;
tr226:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st150;
st150:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof150;
case 150:
#line 4117 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr228;
	goto st0;
tr227:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st151;
tr228:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st151;
st151:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof151;
case 151:
#line 4141 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr229;
		case 32: goto tr229;
		case 46: goto tr230;
		case 59: goto tr231;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr228;
	} else if ( (*( state.p)) >= 9 )
		goto tr229;
	goto st0;
tr230:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st152;
st152:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof152;
case 152:
#line 4164 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr232;
	goto st0;
tr232:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st153;
st153:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof153;
case 153:
#line 4178 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr229;
		case 32: goto tr229;
		case 59: goto tr231;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr232;
	} else if ( (*( state.p)) >= 9 )
		goto tr229;
	goto st0;
st154:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof154;
case 154:
	if ( (*( state.p)) == 97 )
		goto st155;
	goto st0;
st155:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof155;
case 155:
	if ( (*( state.p)) == 98 )
		goto st156;
	goto st0;
st156:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof156;
case 156:
	if ( (*( state.p)) == 105 )
		goto st157;
	goto st0;
st157:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof157;
case 157:
	if ( (*( state.p)) == 116 )
		goto st158;
	goto st0;
st158:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof158;
case 158:
	if ( (*( state.p)) == 97 )
		goto st159;
	goto st0;
st159:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof159;
case 159:
	if ( (*( state.p)) == 116 )
		goto st160;
	goto st0;
st160:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof160;
case 160:
	switch( (*( state.p)) ) {
		case 13: goto st161;
		case 32: goto st161;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st161;
	goto st0;
st161:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof161;
case 161:
	switch( (*( state.p)) ) {
		case 13: goto st161;
		case 32: goto st161;
		case 99: goto st162;
		case 102: goto st168;
		case 115: goto st173;
		case 119: goto st182;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st161;
	goto st0;
st162:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof162;
case 162:
	if ( (*( state.p)) == 111 )
		goto st163;
	goto st0;
st163:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof163;
case 163:
	if ( (*( state.p)) == 114 )
		goto st164;
	goto st0;
st164:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof164;
case 164:
	if ( (*( state.p)) == 110 )
		goto st165;
	goto st0;
st165:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof165;
case 165:
	if ( (*( state.p)) == 101 )
		goto st166;
	goto st0;
st166:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof166;
case 166:
	if ( (*( state.p)) == 114 )
		goto st167;
	goto st0;
st167:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof167;
case 167:
	switch( (*( state.p)) ) {
		case 13: goto tr249;
		case 32: goto tr249;
		case 59: goto tr250;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr249;
	goto st0;
st168:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof168;
case 168:
	if ( (*( state.p)) == 108 )
		goto st169;
	goto st0;
st169:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof169;
case 169:
	if ( (*( state.p)) == 111 )
		goto st170;
	goto st0;
st170:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof170;
case 170:
	if ( (*( state.p)) == 111 )
		goto st171;
	goto st0;
st171:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof171;
case 171:
	if ( (*( state.p)) == 114 )
		goto st172;
	goto st0;
st172:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof172;
case 172:
	switch( (*( state.p)) ) {
		case 13: goto tr255;
		case 32: goto tr255;
		case 59: goto tr256;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr255;
	goto st0;
st173:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof173;
case 173:
	if ( (*( state.p)) == 104 )
		goto st174;
	goto st0;
st174:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof174;
case 174:
	if ( (*( state.p)) == 111 )
		goto st175;
	goto st0;
st175:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof175;
case 175:
	if ( (*( state.p)) == 114 )
		goto st176;
	goto st0;
st176:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof176;
case 176:
	if ( (*( state.p)) == 101 )
		goto st177;
	goto st0;
st177:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof177;
case 177:
	if ( (*( state.p)) == 108 )
		goto st178;
	goto st0;
st178:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof178;
case 178:
	if ( (*( state.p)) == 105 )
		goto st179;
	goto st0;
st179:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof179;
case 179:
	if ( (*( state.p)) == 110 )
		goto st180;
	goto st0;
st180:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof180;
case 180:
	if ( (*( state.p)) == 101 )
		goto st181;
	goto st0;
st181:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof181;
case 181:
	switch( (*( state.p)) ) {
		case 13: goto tr265;
		case 32: goto tr265;
		case 59: goto tr266;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr265;
	goto st0;
st182:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof182;
case 182:
	if ( (*( state.p)) == 97 )
		goto st183;
	goto st0;
st183:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof183;
case 183:
	switch( (*( state.p)) ) {
		case 108: goto st184;
		case 116: goto st186;
	}
	goto st0;
st184:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof184;
case 184:
	if ( (*( state.p)) == 107 )
		goto st185;
	goto st0;
st185:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof185;
case 185:
	switch( (*( state.p)) ) {
		case 13: goto tr271;
		case 32: goto tr271;
		case 59: goto tr272;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr271;
	goto st0;
st186:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof186;
case 186:
	if ( (*( state.p)) == 101 )
		goto st187;
	goto st0;
st187:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof187;
case 187:
	if ( (*( state.p)) == 114 )
		goto st188;
	goto st0;
st188:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof188;
case 188:
	switch( (*( state.p)) ) {
		case 13: goto tr275;
		case 32: goto tr275;
		case 59: goto tr276;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr275;
	goto st0;
st189:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof189;
case 189:
	if ( (*( state.p)) == 100 )
		goto st190;
	goto st0;
st190:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof190;
case 190:
	if ( (*( state.p)) == 108 )
		goto st191;
	goto st0;
st191:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof191;
case 191:
	if ( (*( state.p)) == 101 )
		goto st192;
	goto st0;
st192:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof192;
case 192:
	if ( (*( state.p)) == 95 )
		goto st193;
	goto st0;
st193:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof193;
case 193:
	if ( (*( state.p)) == 97 )
		goto st194;
	goto st0;
st194:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof194;
case 194:
	if ( (*( state.p)) == 105 )
		goto st195;
	goto st0;
st195:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof195;
case 195:
	switch( (*( state.p)) ) {
		case 13: goto st196;
		case 32: goto st196;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st196;
	goto st0;
st196:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof196;
case 196:
	switch( (*( state.p)) ) {
		case 13: goto st196;
		case 32: goto st196;
		case 110: goto st197;
		case 114: goto st201;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st196;
	goto st0;
st197:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof197;
case 197:
	if ( (*( state.p)) == 111 )
		goto st198;
	goto st0;
st198:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof198;
case 198:
	if ( (*( state.p)) == 110 )
		goto st199;
	goto st0;
st199:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof199;
case 199:
	if ( (*( state.p)) == 101 )
		goto st200;
	goto st0;
st200:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof200;
case 200:
	switch( (*( state.p)) ) {
		case 13: goto tr289;
		case 32: goto tr289;
		case 59: goto tr290;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr289;
	goto st0;
st201:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof201;
case 201:
	if ( (*( state.p)) == 97 )
		goto st202;
	goto st0;
st202:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof202;
case 202:
	if ( (*( state.p)) == 110 )
		goto st203;
	goto st0;
st203:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof203;
case 203:
	if ( (*( state.p)) == 100 )
		goto st204;
	goto st0;
st204:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof204;
case 204:
	if ( (*( state.p)) == 111 )
		goto st205;
	goto st0;
st205:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof205;
case 205:
	if ( (*( state.p)) == 109 )
		goto st206;
	goto st0;
st206:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof206;
case 206:
	switch( (*( state.p)) ) {
		case 13: goto tr296;
		case 32: goto tr296;
		case 59: goto tr297;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr296;
	goto st0;
st207:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof207;
case 207:
	if ( (*( state.p)) == 111 )
		goto st208;
	goto st0;
st208:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof208;
case 208:
	if ( (*( state.p)) == 118 )
		goto st209;
	goto st0;
st209:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof209;
case 209:
	if ( (*( state.p)) == 101 )
		goto st210;
	goto st0;
st210:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof210;
case 210:
	switch( (*( state.p)) ) {
		case 13: goto st211;
		case 32: goto st211;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st211;
	goto st0;
st211:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof211;
case 211:
	switch( (*( state.p)) ) {
		case 13: goto st211;
		case 32: goto st211;
		case 97: goto st212;
		case 99: goto st215;
		case 102: goto st221;
		case 119: goto st226;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st211;
	goto st0;
st212:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof212;
case 212:
	if ( (*( state.p)) == 110 )
		goto st213;
	goto st0;
st213:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof213;
case 213:
	if ( (*( state.p)) == 121 )
		goto st214;
	goto st0;
st214:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof214;
case 214:
	switch( (*( state.p)) ) {
		case 13: goto tr308;
		case 32: goto tr308;
		case 59: goto tr309;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr308;
	goto st0;
st215:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof215;
case 215:
	if ( (*( state.p)) == 111 )
		goto st216;
	goto st0;
st216:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof216;
case 216:
	if ( (*( state.p)) == 114 )
		goto st217;
	goto st0;
st217:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof217;
case 217:
	if ( (*( state.p)) == 110 )
		goto st218;
	goto st0;
st218:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof218;
case 218:
	if ( (*( state.p)) == 101 )
		goto st219;
	goto st0;
st219:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof219;
case 219:
	if ( (*( state.p)) == 114 )
		goto st220;
	goto st0;
st220:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof220;
case 220:
	switch( (*( state.p)) ) {
		case 13: goto tr315;
		case 32: goto tr315;
		case 59: goto tr316;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr315;
	goto st0;
st221:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof221;
case 221:
	if ( (*( state.p)) == 108 )
		goto st222;
	goto st0;
st222:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof222;
case 222:
	if ( (*( state.p)) == 111 )
		goto st223;
	goto st0;
st223:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof223;
case 223:
	if ( (*( state.p)) == 111 )
		goto st224;
	goto st0;
st224:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof224;
case 224:
	if ( (*( state.p)) == 114 )
		goto st225;
	goto st0;
st225:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof225;
case 225:
	switch( (*( state.p)) ) {
		case 13: goto tr321;
		case 32: goto tr321;
		case 59: goto tr322;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr321;
	goto st0;
st226:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof226;
case 226:
	if ( (*( state.p)) == 97 )
		goto st227;
	goto st0;
st227:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof227;
case 227:
	if ( (*( state.p)) == 116 )
		goto st228;
	goto st0;
st228:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof228;
case 228:
	if ( (*( state.p)) == 101 )
		goto st229;
	goto st0;
st229:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof229;
case 229:
	if ( (*( state.p)) == 114 )
		goto st230;
	goto st0;
st230:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof230;
case 230:
	switch( (*( state.p)) ) {
		case 13: goto tr327;
		case 32: goto tr327;
		case 59: goto tr328;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr327;
	goto st0;
st231:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof231;
case 231:
	if ( (*( state.p)) == 97 )
		goto st232;
	goto st0;
st232:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof232;
case 232:
	if ( (*( state.p)) == 109 )
		goto st233;
	goto st0;
st233:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof233;
case 233:
	if ( (*( state.p)) == 101 )
		goto st234;
	goto st0;
st234:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof234;
case 234:
	switch( (*( state.p)) ) {
		case 13: goto st235;
		case 32: goto st235;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st235;
	goto st0;
st235:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof235;
case 235:
	switch( (*( state.p)) ) {
		case 13: goto st235;
		case 32: goto st235;
		case 34: goto tr333;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st235;
	goto st0;
tr334:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st236;
tr333:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st236;
tr336:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 236; goto st47;}}
	goto st236;
st236:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof236;
case 236:
#line 4884 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st237;
		case 92: goto tr336;
	}
	goto tr334;
st237:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof237;
case 237:
	switch( (*( state.p)) ) {
		case 13: goto tr337;
		case 32: goto tr337;
		case 59: goto tr338;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr337;
	goto st0;
st238:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof238;
case 238:
	if ( (*( state.p)) == 97 )
		goto st239;
	goto st0;
st239:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof239;
case 239:
	if ( (*( state.p)) == 110 )
		goto st240;
	goto st0;
st240:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof240;
case 240:
	if ( (*( state.p)) == 103 )
		goto st241;
	goto st0;
st241:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof241;
case 241:
	if ( (*( state.p)) == 101 )
		goto st242;
	goto st0;
st242:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof242;
case 242:
	switch( (*( state.p)) ) {
		case 13: goto st243;
		case 32: goto st243;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st243;
	goto st0;
st243:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof243;
case 243:
	switch( (*( state.p)) ) {
		case 13: goto st243;
		case 32: goto st243;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr344;
	} else if ( (*( state.p)) >= 9 )
		goto st243;
	goto st0;
tr344:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st244;
tr346:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st244;
st244:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof244;
case 244:
#line 4975 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr345;
		case 32: goto tr345;
		case 59: goto tr347;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr346;
	} else if ( (*( state.p)) >= 9 )
		goto tr345;
	goto st0;
st245:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof245;
case 245:
	if ( (*( state.p)) == 107 )
		goto st246;
	goto st0;
st246:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof246;
case 246:
	if ( (*( state.p)) == 105 )
		goto st247;
	goto st0;
st247:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof247;
case 247:
	if ( (*( state.p)) == 110 )
		goto st248;
	goto st0;
st248:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof248;
case 248:
	switch( (*( state.p)) ) {
		case 13: goto st249;
		case 32: goto st249;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st249;
	goto st0;
st249:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof249;
case 249:
	switch( (*( state.p)) ) {
		case 13: goto st249;
		case 32: goto st249;
		case 34: goto tr352;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st249;
	goto st0;
tr353:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st250;
tr352:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st250;
tr355:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 250; goto st47;}}
	goto st250;
st250:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof250;
case 250:
#line 5051 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st251;
		case 92: goto tr355;
	}
	goto tr353;
st251:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof251;
case 251:
	switch( (*( state.p)) ) {
		case 13: goto tr356;
		case 32: goto tr356;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr356;
	goto st0;
tr356:
#line 164 "configparser.rl"
	{ skin.text = state.match; }
	goto st252;
st252:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof252;
case 252:
#line 5076 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st252;
		case 32: goto st252;
		case 98: goto st253;
		case 100: goto st298;
		case 110: goto st301;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st252;
	goto st0;
st253:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof253;
case 253:
	if ( (*( state.p)) == 114 )
		goto st254;
	goto st0;
st254:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof254;
case 254:
	if ( (*( state.p)) == 105 )
		goto st255;
	goto st0;
st255:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof255;
case 255:
	if ( (*( state.p)) == 103 )
		goto st256;
	goto st0;
st256:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof256;
case 256:
	if ( (*( state.p)) == 104 )
		goto st257;
	goto st0;
st257:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof257;
case 257:
	if ( (*( state.p)) == 116 )
		goto st258;
	goto st0;
st258:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof258;
case 258:
	switch( (*( state.p)) ) {
		case 13: goto tr366;
		case 32: goto tr366;
		case 95: goto tr367;
		case 98: goto tr368;
		case 99: goto tr369;
		case 103: goto tr370;
		case 109: goto tr371;
		case 114: goto tr372;
		case 119: goto tr373;
		case 121: goto tr374;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr366;
	goto st0;
tr366:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st259;
tr431:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st259;
st259:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof259;
case 259:
#line 5153 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st259;
		case 32: goto st259;
		case 98: goto st260;
		case 99: goto st267;
		case 103: goto st271;
		case 109: goto st276;
		case 114: goto st283;
		case 119: goto st286;
		case 121: goto st291;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st259;
	goto st0;
tr368:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st260;
tr433:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st260;
st260:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof260;
case 260:
#line 5180 "configparser.h"
	if ( (*( state.p)) == 108 )
		goto st261;
	goto st0;
st261:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof261;
case 261:
	switch( (*( state.p)) ) {
		case 97: goto st262;
		case 117: goto st265;
	}
	goto st0;
st262:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof262;
case 262:
	if ( (*( state.p)) == 99 )
		goto st263;
	goto st0;
st263:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof263;
case 263:
	if ( (*( state.p)) == 107 )
		goto st264;
	goto st0;
st264:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof264;
case 264:
	switch( (*( state.p)) ) {
		case 13: goto tr388;
		case 32: goto tr388;
		case 59: goto tr389;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr388;
	goto st0;
st265:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof265;
case 265:
	if ( (*( state.p)) == 101 )
		goto st266;
	goto st0;
st266:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof266;
case 266:
	switch( (*( state.p)) ) {
		case 13: goto tr391;
		case 32: goto tr391;
		case 59: goto tr392;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr391;
	goto st0;
tr369:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st267;
tr434:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st267;
st267:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof267;
case 267:
#line 5250 "configparser.h"
	if ( (*( state.p)) == 121 )
		goto st268;
	goto st0;
st268:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof268;
case 268:
	if ( (*( state.p)) == 97 )
		goto st269;
	goto st0;
st269:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof269;
case 269:
	if ( (*( state.p)) == 110 )
		goto st270;
	goto st0;
st270:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof270;
case 270:
	switch( (*( state.p)) ) {
		case 13: goto tr396;
		case 32: goto tr396;
		case 59: goto tr397;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr396;
	goto st0;
tr370:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st271;
tr435:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st271;
st271:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof271;
case 271:
#line 5292 "configparser.h"
	if ( (*( state.p)) == 114 )
		goto st272;
	goto st0;
st272:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof272;
case 272:
	if ( (*( state.p)) == 101 )
		goto st273;
	goto st0;
st273:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof273;
case 273:
	if ( (*( state.p)) == 101 )
		goto st274;
	goto st0;
st274:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof274;
case 274:
	if ( (*( state.p)) == 110 )
		goto st275;
	goto st0;
st275:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof275;
case 275:
	switch( (*( state.p)) ) {
		case 13: goto tr402;
		case 32: goto tr402;
		case 59: goto tr403;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr402;
	goto st0;
tr371:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st276;
tr436:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st276;
st276:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof276;
case 276:
#line 5341 "configparser.h"
	if ( (*( state.p)) == 97 )
		goto st277;
	goto st0;
st277:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof277;
case 277:
	if ( (*( state.p)) == 103 )
		goto st278;
	goto st0;
st278:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof278;
case 278:
	if ( (*( state.p)) == 101 )
		goto st279;
	goto st0;
st279:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof279;
case 279:
	if ( (*( state.p)) == 110 )
		goto st280;
	goto st0;
st280:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof280;
case 280:
	if ( (*( state.p)) == 116 )
		goto st281;
	goto st0;
st281:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof281;
case 281:
	if ( (*( state.p)) == 97 )
		goto st282;
	goto st0;
st282:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof282;
case 282:
	switch( (*( state.p)) ) {
		case 13: goto tr410;
		case 32: goto tr410;
		case 59: goto tr411;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr410;
	goto st0;
tr372:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st283;
tr437:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st283;
st283:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof283;
case 283:
#line 5404 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st284;
	goto st0;
st284:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof284;
case 284:
	if ( (*( state.p)) == 100 )
		goto st285;
	goto st0;
st285:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof285;
case 285:
	switch( (*( state.p)) ) {
		case 13: goto tr414;
		case 32: goto tr414;
		case 59: goto tr415;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr414;
	goto st0;
tr373:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st286;
tr438:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st286;
st286:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof286;
case 286:
#line 5439 "configparser.h"
	if ( (*( state.p)) == 104 )
		goto st287;
	goto st0;
st287:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof287;
case 287:
	if ( (*( state.p)) == 105 )
		goto st288;
	goto st0;
st288:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof288;
case 288:
	if ( (*( state.p)) == 116 )
		goto st289;
	goto st0;
st289:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof289;
case 289:
	if ( (*( state.p)) == 101 )
		goto st290;
	goto st0;
st290:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof290;
case 290:
	switch( (*( state.p)) ) {
		case 13: goto tr420;
		case 32: goto tr420;
		case 59: goto tr421;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr420;
	goto st0;
tr374:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st291;
tr439:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st291;
st291:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof291;
case 291:
#line 5488 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st292;
	goto st0;
st292:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof292;
case 292:
	if ( (*( state.p)) == 108 )
		goto st293;
	goto st0;
st293:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof293;
case 293:
	if ( (*( state.p)) == 108 )
		goto st294;
	goto st0;
st294:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof294;
case 294:
	if ( (*( state.p)) == 111 )
		goto st295;
	goto st0;
st295:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof295;
case 295:
	if ( (*( state.p)) == 119 )
		goto st296;
	goto st0;
st296:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof296;
case 296:
	switch( (*( state.p)) ) {
		case 13: goto tr427;
		case 32: goto tr427;
		case 59: goto tr428;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr427;
	goto st0;
tr367:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st297;
tr432:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st297;
st297:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof297;
case 297:
#line 5544 "configparser.h"
	switch( (*( state.p)) ) {
		case 98: goto st260;
		case 99: goto st267;
		case 103: goto st271;
		case 109: goto st276;
		case 114: goto st283;
		case 119: goto st286;
		case 121: goto st291;
	}
	goto st0;
st298:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof298;
case 298:
	if ( (*( state.p)) == 105 )
		goto st299;
	goto st0;
st299:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof299;
case 299:
	if ( (*( state.p)) == 109 )
		goto st300;
	goto st0;
st300:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof300;
case 300:
	switch( (*( state.p)) ) {
		case 13: goto tr431;
		case 32: goto tr431;
		case 95: goto tr432;
		case 98: goto tr433;
		case 99: goto tr434;
		case 103: goto tr435;
		case 109: goto tr436;
		case 114: goto tr437;
		case 119: goto tr438;
		case 121: goto tr439;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr431;
	goto st0;
st301:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof301;
case 301:
	if ( (*( state.p)) == 111 )
		goto st302;
	goto st0;
st302:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof302;
case 302:
	if ( (*( state.p)) == 110 )
		goto st303;
	goto st0;
st303:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof303;
case 303:
	if ( (*( state.p)) == 101 )
		goto st264;
	goto st0;
st304:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof304;
case 304:
	if ( (*( state.p)) == 111 )
		goto st305;
	goto st0;
st305:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof305;
case 305:
	if ( (*( state.p)) == 110 )
		goto st306;
	goto st0;
st306:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof306;
case 306:
	if ( (*( state.p)) == 101 )
		goto st307;
	goto st0;
st307:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof307;
case 307:
	switch( (*( state.p)) ) {
		case 13: goto tr445;
		case 32: goto tr445;
		case 59: goto tr446;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr445;
	goto st0;
st308:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof308;
case 308:
	if ( (*( state.p)) == 97 )
		goto st309;
	goto st0;
st309:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof309;
case 309:
	if ( (*( state.p)) == 110 )
		goto st310;
	goto st0;
st310:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof310;
case 310:
	if ( (*( state.p)) == 100 )
		goto st311;
	goto st0;
st311:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof311;
case 311:
	if ( (*( state.p)) == 111 )
		goto st312;
	goto st0;
st312:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof312;
case 312:
	if ( (*( state.p)) == 109 )
		goto st313;
	goto st0;
st313:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof313;
case 313:
	switch( (*( state.p)) ) {
		case 13: goto tr452;
		case 32: goto tr452;
		case 59: goto tr453;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr452;
	goto st0;
st314:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof314;
case 314:
	if ( (*( state.p)) == 101 )
		goto st315;
	goto st0;
st315:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof315;
case 315:
	if ( (*( state.p)) == 101 )
		goto st316;
	goto st0;
st316:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof316;
case 316:
	if ( (*( state.p)) == 107 )
		goto st317;
	goto st0;
st317:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof317;
case 317:
	if ( (*( state.p)) == 95 )
		goto st318;
	goto st0;
st318:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof318;
case 318:
	if ( (*( state.p)) == 112 )
		goto st319;
	goto st0;
st319:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof319;
case 319:
	if ( (*( state.p)) == 108 )
		goto st320;
	goto st0;
st320:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof320;
case 320:
	if ( (*( state.p)) == 97 )
		goto st321;
	goto st0;
st321:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof321;
case 321:
	if ( (*( state.p)) == 121 )
		goto st322;
	goto st0;
st322:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof322;
case 322:
	if ( (*( state.p)) == 101 )
		goto st323;
	goto st0;
st323:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof323;
case 323:
	if ( (*( state.p)) == 114 )
		goto st324;
	goto st0;
st324:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof324;
case 324:
	switch( (*( state.p)) ) {
		case 13: goto tr464;
		case 32: goto tr464;
		case 59: goto tr465;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr464;
	goto st0;
st325:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof325;
case 325:
	if ( (*( state.p)) == 116 )
		goto st326;
	goto st0;
st326:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof326;
case 326:
	if ( (*( state.p)) == 97 )
		goto st327;
	goto st0;
st327:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof327;
case 327:
	if ( (*( state.p)) == 99 )
		goto st328;
	goto st0;
st328:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof328;
case 328:
	if ( (*( state.p)) == 107 )
		goto st329;
	goto st0;
st329:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof329;
case 329:
	switch( (*( state.p)) ) {
		case 13: goto st330;
		case 32: goto st330;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st330;
	goto st0;
st330:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof330;
case 330:
	switch( (*( state.p)) ) {
		case 13: goto st330;
		case 32: goto st330;
		case 45: goto tr471;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr472;
	} else if ( (*( state.p)) >= 9 )
		goto st330;
	goto st0;
tr471:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st331;
st331:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof331;
case 331:
#line 5839 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr473;
	goto st0;
tr472:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st332;
tr473:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st332;
st332:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof332;
case 332:
#line 5863 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr474;
		case 32: goto tr474;
		case 46: goto tr475;
		case 59: goto tr476;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr473;
	} else if ( (*( state.p)) >= 9 )
		goto tr474;
	goto st0;
tr475:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st333;
st333:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof333;
case 333:
#line 5886 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr477;
	goto st0;
tr477:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st334;
st334:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof334;
case 334:
#line 5900 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr474;
		case 32: goto tr474;
		case 59: goto tr476;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr477;
	} else if ( (*( state.p)) >= 9 )
		goto tr474;
	goto st0;
st335:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof335;
case 335:
	switch( (*( state.p)) ) {
		case 13: goto st335;
		case 32: goto st335;
		case 97: goto st336;
		case 99: goto st346;
		case 100: goto st353;
		case 104: goto st371;
		case 110: goto st380;
		case 115: goto st387;
		case 116: goto st463;
		case 117: goto st475;
		case 125: goto tr487;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st335;
	goto st0;
st336:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof336;
case 336:
	if ( (*( state.p)) == 116 )
		goto st337;
	goto st0;
st337:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof337;
case 337:
	if ( (*( state.p)) == 116 )
		goto st338;
	goto st0;
st338:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof338;
case 338:
	if ( (*( state.p)) == 97 )
		goto st339;
	goto st0;
st339:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof339;
case 339:
	if ( (*( state.p)) == 99 )
		goto st340;
	goto st0;
st340:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof340;
case 340:
	if ( (*( state.p)) == 107 )
		goto st341;
	goto st0;
st341:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof341;
case 341:
	switch( (*( state.p)) ) {
		case 13: goto st342;
		case 32: goto st342;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st342;
	goto st0;
st342:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof342;
case 342:
	switch( (*( state.p)) ) {
		case 13: goto st342;
		case 32: goto st342;
		case 45: goto tr494;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr495;
	} else if ( (*( state.p)) >= 9 )
		goto st342;
	goto st0;
tr494:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st343;
st343:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof343;
case 343:
#line 6007 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr496;
	goto st0;
tr495:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st344;
tr496:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st344;
st344:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof344;
case 344:
#line 6031 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr497;
		case 32: goto tr497;
		case 46: goto tr498;
		case 59: goto tr499;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr496;
	} else if ( (*( state.p)) >= 9 )
		goto tr497;
	goto st0;
tr487:
#line 269 "configparser.rl"
	{ { state.cs =  state.stack[-- state.top];goto _again;} }
	goto st345;
tr497:
#line 257 "configparser.rl"
	{ des.attack = toreal(state.match); }
	goto st345;
tr508:
#line 252 "configparser.rl"
	{ des.count = toint(state.match); }
	goto st345;
tr522:
#line 258 "configparser.rl"
	{ des.defense = toreal(state.match); }
	goto st345;
tr533:
#line 256 "configparser.rl"
	{ des.descr = state.match; }
	goto st345;
tr542:
#line 260 "configparser.rl"
	{ des.heal = toreal(state.match); }
	goto st345;
tr554:
#line 253 "configparser.rl"
	{ des.name = state.match; }
	goto st345;
tr598:
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st345;
tr601:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st345;
tr606:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st345;
tr612:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st345;
tr620:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st345;
tr624:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st345;
tr630:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st345;
tr637:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st345;
tr659:
#line 255 "configparser.rl"
	{ des.slot = state.match; }
	goto st345;
tr671:
#line 259 "configparser.rl"
	{ des.stackrange = toint(state.match); }
	goto st345;
tr685:
#line 262 "configparser.rl"
	{ des.throwrange = toint(state.match); }
	goto st345;
tr693:
#line 261 "configparser.rl"
	{ des.usable = true; }
	goto st345;
st345:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof345;
case 345:
#line 6138 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st345;
		case 32: goto st345;
		case 59: goto st1358;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st345;
	goto st0;
tr499:
#line 257 "configparser.rl"
	{ des.attack = toreal(state.match); }
	goto st1358;
tr510:
#line 252 "configparser.rl"
	{ des.count = toint(state.match); }
	goto st1358;
tr524:
#line 258 "configparser.rl"
	{ des.defense = toreal(state.match); }
	goto st1358;
tr534:
#line 256 "configparser.rl"
	{ des.descr = state.match; }
	goto st1358;
tr544:
#line 260 "configparser.rl"
	{ des.heal = toreal(state.match); }
	goto st1358;
tr555:
#line 253 "configparser.rl"
	{ des.name = state.match; }
	goto st1358;
tr599:
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st1358;
tr602:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st1358;
tr607:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st1358;
tr613:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st1358;
tr621:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st1358;
tr625:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st1358;
tr631:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st1358;
tr638:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 254 "configparser.rl"
	{ des.skin = skin; }
	goto st1358;
tr660:
#line 255 "configparser.rl"
	{ des.slot = state.match; }
	goto st1358;
tr673:
#line 259 "configparser.rl"
	{ des.stackrange = toint(state.match); }
	goto st1358;
tr687:
#line 262 "configparser.rl"
	{ des.throwrange = toint(state.match); }
	goto st1358;
tr694:
#line 261 "configparser.rl"
	{ des.usable = true; }
	goto st1358;
st1358:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1358;
case 1358:
#line 6237 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st335;
		case 32: goto st335;
		case 97: goto st336;
		case 99: goto st346;
		case 100: goto st353;
		case 104: goto st371;
		case 110: goto st380;
		case 115: goto st387;
		case 116: goto st463;
		case 117: goto st475;
		case 125: goto tr487;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st335;
	goto st0;
st346:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof346;
case 346:
	if ( (*( state.p)) == 111 )
		goto st347;
	goto st0;
st347:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof347;
case 347:
	if ( (*( state.p)) == 117 )
		goto st348;
	goto st0;
st348:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof348;
case 348:
	if ( (*( state.p)) == 110 )
		goto st349;
	goto st0;
st349:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof349;
case 349:
	if ( (*( state.p)) == 116 )
		goto st350;
	goto st0;
st350:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof350;
case 350:
	switch( (*( state.p)) ) {
		case 13: goto st351;
		case 32: goto st351;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st351;
	goto st0;
st351:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof351;
case 351:
	switch( (*( state.p)) ) {
		case 13: goto st351;
		case 32: goto st351;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr507;
	} else if ( (*( state.p)) >= 9 )
		goto st351;
	goto st0;
tr507:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st352;
tr509:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st352;
st352:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof352;
case 352:
#line 6327 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr508;
		case 32: goto tr508;
		case 59: goto tr510;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr509;
	} else if ( (*( state.p)) >= 9 )
		goto tr508;
	goto st0;
st353:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof353;
case 353:
	if ( (*( state.p)) == 101 )
		goto st354;
	goto st0;
st354:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof354;
case 354:
	switch( (*( state.p)) ) {
		case 102: goto st355;
		case 115: goto st365;
	}
	goto st0;
st355:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof355;
case 355:
	if ( (*( state.p)) == 101 )
		goto st356;
	goto st0;
st356:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof356;
case 356:
	if ( (*( state.p)) == 110 )
		goto st357;
	goto st0;
st357:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof357;
case 357:
	if ( (*( state.p)) == 115 )
		goto st358;
	goto st0;
st358:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof358;
case 358:
	if ( (*( state.p)) == 101 )
		goto st359;
	goto st0;
st359:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof359;
case 359:
	switch( (*( state.p)) ) {
		case 13: goto st360;
		case 32: goto st360;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st360;
	goto st0;
st360:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof360;
case 360:
	switch( (*( state.p)) ) {
		case 13: goto st360;
		case 32: goto st360;
		case 45: goto tr519;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr520;
	} else if ( (*( state.p)) >= 9 )
		goto st360;
	goto st0;
tr519:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st361;
st361:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof361;
case 361:
#line 6423 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr521;
	goto st0;
tr520:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st362;
tr521:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st362;
st362:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof362;
case 362:
#line 6447 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr522;
		case 32: goto tr522;
		case 46: goto tr523;
		case 59: goto tr524;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr521;
	} else if ( (*( state.p)) >= 9 )
		goto tr522;
	goto st0;
tr523:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st363;
st363:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof363;
case 363:
#line 6470 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr525;
	goto st0;
tr525:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st364;
st364:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof364;
case 364:
#line 6484 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr522;
		case 32: goto tr522;
		case 59: goto tr524;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr525;
	} else if ( (*( state.p)) >= 9 )
		goto tr522;
	goto st0;
st365:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof365;
case 365:
	if ( (*( state.p)) == 99 )
		goto st366;
	goto st0;
st366:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof366;
case 366:
	if ( (*( state.p)) == 114 )
		goto st367;
	goto st0;
st367:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof367;
case 367:
	switch( (*( state.p)) ) {
		case 13: goto st368;
		case 32: goto st368;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st368;
	goto st0;
st368:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof368;
case 368:
	switch( (*( state.p)) ) {
		case 13: goto st368;
		case 32: goto st368;
		case 34: goto tr529;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st368;
	goto st0;
tr530:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st369;
tr529:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st369;
tr532:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 369; goto st47;}}
	goto st369;
st369:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof369;
case 369:
#line 6553 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st370;
		case 92: goto tr532;
	}
	goto tr530;
st370:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof370;
case 370:
	switch( (*( state.p)) ) {
		case 13: goto tr533;
		case 32: goto tr533;
		case 59: goto tr534;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr533;
	goto st0;
st371:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof371;
case 371:
	if ( (*( state.p)) == 101 )
		goto st372;
	goto st0;
st372:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof372;
case 372:
	if ( (*( state.p)) == 97 )
		goto st373;
	goto st0;
st373:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof373;
case 373:
	if ( (*( state.p)) == 108 )
		goto st374;
	goto st0;
st374:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof374;
case 374:
	switch( (*( state.p)) ) {
		case 13: goto st375;
		case 32: goto st375;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st375;
	goto st0;
st375:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof375;
case 375:
	switch( (*( state.p)) ) {
		case 13: goto st375;
		case 32: goto st375;
		case 45: goto tr539;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr540;
	} else if ( (*( state.p)) >= 9 )
		goto st375;
	goto st0;
tr539:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st376;
st376:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof376;
case 376:
#line 6632 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr541;
	goto st0;
tr540:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st377;
tr541:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st377;
st377:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof377;
case 377:
#line 6656 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr542;
		case 32: goto tr542;
		case 46: goto tr543;
		case 59: goto tr544;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr541;
	} else if ( (*( state.p)) >= 9 )
		goto tr542;
	goto st0;
tr543:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st378;
st378:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof378;
case 378:
#line 6679 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr545;
	goto st0;
tr545:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st379;
st379:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof379;
case 379:
#line 6693 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr542;
		case 32: goto tr542;
		case 59: goto tr544;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr545;
	} else if ( (*( state.p)) >= 9 )
		goto tr542;
	goto st0;
st380:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof380;
case 380:
	if ( (*( state.p)) == 97 )
		goto st381;
	goto st0;
st381:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof381;
case 381:
	if ( (*( state.p)) == 109 )
		goto st382;
	goto st0;
st382:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof382;
case 382:
	if ( (*( state.p)) == 101 )
		goto st383;
	goto st0;
st383:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof383;
case 383:
	switch( (*( state.p)) ) {
		case 13: goto st384;
		case 32: goto st384;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st384;
	goto st0;
st384:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof384;
case 384:
	switch( (*( state.p)) ) {
		case 13: goto st384;
		case 32: goto st384;
		case 34: goto tr550;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st384;
	goto st0;
tr551:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st385;
tr550:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st385;
tr553:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 385; goto st47;}}
	goto st385;
st385:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof385;
case 385:
#line 6769 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st386;
		case 92: goto tr553;
	}
	goto tr551;
st386:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof386;
case 386:
	switch( (*( state.p)) ) {
		case 13: goto tr554;
		case 32: goto tr554;
		case 59: goto tr555;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr554;
	goto st0;
st387:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof387;
case 387:
	switch( (*( state.p)) ) {
		case 107: goto st388;
		case 108: goto st446;
		case 116: goto st452;
	}
	goto st0;
st388:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof388;
case 388:
	if ( (*( state.p)) == 105 )
		goto st389;
	goto st0;
st389:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof389;
case 389:
	if ( (*( state.p)) == 110 )
		goto st390;
	goto st0;
st390:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof390;
case 390:
	switch( (*( state.p)) ) {
		case 13: goto st391;
		case 32: goto st391;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st391;
	goto st0;
st391:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof391;
case 391:
	switch( (*( state.p)) ) {
		case 13: goto st391;
		case 32: goto st391;
		case 34: goto tr562;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st391;
	goto st0;
tr563:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st392;
tr562:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st392;
tr565:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 392; goto st47;}}
	goto st392;
st392:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof392;
case 392:
#line 6854 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st393;
		case 92: goto tr565;
	}
	goto tr563;
st393:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof393;
case 393:
	switch( (*( state.p)) ) {
		case 13: goto tr566;
		case 32: goto tr566;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr566;
	goto st0;
tr566:
#line 164 "configparser.rl"
	{ skin.text = state.match; }
	goto st394;
st394:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof394;
case 394:
#line 6879 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st394;
		case 32: goto st394;
		case 98: goto st395;
		case 100: goto st440;
		case 110: goto st443;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st394;
	goto st0;
st395:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof395;
case 395:
	if ( (*( state.p)) == 114 )
		goto st396;
	goto st0;
st396:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof396;
case 396:
	if ( (*( state.p)) == 105 )
		goto st397;
	goto st0;
st397:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof397;
case 397:
	if ( (*( state.p)) == 103 )
		goto st398;
	goto st0;
st398:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof398;
case 398:
	if ( (*( state.p)) == 104 )
		goto st399;
	goto st0;
st399:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof399;
case 399:
	if ( (*( state.p)) == 116 )
		goto st400;
	goto st0;
st400:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof400;
case 400:
	switch( (*( state.p)) ) {
		case 13: goto tr576;
		case 32: goto tr576;
		case 95: goto tr577;
		case 98: goto tr578;
		case 99: goto tr579;
		case 103: goto tr580;
		case 109: goto tr581;
		case 114: goto tr582;
		case 119: goto tr583;
		case 121: goto tr584;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr576;
	goto st0;
tr576:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st401;
tr641:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st401;
st401:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof401;
case 401:
#line 6956 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st401;
		case 32: goto st401;
		case 98: goto st402;
		case 99: goto st409;
		case 103: goto st413;
		case 109: goto st418;
		case 114: goto st425;
		case 119: goto st428;
		case 121: goto st433;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st401;
	goto st0;
tr578:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st402;
tr643:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st402;
st402:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof402;
case 402:
#line 6983 "configparser.h"
	if ( (*( state.p)) == 108 )
		goto st403;
	goto st0;
st403:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof403;
case 403:
	switch( (*( state.p)) ) {
		case 97: goto st404;
		case 117: goto st407;
	}
	goto st0;
st404:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof404;
case 404:
	if ( (*( state.p)) == 99 )
		goto st405;
	goto st0;
st405:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof405;
case 405:
	if ( (*( state.p)) == 107 )
		goto st406;
	goto st0;
st406:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof406;
case 406:
	switch( (*( state.p)) ) {
		case 13: goto tr598;
		case 32: goto tr598;
		case 59: goto tr599;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr598;
	goto st0;
st407:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof407;
case 407:
	if ( (*( state.p)) == 101 )
		goto st408;
	goto st0;
st408:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof408;
case 408:
	switch( (*( state.p)) ) {
		case 13: goto tr601;
		case 32: goto tr601;
		case 59: goto tr602;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr601;
	goto st0;
tr579:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st409;
tr644:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st409;
st409:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof409;
case 409:
#line 7053 "configparser.h"
	if ( (*( state.p)) == 121 )
		goto st410;
	goto st0;
st410:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof410;
case 410:
	if ( (*( state.p)) == 97 )
		goto st411;
	goto st0;
st411:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof411;
case 411:
	if ( (*( state.p)) == 110 )
		goto st412;
	goto st0;
st412:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof412;
case 412:
	switch( (*( state.p)) ) {
		case 13: goto tr606;
		case 32: goto tr606;
		case 59: goto tr607;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr606;
	goto st0;
tr580:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st413;
tr645:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st413;
st413:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof413;
case 413:
#line 7095 "configparser.h"
	if ( (*( state.p)) == 114 )
		goto st414;
	goto st0;
st414:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof414;
case 414:
	if ( (*( state.p)) == 101 )
		goto st415;
	goto st0;
st415:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof415;
case 415:
	if ( (*( state.p)) == 101 )
		goto st416;
	goto st0;
st416:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof416;
case 416:
	if ( (*( state.p)) == 110 )
		goto st417;
	goto st0;
st417:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof417;
case 417:
	switch( (*( state.p)) ) {
		case 13: goto tr612;
		case 32: goto tr612;
		case 59: goto tr613;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr612;
	goto st0;
tr581:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st418;
tr646:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st418;
st418:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof418;
case 418:
#line 7144 "configparser.h"
	if ( (*( state.p)) == 97 )
		goto st419;
	goto st0;
st419:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof419;
case 419:
	if ( (*( state.p)) == 103 )
		goto st420;
	goto st0;
st420:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof420;
case 420:
	if ( (*( state.p)) == 101 )
		goto st421;
	goto st0;
st421:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof421;
case 421:
	if ( (*( state.p)) == 110 )
		goto st422;
	goto st0;
st422:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof422;
case 422:
	if ( (*( state.p)) == 116 )
		goto st423;
	goto st0;
st423:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof423;
case 423:
	if ( (*( state.p)) == 97 )
		goto st424;
	goto st0;
st424:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof424;
case 424:
	switch( (*( state.p)) ) {
		case 13: goto tr620;
		case 32: goto tr620;
		case 59: goto tr621;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr620;
	goto st0;
tr582:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st425;
tr647:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st425;
st425:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof425;
case 425:
#line 7207 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st426;
	goto st0;
st426:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof426;
case 426:
	if ( (*( state.p)) == 100 )
		goto st427;
	goto st0;
st427:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof427;
case 427:
	switch( (*( state.p)) ) {
		case 13: goto tr624;
		case 32: goto tr624;
		case 59: goto tr625;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr624;
	goto st0;
tr583:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st428;
tr648:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st428;
st428:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof428;
case 428:
#line 7242 "configparser.h"
	if ( (*( state.p)) == 104 )
		goto st429;
	goto st0;
st429:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof429;
case 429:
	if ( (*( state.p)) == 105 )
		goto st430;
	goto st0;
st430:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof430;
case 430:
	if ( (*( state.p)) == 116 )
		goto st431;
	goto st0;
st431:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof431;
case 431:
	if ( (*( state.p)) == 101 )
		goto st432;
	goto st0;
st432:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof432;
case 432:
	switch( (*( state.p)) ) {
		case 13: goto tr630;
		case 32: goto tr630;
		case 59: goto tr631;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr630;
	goto st0;
tr584:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st433;
tr649:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st433;
st433:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof433;
case 433:
#line 7291 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st434;
	goto st0;
st434:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof434;
case 434:
	if ( (*( state.p)) == 108 )
		goto st435;
	goto st0;
st435:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof435;
case 435:
	if ( (*( state.p)) == 108 )
		goto st436;
	goto st0;
st436:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof436;
case 436:
	if ( (*( state.p)) == 111 )
		goto st437;
	goto st0;
st437:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof437;
case 437:
	if ( (*( state.p)) == 119 )
		goto st438;
	goto st0;
st438:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof438;
case 438:
	switch( (*( state.p)) ) {
		case 13: goto tr637;
		case 32: goto tr637;
		case 59: goto tr638;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr637;
	goto st0;
tr577:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st439;
tr642:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st439;
st439:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof439;
case 439:
#line 7347 "configparser.h"
	switch( (*( state.p)) ) {
		case 98: goto st402;
		case 99: goto st409;
		case 103: goto st413;
		case 109: goto st418;
		case 114: goto st425;
		case 119: goto st428;
		case 121: goto st433;
	}
	goto st0;
st440:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof440;
case 440:
	if ( (*( state.p)) == 105 )
		goto st441;
	goto st0;
st441:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof441;
case 441:
	if ( (*( state.p)) == 109 )
		goto st442;
	goto st0;
st442:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof442;
case 442:
	switch( (*( state.p)) ) {
		case 13: goto tr641;
		case 32: goto tr641;
		case 95: goto tr642;
		case 98: goto tr643;
		case 99: goto tr644;
		case 103: goto tr645;
		case 109: goto tr646;
		case 114: goto tr647;
		case 119: goto tr648;
		case 121: goto tr649;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr641;
	goto st0;
st443:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof443;
case 443:
	if ( (*( state.p)) == 111 )
		goto st444;
	goto st0;
st444:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof444;
case 444:
	if ( (*( state.p)) == 110 )
		goto st445;
	goto st0;
st445:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof445;
case 445:
	if ( (*( state.p)) == 101 )
		goto st406;
	goto st0;
st446:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof446;
case 446:
	if ( (*( state.p)) == 111 )
		goto st447;
	goto st0;
st447:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof447;
case 447:
	if ( (*( state.p)) == 116 )
		goto st448;
	goto st0;
st448:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof448;
case 448:
	switch( (*( state.p)) ) {
		case 13: goto st449;
		case 32: goto st449;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st449;
	goto st0;
st449:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof449;
case 449:
	switch( (*( state.p)) ) {
		case 13: goto st449;
		case 32: goto st449;
		case 34: goto tr655;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st449;
	goto st0;
tr656:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st450;
tr655:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st450;
tr658:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 450; goto st47;}}
	goto st450;
st450:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof450;
case 450:
#line 7469 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st451;
		case 92: goto tr658;
	}
	goto tr656;
st451:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof451;
case 451:
	switch( (*( state.p)) ) {
		case 13: goto tr659;
		case 32: goto tr659;
		case 59: goto tr660;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr659;
	goto st0;
st452:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof452;
case 452:
	if ( (*( state.p)) == 97 )
		goto st453;
	goto st0;
st453:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof453;
case 453:
	if ( (*( state.p)) == 99 )
		goto st454;
	goto st0;
st454:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof454;
case 454:
	if ( (*( state.p)) == 107 )
		goto st455;
	goto st0;
st455:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof455;
case 455:
	if ( (*( state.p)) == 114 )
		goto st456;
	goto st0;
st456:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof456;
case 456:
	if ( (*( state.p)) == 97 )
		goto st457;
	goto st0;
st457:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof457;
case 457:
	if ( (*( state.p)) == 110 )
		goto st458;
	goto st0;
st458:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof458;
case 458:
	if ( (*( state.p)) == 103 )
		goto st459;
	goto st0;
st459:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof459;
case 459:
	if ( (*( state.p)) == 101 )
		goto st460;
	goto st0;
st460:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof460;
case 460:
	switch( (*( state.p)) ) {
		case 13: goto st461;
		case 32: goto st461;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st461;
	goto st0;
st461:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof461;
case 461:
	switch( (*( state.p)) ) {
		case 13: goto st461;
		case 32: goto st461;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr670;
	} else if ( (*( state.p)) >= 9 )
		goto st461;
	goto st0;
tr670:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st462;
tr672:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st462;
st462:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof462;
case 462:
#line 7588 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr671;
		case 32: goto tr671;
		case 59: goto tr673;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr672;
	} else if ( (*( state.p)) >= 9 )
		goto tr671;
	goto st0;
st463:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof463;
case 463:
	if ( (*( state.p)) == 104 )
		goto st464;
	goto st0;
st464:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof464;
case 464:
	if ( (*( state.p)) == 114 )
		goto st465;
	goto st0;
st465:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof465;
case 465:
	if ( (*( state.p)) == 111 )
		goto st466;
	goto st0;
st466:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof466;
case 466:
	if ( (*( state.p)) == 119 )
		goto st467;
	goto st0;
st467:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof467;
case 467:
	if ( (*( state.p)) == 114 )
		goto st468;
	goto st0;
st468:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof468;
case 468:
	if ( (*( state.p)) == 97 )
		goto st469;
	goto st0;
st469:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof469;
case 469:
	if ( (*( state.p)) == 110 )
		goto st470;
	goto st0;
st470:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof470;
case 470:
	if ( (*( state.p)) == 103 )
		goto st471;
	goto st0;
st471:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof471;
case 471:
	if ( (*( state.p)) == 101 )
		goto st472;
	goto st0;
st472:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof472;
case 472:
	switch( (*( state.p)) ) {
		case 13: goto st473;
		case 32: goto st473;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st473;
	goto st0;
st473:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof473;
case 473:
	switch( (*( state.p)) ) {
		case 13: goto st473;
		case 32: goto st473;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr684;
	} else if ( (*( state.p)) >= 9 )
		goto st473;
	goto st0;
tr684:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st474;
tr686:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st474;
st474:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof474;
case 474:
#line 7708 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr685;
		case 32: goto tr685;
		case 59: goto tr687;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr686;
	} else if ( (*( state.p)) >= 9 )
		goto tr685;
	goto st0;
st475:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof475;
case 475:
	if ( (*( state.p)) == 115 )
		goto st476;
	goto st0;
st476:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof476;
case 476:
	if ( (*( state.p)) == 97 )
		goto st477;
	goto st0;
st477:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof477;
case 477:
	if ( (*( state.p)) == 98 )
		goto st478;
	goto st0;
st478:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof478;
case 478:
	if ( (*( state.p)) == 108 )
		goto st479;
	goto st0;
st479:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof479;
case 479:
	if ( (*( state.p)) == 101 )
		goto st480;
	goto st0;
st480:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof480;
case 480:
	switch( (*( state.p)) ) {
		case 13: goto tr693;
		case 32: goto tr693;
		case 59: goto tr694;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr693;
	goto st0;
tr498:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st481;
st481:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof481;
case 481:
#line 7777 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr695;
	goto st0;
tr695:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st482;
st482:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof482;
case 482:
#line 7791 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr497;
		case 32: goto tr497;
		case 59: goto tr499;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr695;
	} else if ( (*( state.p)) >= 9 )
		goto tr497;
	goto st0;
st483:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof483;
case 483:
	switch( (*( state.p)) ) {
		case 13: goto st483;
		case 32: goto st483;
		case 99: goto st484;
		case 100: goto st492;
		case 110: goto st499;
		case 112: goto st506;
		case 115: goto st532;
		case 116: goto st598;
		case 118: goto st610;
		case 119: goto st619;
		case 125: goto tr705;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st483;
	goto st0;
st484:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof484;
case 484:
	if ( (*( state.p)) == 111 )
		goto st485;
	goto st0;
st485:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof485;
case 485:
	if ( (*( state.p)) == 117 )
		goto st486;
	goto st0;
st486:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof486;
case 486:
	if ( (*( state.p)) == 110 )
		goto st487;
	goto st0;
st487:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof487;
case 487:
	if ( (*( state.p)) == 116 )
		goto st488;
	goto st0;
st488:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof488;
case 488:
	switch( (*( state.p)) ) {
		case 13: goto st489;
		case 32: goto st489;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st489;
	goto st0;
st489:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof489;
case 489:
	switch( (*( state.p)) ) {
		case 13: goto st489;
		case 32: goto st489;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr711;
	} else if ( (*( state.p)) >= 9 )
		goto st489;
	goto st0;
tr711:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st490;
tr713:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st490;
st490:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof490;
case 490:
#line 7896 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr712;
		case 32: goto tr712;
		case 59: goto tr714;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr713;
	} else if ( (*( state.p)) >= 9 )
		goto tr712;
	goto st0;
tr705:
#line 314 "configparser.rl"
	{ { state.cs =  state.stack[-- state.top];goto _again;} }
	goto st491;
tr712:
#line 300 "configparser.rl"
	{ ter.count = toint(state.match); }
	goto st491;
tr723:
#line 307 "configparser.rl"
	{ ter.decay = toint(state.match); }
	goto st491;
tr734:
#line 301 "configparser.rl"
	{ ter.name = state.match; }
	goto st491;
tr753:
#line 293 "configparser.rl"
	{ ter.placement = Terrain::placement_t::corner; }
	goto st491;
tr759:
#line 291 "configparser.rl"
	{ ter.placement = Terrain::placement_t::floor; }
	goto st491;
tr765:
#line 292 "configparser.rl"
	{ ter.placement = Terrain::placement_t::water; }
	goto st491;
tr808:
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st491;
tr811:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st491;
tr816:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st491;
tr822:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st491;
tr830:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st491;
tr834:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st491;
tr840:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st491;
tr847:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st491;
tr868:
#line 304 "configparser.rl"
	{ ter.stairs = toint(state.match); }
	goto st491;
tr885:
#line 297 "configparser.rl"
	{ ter.tunnel_y = toint(state.match); }
	goto st491;
tr895:
#line 305 "configparser.rl"
	{ ter.viewblock = true; }
	goto st491;
tr905:
#line 306 "configparser.rl"
	{ ter.walkblock = true; }
	goto st491;
st491:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof491;
case 491:
#line 8002 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st491;
		case 32: goto st491;
		case 59: goto st1359;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st491;
	goto st0;
tr714:
#line 300 "configparser.rl"
	{ ter.count = toint(state.match); }
	goto st1359;
tr725:
#line 307 "configparser.rl"
	{ ter.decay = toint(state.match); }
	goto st1359;
tr735:
#line 301 "configparser.rl"
	{ ter.name = state.match; }
	goto st1359;
tr754:
#line 293 "configparser.rl"
	{ ter.placement = Terrain::placement_t::corner; }
	goto st1359;
tr760:
#line 291 "configparser.rl"
	{ ter.placement = Terrain::placement_t::floor; }
	goto st1359;
tr766:
#line 292 "configparser.rl"
	{ ter.placement = Terrain::placement_t::water; }
	goto st1359;
tr809:
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st1359;
tr812:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st1359;
tr817:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st1359;
tr823:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st1359;
tr831:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st1359;
tr835:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st1359;
tr841:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st1359;
tr848:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 302 "configparser.rl"
	{ ter.skin = skin; }
	goto st1359;
tr870:
#line 304 "configparser.rl"
	{ ter.stairs = toint(state.match); }
	goto st1359;
tr886:
#line 297 "configparser.rl"
	{ ter.tunnel_y = toint(state.match); }
	goto st1359;
tr896:
#line 305 "configparser.rl"
	{ ter.viewblock = true; }
	goto st1359;
tr906:
#line 306 "configparser.rl"
	{ ter.walkblock = true; }
	goto st1359;
st1359:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1359;
case 1359:
#line 8101 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st483;
		case 32: goto st483;
		case 99: goto st484;
		case 100: goto st492;
		case 110: goto st499;
		case 112: goto st506;
		case 115: goto st532;
		case 116: goto st598;
		case 118: goto st610;
		case 119: goto st619;
		case 125: goto tr705;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st483;
	goto st0;
st492:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof492;
case 492:
	if ( (*( state.p)) == 101 )
		goto st493;
	goto st0;
st493:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof493;
case 493:
	if ( (*( state.p)) == 99 )
		goto st494;
	goto st0;
st494:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof494;
case 494:
	if ( (*( state.p)) == 97 )
		goto st495;
	goto st0;
st495:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof495;
case 495:
	if ( (*( state.p)) == 121 )
		goto st496;
	goto st0;
st496:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof496;
case 496:
	switch( (*( state.p)) ) {
		case 13: goto st497;
		case 32: goto st497;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st497;
	goto st0;
st497:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof497;
case 497:
	switch( (*( state.p)) ) {
		case 13: goto st497;
		case 32: goto st497;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr722;
	} else if ( (*( state.p)) >= 9 )
		goto st497;
	goto st0;
tr722:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st498;
tr724:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st498;
st498:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof498;
case 498:
#line 8191 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr723;
		case 32: goto tr723;
		case 59: goto tr725;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr724;
	} else if ( (*( state.p)) >= 9 )
		goto tr723;
	goto st0;
st499:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof499;
case 499:
	if ( (*( state.p)) == 97 )
		goto st500;
	goto st0;
st500:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof500;
case 500:
	if ( (*( state.p)) == 109 )
		goto st501;
	goto st0;
st501:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof501;
case 501:
	if ( (*( state.p)) == 101 )
		goto st502;
	goto st0;
st502:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof502;
case 502:
	switch( (*( state.p)) ) {
		case 13: goto st503;
		case 32: goto st503;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st503;
	goto st0;
st503:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof503;
case 503:
	switch( (*( state.p)) ) {
		case 13: goto st503;
		case 32: goto st503;
		case 34: goto tr730;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st503;
	goto st0;
tr731:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st504;
tr730:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st504;
tr733:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 504; goto st47;}}
	goto st504;
st504:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof504;
case 504:
#line 8267 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st505;
		case 92: goto tr733;
	}
	goto tr731;
st505:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof505;
case 505:
	switch( (*( state.p)) ) {
		case 13: goto tr734;
		case 32: goto tr734;
		case 59: goto tr735;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr734;
	goto st0;
st506:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof506;
case 506:
	if ( (*( state.p)) == 108 )
		goto st507;
	goto st0;
st507:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof507;
case 507:
	if ( (*( state.p)) == 97 )
		goto st508;
	goto st0;
st508:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof508;
case 508:
	if ( (*( state.p)) == 99 )
		goto st509;
	goto st0;
st509:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof509;
case 509:
	if ( (*( state.p)) == 101 )
		goto st510;
	goto st0;
st510:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof510;
case 510:
	if ( (*( state.p)) == 109 )
		goto st511;
	goto st0;
st511:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof511;
case 511:
	if ( (*( state.p)) == 101 )
		goto st512;
	goto st0;
st512:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof512;
case 512:
	if ( (*( state.p)) == 110 )
		goto st513;
	goto st0;
st513:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof513;
case 513:
	if ( (*( state.p)) == 116 )
		goto st514;
	goto st0;
st514:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof514;
case 514:
	switch( (*( state.p)) ) {
		case 13: goto st515;
		case 32: goto st515;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st515;
	goto st0;
st515:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof515;
case 515:
	switch( (*( state.p)) ) {
		case 13: goto st515;
		case 32: goto st515;
		case 99: goto st516;
		case 102: goto st522;
		case 119: goto st527;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st515;
	goto st0;
st516:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof516;
case 516:
	if ( (*( state.p)) == 111 )
		goto st517;
	goto st0;
st517:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof517;
case 517:
	if ( (*( state.p)) == 114 )
		goto st518;
	goto st0;
st518:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof518;
case 518:
	if ( (*( state.p)) == 110 )
		goto st519;
	goto st0;
st519:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof519;
case 519:
	if ( (*( state.p)) == 101 )
		goto st520;
	goto st0;
st520:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof520;
case 520:
	if ( (*( state.p)) == 114 )
		goto st521;
	goto st0;
st521:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof521;
case 521:
	switch( (*( state.p)) ) {
		case 13: goto tr753;
		case 32: goto tr753;
		case 59: goto tr754;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr753;
	goto st0;
st522:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof522;
case 522:
	if ( (*( state.p)) == 108 )
		goto st523;
	goto st0;
st523:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof523;
case 523:
	if ( (*( state.p)) == 111 )
		goto st524;
	goto st0;
st524:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof524;
case 524:
	if ( (*( state.p)) == 111 )
		goto st525;
	goto st0;
st525:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof525;
case 525:
	if ( (*( state.p)) == 114 )
		goto st526;
	goto st0;
st526:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof526;
case 526:
	switch( (*( state.p)) ) {
		case 13: goto tr759;
		case 32: goto tr759;
		case 59: goto tr760;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr759;
	goto st0;
st527:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof527;
case 527:
	if ( (*( state.p)) == 97 )
		goto st528;
	goto st0;
st528:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof528;
case 528:
	if ( (*( state.p)) == 116 )
		goto st529;
	goto st0;
st529:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof529;
case 529:
	if ( (*( state.p)) == 101 )
		goto st530;
	goto st0;
st530:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof530;
case 530:
	if ( (*( state.p)) == 114 )
		goto st531;
	goto st0;
st531:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof531;
case 531:
	switch( (*( state.p)) ) {
		case 13: goto tr765;
		case 32: goto tr765;
		case 59: goto tr766;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr765;
	goto st0;
st532:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof532;
case 532:
	switch( (*( state.p)) ) {
		case 107: goto st533;
		case 116: goto st591;
	}
	goto st0;
st533:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof533;
case 533:
	if ( (*( state.p)) == 105 )
		goto st534;
	goto st0;
st534:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof534;
case 534:
	if ( (*( state.p)) == 110 )
		goto st535;
	goto st0;
st535:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof535;
case 535:
	switch( (*( state.p)) ) {
		case 13: goto st536;
		case 32: goto st536;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st536;
	goto st0;
st536:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof536;
case 536:
	switch( (*( state.p)) ) {
		case 13: goto st536;
		case 32: goto st536;
		case 34: goto tr772;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st536;
	goto st0;
tr773:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st537;
tr772:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st537;
tr775:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 537; goto st47;}}
	goto st537;
st537:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof537;
case 537:
#line 8559 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st538;
		case 92: goto tr775;
	}
	goto tr773;
st538:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof538;
case 538:
	switch( (*( state.p)) ) {
		case 13: goto tr776;
		case 32: goto tr776;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr776;
	goto st0;
tr776:
#line 164 "configparser.rl"
	{ skin.text = state.match; }
	goto st539;
st539:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof539;
case 539:
#line 8584 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st539;
		case 32: goto st539;
		case 98: goto st540;
		case 100: goto st585;
		case 110: goto st588;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st539;
	goto st0;
st540:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof540;
case 540:
	if ( (*( state.p)) == 114 )
		goto st541;
	goto st0;
st541:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof541;
case 541:
	if ( (*( state.p)) == 105 )
		goto st542;
	goto st0;
st542:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof542;
case 542:
	if ( (*( state.p)) == 103 )
		goto st543;
	goto st0;
st543:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof543;
case 543:
	if ( (*( state.p)) == 104 )
		goto st544;
	goto st0;
st544:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof544;
case 544:
	if ( (*( state.p)) == 116 )
		goto st545;
	goto st0;
st545:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof545;
case 545:
	switch( (*( state.p)) ) {
		case 13: goto tr786;
		case 32: goto tr786;
		case 95: goto tr787;
		case 98: goto tr788;
		case 99: goto tr789;
		case 103: goto tr790;
		case 109: goto tr791;
		case 114: goto tr792;
		case 119: goto tr793;
		case 121: goto tr794;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr786;
	goto st0;
tr786:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st546;
tr851:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st546;
st546:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof546;
case 546:
#line 8661 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st546;
		case 32: goto st546;
		case 98: goto st547;
		case 99: goto st554;
		case 103: goto st558;
		case 109: goto st563;
		case 114: goto st570;
		case 119: goto st573;
		case 121: goto st578;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st546;
	goto st0;
tr788:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st547;
tr853:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st547;
st547:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof547;
case 547:
#line 8688 "configparser.h"
	if ( (*( state.p)) == 108 )
		goto st548;
	goto st0;
st548:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof548;
case 548:
	switch( (*( state.p)) ) {
		case 97: goto st549;
		case 117: goto st552;
	}
	goto st0;
st549:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof549;
case 549:
	if ( (*( state.p)) == 99 )
		goto st550;
	goto st0;
st550:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof550;
case 550:
	if ( (*( state.p)) == 107 )
		goto st551;
	goto st0;
st551:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof551;
case 551:
	switch( (*( state.p)) ) {
		case 13: goto tr808;
		case 32: goto tr808;
		case 59: goto tr809;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr808;
	goto st0;
st552:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof552;
case 552:
	if ( (*( state.p)) == 101 )
		goto st553;
	goto st0;
st553:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof553;
case 553:
	switch( (*( state.p)) ) {
		case 13: goto tr811;
		case 32: goto tr811;
		case 59: goto tr812;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr811;
	goto st0;
tr789:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st554;
tr854:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st554;
st554:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof554;
case 554:
#line 8758 "configparser.h"
	if ( (*( state.p)) == 121 )
		goto st555;
	goto st0;
st555:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof555;
case 555:
	if ( (*( state.p)) == 97 )
		goto st556;
	goto st0;
st556:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof556;
case 556:
	if ( (*( state.p)) == 110 )
		goto st557;
	goto st0;
st557:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof557;
case 557:
	switch( (*( state.p)) ) {
		case 13: goto tr816;
		case 32: goto tr816;
		case 59: goto tr817;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr816;
	goto st0;
tr790:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st558;
tr855:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st558;
st558:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof558;
case 558:
#line 8800 "configparser.h"
	if ( (*( state.p)) == 114 )
		goto st559;
	goto st0;
st559:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof559;
case 559:
	if ( (*( state.p)) == 101 )
		goto st560;
	goto st0;
st560:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof560;
case 560:
	if ( (*( state.p)) == 101 )
		goto st561;
	goto st0;
st561:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof561;
case 561:
	if ( (*( state.p)) == 110 )
		goto st562;
	goto st0;
st562:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof562;
case 562:
	switch( (*( state.p)) ) {
		case 13: goto tr822;
		case 32: goto tr822;
		case 59: goto tr823;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr822;
	goto st0;
tr791:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st563;
tr856:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st563;
st563:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof563;
case 563:
#line 8849 "configparser.h"
	if ( (*( state.p)) == 97 )
		goto st564;
	goto st0;
st564:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof564;
case 564:
	if ( (*( state.p)) == 103 )
		goto st565;
	goto st0;
st565:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof565;
case 565:
	if ( (*( state.p)) == 101 )
		goto st566;
	goto st0;
st566:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof566;
case 566:
	if ( (*( state.p)) == 110 )
		goto st567;
	goto st0;
st567:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof567;
case 567:
	if ( (*( state.p)) == 116 )
		goto st568;
	goto st0;
st568:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof568;
case 568:
	if ( (*( state.p)) == 97 )
		goto st569;
	goto st0;
st569:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof569;
case 569:
	switch( (*( state.p)) ) {
		case 13: goto tr830;
		case 32: goto tr830;
		case 59: goto tr831;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr830;
	goto st0;
tr792:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st570;
tr857:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st570;
st570:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof570;
case 570:
#line 8912 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st571;
	goto st0;
st571:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof571;
case 571:
	if ( (*( state.p)) == 100 )
		goto st572;
	goto st0;
st572:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof572;
case 572:
	switch( (*( state.p)) ) {
		case 13: goto tr834;
		case 32: goto tr834;
		case 59: goto tr835;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr834;
	goto st0;
tr793:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st573;
tr858:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st573;
st573:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof573;
case 573:
#line 8947 "configparser.h"
	if ( (*( state.p)) == 104 )
		goto st574;
	goto st0;
st574:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof574;
case 574:
	if ( (*( state.p)) == 105 )
		goto st575;
	goto st0;
st575:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof575;
case 575:
	if ( (*( state.p)) == 116 )
		goto st576;
	goto st0;
st576:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof576;
case 576:
	if ( (*( state.p)) == 101 )
		goto st577;
	goto st0;
st577:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof577;
case 577:
	switch( (*( state.p)) ) {
		case 13: goto tr840;
		case 32: goto tr840;
		case 59: goto tr841;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr840;
	goto st0;
tr794:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st578;
tr859:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st578;
st578:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof578;
case 578:
#line 8996 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st579;
	goto st0;
st579:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof579;
case 579:
	if ( (*( state.p)) == 108 )
		goto st580;
	goto st0;
st580:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof580;
case 580:
	if ( (*( state.p)) == 108 )
		goto st581;
	goto st0;
st581:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof581;
case 581:
	if ( (*( state.p)) == 111 )
		goto st582;
	goto st0;
st582:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof582;
case 582:
	if ( (*( state.p)) == 119 )
		goto st583;
	goto st0;
st583:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof583;
case 583:
	switch( (*( state.p)) ) {
		case 13: goto tr847;
		case 32: goto tr847;
		case 59: goto tr848;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr847;
	goto st0;
tr787:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st584;
tr852:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st584;
st584:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof584;
case 584:
#line 9052 "configparser.h"
	switch( (*( state.p)) ) {
		case 98: goto st547;
		case 99: goto st554;
		case 103: goto st558;
		case 109: goto st563;
		case 114: goto st570;
		case 119: goto st573;
		case 121: goto st578;
	}
	goto st0;
st585:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof585;
case 585:
	if ( (*( state.p)) == 105 )
		goto st586;
	goto st0;
st586:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof586;
case 586:
	if ( (*( state.p)) == 109 )
		goto st587;
	goto st0;
st587:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof587;
case 587:
	switch( (*( state.p)) ) {
		case 13: goto tr851;
		case 32: goto tr851;
		case 95: goto tr852;
		case 98: goto tr853;
		case 99: goto tr854;
		case 103: goto tr855;
		case 109: goto tr856;
		case 114: goto tr857;
		case 119: goto tr858;
		case 121: goto tr859;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr851;
	goto st0;
st588:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof588;
case 588:
	if ( (*( state.p)) == 111 )
		goto st589;
	goto st0;
st589:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof589;
case 589:
	if ( (*( state.p)) == 110 )
		goto st590;
	goto st0;
st590:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof590;
case 590:
	if ( (*( state.p)) == 101 )
		goto st551;
	goto st0;
st591:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof591;
case 591:
	if ( (*( state.p)) == 97 )
		goto st592;
	goto st0;
st592:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof592;
case 592:
	if ( (*( state.p)) == 105 )
		goto st593;
	goto st0;
st593:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof593;
case 593:
	if ( (*( state.p)) == 114 )
		goto st594;
	goto st0;
st594:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof594;
case 594:
	if ( (*( state.p)) == 115 )
		goto st595;
	goto st0;
st595:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof595;
case 595:
	switch( (*( state.p)) ) {
		case 13: goto st596;
		case 32: goto st596;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st596;
	goto st0;
st596:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof596;
case 596:
	switch( (*( state.p)) ) {
		case 13: goto st596;
		case 32: goto st596;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr867;
	} else if ( (*( state.p)) >= 9 )
		goto st596;
	goto st0;
tr867:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st597;
tr869:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st597;
st597:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof597;
case 597:
#line 9190 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr868;
		case 32: goto tr868;
		case 59: goto tr870;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr869;
	} else if ( (*( state.p)) >= 9 )
		goto tr868;
	goto st0;
st598:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof598;
case 598:
	if ( (*( state.p)) == 117 )
		goto st599;
	goto st0;
st599:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof599;
case 599:
	if ( (*( state.p)) == 110 )
		goto st600;
	goto st0;
st600:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof600;
case 600:
	if ( (*( state.p)) == 110 )
		goto st601;
	goto st0;
st601:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof601;
case 601:
	if ( (*( state.p)) == 101 )
		goto st602;
	goto st0;
st602:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof602;
case 602:
	if ( (*( state.p)) == 108 )
		goto st603;
	goto st0;
st603:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof603;
case 603:
	switch( (*( state.p)) ) {
		case 13: goto st604;
		case 32: goto st604;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st604;
	goto st0;
st604:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof604;
case 604:
	switch( (*( state.p)) ) {
		case 13: goto st604;
		case 32: goto st604;
		case 45: goto tr877;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr878;
	} else if ( (*( state.p)) >= 9 )
		goto st604;
	goto st0;
tr877:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st605;
st605:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof605;
case 605:
#line 9277 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr879;
	goto st0;
tr878:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st606;
tr879:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st606;
st606:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof606;
case 606:
#line 9301 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr880;
		case 32: goto tr880;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr879;
	} else if ( (*( state.p)) >= 9 )
		goto tr880;
	goto st0;
tr880:
#line 296 "configparser.rl"
	{ ter.tunnel_x = toint(state.match); }
	goto st607;
st607:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof607;
case 607:
#line 9320 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st607;
		case 32: goto st607;
		case 45: goto tr882;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr883;
	} else if ( (*( state.p)) >= 9 )
		goto st607;
	goto st0;
tr882:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st608;
st608:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof608;
case 608:
#line 9346 "configparser.h"
	if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
		goto tr884;
	goto st0;
tr883:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st609;
tr884:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st609;
st609:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof609;
case 609:
#line 9370 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr885;
		case 32: goto tr885;
		case 59: goto tr886;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr884;
	} else if ( (*( state.p)) >= 9 )
		goto tr885;
	goto st0;
st610:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof610;
case 610:
	if ( (*( state.p)) == 105 )
		goto st611;
	goto st0;
st611:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof611;
case 611:
	if ( (*( state.p)) == 101 )
		goto st612;
	goto st0;
st612:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof612;
case 612:
	if ( (*( state.p)) == 119 )
		goto st613;
	goto st0;
st613:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof613;
case 613:
	if ( (*( state.p)) == 98 )
		goto st614;
	goto st0;
st614:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof614;
case 614:
	if ( (*( state.p)) == 108 )
		goto st615;
	goto st0;
st615:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof615;
case 615:
	if ( (*( state.p)) == 111 )
		goto st616;
	goto st0;
st616:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof616;
case 616:
	if ( (*( state.p)) == 99 )
		goto st617;
	goto st0;
st617:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof617;
case 617:
	if ( (*( state.p)) == 107 )
		goto st618;
	goto st0;
st618:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof618;
case 618:
	switch( (*( state.p)) ) {
		case 13: goto tr895;
		case 32: goto tr895;
		case 59: goto tr896;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr895;
	goto st0;
st619:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof619;
case 619:
	if ( (*( state.p)) == 97 )
		goto st620;
	goto st0;
st620:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof620;
case 620:
	if ( (*( state.p)) == 108 )
		goto st621;
	goto st0;
st621:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof621;
case 621:
	if ( (*( state.p)) == 107 )
		goto st622;
	goto st0;
st622:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof622;
case 622:
	if ( (*( state.p)) == 98 )
		goto st623;
	goto st0;
st623:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof623;
case 623:
	if ( (*( state.p)) == 108 )
		goto st624;
	goto st0;
st624:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof624;
case 624:
	if ( (*( state.p)) == 111 )
		goto st625;
	goto st0;
st625:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof625;
case 625:
	if ( (*( state.p)) == 99 )
		goto st626;
	goto st0;
st626:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof626;
case 626:
	if ( (*( state.p)) == 107 )
		goto st627;
	goto st0;
st627:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof627;
case 627:
	switch( (*( state.p)) ) {
		case 13: goto tr905;
		case 32: goto tr905;
		case 59: goto tr906;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr905;
	goto st0;
st628:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof628;
case 628:
	switch( (*( state.p)) ) {
		case 13: goto st628;
		case 32: goto st628;
		case 100: goto st629;
		case 102: goto st656;
		case 108: goto st1109;
		case 115: goto st1122;
		case 119: goto st1190;
		case 125: goto tr913;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st628;
	goto st0;
st629:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof629;
case 629:
	if ( (*( state.p)) == 101 )
		goto st630;
	goto st0;
st630:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof630;
case 630:
	if ( (*( state.p)) == 101 )
		goto st631;
	goto st0;
st631:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof631;
case 631:
	if ( (*( state.p)) == 112 )
		goto st632;
	goto st0;
st632:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof632;
case 632:
	if ( (*( state.p)) == 95 )
		goto st633;
	goto st0;
st633:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof633;
case 633:
	if ( (*( state.p)) == 119 )
		goto st634;
	goto st0;
st634:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof634;
case 634:
	if ( (*( state.p)) == 97 )
		goto st635;
	goto st0;
st635:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof635;
case 635:
	if ( (*( state.p)) == 116 )
		goto st636;
	goto st0;
st636:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof636;
case 636:
	if ( (*( state.p)) == 101 )
		goto st637;
	goto st0;
st637:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof637;
case 637:
	if ( (*( state.p)) == 114 )
		goto st638;
	goto st0;
st638:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof638;
case 638:
	switch( (*( state.p)) ) {
		case 13: goto st639;
		case 32: goto st639;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st639;
	goto st0;
st639:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof639;
case 639:
	switch( (*( state.p)) ) {
		case 13: goto st639;
		case 32: goto st639;
		case 34: goto tr924;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st639;
	goto st0;
tr925:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st640;
tr924:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st640;
tr927:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 640; goto st47;}}
	goto st640;
st640:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof640;
case 640:
#line 9641 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st641;
		case 92: goto tr927;
	}
	goto tr925;
st641:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof641;
case 641:
	switch( (*( state.p)) ) {
		case 13: goto tr928;
		case 32: goto tr928;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr928;
	goto st0;
tr928:
#line 164 "configparser.rl"
	{ skin.text = state.match; }
	goto st642;
st642:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof642;
case 642:
#line 9666 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st642;
		case 32: goto st642;
		case 98: goto st643;
		case 100: goto st1345;
		case 110: goto st1348;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st642;
	goto st0;
st643:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof643;
case 643:
	if ( (*( state.p)) == 114 )
		goto st644;
	goto st0;
st644:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof644;
case 644:
	if ( (*( state.p)) == 105 )
		goto st645;
	goto st0;
st645:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof645;
case 645:
	if ( (*( state.p)) == 103 )
		goto st646;
	goto st0;
st646:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof646;
case 646:
	if ( (*( state.p)) == 104 )
		goto st647;
	goto st0;
st647:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof647;
case 647:
	if ( (*( state.p)) == 116 )
		goto st648;
	goto st0;
st648:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof648;
case 648:
	switch( (*( state.p)) ) {
		case 13: goto tr938;
		case 32: goto tr938;
		case 95: goto tr939;
		case 98: goto tr940;
		case 99: goto tr941;
		case 103: goto tr942;
		case 109: goto tr943;
		case 114: goto tr944;
		case 119: goto tr945;
		case 121: goto tr946;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr938;
	goto st0;
tr938:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st649;
tr2056:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st649;
st649:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof649;
case 649:
#line 9743 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st649;
		case 32: goto st649;
		case 98: goto st650;
		case 99: goto st1314;
		case 103: goto st1318;
		case 109: goto st1323;
		case 114: goto st1330;
		case 119: goto st1333;
		case 121: goto st1338;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st649;
	goto st0;
tr940:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st650;
tr2058:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st650;
st650:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof650;
case 650:
#line 9770 "configparser.h"
	if ( (*( state.p)) == 108 )
		goto st651;
	goto st0;
st651:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof651;
case 651:
	switch( (*( state.p)) ) {
		case 97: goto st652;
		case 117: goto st1312;
	}
	goto st0;
st652:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof652;
case 652:
	if ( (*( state.p)) == 99 )
		goto st653;
	goto st0;
st653:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof653;
case 653:
	if ( (*( state.p)) == 107 )
		goto st654;
	goto st0;
st654:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof654;
case 654:
	switch( (*( state.p)) ) {
		case 13: goto tr960;
		case 32: goto tr960;
		case 59: goto tr961;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr960;
	goto st0;
tr913:
#line 353 "configparser.rl"
	{ { state.cs =  state.stack[-- state.top];goto _again;} }
	goto st655;
tr960:
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st655;
tr1013:
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st655;
tr1016:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st655;
tr1021:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st655;
tr1027:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st655;
tr1035:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st655;
tr1039:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st655;
tr1045:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st655;
tr1052:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st655;
tr1104:
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st655;
tr1107:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st655;
tr1112:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st655;
tr1118:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st655;
tr1126:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st655;
tr1130:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st655;
tr1136:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st655;
tr1143:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st655;
tr1195:
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st655;
tr1198:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st655;
tr1203:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st655;
tr1209:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st655;
tr1217:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st655;
tr1221:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st655;
tr1227:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st655;
tr1234:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st655;
tr1286:
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st655;
tr1289:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st655;
tr1294:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st655;
tr1300:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st655;
tr1308:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st655;
tr1312:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st655;
tr1318:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st655;
tr1325:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st655;
tr1377:
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st655;
tr1380:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st655;
tr1385:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st655;
tr1391:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st655;
tr1399:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st655;
tr1403:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st655;
tr1409:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st655;
tr1416:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st655;
tr1468:
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st655;
tr1471:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st655;
tr1476:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st655;
tr1482:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st655;
tr1490:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st655;
tr1494:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st655;
tr1500:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st655;
tr1507:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st655;
tr1559:
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st655;
tr1562:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st655;
tr1567:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st655;
tr1573:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st655;
tr1581:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st655;
tr1585:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st655;
tr1591:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st655;
tr1598:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st655;
tr1650:
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st655;
tr1653:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st655;
tr1658:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st655;
tr1664:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st655;
tr1672:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st655;
tr1676:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st655;
tr1682:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st655;
tr1689:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st655;
tr1716:
#line 344 "configparser.rl"
	{ lev.lightradius = toint(state.match); }
	goto st655;
tr1768:
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st655;
tr1771:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st655;
tr1776:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st655;
tr1782:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st655;
tr1790:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st655;
tr1794:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st655;
tr1800:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st655;
tr1807:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st655;
tr1863:
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st655;
tr1866:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st655;
tr1871:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st655;
tr1877:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st655;
tr1885:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st655;
tr1889:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st655;
tr1895:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st655;
tr1902:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st655;
tr1961:
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st655;
tr1964:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st655;
tr1969:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st655;
tr1975:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st655;
tr1983:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st655;
tr1987:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st655;
tr1993:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st655;
tr2000:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st655;
tr2016:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st655;
tr2021:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st655;
tr2027:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st655;
tr2035:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st655;
tr2039:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st655;
tr2045:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st655;
tr2052:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st655;
st655:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof655;
case 655:
#line 10373 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st655;
		case 32: goto st655;
		case 59: goto st1360;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st655;
	goto st0;
tr961:
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st1360;
tr1014:
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st1360;
tr1017:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st1360;
tr1022:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st1360;
tr1028:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st1360;
tr1036:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st1360;
tr1040:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st1360;
tr1046:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st1360;
tr1053:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 336 "configparser.rl"
	{ lev.floor1 = skin; }
	goto st1360;
tr1105:
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st1360;
tr1108:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st1360;
tr1113:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st1360;
tr1119:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st1360;
tr1127:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st1360;
tr1131:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st1360;
tr1137:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st1360;
tr1144:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 337 "configparser.rl"
	{ lev.floor2 = skin; }
	goto st1360;
tr1196:
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st1360;
tr1199:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st1360;
tr1204:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st1360;
tr1210:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st1360;
tr1218:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st1360;
tr1222:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st1360;
tr1228:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st1360;
tr1235:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 338 "configparser.rl"
	{ lev.floor3 = skin; }
	goto st1360;
tr1287:
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st1360;
tr1290:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st1360;
tr1295:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st1360;
tr1301:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st1360;
tr1309:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st1360;
tr1313:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st1360;
tr1319:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st1360;
tr1326:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 339 "configparser.rl"
	{ lev.floor4 = skin; }
	goto st1360;
tr1378:
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st1360;
tr1381:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st1360;
tr1386:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st1360;
tr1392:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st1360;
tr1400:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st1360;
tr1404:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st1360;
tr1410:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st1360;
tr1417:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 340 "configparser.rl"
	{ lev.floor5 = skin; }
	goto st1360;
tr1469:
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st1360;
tr1472:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st1360;
tr1477:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st1360;
tr1483:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st1360;
tr1491:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st1360;
tr1495:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st1360;
tr1501:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st1360;
tr1508:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 341 "configparser.rl"
	{ lev.floor6 = skin; }
	goto st1360;
tr1560:
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st1360;
tr1563:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st1360;
tr1568:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st1360;
tr1574:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st1360;
tr1582:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st1360;
tr1586:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st1360;
tr1592:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st1360;
tr1599:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 342 "configparser.rl"
	{ lev.floor7 = skin; }
	goto st1360;
tr1651:
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st1360;
tr1654:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st1360;
tr1659:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st1360;
tr1665:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st1360;
tr1673:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st1360;
tr1677:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st1360;
tr1683:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st1360;
tr1690:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 343 "configparser.rl"
	{ lev.floor8 = skin; }
	goto st1360;
tr1718:
#line 344 "configparser.rl"
	{ lev.lightradius = toint(state.match); }
	goto st1360;
tr1769:
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st1360;
tr1772:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st1360;
tr1777:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st1360;
tr1783:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st1360;
tr1791:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st1360;
tr1795:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st1360;
tr1801:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st1360;
tr1808:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 333 "configparser.rl"
	{ lev.shallow_water = skin; }
	goto st1360;
tr1864:
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st1360;
tr1867:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st1360;
tr1872:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st1360;
tr1878:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st1360;
tr1886:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st1360;
tr1890:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st1360;
tr1896:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st1360;
tr1903:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 334 "configparser.rl"
	{ lev.wall = skin; }
	goto st1360;
tr1962:
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st1360;
tr1965:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st1360;
tr1970:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st1360;
tr1976:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st1360;
tr1984:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st1360;
tr1988:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st1360;
tr1994:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st1360;
tr2001:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 335 "configparser.rl"
	{ lev.water_wall = skin; }
	goto st1360;
tr2017:
#line 154 "configparser.rl"
	{ add_color(skin.fore, 4); }
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st1360;
tr2022:
#line 156 "configparser.rl"
	{ add_color(skin.fore, 6); }
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st1360;
tr2028:
#line 152 "configparser.rl"
	{ add_color(skin.fore, 2); }
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st1360;
tr2036:
#line 155 "configparser.rl"
	{ add_color(skin.fore, 5); }
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st1360;
tr2040:
#line 151 "configparser.rl"
	{ add_color(skin.fore, 1); }
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st1360;
tr2046:
#line 157 "configparser.rl"
	{ add_color(skin.fore, 7); }
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st1360;
tr2053:
#line 153 "configparser.rl"
	{ add_color(skin.fore, 3); }
#line 332 "configparser.rl"
	{ lev.deep_water = skin; }
	goto st1360;
st1360:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1360;
case 1360:
#line 10942 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st628;
		case 32: goto st628;
		case 100: goto st629;
		case 102: goto st656;
		case 108: goto st1109;
		case 115: goto st1122;
		case 119: goto st1190;
		case 125: goto tr913;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st628;
	goto st0;
st656:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof656;
case 656:
	if ( (*( state.p)) == 108 )
		goto st657;
	goto st0;
st657:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof657;
case 657:
	if ( (*( state.p)) == 111 )
		goto st658;
	goto st0;
st658:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof658;
case 658:
	if ( (*( state.p)) == 111 )
		goto st659;
	goto st0;
st659:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof659;
case 659:
	if ( (*( state.p)) == 114 )
		goto st660;
	goto st0;
st660:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof660;
case 660:
	switch( (*( state.p)) ) {
		case 49: goto st661;
		case 50: goto st717;
		case 51: goto st773;
		case 52: goto st829;
		case 53: goto st885;
		case 54: goto st941;
		case 55: goto st997;
		case 56: goto st1053;
	}
	goto st0;
st661:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof661;
case 661:
	switch( (*( state.p)) ) {
		case 13: goto st662;
		case 32: goto st662;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st662;
	goto st0;
st662:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof662;
case 662:
	switch( (*( state.p)) ) {
		case 13: goto st662;
		case 32: goto st662;
		case 34: goto tr977;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st662;
	goto st0;
tr978:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st663;
tr977:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st663;
tr980:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 663; goto st47;}}
	goto st663;
st663:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof663;
case 663:
#line 11042 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st664;
		case 92: goto tr980;
	}
	goto tr978;
st664:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof664;
case 664:
	switch( (*( state.p)) ) {
		case 13: goto tr981;
		case 32: goto tr981;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr981;
	goto st0;
tr981:
#line 164 "configparser.rl"
	{ skin.text = state.match; }
	goto st665;
st665:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof665;
case 665:
#line 11067 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st665;
		case 32: goto st665;
		case 98: goto st666;
		case 100: goto st711;
		case 110: goto st714;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st665;
	goto st0;
st666:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof666;
case 666:
	if ( (*( state.p)) == 114 )
		goto st667;
	goto st0;
st667:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof667;
case 667:
	if ( (*( state.p)) == 105 )
		goto st668;
	goto st0;
st668:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof668;
case 668:
	if ( (*( state.p)) == 103 )
		goto st669;
	goto st0;
st669:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof669;
case 669:
	if ( (*( state.p)) == 104 )
		goto st670;
	goto st0;
st670:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof670;
case 670:
	if ( (*( state.p)) == 116 )
		goto st671;
	goto st0;
st671:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof671;
case 671:
	switch( (*( state.p)) ) {
		case 13: goto tr991;
		case 32: goto tr991;
		case 95: goto tr992;
		case 98: goto tr993;
		case 99: goto tr994;
		case 103: goto tr995;
		case 109: goto tr996;
		case 114: goto tr997;
		case 119: goto tr998;
		case 121: goto tr999;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr991;
	goto st0;
tr991:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st672;
tr1056:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st672;
st672:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof672;
case 672:
#line 11144 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st672;
		case 32: goto st672;
		case 98: goto st673;
		case 99: goto st680;
		case 103: goto st684;
		case 109: goto st689;
		case 114: goto st696;
		case 119: goto st699;
		case 121: goto st704;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st672;
	goto st0;
tr993:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st673;
tr1058:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st673;
st673:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof673;
case 673:
#line 11171 "configparser.h"
	if ( (*( state.p)) == 108 )
		goto st674;
	goto st0;
st674:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof674;
case 674:
	switch( (*( state.p)) ) {
		case 97: goto st675;
		case 117: goto st678;
	}
	goto st0;
st675:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof675;
case 675:
	if ( (*( state.p)) == 99 )
		goto st676;
	goto st0;
st676:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof676;
case 676:
	if ( (*( state.p)) == 107 )
		goto st677;
	goto st0;
st677:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof677;
case 677:
	switch( (*( state.p)) ) {
		case 13: goto tr1013;
		case 32: goto tr1013;
		case 59: goto tr1014;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1013;
	goto st0;
st678:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof678;
case 678:
	if ( (*( state.p)) == 101 )
		goto st679;
	goto st0;
st679:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof679;
case 679:
	switch( (*( state.p)) ) {
		case 13: goto tr1016;
		case 32: goto tr1016;
		case 59: goto tr1017;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1016;
	goto st0;
tr994:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st680;
tr1059:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st680;
st680:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof680;
case 680:
#line 11241 "configparser.h"
	if ( (*( state.p)) == 121 )
		goto st681;
	goto st0;
st681:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof681;
case 681:
	if ( (*( state.p)) == 97 )
		goto st682;
	goto st0;
st682:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof682;
case 682:
	if ( (*( state.p)) == 110 )
		goto st683;
	goto st0;
st683:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof683;
case 683:
	switch( (*( state.p)) ) {
		case 13: goto tr1021;
		case 32: goto tr1021;
		case 59: goto tr1022;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1021;
	goto st0;
tr995:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st684;
tr1060:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st684;
st684:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof684;
case 684:
#line 11283 "configparser.h"
	if ( (*( state.p)) == 114 )
		goto st685;
	goto st0;
st685:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof685;
case 685:
	if ( (*( state.p)) == 101 )
		goto st686;
	goto st0;
st686:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof686;
case 686:
	if ( (*( state.p)) == 101 )
		goto st687;
	goto st0;
st687:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof687;
case 687:
	if ( (*( state.p)) == 110 )
		goto st688;
	goto st0;
st688:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof688;
case 688:
	switch( (*( state.p)) ) {
		case 13: goto tr1027;
		case 32: goto tr1027;
		case 59: goto tr1028;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1027;
	goto st0;
tr996:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st689;
tr1061:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st689;
st689:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof689;
case 689:
#line 11332 "configparser.h"
	if ( (*( state.p)) == 97 )
		goto st690;
	goto st0;
st690:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof690;
case 690:
	if ( (*( state.p)) == 103 )
		goto st691;
	goto st0;
st691:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof691;
case 691:
	if ( (*( state.p)) == 101 )
		goto st692;
	goto st0;
st692:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof692;
case 692:
	if ( (*( state.p)) == 110 )
		goto st693;
	goto st0;
st693:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof693;
case 693:
	if ( (*( state.p)) == 116 )
		goto st694;
	goto st0;
st694:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof694;
case 694:
	if ( (*( state.p)) == 97 )
		goto st695;
	goto st0;
st695:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof695;
case 695:
	switch( (*( state.p)) ) {
		case 13: goto tr1035;
		case 32: goto tr1035;
		case 59: goto tr1036;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1035;
	goto st0;
tr997:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st696;
tr1062:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st696;
st696:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof696;
case 696:
#line 11395 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st697;
	goto st0;
st697:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof697;
case 697:
	if ( (*( state.p)) == 100 )
		goto st698;
	goto st0;
st698:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof698;
case 698:
	switch( (*( state.p)) ) {
		case 13: goto tr1039;
		case 32: goto tr1039;
		case 59: goto tr1040;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1039;
	goto st0;
tr998:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st699;
tr1063:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st699;
st699:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof699;
case 699:
#line 11430 "configparser.h"
	if ( (*( state.p)) == 104 )
		goto st700;
	goto st0;
st700:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof700;
case 700:
	if ( (*( state.p)) == 105 )
		goto st701;
	goto st0;
st701:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof701;
case 701:
	if ( (*( state.p)) == 116 )
		goto st702;
	goto st0;
st702:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof702;
case 702:
	if ( (*( state.p)) == 101 )
		goto st703;
	goto st0;
st703:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof703;
case 703:
	switch( (*( state.p)) ) {
		case 13: goto tr1045;
		case 32: goto tr1045;
		case 59: goto tr1046;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1045;
	goto st0;
tr999:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st704;
tr1064:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st704;
st704:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof704;
case 704:
#line 11479 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st705;
	goto st0;
st705:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof705;
case 705:
	if ( (*( state.p)) == 108 )
		goto st706;
	goto st0;
st706:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof706;
case 706:
	if ( (*( state.p)) == 108 )
		goto st707;
	goto st0;
st707:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof707;
case 707:
	if ( (*( state.p)) == 111 )
		goto st708;
	goto st0;
st708:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof708;
case 708:
	if ( (*( state.p)) == 119 )
		goto st709;
	goto st0;
st709:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof709;
case 709:
	switch( (*( state.p)) ) {
		case 13: goto tr1052;
		case 32: goto tr1052;
		case 59: goto tr1053;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1052;
	goto st0;
tr992:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st710;
tr1057:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st710;
st710:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof710;
case 710:
#line 11535 "configparser.h"
	switch( (*( state.p)) ) {
		case 98: goto st673;
		case 99: goto st680;
		case 103: goto st684;
		case 109: goto st689;
		case 114: goto st696;
		case 119: goto st699;
		case 121: goto st704;
	}
	goto st0;
st711:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof711;
case 711:
	if ( (*( state.p)) == 105 )
		goto st712;
	goto st0;
st712:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof712;
case 712:
	if ( (*( state.p)) == 109 )
		goto st713;
	goto st0;
st713:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof713;
case 713:
	switch( (*( state.p)) ) {
		case 13: goto tr1056;
		case 32: goto tr1056;
		case 95: goto tr1057;
		case 98: goto tr1058;
		case 99: goto tr1059;
		case 103: goto tr1060;
		case 109: goto tr1061;
		case 114: goto tr1062;
		case 119: goto tr1063;
		case 121: goto tr1064;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1056;
	goto st0;
st714:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof714;
case 714:
	if ( (*( state.p)) == 111 )
		goto st715;
	goto st0;
st715:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof715;
case 715:
	if ( (*( state.p)) == 110 )
		goto st716;
	goto st0;
st716:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof716;
case 716:
	if ( (*( state.p)) == 101 )
		goto st677;
	goto st0;
st717:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof717;
case 717:
	switch( (*( state.p)) ) {
		case 13: goto st718;
		case 32: goto st718;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st718;
	goto st0;
st718:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof718;
case 718:
	switch( (*( state.p)) ) {
		case 13: goto st718;
		case 32: goto st718;
		case 34: goto tr1068;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st718;
	goto st0;
tr1069:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st719;
tr1068:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st719;
tr1071:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 719; goto st47;}}
	goto st719;
st719:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof719;
case 719:
#line 11643 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st720;
		case 92: goto tr1071;
	}
	goto tr1069;
st720:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof720;
case 720:
	switch( (*( state.p)) ) {
		case 13: goto tr1072;
		case 32: goto tr1072;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1072;
	goto st0;
tr1072:
#line 164 "configparser.rl"
	{ skin.text = state.match; }
	goto st721;
st721:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof721;
case 721:
#line 11668 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st721;
		case 32: goto st721;
		case 98: goto st722;
		case 100: goto st767;
		case 110: goto st770;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st721;
	goto st0;
st722:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof722;
case 722:
	if ( (*( state.p)) == 114 )
		goto st723;
	goto st0;
st723:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof723;
case 723:
	if ( (*( state.p)) == 105 )
		goto st724;
	goto st0;
st724:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof724;
case 724:
	if ( (*( state.p)) == 103 )
		goto st725;
	goto st0;
st725:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof725;
case 725:
	if ( (*( state.p)) == 104 )
		goto st726;
	goto st0;
st726:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof726;
case 726:
	if ( (*( state.p)) == 116 )
		goto st727;
	goto st0;
st727:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof727;
case 727:
	switch( (*( state.p)) ) {
		case 13: goto tr1082;
		case 32: goto tr1082;
		case 95: goto tr1083;
		case 98: goto tr1084;
		case 99: goto tr1085;
		case 103: goto tr1086;
		case 109: goto tr1087;
		case 114: goto tr1088;
		case 119: goto tr1089;
		case 121: goto tr1090;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1082;
	goto st0;
tr1082:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st728;
tr1147:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st728;
st728:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof728;
case 728:
#line 11745 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st728;
		case 32: goto st728;
		case 98: goto st729;
		case 99: goto st736;
		case 103: goto st740;
		case 109: goto st745;
		case 114: goto st752;
		case 119: goto st755;
		case 121: goto st760;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st728;
	goto st0;
tr1084:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st729;
tr1149:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st729;
st729:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof729;
case 729:
#line 11772 "configparser.h"
	if ( (*( state.p)) == 108 )
		goto st730;
	goto st0;
st730:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof730;
case 730:
	switch( (*( state.p)) ) {
		case 97: goto st731;
		case 117: goto st734;
	}
	goto st0;
st731:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof731;
case 731:
	if ( (*( state.p)) == 99 )
		goto st732;
	goto st0;
st732:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof732;
case 732:
	if ( (*( state.p)) == 107 )
		goto st733;
	goto st0;
st733:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof733;
case 733:
	switch( (*( state.p)) ) {
		case 13: goto tr1104;
		case 32: goto tr1104;
		case 59: goto tr1105;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1104;
	goto st0;
st734:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof734;
case 734:
	if ( (*( state.p)) == 101 )
		goto st735;
	goto st0;
st735:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof735;
case 735:
	switch( (*( state.p)) ) {
		case 13: goto tr1107;
		case 32: goto tr1107;
		case 59: goto tr1108;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1107;
	goto st0;
tr1085:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st736;
tr1150:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st736;
st736:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof736;
case 736:
#line 11842 "configparser.h"
	if ( (*( state.p)) == 121 )
		goto st737;
	goto st0;
st737:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof737;
case 737:
	if ( (*( state.p)) == 97 )
		goto st738;
	goto st0;
st738:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof738;
case 738:
	if ( (*( state.p)) == 110 )
		goto st739;
	goto st0;
st739:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof739;
case 739:
	switch( (*( state.p)) ) {
		case 13: goto tr1112;
		case 32: goto tr1112;
		case 59: goto tr1113;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1112;
	goto st0;
tr1086:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st740;
tr1151:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st740;
st740:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof740;
case 740:
#line 11884 "configparser.h"
	if ( (*( state.p)) == 114 )
		goto st741;
	goto st0;
st741:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof741;
case 741:
	if ( (*( state.p)) == 101 )
		goto st742;
	goto st0;
st742:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof742;
case 742:
	if ( (*( state.p)) == 101 )
		goto st743;
	goto st0;
st743:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof743;
case 743:
	if ( (*( state.p)) == 110 )
		goto st744;
	goto st0;
st744:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof744;
case 744:
	switch( (*( state.p)) ) {
		case 13: goto tr1118;
		case 32: goto tr1118;
		case 59: goto tr1119;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1118;
	goto st0;
tr1087:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st745;
tr1152:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st745;
st745:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof745;
case 745:
#line 11933 "configparser.h"
	if ( (*( state.p)) == 97 )
		goto st746;
	goto st0;
st746:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof746;
case 746:
	if ( (*( state.p)) == 103 )
		goto st747;
	goto st0;
st747:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof747;
case 747:
	if ( (*( state.p)) == 101 )
		goto st748;
	goto st0;
st748:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof748;
case 748:
	if ( (*( state.p)) == 110 )
		goto st749;
	goto st0;
st749:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof749;
case 749:
	if ( (*( state.p)) == 116 )
		goto st750;
	goto st0;
st750:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof750;
case 750:
	if ( (*( state.p)) == 97 )
		goto st751;
	goto st0;
st751:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof751;
case 751:
	switch( (*( state.p)) ) {
		case 13: goto tr1126;
		case 32: goto tr1126;
		case 59: goto tr1127;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1126;
	goto st0;
tr1088:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st752;
tr1153:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st752;
st752:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof752;
case 752:
#line 11996 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st753;
	goto st0;
st753:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof753;
case 753:
	if ( (*( state.p)) == 100 )
		goto st754;
	goto st0;
st754:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof754;
case 754:
	switch( (*( state.p)) ) {
		case 13: goto tr1130;
		case 32: goto tr1130;
		case 59: goto tr1131;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1130;
	goto st0;
tr1089:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st755;
tr1154:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st755;
st755:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof755;
case 755:
#line 12031 "configparser.h"
	if ( (*( state.p)) == 104 )
		goto st756;
	goto st0;
st756:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof756;
case 756:
	if ( (*( state.p)) == 105 )
		goto st757;
	goto st0;
st757:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof757;
case 757:
	if ( (*( state.p)) == 116 )
		goto st758;
	goto st0;
st758:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof758;
case 758:
	if ( (*( state.p)) == 101 )
		goto st759;
	goto st0;
st759:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof759;
case 759:
	switch( (*( state.p)) ) {
		case 13: goto tr1136;
		case 32: goto tr1136;
		case 59: goto tr1137;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1136;
	goto st0;
tr1090:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st760;
tr1155:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st760;
st760:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof760;
case 760:
#line 12080 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st761;
	goto st0;
st761:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof761;
case 761:
	if ( (*( state.p)) == 108 )
		goto st762;
	goto st0;
st762:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof762;
case 762:
	if ( (*( state.p)) == 108 )
		goto st763;
	goto st0;
st763:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof763;
case 763:
	if ( (*( state.p)) == 111 )
		goto st764;
	goto st0;
st764:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof764;
case 764:
	if ( (*( state.p)) == 119 )
		goto st765;
	goto st0;
st765:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof765;
case 765:
	switch( (*( state.p)) ) {
		case 13: goto tr1143;
		case 32: goto tr1143;
		case 59: goto tr1144;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1143;
	goto st0;
tr1083:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st766;
tr1148:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st766;
st766:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof766;
case 766:
#line 12136 "configparser.h"
	switch( (*( state.p)) ) {
		case 98: goto st729;
		case 99: goto st736;
		case 103: goto st740;
		case 109: goto st745;
		case 114: goto st752;
		case 119: goto st755;
		case 121: goto st760;
	}
	goto st0;
st767:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof767;
case 767:
	if ( (*( state.p)) == 105 )
		goto st768;
	goto st0;
st768:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof768;
case 768:
	if ( (*( state.p)) == 109 )
		goto st769;
	goto st0;
st769:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof769;
case 769:
	switch( (*( state.p)) ) {
		case 13: goto tr1147;
		case 32: goto tr1147;
		case 95: goto tr1148;
		case 98: goto tr1149;
		case 99: goto tr1150;
		case 103: goto tr1151;
		case 109: goto tr1152;
		case 114: goto tr1153;
		case 119: goto tr1154;
		case 121: goto tr1155;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1147;
	goto st0;
st770:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof770;
case 770:
	if ( (*( state.p)) == 111 )
		goto st771;
	goto st0;
st771:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof771;
case 771:
	if ( (*( state.p)) == 110 )
		goto st772;
	goto st0;
st772:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof772;
case 772:
	if ( (*( state.p)) == 101 )
		goto st733;
	goto st0;
st773:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof773;
case 773:
	switch( (*( state.p)) ) {
		case 13: goto st774;
		case 32: goto st774;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st774;
	goto st0;
st774:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof774;
case 774:
	switch( (*( state.p)) ) {
		case 13: goto st774;
		case 32: goto st774;
		case 34: goto tr1159;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st774;
	goto st0;
tr1160:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st775;
tr1159:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st775;
tr1162:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 775; goto st47;}}
	goto st775;
st775:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof775;
case 775:
#line 12244 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st776;
		case 92: goto tr1162;
	}
	goto tr1160;
st776:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof776;
case 776:
	switch( (*( state.p)) ) {
		case 13: goto tr1163;
		case 32: goto tr1163;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1163;
	goto st0;
tr1163:
#line 164 "configparser.rl"
	{ skin.text = state.match; }
	goto st777;
st777:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof777;
case 777:
#line 12269 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st777;
		case 32: goto st777;
		case 98: goto st778;
		case 100: goto st823;
		case 110: goto st826;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st777;
	goto st0;
st778:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof778;
case 778:
	if ( (*( state.p)) == 114 )
		goto st779;
	goto st0;
st779:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof779;
case 779:
	if ( (*( state.p)) == 105 )
		goto st780;
	goto st0;
st780:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof780;
case 780:
	if ( (*( state.p)) == 103 )
		goto st781;
	goto st0;
st781:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof781;
case 781:
	if ( (*( state.p)) == 104 )
		goto st782;
	goto st0;
st782:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof782;
case 782:
	if ( (*( state.p)) == 116 )
		goto st783;
	goto st0;
st783:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof783;
case 783:
	switch( (*( state.p)) ) {
		case 13: goto tr1173;
		case 32: goto tr1173;
		case 95: goto tr1174;
		case 98: goto tr1175;
		case 99: goto tr1176;
		case 103: goto tr1177;
		case 109: goto tr1178;
		case 114: goto tr1179;
		case 119: goto tr1180;
		case 121: goto tr1181;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1173;
	goto st0;
tr1173:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st784;
tr1238:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st784;
st784:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof784;
case 784:
#line 12346 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st784;
		case 32: goto st784;
		case 98: goto st785;
		case 99: goto st792;
		case 103: goto st796;
		case 109: goto st801;
		case 114: goto st808;
		case 119: goto st811;
		case 121: goto st816;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st784;
	goto st0;
tr1175:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st785;
tr1240:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st785;
st785:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof785;
case 785:
#line 12373 "configparser.h"
	if ( (*( state.p)) == 108 )
		goto st786;
	goto st0;
st786:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof786;
case 786:
	switch( (*( state.p)) ) {
		case 97: goto st787;
		case 117: goto st790;
	}
	goto st0;
st787:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof787;
case 787:
	if ( (*( state.p)) == 99 )
		goto st788;
	goto st0;
st788:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof788;
case 788:
	if ( (*( state.p)) == 107 )
		goto st789;
	goto st0;
st789:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof789;
case 789:
	switch( (*( state.p)) ) {
		case 13: goto tr1195;
		case 32: goto tr1195;
		case 59: goto tr1196;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1195;
	goto st0;
st790:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof790;
case 790:
	if ( (*( state.p)) == 101 )
		goto st791;
	goto st0;
st791:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof791;
case 791:
	switch( (*( state.p)) ) {
		case 13: goto tr1198;
		case 32: goto tr1198;
		case 59: goto tr1199;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1198;
	goto st0;
tr1176:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st792;
tr1241:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st792;
st792:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof792;
case 792:
#line 12443 "configparser.h"
	if ( (*( state.p)) == 121 )
		goto st793;
	goto st0;
st793:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof793;
case 793:
	if ( (*( state.p)) == 97 )
		goto st794;
	goto st0;
st794:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof794;
case 794:
	if ( (*( state.p)) == 110 )
		goto st795;
	goto st0;
st795:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof795;
case 795:
	switch( (*( state.p)) ) {
		case 13: goto tr1203;
		case 32: goto tr1203;
		case 59: goto tr1204;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1203;
	goto st0;
tr1177:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st796;
tr1242:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st796;
st796:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof796;
case 796:
#line 12485 "configparser.h"
	if ( (*( state.p)) == 114 )
		goto st797;
	goto st0;
st797:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof797;
case 797:
	if ( (*( state.p)) == 101 )
		goto st798;
	goto st0;
st798:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof798;
case 798:
	if ( (*( state.p)) == 101 )
		goto st799;
	goto st0;
st799:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof799;
case 799:
	if ( (*( state.p)) == 110 )
		goto st800;
	goto st0;
st800:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof800;
case 800:
	switch( (*( state.p)) ) {
		case 13: goto tr1209;
		case 32: goto tr1209;
		case 59: goto tr1210;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1209;
	goto st0;
tr1178:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st801;
tr1243:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st801;
st801:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof801;
case 801:
#line 12534 "configparser.h"
	if ( (*( state.p)) == 97 )
		goto st802;
	goto st0;
st802:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof802;
case 802:
	if ( (*( state.p)) == 103 )
		goto st803;
	goto st0;
st803:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof803;
case 803:
	if ( (*( state.p)) == 101 )
		goto st804;
	goto st0;
st804:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof804;
case 804:
	if ( (*( state.p)) == 110 )
		goto st805;
	goto st0;
st805:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof805;
case 805:
	if ( (*( state.p)) == 116 )
		goto st806;
	goto st0;
st806:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof806;
case 806:
	if ( (*( state.p)) == 97 )
		goto st807;
	goto st0;
st807:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof807;
case 807:
	switch( (*( state.p)) ) {
		case 13: goto tr1217;
		case 32: goto tr1217;
		case 59: goto tr1218;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1217;
	goto st0;
tr1179:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st808;
tr1244:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st808;
st808:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof808;
case 808:
#line 12597 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st809;
	goto st0;
st809:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof809;
case 809:
	if ( (*( state.p)) == 100 )
		goto st810;
	goto st0;
st810:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof810;
case 810:
	switch( (*( state.p)) ) {
		case 13: goto tr1221;
		case 32: goto tr1221;
		case 59: goto tr1222;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1221;
	goto st0;
tr1180:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st811;
tr1245:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st811;
st811:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof811;
case 811:
#line 12632 "configparser.h"
	if ( (*( state.p)) == 104 )
		goto st812;
	goto st0;
st812:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof812;
case 812:
	if ( (*( state.p)) == 105 )
		goto st813;
	goto st0;
st813:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof813;
case 813:
	if ( (*( state.p)) == 116 )
		goto st814;
	goto st0;
st814:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof814;
case 814:
	if ( (*( state.p)) == 101 )
		goto st815;
	goto st0;
st815:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof815;
case 815:
	switch( (*( state.p)) ) {
		case 13: goto tr1227;
		case 32: goto tr1227;
		case 59: goto tr1228;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1227;
	goto st0;
tr1181:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st816;
tr1246:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st816;
st816:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof816;
case 816:
#line 12681 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st817;
	goto st0;
st817:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof817;
case 817:
	if ( (*( state.p)) == 108 )
		goto st818;
	goto st0;
st818:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof818;
case 818:
	if ( (*( state.p)) == 108 )
		goto st819;
	goto st0;
st819:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof819;
case 819:
	if ( (*( state.p)) == 111 )
		goto st820;
	goto st0;
st820:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof820;
case 820:
	if ( (*( state.p)) == 119 )
		goto st821;
	goto st0;
st821:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof821;
case 821:
	switch( (*( state.p)) ) {
		case 13: goto tr1234;
		case 32: goto tr1234;
		case 59: goto tr1235;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1234;
	goto st0;
tr1174:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st822;
tr1239:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st822;
st822:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof822;
case 822:
#line 12737 "configparser.h"
	switch( (*( state.p)) ) {
		case 98: goto st785;
		case 99: goto st792;
		case 103: goto st796;
		case 109: goto st801;
		case 114: goto st808;
		case 119: goto st811;
		case 121: goto st816;
	}
	goto st0;
st823:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof823;
case 823:
	if ( (*( state.p)) == 105 )
		goto st824;
	goto st0;
st824:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof824;
case 824:
	if ( (*( state.p)) == 109 )
		goto st825;
	goto st0;
st825:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof825;
case 825:
	switch( (*( state.p)) ) {
		case 13: goto tr1238;
		case 32: goto tr1238;
		case 95: goto tr1239;
		case 98: goto tr1240;
		case 99: goto tr1241;
		case 103: goto tr1242;
		case 109: goto tr1243;
		case 114: goto tr1244;
		case 119: goto tr1245;
		case 121: goto tr1246;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1238;
	goto st0;
st826:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof826;
case 826:
	if ( (*( state.p)) == 111 )
		goto st827;
	goto st0;
st827:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof827;
case 827:
	if ( (*( state.p)) == 110 )
		goto st828;
	goto st0;
st828:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof828;
case 828:
	if ( (*( state.p)) == 101 )
		goto st789;
	goto st0;
st829:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof829;
case 829:
	switch( (*( state.p)) ) {
		case 13: goto st830;
		case 32: goto st830;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st830;
	goto st0;
st830:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof830;
case 830:
	switch( (*( state.p)) ) {
		case 13: goto st830;
		case 32: goto st830;
		case 34: goto tr1250;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st830;
	goto st0;
tr1251:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st831;
tr1250:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st831;
tr1253:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 831; goto st47;}}
	goto st831;
st831:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof831;
case 831:
#line 12845 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st832;
		case 92: goto tr1253;
	}
	goto tr1251;
st832:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof832;
case 832:
	switch( (*( state.p)) ) {
		case 13: goto tr1254;
		case 32: goto tr1254;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1254;
	goto st0;
tr1254:
#line 164 "configparser.rl"
	{ skin.text = state.match; }
	goto st833;
st833:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof833;
case 833:
#line 12870 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st833;
		case 32: goto st833;
		case 98: goto st834;
		case 100: goto st879;
		case 110: goto st882;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st833;
	goto st0;
st834:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof834;
case 834:
	if ( (*( state.p)) == 114 )
		goto st835;
	goto st0;
st835:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof835;
case 835:
	if ( (*( state.p)) == 105 )
		goto st836;
	goto st0;
st836:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof836;
case 836:
	if ( (*( state.p)) == 103 )
		goto st837;
	goto st0;
st837:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof837;
case 837:
	if ( (*( state.p)) == 104 )
		goto st838;
	goto st0;
st838:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof838;
case 838:
	if ( (*( state.p)) == 116 )
		goto st839;
	goto st0;
st839:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof839;
case 839:
	switch( (*( state.p)) ) {
		case 13: goto tr1264;
		case 32: goto tr1264;
		case 95: goto tr1265;
		case 98: goto tr1266;
		case 99: goto tr1267;
		case 103: goto tr1268;
		case 109: goto tr1269;
		case 114: goto tr1270;
		case 119: goto tr1271;
		case 121: goto tr1272;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1264;
	goto st0;
tr1264:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st840;
tr1329:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st840;
st840:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof840;
case 840:
#line 12947 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st840;
		case 32: goto st840;
		case 98: goto st841;
		case 99: goto st848;
		case 103: goto st852;
		case 109: goto st857;
		case 114: goto st864;
		case 119: goto st867;
		case 121: goto st872;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st840;
	goto st0;
tr1266:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st841;
tr1331:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st841;
st841:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof841;
case 841:
#line 12974 "configparser.h"
	if ( (*( state.p)) == 108 )
		goto st842;
	goto st0;
st842:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof842;
case 842:
	switch( (*( state.p)) ) {
		case 97: goto st843;
		case 117: goto st846;
	}
	goto st0;
st843:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof843;
case 843:
	if ( (*( state.p)) == 99 )
		goto st844;
	goto st0;
st844:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof844;
case 844:
	if ( (*( state.p)) == 107 )
		goto st845;
	goto st0;
st845:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof845;
case 845:
	switch( (*( state.p)) ) {
		case 13: goto tr1286;
		case 32: goto tr1286;
		case 59: goto tr1287;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1286;
	goto st0;
st846:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof846;
case 846:
	if ( (*( state.p)) == 101 )
		goto st847;
	goto st0;
st847:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof847;
case 847:
	switch( (*( state.p)) ) {
		case 13: goto tr1289;
		case 32: goto tr1289;
		case 59: goto tr1290;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1289;
	goto st0;
tr1267:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st848;
tr1332:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st848;
st848:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof848;
case 848:
#line 13044 "configparser.h"
	if ( (*( state.p)) == 121 )
		goto st849;
	goto st0;
st849:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof849;
case 849:
	if ( (*( state.p)) == 97 )
		goto st850;
	goto st0;
st850:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof850;
case 850:
	if ( (*( state.p)) == 110 )
		goto st851;
	goto st0;
st851:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof851;
case 851:
	switch( (*( state.p)) ) {
		case 13: goto tr1294;
		case 32: goto tr1294;
		case 59: goto tr1295;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1294;
	goto st0;
tr1268:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st852;
tr1333:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st852;
st852:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof852;
case 852:
#line 13086 "configparser.h"
	if ( (*( state.p)) == 114 )
		goto st853;
	goto st0;
st853:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof853;
case 853:
	if ( (*( state.p)) == 101 )
		goto st854;
	goto st0;
st854:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof854;
case 854:
	if ( (*( state.p)) == 101 )
		goto st855;
	goto st0;
st855:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof855;
case 855:
	if ( (*( state.p)) == 110 )
		goto st856;
	goto st0;
st856:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof856;
case 856:
	switch( (*( state.p)) ) {
		case 13: goto tr1300;
		case 32: goto tr1300;
		case 59: goto tr1301;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1300;
	goto st0;
tr1269:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st857;
tr1334:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st857;
st857:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof857;
case 857:
#line 13135 "configparser.h"
	if ( (*( state.p)) == 97 )
		goto st858;
	goto st0;
st858:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof858;
case 858:
	if ( (*( state.p)) == 103 )
		goto st859;
	goto st0;
st859:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof859;
case 859:
	if ( (*( state.p)) == 101 )
		goto st860;
	goto st0;
st860:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof860;
case 860:
	if ( (*( state.p)) == 110 )
		goto st861;
	goto st0;
st861:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof861;
case 861:
	if ( (*( state.p)) == 116 )
		goto st862;
	goto st0;
st862:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof862;
case 862:
	if ( (*( state.p)) == 97 )
		goto st863;
	goto st0;
st863:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof863;
case 863:
	switch( (*( state.p)) ) {
		case 13: goto tr1308;
		case 32: goto tr1308;
		case 59: goto tr1309;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1308;
	goto st0;
tr1270:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st864;
tr1335:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st864;
st864:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof864;
case 864:
#line 13198 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st865;
	goto st0;
st865:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof865;
case 865:
	if ( (*( state.p)) == 100 )
		goto st866;
	goto st0;
st866:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof866;
case 866:
	switch( (*( state.p)) ) {
		case 13: goto tr1312;
		case 32: goto tr1312;
		case 59: goto tr1313;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1312;
	goto st0;
tr1271:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st867;
tr1336:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st867;
st867:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof867;
case 867:
#line 13233 "configparser.h"
	if ( (*( state.p)) == 104 )
		goto st868;
	goto st0;
st868:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof868;
case 868:
	if ( (*( state.p)) == 105 )
		goto st869;
	goto st0;
st869:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof869;
case 869:
	if ( (*( state.p)) == 116 )
		goto st870;
	goto st0;
st870:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof870;
case 870:
	if ( (*( state.p)) == 101 )
		goto st871;
	goto st0;
st871:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof871;
case 871:
	switch( (*( state.p)) ) {
		case 13: goto tr1318;
		case 32: goto tr1318;
		case 59: goto tr1319;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1318;
	goto st0;
tr1272:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st872;
tr1337:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st872;
st872:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof872;
case 872:
#line 13282 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st873;
	goto st0;
st873:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof873;
case 873:
	if ( (*( state.p)) == 108 )
		goto st874;
	goto st0;
st874:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof874;
case 874:
	if ( (*( state.p)) == 108 )
		goto st875;
	goto st0;
st875:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof875;
case 875:
	if ( (*( state.p)) == 111 )
		goto st876;
	goto st0;
st876:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof876;
case 876:
	if ( (*( state.p)) == 119 )
		goto st877;
	goto st0;
st877:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof877;
case 877:
	switch( (*( state.p)) ) {
		case 13: goto tr1325;
		case 32: goto tr1325;
		case 59: goto tr1326;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1325;
	goto st0;
tr1265:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st878;
tr1330:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st878;
st878:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof878;
case 878:
#line 13338 "configparser.h"
	switch( (*( state.p)) ) {
		case 98: goto st841;
		case 99: goto st848;
		case 103: goto st852;
		case 109: goto st857;
		case 114: goto st864;
		case 119: goto st867;
		case 121: goto st872;
	}
	goto st0;
st879:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof879;
case 879:
	if ( (*( state.p)) == 105 )
		goto st880;
	goto st0;
st880:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof880;
case 880:
	if ( (*( state.p)) == 109 )
		goto st881;
	goto st0;
st881:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof881;
case 881:
	switch( (*( state.p)) ) {
		case 13: goto tr1329;
		case 32: goto tr1329;
		case 95: goto tr1330;
		case 98: goto tr1331;
		case 99: goto tr1332;
		case 103: goto tr1333;
		case 109: goto tr1334;
		case 114: goto tr1335;
		case 119: goto tr1336;
		case 121: goto tr1337;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1329;
	goto st0;
st882:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof882;
case 882:
	if ( (*( state.p)) == 111 )
		goto st883;
	goto st0;
st883:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof883;
case 883:
	if ( (*( state.p)) == 110 )
		goto st884;
	goto st0;
st884:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof884;
case 884:
	if ( (*( state.p)) == 101 )
		goto st845;
	goto st0;
st885:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof885;
case 885:
	switch( (*( state.p)) ) {
		case 13: goto st886;
		case 32: goto st886;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st886;
	goto st0;
st886:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof886;
case 886:
	switch( (*( state.p)) ) {
		case 13: goto st886;
		case 32: goto st886;
		case 34: goto tr1341;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st886;
	goto st0;
tr1342:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st887;
tr1341:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st887;
tr1344:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 887; goto st47;}}
	goto st887;
st887:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof887;
case 887:
#line 13446 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st888;
		case 92: goto tr1344;
	}
	goto tr1342;
st888:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof888;
case 888:
	switch( (*( state.p)) ) {
		case 13: goto tr1345;
		case 32: goto tr1345;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1345;
	goto st0;
tr1345:
#line 164 "configparser.rl"
	{ skin.text = state.match; }
	goto st889;
st889:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof889;
case 889:
#line 13471 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st889;
		case 32: goto st889;
		case 98: goto st890;
		case 100: goto st935;
		case 110: goto st938;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st889;
	goto st0;
st890:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof890;
case 890:
	if ( (*( state.p)) == 114 )
		goto st891;
	goto st0;
st891:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof891;
case 891:
	if ( (*( state.p)) == 105 )
		goto st892;
	goto st0;
st892:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof892;
case 892:
	if ( (*( state.p)) == 103 )
		goto st893;
	goto st0;
st893:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof893;
case 893:
	if ( (*( state.p)) == 104 )
		goto st894;
	goto st0;
st894:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof894;
case 894:
	if ( (*( state.p)) == 116 )
		goto st895;
	goto st0;
st895:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof895;
case 895:
	switch( (*( state.p)) ) {
		case 13: goto tr1355;
		case 32: goto tr1355;
		case 95: goto tr1356;
		case 98: goto tr1357;
		case 99: goto tr1358;
		case 103: goto tr1359;
		case 109: goto tr1360;
		case 114: goto tr1361;
		case 119: goto tr1362;
		case 121: goto tr1363;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1355;
	goto st0;
tr1355:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st896;
tr1420:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st896;
st896:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof896;
case 896:
#line 13548 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st896;
		case 32: goto st896;
		case 98: goto st897;
		case 99: goto st904;
		case 103: goto st908;
		case 109: goto st913;
		case 114: goto st920;
		case 119: goto st923;
		case 121: goto st928;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st896;
	goto st0;
tr1357:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st897;
tr1422:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st897;
st897:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof897;
case 897:
#line 13575 "configparser.h"
	if ( (*( state.p)) == 108 )
		goto st898;
	goto st0;
st898:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof898;
case 898:
	switch( (*( state.p)) ) {
		case 97: goto st899;
		case 117: goto st902;
	}
	goto st0;
st899:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof899;
case 899:
	if ( (*( state.p)) == 99 )
		goto st900;
	goto st0;
st900:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof900;
case 900:
	if ( (*( state.p)) == 107 )
		goto st901;
	goto st0;
st901:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof901;
case 901:
	switch( (*( state.p)) ) {
		case 13: goto tr1377;
		case 32: goto tr1377;
		case 59: goto tr1378;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1377;
	goto st0;
st902:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof902;
case 902:
	if ( (*( state.p)) == 101 )
		goto st903;
	goto st0;
st903:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof903;
case 903:
	switch( (*( state.p)) ) {
		case 13: goto tr1380;
		case 32: goto tr1380;
		case 59: goto tr1381;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1380;
	goto st0;
tr1358:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st904;
tr1423:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st904;
st904:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof904;
case 904:
#line 13645 "configparser.h"
	if ( (*( state.p)) == 121 )
		goto st905;
	goto st0;
st905:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof905;
case 905:
	if ( (*( state.p)) == 97 )
		goto st906;
	goto st0;
st906:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof906;
case 906:
	if ( (*( state.p)) == 110 )
		goto st907;
	goto st0;
st907:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof907;
case 907:
	switch( (*( state.p)) ) {
		case 13: goto tr1385;
		case 32: goto tr1385;
		case 59: goto tr1386;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1385;
	goto st0;
tr1359:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st908;
tr1424:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st908;
st908:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof908;
case 908:
#line 13687 "configparser.h"
	if ( (*( state.p)) == 114 )
		goto st909;
	goto st0;
st909:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof909;
case 909:
	if ( (*( state.p)) == 101 )
		goto st910;
	goto st0;
st910:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof910;
case 910:
	if ( (*( state.p)) == 101 )
		goto st911;
	goto st0;
st911:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof911;
case 911:
	if ( (*( state.p)) == 110 )
		goto st912;
	goto st0;
st912:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof912;
case 912:
	switch( (*( state.p)) ) {
		case 13: goto tr1391;
		case 32: goto tr1391;
		case 59: goto tr1392;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1391;
	goto st0;
tr1360:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st913;
tr1425:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st913;
st913:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof913;
case 913:
#line 13736 "configparser.h"
	if ( (*( state.p)) == 97 )
		goto st914;
	goto st0;
st914:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof914;
case 914:
	if ( (*( state.p)) == 103 )
		goto st915;
	goto st0;
st915:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof915;
case 915:
	if ( (*( state.p)) == 101 )
		goto st916;
	goto st0;
st916:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof916;
case 916:
	if ( (*( state.p)) == 110 )
		goto st917;
	goto st0;
st917:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof917;
case 917:
	if ( (*( state.p)) == 116 )
		goto st918;
	goto st0;
st918:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof918;
case 918:
	if ( (*( state.p)) == 97 )
		goto st919;
	goto st0;
st919:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof919;
case 919:
	switch( (*( state.p)) ) {
		case 13: goto tr1399;
		case 32: goto tr1399;
		case 59: goto tr1400;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1399;
	goto st0;
tr1361:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st920;
tr1426:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st920;
st920:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof920;
case 920:
#line 13799 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st921;
	goto st0;
st921:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof921;
case 921:
	if ( (*( state.p)) == 100 )
		goto st922;
	goto st0;
st922:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof922;
case 922:
	switch( (*( state.p)) ) {
		case 13: goto tr1403;
		case 32: goto tr1403;
		case 59: goto tr1404;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1403;
	goto st0;
tr1362:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st923;
tr1427:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st923;
st923:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof923;
case 923:
#line 13834 "configparser.h"
	if ( (*( state.p)) == 104 )
		goto st924;
	goto st0;
st924:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof924;
case 924:
	if ( (*( state.p)) == 105 )
		goto st925;
	goto st0;
st925:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof925;
case 925:
	if ( (*( state.p)) == 116 )
		goto st926;
	goto st0;
st926:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof926;
case 926:
	if ( (*( state.p)) == 101 )
		goto st927;
	goto st0;
st927:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof927;
case 927:
	switch( (*( state.p)) ) {
		case 13: goto tr1409;
		case 32: goto tr1409;
		case 59: goto tr1410;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1409;
	goto st0;
tr1363:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st928;
tr1428:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st928;
st928:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof928;
case 928:
#line 13883 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st929;
	goto st0;
st929:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof929;
case 929:
	if ( (*( state.p)) == 108 )
		goto st930;
	goto st0;
st930:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof930;
case 930:
	if ( (*( state.p)) == 108 )
		goto st931;
	goto st0;
st931:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof931;
case 931:
	if ( (*( state.p)) == 111 )
		goto st932;
	goto st0;
st932:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof932;
case 932:
	if ( (*( state.p)) == 119 )
		goto st933;
	goto st0;
st933:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof933;
case 933:
	switch( (*( state.p)) ) {
		case 13: goto tr1416;
		case 32: goto tr1416;
		case 59: goto tr1417;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1416;
	goto st0;
tr1356:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st934;
tr1421:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st934;
st934:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof934;
case 934:
#line 13939 "configparser.h"
	switch( (*( state.p)) ) {
		case 98: goto st897;
		case 99: goto st904;
		case 103: goto st908;
		case 109: goto st913;
		case 114: goto st920;
		case 119: goto st923;
		case 121: goto st928;
	}
	goto st0;
st935:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof935;
case 935:
	if ( (*( state.p)) == 105 )
		goto st936;
	goto st0;
st936:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof936;
case 936:
	if ( (*( state.p)) == 109 )
		goto st937;
	goto st0;
st937:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof937;
case 937:
	switch( (*( state.p)) ) {
		case 13: goto tr1420;
		case 32: goto tr1420;
		case 95: goto tr1421;
		case 98: goto tr1422;
		case 99: goto tr1423;
		case 103: goto tr1424;
		case 109: goto tr1425;
		case 114: goto tr1426;
		case 119: goto tr1427;
		case 121: goto tr1428;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1420;
	goto st0;
st938:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof938;
case 938:
	if ( (*( state.p)) == 111 )
		goto st939;
	goto st0;
st939:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof939;
case 939:
	if ( (*( state.p)) == 110 )
		goto st940;
	goto st0;
st940:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof940;
case 940:
	if ( (*( state.p)) == 101 )
		goto st901;
	goto st0;
st941:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof941;
case 941:
	switch( (*( state.p)) ) {
		case 13: goto st942;
		case 32: goto st942;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st942;
	goto st0;
st942:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof942;
case 942:
	switch( (*( state.p)) ) {
		case 13: goto st942;
		case 32: goto st942;
		case 34: goto tr1432;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st942;
	goto st0;
tr1433:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st943;
tr1432:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st943;
tr1435:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 943; goto st47;}}
	goto st943;
st943:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof943;
case 943:
#line 14047 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st944;
		case 92: goto tr1435;
	}
	goto tr1433;
st944:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof944;
case 944:
	switch( (*( state.p)) ) {
		case 13: goto tr1436;
		case 32: goto tr1436;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1436;
	goto st0;
tr1436:
#line 164 "configparser.rl"
	{ skin.text = state.match; }
	goto st945;
st945:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof945;
case 945:
#line 14072 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st945;
		case 32: goto st945;
		case 98: goto st946;
		case 100: goto st991;
		case 110: goto st994;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st945;
	goto st0;
st946:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof946;
case 946:
	if ( (*( state.p)) == 114 )
		goto st947;
	goto st0;
st947:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof947;
case 947:
	if ( (*( state.p)) == 105 )
		goto st948;
	goto st0;
st948:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof948;
case 948:
	if ( (*( state.p)) == 103 )
		goto st949;
	goto st0;
st949:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof949;
case 949:
	if ( (*( state.p)) == 104 )
		goto st950;
	goto st0;
st950:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof950;
case 950:
	if ( (*( state.p)) == 116 )
		goto st951;
	goto st0;
st951:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof951;
case 951:
	switch( (*( state.p)) ) {
		case 13: goto tr1446;
		case 32: goto tr1446;
		case 95: goto tr1447;
		case 98: goto tr1448;
		case 99: goto tr1449;
		case 103: goto tr1450;
		case 109: goto tr1451;
		case 114: goto tr1452;
		case 119: goto tr1453;
		case 121: goto tr1454;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1446;
	goto st0;
tr1446:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st952;
tr1511:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st952;
st952:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof952;
case 952:
#line 14149 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st952;
		case 32: goto st952;
		case 98: goto st953;
		case 99: goto st960;
		case 103: goto st964;
		case 109: goto st969;
		case 114: goto st976;
		case 119: goto st979;
		case 121: goto st984;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st952;
	goto st0;
tr1448:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st953;
tr1513:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st953;
st953:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof953;
case 953:
#line 14176 "configparser.h"
	if ( (*( state.p)) == 108 )
		goto st954;
	goto st0;
st954:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof954;
case 954:
	switch( (*( state.p)) ) {
		case 97: goto st955;
		case 117: goto st958;
	}
	goto st0;
st955:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof955;
case 955:
	if ( (*( state.p)) == 99 )
		goto st956;
	goto st0;
st956:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof956;
case 956:
	if ( (*( state.p)) == 107 )
		goto st957;
	goto st0;
st957:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof957;
case 957:
	switch( (*( state.p)) ) {
		case 13: goto tr1468;
		case 32: goto tr1468;
		case 59: goto tr1469;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1468;
	goto st0;
st958:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof958;
case 958:
	if ( (*( state.p)) == 101 )
		goto st959;
	goto st0;
st959:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof959;
case 959:
	switch( (*( state.p)) ) {
		case 13: goto tr1471;
		case 32: goto tr1471;
		case 59: goto tr1472;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1471;
	goto st0;
tr1449:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st960;
tr1514:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st960;
st960:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof960;
case 960:
#line 14246 "configparser.h"
	if ( (*( state.p)) == 121 )
		goto st961;
	goto st0;
st961:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof961;
case 961:
	if ( (*( state.p)) == 97 )
		goto st962;
	goto st0;
st962:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof962;
case 962:
	if ( (*( state.p)) == 110 )
		goto st963;
	goto st0;
st963:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof963;
case 963:
	switch( (*( state.p)) ) {
		case 13: goto tr1476;
		case 32: goto tr1476;
		case 59: goto tr1477;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1476;
	goto st0;
tr1450:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st964;
tr1515:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st964;
st964:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof964;
case 964:
#line 14288 "configparser.h"
	if ( (*( state.p)) == 114 )
		goto st965;
	goto st0;
st965:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof965;
case 965:
	if ( (*( state.p)) == 101 )
		goto st966;
	goto st0;
st966:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof966;
case 966:
	if ( (*( state.p)) == 101 )
		goto st967;
	goto st0;
st967:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof967;
case 967:
	if ( (*( state.p)) == 110 )
		goto st968;
	goto st0;
st968:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof968;
case 968:
	switch( (*( state.p)) ) {
		case 13: goto tr1482;
		case 32: goto tr1482;
		case 59: goto tr1483;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1482;
	goto st0;
tr1451:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st969;
tr1516:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st969;
st969:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof969;
case 969:
#line 14337 "configparser.h"
	if ( (*( state.p)) == 97 )
		goto st970;
	goto st0;
st970:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof970;
case 970:
	if ( (*( state.p)) == 103 )
		goto st971;
	goto st0;
st971:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof971;
case 971:
	if ( (*( state.p)) == 101 )
		goto st972;
	goto st0;
st972:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof972;
case 972:
	if ( (*( state.p)) == 110 )
		goto st973;
	goto st0;
st973:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof973;
case 973:
	if ( (*( state.p)) == 116 )
		goto st974;
	goto st0;
st974:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof974;
case 974:
	if ( (*( state.p)) == 97 )
		goto st975;
	goto st0;
st975:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof975;
case 975:
	switch( (*( state.p)) ) {
		case 13: goto tr1490;
		case 32: goto tr1490;
		case 59: goto tr1491;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1490;
	goto st0;
tr1452:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st976;
tr1517:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st976;
st976:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof976;
case 976:
#line 14400 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st977;
	goto st0;
st977:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof977;
case 977:
	if ( (*( state.p)) == 100 )
		goto st978;
	goto st0;
st978:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof978;
case 978:
	switch( (*( state.p)) ) {
		case 13: goto tr1494;
		case 32: goto tr1494;
		case 59: goto tr1495;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1494;
	goto st0;
tr1453:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st979;
tr1518:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st979;
st979:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof979;
case 979:
#line 14435 "configparser.h"
	if ( (*( state.p)) == 104 )
		goto st980;
	goto st0;
st980:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof980;
case 980:
	if ( (*( state.p)) == 105 )
		goto st981;
	goto st0;
st981:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof981;
case 981:
	if ( (*( state.p)) == 116 )
		goto st982;
	goto st0;
st982:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof982;
case 982:
	if ( (*( state.p)) == 101 )
		goto st983;
	goto st0;
st983:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof983;
case 983:
	switch( (*( state.p)) ) {
		case 13: goto tr1500;
		case 32: goto tr1500;
		case 59: goto tr1501;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1500;
	goto st0;
tr1454:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st984;
tr1519:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st984;
st984:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof984;
case 984:
#line 14484 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st985;
	goto st0;
st985:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof985;
case 985:
	if ( (*( state.p)) == 108 )
		goto st986;
	goto st0;
st986:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof986;
case 986:
	if ( (*( state.p)) == 108 )
		goto st987;
	goto st0;
st987:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof987;
case 987:
	if ( (*( state.p)) == 111 )
		goto st988;
	goto st0;
st988:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof988;
case 988:
	if ( (*( state.p)) == 119 )
		goto st989;
	goto st0;
st989:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof989;
case 989:
	switch( (*( state.p)) ) {
		case 13: goto tr1507;
		case 32: goto tr1507;
		case 59: goto tr1508;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1507;
	goto st0;
tr1447:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st990;
tr1512:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st990;
st990:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof990;
case 990:
#line 14540 "configparser.h"
	switch( (*( state.p)) ) {
		case 98: goto st953;
		case 99: goto st960;
		case 103: goto st964;
		case 109: goto st969;
		case 114: goto st976;
		case 119: goto st979;
		case 121: goto st984;
	}
	goto st0;
st991:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof991;
case 991:
	if ( (*( state.p)) == 105 )
		goto st992;
	goto st0;
st992:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof992;
case 992:
	if ( (*( state.p)) == 109 )
		goto st993;
	goto st0;
st993:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof993;
case 993:
	switch( (*( state.p)) ) {
		case 13: goto tr1511;
		case 32: goto tr1511;
		case 95: goto tr1512;
		case 98: goto tr1513;
		case 99: goto tr1514;
		case 103: goto tr1515;
		case 109: goto tr1516;
		case 114: goto tr1517;
		case 119: goto tr1518;
		case 121: goto tr1519;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1511;
	goto st0;
st994:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof994;
case 994:
	if ( (*( state.p)) == 111 )
		goto st995;
	goto st0;
st995:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof995;
case 995:
	if ( (*( state.p)) == 110 )
		goto st996;
	goto st0;
st996:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof996;
case 996:
	if ( (*( state.p)) == 101 )
		goto st957;
	goto st0;
st997:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof997;
case 997:
	switch( (*( state.p)) ) {
		case 13: goto st998;
		case 32: goto st998;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st998;
	goto st0;
st998:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof998;
case 998:
	switch( (*( state.p)) ) {
		case 13: goto st998;
		case 32: goto st998;
		case 34: goto tr1523;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st998;
	goto st0;
tr1524:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st999;
tr1523:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st999;
tr1526:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 999; goto st47;}}
	goto st999;
st999:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof999;
case 999:
#line 14648 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st1000;
		case 92: goto tr1526;
	}
	goto tr1524;
st1000:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1000;
case 1000:
	switch( (*( state.p)) ) {
		case 13: goto tr1527;
		case 32: goto tr1527;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1527;
	goto st0;
tr1527:
#line 164 "configparser.rl"
	{ skin.text = state.match; }
	goto st1001;
st1001:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1001;
case 1001:
#line 14673 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st1001;
		case 32: goto st1001;
		case 98: goto st1002;
		case 100: goto st1047;
		case 110: goto st1050;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1001;
	goto st0;
st1002:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1002;
case 1002:
	if ( (*( state.p)) == 114 )
		goto st1003;
	goto st0;
st1003:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1003;
case 1003:
	if ( (*( state.p)) == 105 )
		goto st1004;
	goto st0;
st1004:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1004;
case 1004:
	if ( (*( state.p)) == 103 )
		goto st1005;
	goto st0;
st1005:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1005;
case 1005:
	if ( (*( state.p)) == 104 )
		goto st1006;
	goto st0;
st1006:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1006;
case 1006:
	if ( (*( state.p)) == 116 )
		goto st1007;
	goto st0;
st1007:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1007;
case 1007:
	switch( (*( state.p)) ) {
		case 13: goto tr1537;
		case 32: goto tr1537;
		case 95: goto tr1538;
		case 98: goto tr1539;
		case 99: goto tr1540;
		case 103: goto tr1541;
		case 109: goto tr1542;
		case 114: goto tr1543;
		case 119: goto tr1544;
		case 121: goto tr1545;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1537;
	goto st0;
tr1537:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1008;
tr1602:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1008;
st1008:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1008;
case 1008:
#line 14750 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st1008;
		case 32: goto st1008;
		case 98: goto st1009;
		case 99: goto st1016;
		case 103: goto st1020;
		case 109: goto st1025;
		case 114: goto st1032;
		case 119: goto st1035;
		case 121: goto st1040;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1008;
	goto st0;
tr1539:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1009;
tr1604:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1009;
st1009:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1009;
case 1009:
#line 14777 "configparser.h"
	if ( (*( state.p)) == 108 )
		goto st1010;
	goto st0;
st1010:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1010;
case 1010:
	switch( (*( state.p)) ) {
		case 97: goto st1011;
		case 117: goto st1014;
	}
	goto st0;
st1011:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1011;
case 1011:
	if ( (*( state.p)) == 99 )
		goto st1012;
	goto st0;
st1012:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1012;
case 1012:
	if ( (*( state.p)) == 107 )
		goto st1013;
	goto st0;
st1013:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1013;
case 1013:
	switch( (*( state.p)) ) {
		case 13: goto tr1559;
		case 32: goto tr1559;
		case 59: goto tr1560;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1559;
	goto st0;
st1014:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1014;
case 1014:
	if ( (*( state.p)) == 101 )
		goto st1015;
	goto st0;
st1015:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1015;
case 1015:
	switch( (*( state.p)) ) {
		case 13: goto tr1562;
		case 32: goto tr1562;
		case 59: goto tr1563;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1562;
	goto st0;
tr1540:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1016;
tr1605:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1016;
st1016:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1016;
case 1016:
#line 14847 "configparser.h"
	if ( (*( state.p)) == 121 )
		goto st1017;
	goto st0;
st1017:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1017;
case 1017:
	if ( (*( state.p)) == 97 )
		goto st1018;
	goto st0;
st1018:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1018;
case 1018:
	if ( (*( state.p)) == 110 )
		goto st1019;
	goto st0;
st1019:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1019;
case 1019:
	switch( (*( state.p)) ) {
		case 13: goto tr1567;
		case 32: goto tr1567;
		case 59: goto tr1568;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1567;
	goto st0;
tr1541:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1020;
tr1606:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1020;
st1020:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1020;
case 1020:
#line 14889 "configparser.h"
	if ( (*( state.p)) == 114 )
		goto st1021;
	goto st0;
st1021:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1021;
case 1021:
	if ( (*( state.p)) == 101 )
		goto st1022;
	goto st0;
st1022:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1022;
case 1022:
	if ( (*( state.p)) == 101 )
		goto st1023;
	goto st0;
st1023:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1023;
case 1023:
	if ( (*( state.p)) == 110 )
		goto st1024;
	goto st0;
st1024:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1024;
case 1024:
	switch( (*( state.p)) ) {
		case 13: goto tr1573;
		case 32: goto tr1573;
		case 59: goto tr1574;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1573;
	goto st0;
tr1542:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1025;
tr1607:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1025;
st1025:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1025;
case 1025:
#line 14938 "configparser.h"
	if ( (*( state.p)) == 97 )
		goto st1026;
	goto st0;
st1026:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1026;
case 1026:
	if ( (*( state.p)) == 103 )
		goto st1027;
	goto st0;
st1027:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1027;
case 1027:
	if ( (*( state.p)) == 101 )
		goto st1028;
	goto st0;
st1028:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1028;
case 1028:
	if ( (*( state.p)) == 110 )
		goto st1029;
	goto st0;
st1029:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1029;
case 1029:
	if ( (*( state.p)) == 116 )
		goto st1030;
	goto st0;
st1030:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1030;
case 1030:
	if ( (*( state.p)) == 97 )
		goto st1031;
	goto st0;
st1031:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1031;
case 1031:
	switch( (*( state.p)) ) {
		case 13: goto tr1581;
		case 32: goto tr1581;
		case 59: goto tr1582;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1581;
	goto st0;
tr1543:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1032;
tr1608:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1032;
st1032:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1032;
case 1032:
#line 15001 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st1033;
	goto st0;
st1033:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1033;
case 1033:
	if ( (*( state.p)) == 100 )
		goto st1034;
	goto st0;
st1034:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1034;
case 1034:
	switch( (*( state.p)) ) {
		case 13: goto tr1585;
		case 32: goto tr1585;
		case 59: goto tr1586;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1585;
	goto st0;
tr1544:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1035;
tr1609:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1035;
st1035:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1035;
case 1035:
#line 15036 "configparser.h"
	if ( (*( state.p)) == 104 )
		goto st1036;
	goto st0;
st1036:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1036;
case 1036:
	if ( (*( state.p)) == 105 )
		goto st1037;
	goto st0;
st1037:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1037;
case 1037:
	if ( (*( state.p)) == 116 )
		goto st1038;
	goto st0;
st1038:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1038;
case 1038:
	if ( (*( state.p)) == 101 )
		goto st1039;
	goto st0;
st1039:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1039;
case 1039:
	switch( (*( state.p)) ) {
		case 13: goto tr1591;
		case 32: goto tr1591;
		case 59: goto tr1592;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1591;
	goto st0;
tr1545:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1040;
tr1610:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1040;
st1040:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1040;
case 1040:
#line 15085 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st1041;
	goto st0;
st1041:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1041;
case 1041:
	if ( (*( state.p)) == 108 )
		goto st1042;
	goto st0;
st1042:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1042;
case 1042:
	if ( (*( state.p)) == 108 )
		goto st1043;
	goto st0;
st1043:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1043;
case 1043:
	if ( (*( state.p)) == 111 )
		goto st1044;
	goto st0;
st1044:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1044;
case 1044:
	if ( (*( state.p)) == 119 )
		goto st1045;
	goto st0;
st1045:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1045;
case 1045:
	switch( (*( state.p)) ) {
		case 13: goto tr1598;
		case 32: goto tr1598;
		case 59: goto tr1599;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1598;
	goto st0;
tr1538:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1046;
tr1603:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1046;
st1046:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1046;
case 1046:
#line 15141 "configparser.h"
	switch( (*( state.p)) ) {
		case 98: goto st1009;
		case 99: goto st1016;
		case 103: goto st1020;
		case 109: goto st1025;
		case 114: goto st1032;
		case 119: goto st1035;
		case 121: goto st1040;
	}
	goto st0;
st1047:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1047;
case 1047:
	if ( (*( state.p)) == 105 )
		goto st1048;
	goto st0;
st1048:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1048;
case 1048:
	if ( (*( state.p)) == 109 )
		goto st1049;
	goto st0;
st1049:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1049;
case 1049:
	switch( (*( state.p)) ) {
		case 13: goto tr1602;
		case 32: goto tr1602;
		case 95: goto tr1603;
		case 98: goto tr1604;
		case 99: goto tr1605;
		case 103: goto tr1606;
		case 109: goto tr1607;
		case 114: goto tr1608;
		case 119: goto tr1609;
		case 121: goto tr1610;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1602;
	goto st0;
st1050:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1050;
case 1050:
	if ( (*( state.p)) == 111 )
		goto st1051;
	goto st0;
st1051:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1051;
case 1051:
	if ( (*( state.p)) == 110 )
		goto st1052;
	goto st0;
st1052:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1052;
case 1052:
	if ( (*( state.p)) == 101 )
		goto st1013;
	goto st0;
st1053:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1053;
case 1053:
	switch( (*( state.p)) ) {
		case 13: goto st1054;
		case 32: goto st1054;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1054;
	goto st0;
st1054:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1054;
case 1054:
	switch( (*( state.p)) ) {
		case 13: goto st1054;
		case 32: goto st1054;
		case 34: goto tr1614;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1054;
	goto st0;
tr1615:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st1055;
tr1614:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st1055;
tr1617:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 1055; goto st47;}}
	goto st1055;
st1055:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1055;
case 1055:
#line 15249 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st1056;
		case 92: goto tr1617;
	}
	goto tr1615;
st1056:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1056;
case 1056:
	switch( (*( state.p)) ) {
		case 13: goto tr1618;
		case 32: goto tr1618;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1618;
	goto st0;
tr1618:
#line 164 "configparser.rl"
	{ skin.text = state.match; }
	goto st1057;
st1057:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1057;
case 1057:
#line 15274 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st1057;
		case 32: goto st1057;
		case 98: goto st1058;
		case 100: goto st1103;
		case 110: goto st1106;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1057;
	goto st0;
st1058:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1058;
case 1058:
	if ( (*( state.p)) == 114 )
		goto st1059;
	goto st0;
st1059:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1059;
case 1059:
	if ( (*( state.p)) == 105 )
		goto st1060;
	goto st0;
st1060:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1060;
case 1060:
	if ( (*( state.p)) == 103 )
		goto st1061;
	goto st0;
st1061:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1061;
case 1061:
	if ( (*( state.p)) == 104 )
		goto st1062;
	goto st0;
st1062:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1062;
case 1062:
	if ( (*( state.p)) == 116 )
		goto st1063;
	goto st0;
st1063:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1063;
case 1063:
	switch( (*( state.p)) ) {
		case 13: goto tr1628;
		case 32: goto tr1628;
		case 95: goto tr1629;
		case 98: goto tr1630;
		case 99: goto tr1631;
		case 103: goto tr1632;
		case 109: goto tr1633;
		case 114: goto tr1634;
		case 119: goto tr1635;
		case 121: goto tr1636;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1628;
	goto st0;
tr1628:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1064;
tr1693:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1064;
st1064:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1064;
case 1064:
#line 15351 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st1064;
		case 32: goto st1064;
		case 98: goto st1065;
		case 99: goto st1072;
		case 103: goto st1076;
		case 109: goto st1081;
		case 114: goto st1088;
		case 119: goto st1091;
		case 121: goto st1096;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1064;
	goto st0;
tr1630:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1065;
tr1695:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1065;
st1065:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1065;
case 1065:
#line 15378 "configparser.h"
	if ( (*( state.p)) == 108 )
		goto st1066;
	goto st0;
st1066:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1066;
case 1066:
	switch( (*( state.p)) ) {
		case 97: goto st1067;
		case 117: goto st1070;
	}
	goto st0;
st1067:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1067;
case 1067:
	if ( (*( state.p)) == 99 )
		goto st1068;
	goto st0;
st1068:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1068;
case 1068:
	if ( (*( state.p)) == 107 )
		goto st1069;
	goto st0;
st1069:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1069;
case 1069:
	switch( (*( state.p)) ) {
		case 13: goto tr1650;
		case 32: goto tr1650;
		case 59: goto tr1651;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1650;
	goto st0;
st1070:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1070;
case 1070:
	if ( (*( state.p)) == 101 )
		goto st1071;
	goto st0;
st1071:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1071;
case 1071:
	switch( (*( state.p)) ) {
		case 13: goto tr1653;
		case 32: goto tr1653;
		case 59: goto tr1654;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1653;
	goto st0;
tr1631:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1072;
tr1696:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1072;
st1072:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1072;
case 1072:
#line 15448 "configparser.h"
	if ( (*( state.p)) == 121 )
		goto st1073;
	goto st0;
st1073:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1073;
case 1073:
	if ( (*( state.p)) == 97 )
		goto st1074;
	goto st0;
st1074:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1074;
case 1074:
	if ( (*( state.p)) == 110 )
		goto st1075;
	goto st0;
st1075:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1075;
case 1075:
	switch( (*( state.p)) ) {
		case 13: goto tr1658;
		case 32: goto tr1658;
		case 59: goto tr1659;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1658;
	goto st0;
tr1632:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1076;
tr1697:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1076;
st1076:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1076;
case 1076:
#line 15490 "configparser.h"
	if ( (*( state.p)) == 114 )
		goto st1077;
	goto st0;
st1077:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1077;
case 1077:
	if ( (*( state.p)) == 101 )
		goto st1078;
	goto st0;
st1078:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1078;
case 1078:
	if ( (*( state.p)) == 101 )
		goto st1079;
	goto st0;
st1079:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1079;
case 1079:
	if ( (*( state.p)) == 110 )
		goto st1080;
	goto st0;
st1080:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1080;
case 1080:
	switch( (*( state.p)) ) {
		case 13: goto tr1664;
		case 32: goto tr1664;
		case 59: goto tr1665;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1664;
	goto st0;
tr1633:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1081;
tr1698:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1081;
st1081:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1081;
case 1081:
#line 15539 "configparser.h"
	if ( (*( state.p)) == 97 )
		goto st1082;
	goto st0;
st1082:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1082;
case 1082:
	if ( (*( state.p)) == 103 )
		goto st1083;
	goto st0;
st1083:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1083;
case 1083:
	if ( (*( state.p)) == 101 )
		goto st1084;
	goto st0;
st1084:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1084;
case 1084:
	if ( (*( state.p)) == 110 )
		goto st1085;
	goto st0;
st1085:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1085;
case 1085:
	if ( (*( state.p)) == 116 )
		goto st1086;
	goto st0;
st1086:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1086;
case 1086:
	if ( (*( state.p)) == 97 )
		goto st1087;
	goto st0;
st1087:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1087;
case 1087:
	switch( (*( state.p)) ) {
		case 13: goto tr1672;
		case 32: goto tr1672;
		case 59: goto tr1673;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1672;
	goto st0;
tr1634:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1088;
tr1699:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1088;
st1088:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1088;
case 1088:
#line 15602 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st1089;
	goto st0;
st1089:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1089;
case 1089:
	if ( (*( state.p)) == 100 )
		goto st1090;
	goto st0;
st1090:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1090;
case 1090:
	switch( (*( state.p)) ) {
		case 13: goto tr1676;
		case 32: goto tr1676;
		case 59: goto tr1677;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1676;
	goto st0;
tr1635:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1091;
tr1700:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1091;
st1091:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1091;
case 1091:
#line 15637 "configparser.h"
	if ( (*( state.p)) == 104 )
		goto st1092;
	goto st0;
st1092:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1092;
case 1092:
	if ( (*( state.p)) == 105 )
		goto st1093;
	goto st0;
st1093:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1093;
case 1093:
	if ( (*( state.p)) == 116 )
		goto st1094;
	goto st0;
st1094:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1094;
case 1094:
	if ( (*( state.p)) == 101 )
		goto st1095;
	goto st0;
st1095:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1095;
case 1095:
	switch( (*( state.p)) ) {
		case 13: goto tr1682;
		case 32: goto tr1682;
		case 59: goto tr1683;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1682;
	goto st0;
tr1636:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1096;
tr1701:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1096;
st1096:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1096;
case 1096:
#line 15686 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st1097;
	goto st0;
st1097:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1097;
case 1097:
	if ( (*( state.p)) == 108 )
		goto st1098;
	goto st0;
st1098:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1098;
case 1098:
	if ( (*( state.p)) == 108 )
		goto st1099;
	goto st0;
st1099:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1099;
case 1099:
	if ( (*( state.p)) == 111 )
		goto st1100;
	goto st0;
st1100:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1100;
case 1100:
	if ( (*( state.p)) == 119 )
		goto st1101;
	goto st0;
st1101:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1101;
case 1101:
	switch( (*( state.p)) ) {
		case 13: goto tr1689;
		case 32: goto tr1689;
		case 59: goto tr1690;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1689;
	goto st0;
tr1629:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1102;
tr1694:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1102;
st1102:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1102;
case 1102:
#line 15742 "configparser.h"
	switch( (*( state.p)) ) {
		case 98: goto st1065;
		case 99: goto st1072;
		case 103: goto st1076;
		case 109: goto st1081;
		case 114: goto st1088;
		case 119: goto st1091;
		case 121: goto st1096;
	}
	goto st0;
st1103:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1103;
case 1103:
	if ( (*( state.p)) == 105 )
		goto st1104;
	goto st0;
st1104:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1104;
case 1104:
	if ( (*( state.p)) == 109 )
		goto st1105;
	goto st0;
st1105:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1105;
case 1105:
	switch( (*( state.p)) ) {
		case 13: goto tr1693;
		case 32: goto tr1693;
		case 95: goto tr1694;
		case 98: goto tr1695;
		case 99: goto tr1696;
		case 103: goto tr1697;
		case 109: goto tr1698;
		case 114: goto tr1699;
		case 119: goto tr1700;
		case 121: goto tr1701;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1693;
	goto st0;
st1106:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1106;
case 1106:
	if ( (*( state.p)) == 111 )
		goto st1107;
	goto st0;
st1107:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1107;
case 1107:
	if ( (*( state.p)) == 110 )
		goto st1108;
	goto st0;
st1108:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1108;
case 1108:
	if ( (*( state.p)) == 101 )
		goto st1069;
	goto st0;
st1109:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1109;
case 1109:
	if ( (*( state.p)) == 105 )
		goto st1110;
	goto st0;
st1110:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1110;
case 1110:
	if ( (*( state.p)) == 103 )
		goto st1111;
	goto st0;
st1111:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1111;
case 1111:
	if ( (*( state.p)) == 104 )
		goto st1112;
	goto st0;
st1112:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1112;
case 1112:
	if ( (*( state.p)) == 116 )
		goto st1113;
	goto st0;
st1113:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1113;
case 1113:
	if ( (*( state.p)) == 114 )
		goto st1114;
	goto st0;
st1114:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1114;
case 1114:
	if ( (*( state.p)) == 97 )
		goto st1115;
	goto st0;
st1115:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1115;
case 1115:
	if ( (*( state.p)) == 100 )
		goto st1116;
	goto st0;
st1116:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1116;
case 1116:
	if ( (*( state.p)) == 105 )
		goto st1117;
	goto st0;
st1117:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1117;
case 1117:
	if ( (*( state.p)) == 117 )
		goto st1118;
	goto st0;
st1118:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1118;
case 1118:
	if ( (*( state.p)) == 115 )
		goto st1119;
	goto st0;
st1119:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1119;
case 1119:
	switch( (*( state.p)) ) {
		case 13: goto st1120;
		case 32: goto st1120;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1120;
	goto st0;
st1120:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1120;
case 1120:
	switch( (*( state.p)) ) {
		case 13: goto st1120;
		case 32: goto st1120;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr1715;
	} else if ( (*( state.p)) >= 9 )
		goto st1120;
	goto st0;
tr1715:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st1121;
tr1717:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st1121;
st1121:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1121;
case 1121:
#line 15922 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto tr1716;
		case 32: goto tr1716;
		case 59: goto tr1718;
	}
	if ( (*( state.p)) > 10 ) {
		if ( 48 <= (*( state.p)) && (*( state.p)) <= 57 )
			goto tr1717;
	} else if ( (*( state.p)) >= 9 )
		goto tr1716;
	goto st0;
st1122:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1122;
case 1122:
	if ( (*( state.p)) == 104 )
		goto st1123;
	goto st0;
st1123:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1123;
case 1123:
	if ( (*( state.p)) == 97 )
		goto st1124;
	goto st0;
st1124:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1124;
case 1124:
	if ( (*( state.p)) == 108 )
		goto st1125;
	goto st0;
st1125:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1125;
case 1125:
	if ( (*( state.p)) == 108 )
		goto st1126;
	goto st0;
st1126:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1126;
case 1126:
	if ( (*( state.p)) == 111 )
		goto st1127;
	goto st0;
st1127:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1127;
case 1127:
	if ( (*( state.p)) == 119 )
		goto st1128;
	goto st0;
st1128:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1128;
case 1128:
	if ( (*( state.p)) == 95 )
		goto st1129;
	goto st0;
st1129:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1129;
case 1129:
	if ( (*( state.p)) == 119 )
		goto st1130;
	goto st0;
st1130:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1130;
case 1130:
	if ( (*( state.p)) == 97 )
		goto st1131;
	goto st0;
st1131:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1131;
case 1131:
	if ( (*( state.p)) == 116 )
		goto st1132;
	goto st0;
st1132:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1132;
case 1132:
	if ( (*( state.p)) == 101 )
		goto st1133;
	goto st0;
st1133:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1133;
case 1133:
	if ( (*( state.p)) == 114 )
		goto st1134;
	goto st0;
st1134:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1134;
case 1134:
	switch( (*( state.p)) ) {
		case 13: goto st1135;
		case 32: goto st1135;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1135;
	goto st0;
st1135:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1135;
case 1135:
	switch( (*( state.p)) ) {
		case 13: goto st1135;
		case 32: goto st1135;
		case 34: goto tr1732;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1135;
	goto st0;
tr1733:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st1136;
tr1732:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st1136;
tr1735:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 1136; goto st47;}}
	goto st1136;
st1136:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1136;
case 1136:
#line 16061 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st1137;
		case 92: goto tr1735;
	}
	goto tr1733;
st1137:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1137;
case 1137:
	switch( (*( state.p)) ) {
		case 13: goto tr1736;
		case 32: goto tr1736;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1736;
	goto st0;
tr1736:
#line 164 "configparser.rl"
	{ skin.text = state.match; }
	goto st1138;
st1138:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1138;
case 1138:
#line 16086 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st1138;
		case 32: goto st1138;
		case 98: goto st1139;
		case 100: goto st1184;
		case 110: goto st1187;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1138;
	goto st0;
st1139:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1139;
case 1139:
	if ( (*( state.p)) == 114 )
		goto st1140;
	goto st0;
st1140:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1140;
case 1140:
	if ( (*( state.p)) == 105 )
		goto st1141;
	goto st0;
st1141:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1141;
case 1141:
	if ( (*( state.p)) == 103 )
		goto st1142;
	goto st0;
st1142:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1142;
case 1142:
	if ( (*( state.p)) == 104 )
		goto st1143;
	goto st0;
st1143:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1143;
case 1143:
	if ( (*( state.p)) == 116 )
		goto st1144;
	goto st0;
st1144:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1144;
case 1144:
	switch( (*( state.p)) ) {
		case 13: goto tr1746;
		case 32: goto tr1746;
		case 95: goto tr1747;
		case 98: goto tr1748;
		case 99: goto tr1749;
		case 103: goto tr1750;
		case 109: goto tr1751;
		case 114: goto tr1752;
		case 119: goto tr1753;
		case 121: goto tr1754;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1746;
	goto st0;
tr1746:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1145;
tr1811:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1145;
st1145:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1145;
case 1145:
#line 16163 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st1145;
		case 32: goto st1145;
		case 98: goto st1146;
		case 99: goto st1153;
		case 103: goto st1157;
		case 109: goto st1162;
		case 114: goto st1169;
		case 119: goto st1172;
		case 121: goto st1177;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1145;
	goto st0;
tr1748:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1146;
tr1813:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1146;
st1146:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1146;
case 1146:
#line 16190 "configparser.h"
	if ( (*( state.p)) == 108 )
		goto st1147;
	goto st0;
st1147:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1147;
case 1147:
	switch( (*( state.p)) ) {
		case 97: goto st1148;
		case 117: goto st1151;
	}
	goto st0;
st1148:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1148;
case 1148:
	if ( (*( state.p)) == 99 )
		goto st1149;
	goto st0;
st1149:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1149;
case 1149:
	if ( (*( state.p)) == 107 )
		goto st1150;
	goto st0;
st1150:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1150;
case 1150:
	switch( (*( state.p)) ) {
		case 13: goto tr1768;
		case 32: goto tr1768;
		case 59: goto tr1769;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1768;
	goto st0;
st1151:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1151;
case 1151:
	if ( (*( state.p)) == 101 )
		goto st1152;
	goto st0;
st1152:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1152;
case 1152:
	switch( (*( state.p)) ) {
		case 13: goto tr1771;
		case 32: goto tr1771;
		case 59: goto tr1772;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1771;
	goto st0;
tr1749:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1153;
tr1814:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1153;
st1153:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1153;
case 1153:
#line 16260 "configparser.h"
	if ( (*( state.p)) == 121 )
		goto st1154;
	goto st0;
st1154:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1154;
case 1154:
	if ( (*( state.p)) == 97 )
		goto st1155;
	goto st0;
st1155:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1155;
case 1155:
	if ( (*( state.p)) == 110 )
		goto st1156;
	goto st0;
st1156:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1156;
case 1156:
	switch( (*( state.p)) ) {
		case 13: goto tr1776;
		case 32: goto tr1776;
		case 59: goto tr1777;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1776;
	goto st0;
tr1750:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1157;
tr1815:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1157;
st1157:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1157;
case 1157:
#line 16302 "configparser.h"
	if ( (*( state.p)) == 114 )
		goto st1158;
	goto st0;
st1158:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1158;
case 1158:
	if ( (*( state.p)) == 101 )
		goto st1159;
	goto st0;
st1159:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1159;
case 1159:
	if ( (*( state.p)) == 101 )
		goto st1160;
	goto st0;
st1160:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1160;
case 1160:
	if ( (*( state.p)) == 110 )
		goto st1161;
	goto st0;
st1161:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1161;
case 1161:
	switch( (*( state.p)) ) {
		case 13: goto tr1782;
		case 32: goto tr1782;
		case 59: goto tr1783;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1782;
	goto st0;
tr1751:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1162;
tr1816:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1162;
st1162:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1162;
case 1162:
#line 16351 "configparser.h"
	if ( (*( state.p)) == 97 )
		goto st1163;
	goto st0;
st1163:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1163;
case 1163:
	if ( (*( state.p)) == 103 )
		goto st1164;
	goto st0;
st1164:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1164;
case 1164:
	if ( (*( state.p)) == 101 )
		goto st1165;
	goto st0;
st1165:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1165;
case 1165:
	if ( (*( state.p)) == 110 )
		goto st1166;
	goto st0;
st1166:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1166;
case 1166:
	if ( (*( state.p)) == 116 )
		goto st1167;
	goto st0;
st1167:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1167;
case 1167:
	if ( (*( state.p)) == 97 )
		goto st1168;
	goto st0;
st1168:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1168;
case 1168:
	switch( (*( state.p)) ) {
		case 13: goto tr1790;
		case 32: goto tr1790;
		case 59: goto tr1791;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1790;
	goto st0;
tr1752:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1169;
tr1817:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1169;
st1169:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1169;
case 1169:
#line 16414 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st1170;
	goto st0;
st1170:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1170;
case 1170:
	if ( (*( state.p)) == 100 )
		goto st1171;
	goto st0;
st1171:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1171;
case 1171:
	switch( (*( state.p)) ) {
		case 13: goto tr1794;
		case 32: goto tr1794;
		case 59: goto tr1795;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1794;
	goto st0;
tr1753:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1172;
tr1818:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1172;
st1172:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1172;
case 1172:
#line 16449 "configparser.h"
	if ( (*( state.p)) == 104 )
		goto st1173;
	goto st0;
st1173:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1173;
case 1173:
	if ( (*( state.p)) == 105 )
		goto st1174;
	goto st0;
st1174:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1174;
case 1174:
	if ( (*( state.p)) == 116 )
		goto st1175;
	goto st0;
st1175:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1175;
case 1175:
	if ( (*( state.p)) == 101 )
		goto st1176;
	goto st0;
st1176:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1176;
case 1176:
	switch( (*( state.p)) ) {
		case 13: goto tr1800;
		case 32: goto tr1800;
		case 59: goto tr1801;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1800;
	goto st0;
tr1754:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1177;
tr1819:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1177;
st1177:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1177;
case 1177:
#line 16498 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st1178;
	goto st0;
st1178:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1178;
case 1178:
	if ( (*( state.p)) == 108 )
		goto st1179;
	goto st0;
st1179:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1179;
case 1179:
	if ( (*( state.p)) == 108 )
		goto st1180;
	goto st0;
st1180:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1180;
case 1180:
	if ( (*( state.p)) == 111 )
		goto st1181;
	goto st0;
st1181:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1181;
case 1181:
	if ( (*( state.p)) == 119 )
		goto st1182;
	goto st0;
st1182:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1182;
case 1182:
	switch( (*( state.p)) ) {
		case 13: goto tr1807;
		case 32: goto tr1807;
		case 59: goto tr1808;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1807;
	goto st0;
tr1747:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1183;
tr1812:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1183;
st1183:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1183;
case 1183:
#line 16554 "configparser.h"
	switch( (*( state.p)) ) {
		case 98: goto st1146;
		case 99: goto st1153;
		case 103: goto st1157;
		case 109: goto st1162;
		case 114: goto st1169;
		case 119: goto st1172;
		case 121: goto st1177;
	}
	goto st0;
st1184:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1184;
case 1184:
	if ( (*( state.p)) == 105 )
		goto st1185;
	goto st0;
st1185:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1185;
case 1185:
	if ( (*( state.p)) == 109 )
		goto st1186;
	goto st0;
st1186:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1186;
case 1186:
	switch( (*( state.p)) ) {
		case 13: goto tr1811;
		case 32: goto tr1811;
		case 95: goto tr1812;
		case 98: goto tr1813;
		case 99: goto tr1814;
		case 103: goto tr1815;
		case 109: goto tr1816;
		case 114: goto tr1817;
		case 119: goto tr1818;
		case 121: goto tr1819;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1811;
	goto st0;
st1187:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1187;
case 1187:
	if ( (*( state.p)) == 111 )
		goto st1188;
	goto st0;
st1188:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1188;
case 1188:
	if ( (*( state.p)) == 110 )
		goto st1189;
	goto st0;
st1189:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1189;
case 1189:
	if ( (*( state.p)) == 101 )
		goto st1150;
	goto st0;
st1190:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1190;
case 1190:
	if ( (*( state.p)) == 97 )
		goto st1191;
	goto st0;
st1191:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1191;
case 1191:
	switch( (*( state.p)) ) {
		case 108: goto st1192;
		case 116: goto st1249;
	}
	goto st0;
st1192:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1192;
case 1192:
	if ( (*( state.p)) == 108 )
		goto st1193;
	goto st0;
st1193:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1193;
case 1193:
	switch( (*( state.p)) ) {
		case 13: goto st1194;
		case 32: goto st1194;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1194;
	goto st0;
st1194:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1194;
case 1194:
	switch( (*( state.p)) ) {
		case 13: goto st1194;
		case 32: goto st1194;
		case 34: goto tr1827;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1194;
	goto st0;
tr1828:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st1195;
tr1827:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st1195;
tr1830:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 1195; goto st47;}}
	goto st1195;
st1195:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1195;
case 1195:
#line 16685 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st1196;
		case 92: goto tr1830;
	}
	goto tr1828;
st1196:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1196;
case 1196:
	switch( (*( state.p)) ) {
		case 13: goto tr1831;
		case 32: goto tr1831;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1831;
	goto st0;
tr1831:
#line 164 "configparser.rl"
	{ skin.text = state.match; }
	goto st1197;
st1197:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1197;
case 1197:
#line 16710 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st1197;
		case 32: goto st1197;
		case 98: goto st1198;
		case 100: goto st1243;
		case 110: goto st1246;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1197;
	goto st0;
st1198:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1198;
case 1198:
	if ( (*( state.p)) == 114 )
		goto st1199;
	goto st0;
st1199:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1199;
case 1199:
	if ( (*( state.p)) == 105 )
		goto st1200;
	goto st0;
st1200:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1200;
case 1200:
	if ( (*( state.p)) == 103 )
		goto st1201;
	goto st0;
st1201:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1201;
case 1201:
	if ( (*( state.p)) == 104 )
		goto st1202;
	goto st0;
st1202:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1202;
case 1202:
	if ( (*( state.p)) == 116 )
		goto st1203;
	goto st0;
st1203:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1203;
case 1203:
	switch( (*( state.p)) ) {
		case 13: goto tr1841;
		case 32: goto tr1841;
		case 95: goto tr1842;
		case 98: goto tr1843;
		case 99: goto tr1844;
		case 103: goto tr1845;
		case 109: goto tr1846;
		case 114: goto tr1847;
		case 119: goto tr1848;
		case 121: goto tr1849;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1841;
	goto st0;
tr1841:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1204;
tr1906:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1204;
st1204:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1204;
case 1204:
#line 16787 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st1204;
		case 32: goto st1204;
		case 98: goto st1205;
		case 99: goto st1212;
		case 103: goto st1216;
		case 109: goto st1221;
		case 114: goto st1228;
		case 119: goto st1231;
		case 121: goto st1236;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1204;
	goto st0;
tr1843:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1205;
tr1908:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1205;
st1205:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1205;
case 1205:
#line 16814 "configparser.h"
	if ( (*( state.p)) == 108 )
		goto st1206;
	goto st0;
st1206:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1206;
case 1206:
	switch( (*( state.p)) ) {
		case 97: goto st1207;
		case 117: goto st1210;
	}
	goto st0;
st1207:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1207;
case 1207:
	if ( (*( state.p)) == 99 )
		goto st1208;
	goto st0;
st1208:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1208;
case 1208:
	if ( (*( state.p)) == 107 )
		goto st1209;
	goto st0;
st1209:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1209;
case 1209:
	switch( (*( state.p)) ) {
		case 13: goto tr1863;
		case 32: goto tr1863;
		case 59: goto tr1864;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1863;
	goto st0;
st1210:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1210;
case 1210:
	if ( (*( state.p)) == 101 )
		goto st1211;
	goto st0;
st1211:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1211;
case 1211:
	switch( (*( state.p)) ) {
		case 13: goto tr1866;
		case 32: goto tr1866;
		case 59: goto tr1867;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1866;
	goto st0;
tr1844:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1212;
tr1909:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1212;
st1212:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1212;
case 1212:
#line 16884 "configparser.h"
	if ( (*( state.p)) == 121 )
		goto st1213;
	goto st0;
st1213:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1213;
case 1213:
	if ( (*( state.p)) == 97 )
		goto st1214;
	goto st0;
st1214:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1214;
case 1214:
	if ( (*( state.p)) == 110 )
		goto st1215;
	goto st0;
st1215:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1215;
case 1215:
	switch( (*( state.p)) ) {
		case 13: goto tr1871;
		case 32: goto tr1871;
		case 59: goto tr1872;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1871;
	goto st0;
tr1845:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1216;
tr1910:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1216;
st1216:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1216;
case 1216:
#line 16926 "configparser.h"
	if ( (*( state.p)) == 114 )
		goto st1217;
	goto st0;
st1217:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1217;
case 1217:
	if ( (*( state.p)) == 101 )
		goto st1218;
	goto st0;
st1218:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1218;
case 1218:
	if ( (*( state.p)) == 101 )
		goto st1219;
	goto st0;
st1219:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1219;
case 1219:
	if ( (*( state.p)) == 110 )
		goto st1220;
	goto st0;
st1220:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1220;
case 1220:
	switch( (*( state.p)) ) {
		case 13: goto tr1877;
		case 32: goto tr1877;
		case 59: goto tr1878;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1877;
	goto st0;
tr1846:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1221;
tr1911:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1221;
st1221:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1221;
case 1221:
#line 16975 "configparser.h"
	if ( (*( state.p)) == 97 )
		goto st1222;
	goto st0;
st1222:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1222;
case 1222:
	if ( (*( state.p)) == 103 )
		goto st1223;
	goto st0;
st1223:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1223;
case 1223:
	if ( (*( state.p)) == 101 )
		goto st1224;
	goto st0;
st1224:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1224;
case 1224:
	if ( (*( state.p)) == 110 )
		goto st1225;
	goto st0;
st1225:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1225;
case 1225:
	if ( (*( state.p)) == 116 )
		goto st1226;
	goto st0;
st1226:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1226;
case 1226:
	if ( (*( state.p)) == 97 )
		goto st1227;
	goto st0;
st1227:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1227;
case 1227:
	switch( (*( state.p)) ) {
		case 13: goto tr1885;
		case 32: goto tr1885;
		case 59: goto tr1886;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1885;
	goto st0;
tr1847:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1228;
tr1912:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1228;
st1228:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1228;
case 1228:
#line 17038 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st1229;
	goto st0;
st1229:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1229;
case 1229:
	if ( (*( state.p)) == 100 )
		goto st1230;
	goto st0;
st1230:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1230;
case 1230:
	switch( (*( state.p)) ) {
		case 13: goto tr1889;
		case 32: goto tr1889;
		case 59: goto tr1890;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1889;
	goto st0;
tr1848:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1231;
tr1913:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1231;
st1231:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1231;
case 1231:
#line 17073 "configparser.h"
	if ( (*( state.p)) == 104 )
		goto st1232;
	goto st0;
st1232:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1232;
case 1232:
	if ( (*( state.p)) == 105 )
		goto st1233;
	goto st0;
st1233:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1233;
case 1233:
	if ( (*( state.p)) == 116 )
		goto st1234;
	goto st0;
st1234:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1234;
case 1234:
	if ( (*( state.p)) == 101 )
		goto st1235;
	goto st0;
st1235:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1235;
case 1235:
	switch( (*( state.p)) ) {
		case 13: goto tr1895;
		case 32: goto tr1895;
		case 59: goto tr1896;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1895;
	goto st0;
tr1849:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1236;
tr1914:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1236;
st1236:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1236;
case 1236:
#line 17122 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st1237;
	goto st0;
st1237:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1237;
case 1237:
	if ( (*( state.p)) == 108 )
		goto st1238;
	goto st0;
st1238:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1238;
case 1238:
	if ( (*( state.p)) == 108 )
		goto st1239;
	goto st0;
st1239:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1239;
case 1239:
	if ( (*( state.p)) == 111 )
		goto st1240;
	goto st0;
st1240:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1240;
case 1240:
	if ( (*( state.p)) == 119 )
		goto st1241;
	goto st0;
st1241:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1241;
case 1241:
	switch( (*( state.p)) ) {
		case 13: goto tr1902;
		case 32: goto tr1902;
		case 59: goto tr1903;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1902;
	goto st0;
tr1842:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1242;
tr1907:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1242;
st1242:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1242;
case 1242:
#line 17178 "configparser.h"
	switch( (*( state.p)) ) {
		case 98: goto st1205;
		case 99: goto st1212;
		case 103: goto st1216;
		case 109: goto st1221;
		case 114: goto st1228;
		case 119: goto st1231;
		case 121: goto st1236;
	}
	goto st0;
st1243:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1243;
case 1243:
	if ( (*( state.p)) == 105 )
		goto st1244;
	goto st0;
st1244:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1244;
case 1244:
	if ( (*( state.p)) == 109 )
		goto st1245;
	goto st0;
st1245:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1245;
case 1245:
	switch( (*( state.p)) ) {
		case 13: goto tr1906;
		case 32: goto tr1906;
		case 95: goto tr1907;
		case 98: goto tr1908;
		case 99: goto tr1909;
		case 103: goto tr1910;
		case 109: goto tr1911;
		case 114: goto tr1912;
		case 119: goto tr1913;
		case 121: goto tr1914;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1906;
	goto st0;
st1246:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1246;
case 1246:
	if ( (*( state.p)) == 111 )
		goto st1247;
	goto st0;
st1247:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1247;
case 1247:
	if ( (*( state.p)) == 110 )
		goto st1248;
	goto st0;
st1248:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1248;
case 1248:
	if ( (*( state.p)) == 101 )
		goto st1209;
	goto st0;
st1249:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1249;
case 1249:
	if ( (*( state.p)) == 101 )
		goto st1250;
	goto st0;
st1250:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1250;
case 1250:
	if ( (*( state.p)) == 114 )
		goto st1251;
	goto st0;
st1251:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1251;
case 1251:
	if ( (*( state.p)) == 95 )
		goto st1252;
	goto st0;
st1252:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1252;
case 1252:
	if ( (*( state.p)) == 119 )
		goto st1253;
	goto st0;
st1253:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1253;
case 1253:
	if ( (*( state.p)) == 97 )
		goto st1254;
	goto st0;
st1254:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1254;
case 1254:
	if ( (*( state.p)) == 108 )
		goto st1255;
	goto st0;
st1255:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1255;
case 1255:
	if ( (*( state.p)) == 108 )
		goto st1256;
	goto st0;
st1256:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1256;
case 1256:
	switch( (*( state.p)) ) {
		case 13: goto st1257;
		case 32: goto st1257;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1257;
	goto st0;
st1257:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1257;
case 1257:
	switch( (*( state.p)) ) {
		case 13: goto st1257;
		case 32: goto st1257;
		case 34: goto tr1925;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1257;
	goto st0;
tr1926:
#line 111 "configparser.rl"
	{
            state.match += (*( state.p));
        }
	goto st1258;
tr1925:
#line 107 "configparser.rl"
	{
            state.match.clear();
        }
	goto st1258;
tr1928:
#line 142 "configparser.rl"
	{{ state.stack[ state.top++] = 1258; goto st47;}}
	goto st1258;
st1258:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1258;
case 1258:
#line 17335 "configparser.h"
	switch( (*( state.p)) ) {
		case 34: goto st1259;
		case 92: goto tr1928;
	}
	goto tr1926;
st1259:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1259;
case 1259:
	switch( (*( state.p)) ) {
		case 13: goto tr1929;
		case 32: goto tr1929;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1929;
	goto st0;
tr1929:
#line 164 "configparser.rl"
	{ skin.text = state.match; }
	goto st1260;
st1260:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1260;
case 1260:
#line 17360 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st1260;
		case 32: goto st1260;
		case 98: goto st1261;
		case 100: goto st1306;
		case 110: goto st1309;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1260;
	goto st0;
st1261:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1261;
case 1261:
	if ( (*( state.p)) == 114 )
		goto st1262;
	goto st0;
st1262:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1262;
case 1262:
	if ( (*( state.p)) == 105 )
		goto st1263;
	goto st0;
st1263:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1263;
case 1263:
	if ( (*( state.p)) == 103 )
		goto st1264;
	goto st0;
st1264:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1264;
case 1264:
	if ( (*( state.p)) == 104 )
		goto st1265;
	goto st0;
st1265:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1265;
case 1265:
	if ( (*( state.p)) == 116 )
		goto st1266;
	goto st0;
st1266:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1266;
case 1266:
	switch( (*( state.p)) ) {
		case 13: goto tr1939;
		case 32: goto tr1939;
		case 95: goto tr1940;
		case 98: goto tr1941;
		case 99: goto tr1942;
		case 103: goto tr1943;
		case 109: goto tr1944;
		case 114: goto tr1945;
		case 119: goto tr1946;
		case 121: goto tr1947;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1939;
	goto st0;
tr1939:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1267;
tr2004:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1267;
st1267:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1267;
case 1267:
#line 17437 "configparser.h"
	switch( (*( state.p)) ) {
		case 13: goto st1267;
		case 32: goto st1267;
		case 98: goto st1268;
		case 99: goto st1275;
		case 103: goto st1279;
		case 109: goto st1284;
		case 114: goto st1291;
		case 119: goto st1294;
		case 121: goto st1299;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto st1267;
	goto st0;
tr1941:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1268;
tr2006:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1268;
st1268:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1268;
case 1268:
#line 17464 "configparser.h"
	if ( (*( state.p)) == 108 )
		goto st1269;
	goto st0;
st1269:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1269;
case 1269:
	switch( (*( state.p)) ) {
		case 97: goto st1270;
		case 117: goto st1273;
	}
	goto st0;
st1270:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1270;
case 1270:
	if ( (*( state.p)) == 99 )
		goto st1271;
	goto st0;
st1271:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1271;
case 1271:
	if ( (*( state.p)) == 107 )
		goto st1272;
	goto st0;
st1272:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1272;
case 1272:
	switch( (*( state.p)) ) {
		case 13: goto tr1961;
		case 32: goto tr1961;
		case 59: goto tr1962;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1961;
	goto st0;
st1273:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1273;
case 1273:
	if ( (*( state.p)) == 101 )
		goto st1274;
	goto st0;
st1274:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1274;
case 1274:
	switch( (*( state.p)) ) {
		case 13: goto tr1964;
		case 32: goto tr1964;
		case 59: goto tr1965;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1964;
	goto st0;
tr1942:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1275;
tr2007:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1275;
st1275:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1275;
case 1275:
#line 17534 "configparser.h"
	if ( (*( state.p)) == 121 )
		goto st1276;
	goto st0;
st1276:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1276;
case 1276:
	if ( (*( state.p)) == 97 )
		goto st1277;
	goto st0;
st1277:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1277;
case 1277:
	if ( (*( state.p)) == 110 )
		goto st1278;
	goto st0;
st1278:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1278;
case 1278:
	switch( (*( state.p)) ) {
		case 13: goto tr1969;
		case 32: goto tr1969;
		case 59: goto tr1970;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1969;
	goto st0;
tr1943:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1279;
tr2008:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1279;
st1279:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1279;
case 1279:
#line 17576 "configparser.h"
	if ( (*( state.p)) == 114 )
		goto st1280;
	goto st0;
st1280:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1280;
case 1280:
	if ( (*( state.p)) == 101 )
		goto st1281;
	goto st0;
st1281:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1281;
case 1281:
	if ( (*( state.p)) == 101 )
		goto st1282;
	goto st0;
st1282:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1282;
case 1282:
	if ( (*( state.p)) == 110 )
		goto st1283;
	goto st0;
st1283:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1283;
case 1283:
	switch( (*( state.p)) ) {
		case 13: goto tr1975;
		case 32: goto tr1975;
		case 59: goto tr1976;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1975;
	goto st0;
tr1944:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1284;
tr2009:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1284;
st1284:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1284;
case 1284:
#line 17625 "configparser.h"
	if ( (*( state.p)) == 97 )
		goto st1285;
	goto st0;
st1285:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1285;
case 1285:
	if ( (*( state.p)) == 103 )
		goto st1286;
	goto st0;
st1286:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1286;
case 1286:
	if ( (*( state.p)) == 101 )
		goto st1287;
	goto st0;
st1287:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1287;
case 1287:
	if ( (*( state.p)) == 110 )
		goto st1288;
	goto st0;
st1288:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1288;
case 1288:
	if ( (*( state.p)) == 116 )
		goto st1289;
	goto st0;
st1289:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1289;
case 1289:
	if ( (*( state.p)) == 97 )
		goto st1290;
	goto st0;
st1290:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1290;
case 1290:
	switch( (*( state.p)) ) {
		case 13: goto tr1983;
		case 32: goto tr1983;
		case 59: goto tr1984;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1983;
	goto st0;
tr1945:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1291;
tr2010:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1291;
st1291:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1291;
case 1291:
#line 17688 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st1292;
	goto st0;
st1292:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1292;
case 1292:
	if ( (*( state.p)) == 100 )
		goto st1293;
	goto st0;
st1293:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1293;
case 1293:
	switch( (*( state.p)) ) {
		case 13: goto tr1987;
		case 32: goto tr1987;
		case 59: goto tr1988;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1987;
	goto st0;
tr1946:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1294;
tr2011:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1294;
st1294:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1294;
case 1294:
#line 17723 "configparser.h"
	if ( (*( state.p)) == 104 )
		goto st1295;
	goto st0;
st1295:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1295;
case 1295:
	if ( (*( state.p)) == 105 )
		goto st1296;
	goto st0;
st1296:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1296;
case 1296:
	if ( (*( state.p)) == 116 )
		goto st1297;
	goto st0;
st1297:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1297;
case 1297:
	if ( (*( state.p)) == 101 )
		goto st1298;
	goto st0;
st1298:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1298;
case 1298:
	switch( (*( state.p)) ) {
		case 13: goto tr1993;
		case 32: goto tr1993;
		case 59: goto tr1994;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr1993;
	goto st0;
tr1947:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1299;
tr2012:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1299;
st1299:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1299;
case 1299:
#line 17772 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st1300;
	goto st0;
st1300:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1300;
case 1300:
	if ( (*( state.p)) == 108 )
		goto st1301;
	goto st0;
st1301:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1301;
case 1301:
	if ( (*( state.p)) == 108 )
		goto st1302;
	goto st0;
st1302:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1302;
case 1302:
	if ( (*( state.p)) == 111 )
		goto st1303;
	goto st0;
st1303:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1303;
case 1303:
	if ( (*( state.p)) == 119 )
		goto st1304;
	goto st0;
st1304:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1304;
case 1304:
	switch( (*( state.p)) ) {
		case 13: goto tr2000;
		case 32: goto tr2000;
		case 59: goto tr2001;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr2000;
	goto st0;
tr1940:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1305;
tr2005:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1305;
st1305:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1305;
case 1305:
#line 17828 "configparser.h"
	switch( (*( state.p)) ) {
		case 98: goto st1268;
		case 99: goto st1275;
		case 103: goto st1279;
		case 109: goto st1284;
		case 114: goto st1291;
		case 119: goto st1294;
		case 121: goto st1299;
	}
	goto st0;
st1306:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1306;
case 1306:
	if ( (*( state.p)) == 105 )
		goto st1307;
	goto st0;
st1307:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1307;
case 1307:
	if ( (*( state.p)) == 109 )
		goto st1308;
	goto st0;
st1308:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1308;
case 1308:
	switch( (*( state.p)) ) {
		case 13: goto tr2004;
		case 32: goto tr2004;
		case 95: goto tr2005;
		case 98: goto tr2006;
		case 99: goto tr2007;
		case 103: goto tr2008;
		case 109: goto tr2009;
		case 114: goto tr2010;
		case 119: goto tr2011;
		case 121: goto tr2012;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr2004;
	goto st0;
st1309:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1309;
case 1309:
	if ( (*( state.p)) == 111 )
		goto st1310;
	goto st0;
st1310:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1310;
case 1310:
	if ( (*( state.p)) == 110 )
		goto st1311;
	goto st0;
st1311:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1311;
case 1311:
	if ( (*( state.p)) == 101 )
		goto st1272;
	goto st0;
st1312:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1312;
case 1312:
	if ( (*( state.p)) == 101 )
		goto st1313;
	goto st0;
st1313:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1313;
case 1313:
	switch( (*( state.p)) ) {
		case 13: goto tr2016;
		case 32: goto tr2016;
		case 59: goto tr2017;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr2016;
	goto st0;
tr941:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1314;
tr2059:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1314;
st1314:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1314;
case 1314:
#line 17924 "configparser.h"
	if ( (*( state.p)) == 121 )
		goto st1315;
	goto st0;
st1315:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1315;
case 1315:
	if ( (*( state.p)) == 97 )
		goto st1316;
	goto st0;
st1316:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1316;
case 1316:
	if ( (*( state.p)) == 110 )
		goto st1317;
	goto st0;
st1317:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1317;
case 1317:
	switch( (*( state.p)) ) {
		case 13: goto tr2021;
		case 32: goto tr2021;
		case 59: goto tr2022;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr2021;
	goto st0;
tr942:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1318;
tr2060:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1318;
st1318:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1318;
case 1318:
#line 17966 "configparser.h"
	if ( (*( state.p)) == 114 )
		goto st1319;
	goto st0;
st1319:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1319;
case 1319:
	if ( (*( state.p)) == 101 )
		goto st1320;
	goto st0;
st1320:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1320;
case 1320:
	if ( (*( state.p)) == 101 )
		goto st1321;
	goto st0;
st1321:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1321;
case 1321:
	if ( (*( state.p)) == 110 )
		goto st1322;
	goto st0;
st1322:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1322;
case 1322:
	switch( (*( state.p)) ) {
		case 13: goto tr2027;
		case 32: goto tr2027;
		case 59: goto tr2028;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr2027;
	goto st0;
tr943:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1323;
tr2061:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1323;
st1323:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1323;
case 1323:
#line 18015 "configparser.h"
	if ( (*( state.p)) == 97 )
		goto st1324;
	goto st0;
st1324:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1324;
case 1324:
	if ( (*( state.p)) == 103 )
		goto st1325;
	goto st0;
st1325:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1325;
case 1325:
	if ( (*( state.p)) == 101 )
		goto st1326;
	goto st0;
st1326:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1326;
case 1326:
	if ( (*( state.p)) == 110 )
		goto st1327;
	goto st0;
st1327:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1327;
case 1327:
	if ( (*( state.p)) == 116 )
		goto st1328;
	goto st0;
st1328:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1328;
case 1328:
	if ( (*( state.p)) == 97 )
		goto st1329;
	goto st0;
st1329:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1329;
case 1329:
	switch( (*( state.p)) ) {
		case 13: goto tr2035;
		case 32: goto tr2035;
		case 59: goto tr2036;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr2035;
	goto st0;
tr944:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1330;
tr2062:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1330;
st1330:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1330;
case 1330:
#line 18078 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st1331;
	goto st0;
st1331:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1331;
case 1331:
	if ( (*( state.p)) == 100 )
		goto st1332;
	goto st0;
st1332:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1332;
case 1332:
	switch( (*( state.p)) ) {
		case 13: goto tr2039;
		case 32: goto tr2039;
		case 59: goto tr2040;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr2039;
	goto st0;
tr945:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1333;
tr2063:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1333;
st1333:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1333;
case 1333:
#line 18113 "configparser.h"
	if ( (*( state.p)) == 104 )
		goto st1334;
	goto st0;
st1334:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1334;
case 1334:
	if ( (*( state.p)) == 105 )
		goto st1335;
	goto st0;
st1335:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1335;
case 1335:
	if ( (*( state.p)) == 116 )
		goto st1336;
	goto st0;
st1336:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1336;
case 1336:
	if ( (*( state.p)) == 101 )
		goto st1337;
	goto st0;
st1337:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1337;
case 1337:
	switch( (*( state.p)) ) {
		case 13: goto tr2045;
		case 32: goto tr2045;
		case 59: goto tr2046;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr2045;
	goto st0;
tr946:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1338;
tr2064:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1338;
st1338:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1338;
case 1338:
#line 18162 "configparser.h"
	if ( (*( state.p)) == 101 )
		goto st1339;
	goto st0;
st1339:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1339;
case 1339:
	if ( (*( state.p)) == 108 )
		goto st1340;
	goto st0;
st1340:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1340;
case 1340:
	if ( (*( state.p)) == 108 )
		goto st1341;
	goto st0;
st1341:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1341;
case 1341:
	if ( (*( state.p)) == 111 )
		goto st1342;
	goto st0;
st1342:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1342;
case 1342:
	if ( (*( state.p)) == 119 )
		goto st1343;
	goto st0;
st1343:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1343;
case 1343:
	switch( (*( state.p)) ) {
		case 13: goto tr2052;
		case 32: goto tr2052;
		case 59: goto tr2053;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr2052;
	goto st0;
tr939:
#line 162 "configparser.rl"
	{ skin.fore = maudit::color::bright_black; }
	goto st1344;
tr2057:
#line 161 "configparser.rl"
	{ skin.fore = maudit::color::dim_black; }
	goto st1344;
st1344:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1344;
case 1344:
#line 18218 "configparser.h"
	switch( (*( state.p)) ) {
		case 98: goto st650;
		case 99: goto st1314;
		case 103: goto st1318;
		case 109: goto st1323;
		case 114: goto st1330;
		case 119: goto st1333;
		case 121: goto st1338;
	}
	goto st0;
st1345:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1345;
case 1345:
	if ( (*( state.p)) == 105 )
		goto st1346;
	goto st0;
st1346:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1346;
case 1346:
	if ( (*( state.p)) == 109 )
		goto st1347;
	goto st0;
st1347:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1347;
case 1347:
	switch( (*( state.p)) ) {
		case 13: goto tr2056;
		case 32: goto tr2056;
		case 95: goto tr2057;
		case 98: goto tr2058;
		case 99: goto tr2059;
		case 103: goto tr2060;
		case 109: goto tr2061;
		case 114: goto tr2062;
		case 119: goto tr2063;
		case 121: goto tr2064;
	}
	if ( 9 <= (*( state.p)) && (*( state.p)) <= 10 )
		goto tr2056;
	goto st0;
st1348:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1348;
case 1348:
	if ( (*( state.p)) == 111 )
		goto st1349;
	goto st0;
st1349:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1349;
case 1349:
	if ( (*( state.p)) == 110 )
		goto st1350;
	goto st0;
st1350:
	if ( ++( state.p) == ( state.pe) )
		goto _test_eof1350;
case 1350:
	if ( (*( state.p)) == 101 )
		goto st654;
	goto st0;
	}
	_test_eof1:  state.cs = 1; goto _test_eof; 
	_test_eof2:  state.cs = 2; goto _test_eof; 
	_test_eof3:  state.cs = 3; goto _test_eof; 
	_test_eof4:  state.cs = 4; goto _test_eof; 
	_test_eof5:  state.cs = 5; goto _test_eof; 
	_test_eof6:  state.cs = 6; goto _test_eof; 
	_test_eof7:  state.cs = 7; goto _test_eof; 
	_test_eof8:  state.cs = 8; goto _test_eof; 
	_test_eof9:  state.cs = 9; goto _test_eof; 
	_test_eof10:  state.cs = 10; goto _test_eof; 
	_test_eof11:  state.cs = 11; goto _test_eof; 
	_test_eof12:  state.cs = 12; goto _test_eof; 
	_test_eof1351:  state.cs = 1351; goto _test_eof; 
	_test_eof1352:  state.cs = 1352; goto _test_eof; 
	_test_eof13:  state.cs = 13; goto _test_eof; 
	_test_eof14:  state.cs = 14; goto _test_eof; 
	_test_eof15:  state.cs = 15; goto _test_eof; 
	_test_eof16:  state.cs = 16; goto _test_eof; 
	_test_eof17:  state.cs = 17; goto _test_eof; 
	_test_eof18:  state.cs = 18; goto _test_eof; 
	_test_eof19:  state.cs = 19; goto _test_eof; 
	_test_eof20:  state.cs = 20; goto _test_eof; 
	_test_eof21:  state.cs = 21; goto _test_eof; 
	_test_eof22:  state.cs = 22; goto _test_eof; 
	_test_eof23:  state.cs = 23; goto _test_eof; 
	_test_eof24:  state.cs = 24; goto _test_eof; 
	_test_eof1353:  state.cs = 1353; goto _test_eof; 
	_test_eof25:  state.cs = 25; goto _test_eof; 
	_test_eof26:  state.cs = 26; goto _test_eof; 
	_test_eof27:  state.cs = 27; goto _test_eof; 
	_test_eof28:  state.cs = 28; goto _test_eof; 
	_test_eof29:  state.cs = 29; goto _test_eof; 
	_test_eof30:  state.cs = 30; goto _test_eof; 
	_test_eof31:  state.cs = 31; goto _test_eof; 
	_test_eof32:  state.cs = 32; goto _test_eof; 
	_test_eof33:  state.cs = 33; goto _test_eof; 
	_test_eof34:  state.cs = 34; goto _test_eof; 
	_test_eof35:  state.cs = 35; goto _test_eof; 
	_test_eof36:  state.cs = 36; goto _test_eof; 
	_test_eof1354:  state.cs = 1354; goto _test_eof; 
	_test_eof37:  state.cs = 37; goto _test_eof; 
	_test_eof38:  state.cs = 38; goto _test_eof; 
	_test_eof39:  state.cs = 39; goto _test_eof; 
	_test_eof40:  state.cs = 40; goto _test_eof; 
	_test_eof41:  state.cs = 41; goto _test_eof; 
	_test_eof42:  state.cs = 42; goto _test_eof; 
	_test_eof43:  state.cs = 43; goto _test_eof; 
	_test_eof44:  state.cs = 44; goto _test_eof; 
	_test_eof45:  state.cs = 45; goto _test_eof; 
	_test_eof46:  state.cs = 46; goto _test_eof; 
	_test_eof1355:  state.cs = 1355; goto _test_eof; 
	_test_eof47:  state.cs = 47; goto _test_eof; 
	_test_eof1356:  state.cs = 1356; goto _test_eof; 
	_test_eof48:  state.cs = 48; goto _test_eof; 
	_test_eof49:  state.cs = 49; goto _test_eof; 
	_test_eof50:  state.cs = 50; goto _test_eof; 
	_test_eof51:  state.cs = 51; goto _test_eof; 
	_test_eof52:  state.cs = 52; goto _test_eof; 
	_test_eof53:  state.cs = 53; goto _test_eof; 
	_test_eof54:  state.cs = 54; goto _test_eof; 
	_test_eof55:  state.cs = 55; goto _test_eof; 
	_test_eof56:  state.cs = 56; goto _test_eof; 
	_test_eof57:  state.cs = 57; goto _test_eof; 
	_test_eof58:  state.cs = 58; goto _test_eof; 
	_test_eof59:  state.cs = 59; goto _test_eof; 
	_test_eof60:  state.cs = 60; goto _test_eof; 
	_test_eof61:  state.cs = 61; goto _test_eof; 
	_test_eof62:  state.cs = 62; goto _test_eof; 
	_test_eof63:  state.cs = 63; goto _test_eof; 
	_test_eof64:  state.cs = 64; goto _test_eof; 
	_test_eof65:  state.cs = 65; goto _test_eof; 
	_test_eof66:  state.cs = 66; goto _test_eof; 
	_test_eof1357:  state.cs = 1357; goto _test_eof; 
	_test_eof67:  state.cs = 67; goto _test_eof; 
	_test_eof68:  state.cs = 68; goto _test_eof; 
	_test_eof69:  state.cs = 69; goto _test_eof; 
	_test_eof70:  state.cs = 70; goto _test_eof; 
	_test_eof71:  state.cs = 71; goto _test_eof; 
	_test_eof72:  state.cs = 72; goto _test_eof; 
	_test_eof73:  state.cs = 73; goto _test_eof; 
	_test_eof74:  state.cs = 74; goto _test_eof; 
	_test_eof75:  state.cs = 75; goto _test_eof; 
	_test_eof76:  state.cs = 76; goto _test_eof; 
	_test_eof77:  state.cs = 77; goto _test_eof; 
	_test_eof78:  state.cs = 78; goto _test_eof; 
	_test_eof79:  state.cs = 79; goto _test_eof; 
	_test_eof80:  state.cs = 80; goto _test_eof; 
	_test_eof81:  state.cs = 81; goto _test_eof; 
	_test_eof82:  state.cs = 82; goto _test_eof; 
	_test_eof83:  state.cs = 83; goto _test_eof; 
	_test_eof84:  state.cs = 84; goto _test_eof; 
	_test_eof85:  state.cs = 85; goto _test_eof; 
	_test_eof86:  state.cs = 86; goto _test_eof; 
	_test_eof87:  state.cs = 87; goto _test_eof; 
	_test_eof88:  state.cs = 88; goto _test_eof; 
	_test_eof89:  state.cs = 89; goto _test_eof; 
	_test_eof90:  state.cs = 90; goto _test_eof; 
	_test_eof91:  state.cs = 91; goto _test_eof; 
	_test_eof92:  state.cs = 92; goto _test_eof; 
	_test_eof93:  state.cs = 93; goto _test_eof; 
	_test_eof94:  state.cs = 94; goto _test_eof; 
	_test_eof95:  state.cs = 95; goto _test_eof; 
	_test_eof96:  state.cs = 96; goto _test_eof; 
	_test_eof97:  state.cs = 97; goto _test_eof; 
	_test_eof98:  state.cs = 98; goto _test_eof; 
	_test_eof99:  state.cs = 99; goto _test_eof; 
	_test_eof100:  state.cs = 100; goto _test_eof; 
	_test_eof101:  state.cs = 101; goto _test_eof; 
	_test_eof102:  state.cs = 102; goto _test_eof; 
	_test_eof103:  state.cs = 103; goto _test_eof; 
	_test_eof104:  state.cs = 104; goto _test_eof; 
	_test_eof105:  state.cs = 105; goto _test_eof; 
	_test_eof106:  state.cs = 106; goto _test_eof; 
	_test_eof107:  state.cs = 107; goto _test_eof; 
	_test_eof108:  state.cs = 108; goto _test_eof; 
	_test_eof109:  state.cs = 109; goto _test_eof; 
	_test_eof110:  state.cs = 110; goto _test_eof; 
	_test_eof111:  state.cs = 111; goto _test_eof; 
	_test_eof112:  state.cs = 112; goto _test_eof; 
	_test_eof113:  state.cs = 113; goto _test_eof; 
	_test_eof114:  state.cs = 114; goto _test_eof; 
	_test_eof115:  state.cs = 115; goto _test_eof; 
	_test_eof116:  state.cs = 116; goto _test_eof; 
	_test_eof117:  state.cs = 117; goto _test_eof; 
	_test_eof118:  state.cs = 118; goto _test_eof; 
	_test_eof119:  state.cs = 119; goto _test_eof; 
	_test_eof120:  state.cs = 120; goto _test_eof; 
	_test_eof121:  state.cs = 121; goto _test_eof; 
	_test_eof122:  state.cs = 122; goto _test_eof; 
	_test_eof123:  state.cs = 123; goto _test_eof; 
	_test_eof124:  state.cs = 124; goto _test_eof; 
	_test_eof125:  state.cs = 125; goto _test_eof; 
	_test_eof126:  state.cs = 126; goto _test_eof; 
	_test_eof127:  state.cs = 127; goto _test_eof; 
	_test_eof128:  state.cs = 128; goto _test_eof; 
	_test_eof129:  state.cs = 129; goto _test_eof; 
	_test_eof130:  state.cs = 130; goto _test_eof; 
	_test_eof131:  state.cs = 131; goto _test_eof; 
	_test_eof132:  state.cs = 132; goto _test_eof; 
	_test_eof133:  state.cs = 133; goto _test_eof; 
	_test_eof134:  state.cs = 134; goto _test_eof; 
	_test_eof135:  state.cs = 135; goto _test_eof; 
	_test_eof136:  state.cs = 136; goto _test_eof; 
	_test_eof137:  state.cs = 137; goto _test_eof; 
	_test_eof138:  state.cs = 138; goto _test_eof; 
	_test_eof139:  state.cs = 139; goto _test_eof; 
	_test_eof140:  state.cs = 140; goto _test_eof; 
	_test_eof141:  state.cs = 141; goto _test_eof; 
	_test_eof142:  state.cs = 142; goto _test_eof; 
	_test_eof143:  state.cs = 143; goto _test_eof; 
	_test_eof144:  state.cs = 144; goto _test_eof; 
	_test_eof145:  state.cs = 145; goto _test_eof; 
	_test_eof146:  state.cs = 146; goto _test_eof; 
	_test_eof147:  state.cs = 147; goto _test_eof; 
	_test_eof148:  state.cs = 148; goto _test_eof; 
	_test_eof149:  state.cs = 149; goto _test_eof; 
	_test_eof150:  state.cs = 150; goto _test_eof; 
	_test_eof151:  state.cs = 151; goto _test_eof; 
	_test_eof152:  state.cs = 152; goto _test_eof; 
	_test_eof153:  state.cs = 153; goto _test_eof; 
	_test_eof154:  state.cs = 154; goto _test_eof; 
	_test_eof155:  state.cs = 155; goto _test_eof; 
	_test_eof156:  state.cs = 156; goto _test_eof; 
	_test_eof157:  state.cs = 157; goto _test_eof; 
	_test_eof158:  state.cs = 158; goto _test_eof; 
	_test_eof159:  state.cs = 159; goto _test_eof; 
	_test_eof160:  state.cs = 160; goto _test_eof; 
	_test_eof161:  state.cs = 161; goto _test_eof; 
	_test_eof162:  state.cs = 162; goto _test_eof; 
	_test_eof163:  state.cs = 163; goto _test_eof; 
	_test_eof164:  state.cs = 164; goto _test_eof; 
	_test_eof165:  state.cs = 165; goto _test_eof; 
	_test_eof166:  state.cs = 166; goto _test_eof; 
	_test_eof167:  state.cs = 167; goto _test_eof; 
	_test_eof168:  state.cs = 168; goto _test_eof; 
	_test_eof169:  state.cs = 169; goto _test_eof; 
	_test_eof170:  state.cs = 170; goto _test_eof; 
	_test_eof171:  state.cs = 171; goto _test_eof; 
	_test_eof172:  state.cs = 172; goto _test_eof; 
	_test_eof173:  state.cs = 173; goto _test_eof; 
	_test_eof174:  state.cs = 174; goto _test_eof; 
	_test_eof175:  state.cs = 175; goto _test_eof; 
	_test_eof176:  state.cs = 176; goto _test_eof; 
	_test_eof177:  state.cs = 177; goto _test_eof; 
	_test_eof178:  state.cs = 178; goto _test_eof; 
	_test_eof179:  state.cs = 179; goto _test_eof; 
	_test_eof180:  state.cs = 180; goto _test_eof; 
	_test_eof181:  state.cs = 181; goto _test_eof; 
	_test_eof182:  state.cs = 182; goto _test_eof; 
	_test_eof183:  state.cs = 183; goto _test_eof; 
	_test_eof184:  state.cs = 184; goto _test_eof; 
	_test_eof185:  state.cs = 185; goto _test_eof; 
	_test_eof186:  state.cs = 186; goto _test_eof; 
	_test_eof187:  state.cs = 187; goto _test_eof; 
	_test_eof188:  state.cs = 188; goto _test_eof; 
	_test_eof189:  state.cs = 189; goto _test_eof; 
	_test_eof190:  state.cs = 190; goto _test_eof; 
	_test_eof191:  state.cs = 191; goto _test_eof; 
	_test_eof192:  state.cs = 192; goto _test_eof; 
	_test_eof193:  state.cs = 193; goto _test_eof; 
	_test_eof194:  state.cs = 194; goto _test_eof; 
	_test_eof195:  state.cs = 195; goto _test_eof; 
	_test_eof196:  state.cs = 196; goto _test_eof; 
	_test_eof197:  state.cs = 197; goto _test_eof; 
	_test_eof198:  state.cs = 198; goto _test_eof; 
	_test_eof199:  state.cs = 199; goto _test_eof; 
	_test_eof200:  state.cs = 200; goto _test_eof; 
	_test_eof201:  state.cs = 201; goto _test_eof; 
	_test_eof202:  state.cs = 202; goto _test_eof; 
	_test_eof203:  state.cs = 203; goto _test_eof; 
	_test_eof204:  state.cs = 204; goto _test_eof; 
	_test_eof205:  state.cs = 205; goto _test_eof; 
	_test_eof206:  state.cs = 206; goto _test_eof; 
	_test_eof207:  state.cs = 207; goto _test_eof; 
	_test_eof208:  state.cs = 208; goto _test_eof; 
	_test_eof209:  state.cs = 209; goto _test_eof; 
	_test_eof210:  state.cs = 210; goto _test_eof; 
	_test_eof211:  state.cs = 211; goto _test_eof; 
	_test_eof212:  state.cs = 212; goto _test_eof; 
	_test_eof213:  state.cs = 213; goto _test_eof; 
	_test_eof214:  state.cs = 214; goto _test_eof; 
	_test_eof215:  state.cs = 215; goto _test_eof; 
	_test_eof216:  state.cs = 216; goto _test_eof; 
	_test_eof217:  state.cs = 217; goto _test_eof; 
	_test_eof218:  state.cs = 218; goto _test_eof; 
	_test_eof219:  state.cs = 219; goto _test_eof; 
	_test_eof220:  state.cs = 220; goto _test_eof; 
	_test_eof221:  state.cs = 221; goto _test_eof; 
	_test_eof222:  state.cs = 222; goto _test_eof; 
	_test_eof223:  state.cs = 223; goto _test_eof; 
	_test_eof224:  state.cs = 224; goto _test_eof; 
	_test_eof225:  state.cs = 225; goto _test_eof; 
	_test_eof226:  state.cs = 226; goto _test_eof; 
	_test_eof227:  state.cs = 227; goto _test_eof; 
	_test_eof228:  state.cs = 228; goto _test_eof; 
	_test_eof229:  state.cs = 229; goto _test_eof; 
	_test_eof230:  state.cs = 230; goto _test_eof; 
	_test_eof231:  state.cs = 231; goto _test_eof; 
	_test_eof232:  state.cs = 232; goto _test_eof; 
	_test_eof233:  state.cs = 233; goto _test_eof; 
	_test_eof234:  state.cs = 234; goto _test_eof; 
	_test_eof235:  state.cs = 235; goto _test_eof; 
	_test_eof236:  state.cs = 236; goto _test_eof; 
	_test_eof237:  state.cs = 237; goto _test_eof; 
	_test_eof238:  state.cs = 238; goto _test_eof; 
	_test_eof239:  state.cs = 239; goto _test_eof; 
	_test_eof240:  state.cs = 240; goto _test_eof; 
	_test_eof241:  state.cs = 241; goto _test_eof; 
	_test_eof242:  state.cs = 242; goto _test_eof; 
	_test_eof243:  state.cs = 243; goto _test_eof; 
	_test_eof244:  state.cs = 244; goto _test_eof; 
	_test_eof245:  state.cs = 245; goto _test_eof; 
	_test_eof246:  state.cs = 246; goto _test_eof; 
	_test_eof247:  state.cs = 247; goto _test_eof; 
	_test_eof248:  state.cs = 248; goto _test_eof; 
	_test_eof249:  state.cs = 249; goto _test_eof; 
	_test_eof250:  state.cs = 250; goto _test_eof; 
	_test_eof251:  state.cs = 251; goto _test_eof; 
	_test_eof252:  state.cs = 252; goto _test_eof; 
	_test_eof253:  state.cs = 253; goto _test_eof; 
	_test_eof254:  state.cs = 254; goto _test_eof; 
	_test_eof255:  state.cs = 255; goto _test_eof; 
	_test_eof256:  state.cs = 256; goto _test_eof; 
	_test_eof257:  state.cs = 257; goto _test_eof; 
	_test_eof258:  state.cs = 258; goto _test_eof; 
	_test_eof259:  state.cs = 259; goto _test_eof; 
	_test_eof260:  state.cs = 260; goto _test_eof; 
	_test_eof261:  state.cs = 261; goto _test_eof; 
	_test_eof262:  state.cs = 262; goto _test_eof; 
	_test_eof263:  state.cs = 263; goto _test_eof; 
	_test_eof264:  state.cs = 264; goto _test_eof; 
	_test_eof265:  state.cs = 265; goto _test_eof; 
	_test_eof266:  state.cs = 266; goto _test_eof; 
	_test_eof267:  state.cs = 267; goto _test_eof; 
	_test_eof268:  state.cs = 268; goto _test_eof; 
	_test_eof269:  state.cs = 269; goto _test_eof; 
	_test_eof270:  state.cs = 270; goto _test_eof; 
	_test_eof271:  state.cs = 271; goto _test_eof; 
	_test_eof272:  state.cs = 272; goto _test_eof; 
	_test_eof273:  state.cs = 273; goto _test_eof; 
	_test_eof274:  state.cs = 274; goto _test_eof; 
	_test_eof275:  state.cs = 275; goto _test_eof; 
	_test_eof276:  state.cs = 276; goto _test_eof; 
	_test_eof277:  state.cs = 277; goto _test_eof; 
	_test_eof278:  state.cs = 278; goto _test_eof; 
	_test_eof279:  state.cs = 279; goto _test_eof; 
	_test_eof280:  state.cs = 280; goto _test_eof; 
	_test_eof281:  state.cs = 281; goto _test_eof; 
	_test_eof282:  state.cs = 282; goto _test_eof; 
	_test_eof283:  state.cs = 283; goto _test_eof; 
	_test_eof284:  state.cs = 284; goto _test_eof; 
	_test_eof285:  state.cs = 285; goto _test_eof; 
	_test_eof286:  state.cs = 286; goto _test_eof; 
	_test_eof287:  state.cs = 287; goto _test_eof; 
	_test_eof288:  state.cs = 288; goto _test_eof; 
	_test_eof289:  state.cs = 289; goto _test_eof; 
	_test_eof290:  state.cs = 290; goto _test_eof; 
	_test_eof291:  state.cs = 291; goto _test_eof; 
	_test_eof292:  state.cs = 292; goto _test_eof; 
	_test_eof293:  state.cs = 293; goto _test_eof; 
	_test_eof294:  state.cs = 294; goto _test_eof; 
	_test_eof295:  state.cs = 295; goto _test_eof; 
	_test_eof296:  state.cs = 296; goto _test_eof; 
	_test_eof297:  state.cs = 297; goto _test_eof; 
	_test_eof298:  state.cs = 298; goto _test_eof; 
	_test_eof299:  state.cs = 299; goto _test_eof; 
	_test_eof300:  state.cs = 300; goto _test_eof; 
	_test_eof301:  state.cs = 301; goto _test_eof; 
	_test_eof302:  state.cs = 302; goto _test_eof; 
	_test_eof303:  state.cs = 303; goto _test_eof; 
	_test_eof304:  state.cs = 304; goto _test_eof; 
	_test_eof305:  state.cs = 305; goto _test_eof; 
	_test_eof306:  state.cs = 306; goto _test_eof; 
	_test_eof307:  state.cs = 307; goto _test_eof; 
	_test_eof308:  state.cs = 308; goto _test_eof; 
	_test_eof309:  state.cs = 309; goto _test_eof; 
	_test_eof310:  state.cs = 310; goto _test_eof; 
	_test_eof311:  state.cs = 311; goto _test_eof; 
	_test_eof312:  state.cs = 312; goto _test_eof; 
	_test_eof313:  state.cs = 313; goto _test_eof; 
	_test_eof314:  state.cs = 314; goto _test_eof; 
	_test_eof315:  state.cs = 315; goto _test_eof; 
	_test_eof316:  state.cs = 316; goto _test_eof; 
	_test_eof317:  state.cs = 317; goto _test_eof; 
	_test_eof318:  state.cs = 318; goto _test_eof; 
	_test_eof319:  state.cs = 319; goto _test_eof; 
	_test_eof320:  state.cs = 320; goto _test_eof; 
	_test_eof321:  state.cs = 321; goto _test_eof; 
	_test_eof322:  state.cs = 322; goto _test_eof; 
	_test_eof323:  state.cs = 323; goto _test_eof; 
	_test_eof324:  state.cs = 324; goto _test_eof; 
	_test_eof325:  state.cs = 325; goto _test_eof; 
	_test_eof326:  state.cs = 326; goto _test_eof; 
	_test_eof327:  state.cs = 327; goto _test_eof; 
	_test_eof328:  state.cs = 328; goto _test_eof; 
	_test_eof329:  state.cs = 329; goto _test_eof; 
	_test_eof330:  state.cs = 330; goto _test_eof; 
	_test_eof331:  state.cs = 331; goto _test_eof; 
	_test_eof332:  state.cs = 332; goto _test_eof; 
	_test_eof333:  state.cs = 333; goto _test_eof; 
	_test_eof334:  state.cs = 334; goto _test_eof; 
	_test_eof335:  state.cs = 335; goto _test_eof; 
	_test_eof336:  state.cs = 336; goto _test_eof; 
	_test_eof337:  state.cs = 337; goto _test_eof; 
	_test_eof338:  state.cs = 338; goto _test_eof; 
	_test_eof339:  state.cs = 339; goto _test_eof; 
	_test_eof340:  state.cs = 340; goto _test_eof; 
	_test_eof341:  state.cs = 341; goto _test_eof; 
	_test_eof342:  state.cs = 342; goto _test_eof; 
	_test_eof343:  state.cs = 343; goto _test_eof; 
	_test_eof344:  state.cs = 344; goto _test_eof; 
	_test_eof345:  state.cs = 345; goto _test_eof; 
	_test_eof1358:  state.cs = 1358; goto _test_eof; 
	_test_eof346:  state.cs = 346; goto _test_eof; 
	_test_eof347:  state.cs = 347; goto _test_eof; 
	_test_eof348:  state.cs = 348; goto _test_eof; 
	_test_eof349:  state.cs = 349; goto _test_eof; 
	_test_eof350:  state.cs = 350; goto _test_eof; 
	_test_eof351:  state.cs = 351; goto _test_eof; 
	_test_eof352:  state.cs = 352; goto _test_eof; 
	_test_eof353:  state.cs = 353; goto _test_eof; 
	_test_eof354:  state.cs = 354; goto _test_eof; 
	_test_eof355:  state.cs = 355; goto _test_eof; 
	_test_eof356:  state.cs = 356; goto _test_eof; 
	_test_eof357:  state.cs = 357; goto _test_eof; 
	_test_eof358:  state.cs = 358; goto _test_eof; 
	_test_eof359:  state.cs = 359; goto _test_eof; 
	_test_eof360:  state.cs = 360; goto _test_eof; 
	_test_eof361:  state.cs = 361; goto _test_eof; 
	_test_eof362:  state.cs = 362; goto _test_eof; 
	_test_eof363:  state.cs = 363; goto _test_eof; 
	_test_eof364:  state.cs = 364; goto _test_eof; 
	_test_eof365:  state.cs = 365; goto _test_eof; 
	_test_eof366:  state.cs = 366; goto _test_eof; 
	_test_eof367:  state.cs = 367; goto _test_eof; 
	_test_eof368:  state.cs = 368; goto _test_eof; 
	_test_eof369:  state.cs = 369; goto _test_eof; 
	_test_eof370:  state.cs = 370; goto _test_eof; 
	_test_eof371:  state.cs = 371; goto _test_eof; 
	_test_eof372:  state.cs = 372; goto _test_eof; 
	_test_eof373:  state.cs = 373; goto _test_eof; 
	_test_eof374:  state.cs = 374; goto _test_eof; 
	_test_eof375:  state.cs = 375; goto _test_eof; 
	_test_eof376:  state.cs = 376; goto _test_eof; 
	_test_eof377:  state.cs = 377; goto _test_eof; 
	_test_eof378:  state.cs = 378; goto _test_eof; 
	_test_eof379:  state.cs = 379; goto _test_eof; 
	_test_eof380:  state.cs = 380; goto _test_eof; 
	_test_eof381:  state.cs = 381; goto _test_eof; 
	_test_eof382:  state.cs = 382; goto _test_eof; 
	_test_eof383:  state.cs = 383; goto _test_eof; 
	_test_eof384:  state.cs = 384; goto _test_eof; 
	_test_eof385:  state.cs = 385; goto _test_eof; 
	_test_eof386:  state.cs = 386; goto _test_eof; 
	_test_eof387:  state.cs = 387; goto _test_eof; 
	_test_eof388:  state.cs = 388; goto _test_eof; 
	_test_eof389:  state.cs = 389; goto _test_eof; 
	_test_eof390:  state.cs = 390; goto _test_eof; 
	_test_eof391:  state.cs = 391; goto _test_eof; 
	_test_eof392:  state.cs = 392; goto _test_eof; 
	_test_eof393:  state.cs = 393; goto _test_eof; 
	_test_eof394:  state.cs = 394; goto _test_eof; 
	_test_eof395:  state.cs = 395; goto _test_eof; 
	_test_eof396:  state.cs = 396; goto _test_eof; 
	_test_eof397:  state.cs = 397; goto _test_eof; 
	_test_eof398:  state.cs = 398; goto _test_eof; 
	_test_eof399:  state.cs = 399; goto _test_eof; 
	_test_eof400:  state.cs = 400; goto _test_eof; 
	_test_eof401:  state.cs = 401; goto _test_eof; 
	_test_eof402:  state.cs = 402; goto _test_eof; 
	_test_eof403:  state.cs = 403; goto _test_eof; 
	_test_eof404:  state.cs = 404; goto _test_eof; 
	_test_eof405:  state.cs = 405; goto _test_eof; 
	_test_eof406:  state.cs = 406; goto _test_eof; 
	_test_eof407:  state.cs = 407; goto _test_eof; 
	_test_eof408:  state.cs = 408; goto _test_eof; 
	_test_eof409:  state.cs = 409; goto _test_eof; 
	_test_eof410:  state.cs = 410; goto _test_eof; 
	_test_eof411:  state.cs = 411; goto _test_eof; 
	_test_eof412:  state.cs = 412; goto _test_eof; 
	_test_eof413:  state.cs = 413; goto _test_eof; 
	_test_eof414:  state.cs = 414; goto _test_eof; 
	_test_eof415:  state.cs = 415; goto _test_eof; 
	_test_eof416:  state.cs = 416; goto _test_eof; 
	_test_eof417:  state.cs = 417; goto _test_eof; 
	_test_eof418:  state.cs = 418; goto _test_eof; 
	_test_eof419:  state.cs = 419; goto _test_eof; 
	_test_eof420:  state.cs = 420; goto _test_eof; 
	_test_eof421:  state.cs = 421; goto _test_eof; 
	_test_eof422:  state.cs = 422; goto _test_eof; 
	_test_eof423:  state.cs = 423; goto _test_eof; 
	_test_eof424:  state.cs = 424; goto _test_eof; 
	_test_eof425:  state.cs = 425; goto _test_eof; 
	_test_eof426:  state.cs = 426; goto _test_eof; 
	_test_eof427:  state.cs = 427; goto _test_eof; 
	_test_eof428:  state.cs = 428; goto _test_eof; 
	_test_eof429:  state.cs = 429; goto _test_eof; 
	_test_eof430:  state.cs = 430; goto _test_eof; 
	_test_eof431:  state.cs = 431; goto _test_eof; 
	_test_eof432:  state.cs = 432; goto _test_eof; 
	_test_eof433:  state.cs = 433; goto _test_eof; 
	_test_eof434:  state.cs = 434; goto _test_eof; 
	_test_eof435:  state.cs = 435; goto _test_eof; 
	_test_eof436:  state.cs = 436; goto _test_eof; 
	_test_eof437:  state.cs = 437; goto _test_eof; 
	_test_eof438:  state.cs = 438; goto _test_eof; 
	_test_eof439:  state.cs = 439; goto _test_eof; 
	_test_eof440:  state.cs = 440; goto _test_eof; 
	_test_eof441:  state.cs = 441; goto _test_eof; 
	_test_eof442:  state.cs = 442; goto _test_eof; 
	_test_eof443:  state.cs = 443; goto _test_eof; 
	_test_eof444:  state.cs = 444; goto _test_eof; 
	_test_eof445:  state.cs = 445; goto _test_eof; 
	_test_eof446:  state.cs = 446; goto _test_eof; 
	_test_eof447:  state.cs = 447; goto _test_eof; 
	_test_eof448:  state.cs = 448; goto _test_eof; 
	_test_eof449:  state.cs = 449; goto _test_eof; 
	_test_eof450:  state.cs = 450; goto _test_eof; 
	_test_eof451:  state.cs = 451; goto _test_eof; 
	_test_eof452:  state.cs = 452; goto _test_eof; 
	_test_eof453:  state.cs = 453; goto _test_eof; 
	_test_eof454:  state.cs = 454; goto _test_eof; 
	_test_eof455:  state.cs = 455; goto _test_eof; 
	_test_eof456:  state.cs = 456; goto _test_eof; 
	_test_eof457:  state.cs = 457; goto _test_eof; 
	_test_eof458:  state.cs = 458; goto _test_eof; 
	_test_eof459:  state.cs = 459; goto _test_eof; 
	_test_eof460:  state.cs = 460; goto _test_eof; 
	_test_eof461:  state.cs = 461; goto _test_eof; 
	_test_eof462:  state.cs = 462; goto _test_eof; 
	_test_eof463:  state.cs = 463; goto _test_eof; 
	_test_eof464:  state.cs = 464; goto _test_eof; 
	_test_eof465:  state.cs = 465; goto _test_eof; 
	_test_eof466:  state.cs = 466; goto _test_eof; 
	_test_eof467:  state.cs = 467; goto _test_eof; 
	_test_eof468:  state.cs = 468; goto _test_eof; 
	_test_eof469:  state.cs = 469; goto _test_eof; 
	_test_eof470:  state.cs = 470; goto _test_eof; 
	_test_eof471:  state.cs = 471; goto _test_eof; 
	_test_eof472:  state.cs = 472; goto _test_eof; 
	_test_eof473:  state.cs = 473; goto _test_eof; 
	_test_eof474:  state.cs = 474; goto _test_eof; 
	_test_eof475:  state.cs = 475; goto _test_eof; 
	_test_eof476:  state.cs = 476; goto _test_eof; 
	_test_eof477:  state.cs = 477; goto _test_eof; 
	_test_eof478:  state.cs = 478; goto _test_eof; 
	_test_eof479:  state.cs = 479; goto _test_eof; 
	_test_eof480:  state.cs = 480; goto _test_eof; 
	_test_eof481:  state.cs = 481; goto _test_eof; 
	_test_eof482:  state.cs = 482; goto _test_eof; 
	_test_eof483:  state.cs = 483; goto _test_eof; 
	_test_eof484:  state.cs = 484; goto _test_eof; 
	_test_eof485:  state.cs = 485; goto _test_eof; 
	_test_eof486:  state.cs = 486; goto _test_eof; 
	_test_eof487:  state.cs = 487; goto _test_eof; 
	_test_eof488:  state.cs = 488; goto _test_eof; 
	_test_eof489:  state.cs = 489; goto _test_eof; 
	_test_eof490:  state.cs = 490; goto _test_eof; 
	_test_eof491:  state.cs = 491; goto _test_eof; 
	_test_eof1359:  state.cs = 1359; goto _test_eof; 
	_test_eof492:  state.cs = 492; goto _test_eof; 
	_test_eof493:  state.cs = 493; goto _test_eof; 
	_test_eof494:  state.cs = 494; goto _test_eof; 
	_test_eof495:  state.cs = 495; goto _test_eof; 
	_test_eof496:  state.cs = 496; goto _test_eof; 
	_test_eof497:  state.cs = 497; goto _test_eof; 
	_test_eof498:  state.cs = 498; goto _test_eof; 
	_test_eof499:  state.cs = 499; goto _test_eof; 
	_test_eof500:  state.cs = 500; goto _test_eof; 
	_test_eof501:  state.cs = 501; goto _test_eof; 
	_test_eof502:  state.cs = 502; goto _test_eof; 
	_test_eof503:  state.cs = 503; goto _test_eof; 
	_test_eof504:  state.cs = 504; goto _test_eof; 
	_test_eof505:  state.cs = 505; goto _test_eof; 
	_test_eof506:  state.cs = 506; goto _test_eof; 
	_test_eof507:  state.cs = 507; goto _test_eof; 
	_test_eof508:  state.cs = 508; goto _test_eof; 
	_test_eof509:  state.cs = 509; goto _test_eof; 
	_test_eof510:  state.cs = 510; goto _test_eof; 
	_test_eof511:  state.cs = 511; goto _test_eof; 
	_test_eof512:  state.cs = 512; goto _test_eof; 
	_test_eof513:  state.cs = 513; goto _test_eof; 
	_test_eof514:  state.cs = 514; goto _test_eof; 
	_test_eof515:  state.cs = 515; goto _test_eof; 
	_test_eof516:  state.cs = 516; goto _test_eof; 
	_test_eof517:  state.cs = 517; goto _test_eof; 
	_test_eof518:  state.cs = 518; goto _test_eof; 
	_test_eof519:  state.cs = 519; goto _test_eof; 
	_test_eof520:  state.cs = 520; goto _test_eof; 
	_test_eof521:  state.cs = 521; goto _test_eof; 
	_test_eof522:  state.cs = 522; goto _test_eof; 
	_test_eof523:  state.cs = 523; goto _test_eof; 
	_test_eof524:  state.cs = 524; goto _test_eof; 
	_test_eof525:  state.cs = 525; goto _test_eof; 
	_test_eof526:  state.cs = 526; goto _test_eof; 
	_test_eof527:  state.cs = 527; goto _test_eof; 
	_test_eof528:  state.cs = 528; goto _test_eof; 
	_test_eof529:  state.cs = 529; goto _test_eof; 
	_test_eof530:  state.cs = 530; goto _test_eof; 
	_test_eof531:  state.cs = 531; goto _test_eof; 
	_test_eof532:  state.cs = 532; goto _test_eof; 
	_test_eof533:  state.cs = 533; goto _test_eof; 
	_test_eof534:  state.cs = 534; goto _test_eof; 
	_test_eof535:  state.cs = 535; goto _test_eof; 
	_test_eof536:  state.cs = 536; goto _test_eof; 
	_test_eof537:  state.cs = 537; goto _test_eof; 
	_test_eof538:  state.cs = 538; goto _test_eof; 
	_test_eof539:  state.cs = 539; goto _test_eof; 
	_test_eof540:  state.cs = 540; goto _test_eof; 
	_test_eof541:  state.cs = 541; goto _test_eof; 
	_test_eof542:  state.cs = 542; goto _test_eof; 
	_test_eof543:  state.cs = 543; goto _test_eof; 
	_test_eof544:  state.cs = 544; goto _test_eof; 
	_test_eof545:  state.cs = 545; goto _test_eof; 
	_test_eof546:  state.cs = 546; goto _test_eof; 
	_test_eof547:  state.cs = 547; goto _test_eof; 
	_test_eof548:  state.cs = 548; goto _test_eof; 
	_test_eof549:  state.cs = 549; goto _test_eof; 
	_test_eof550:  state.cs = 550; goto _test_eof; 
	_test_eof551:  state.cs = 551; goto _test_eof; 
	_test_eof552:  state.cs = 552; goto _test_eof; 
	_test_eof553:  state.cs = 553; goto _test_eof; 
	_test_eof554:  state.cs = 554; goto _test_eof; 
	_test_eof555:  state.cs = 555; goto _test_eof; 
	_test_eof556:  state.cs = 556; goto _test_eof; 
	_test_eof557:  state.cs = 557; goto _test_eof; 
	_test_eof558:  state.cs = 558; goto _test_eof; 
	_test_eof559:  state.cs = 559; goto _test_eof; 
	_test_eof560:  state.cs = 560; goto _test_eof; 
	_test_eof561:  state.cs = 561; goto _test_eof; 
	_test_eof562:  state.cs = 562; goto _test_eof; 
	_test_eof563:  state.cs = 563; goto _test_eof; 
	_test_eof564:  state.cs = 564; goto _test_eof; 
	_test_eof565:  state.cs = 565; goto _test_eof; 
	_test_eof566:  state.cs = 566; goto _test_eof; 
	_test_eof567:  state.cs = 567; goto _test_eof; 
	_test_eof568:  state.cs = 568; goto _test_eof; 
	_test_eof569:  state.cs = 569; goto _test_eof; 
	_test_eof570:  state.cs = 570; goto _test_eof; 
	_test_eof571:  state.cs = 571; goto _test_eof; 
	_test_eof572:  state.cs = 572; goto _test_eof; 
	_test_eof573:  state.cs = 573; goto _test_eof; 
	_test_eof574:  state.cs = 574; goto _test_eof; 
	_test_eof575:  state.cs = 575; goto _test_eof; 
	_test_eof576:  state.cs = 576; goto _test_eof; 
	_test_eof577:  state.cs = 577; goto _test_eof; 
	_test_eof578:  state.cs = 578; goto _test_eof; 
	_test_eof579:  state.cs = 579; goto _test_eof; 
	_test_eof580:  state.cs = 580; goto _test_eof; 
	_test_eof581:  state.cs = 581; goto _test_eof; 
	_test_eof582:  state.cs = 582; goto _test_eof; 
	_test_eof583:  state.cs = 583; goto _test_eof; 
	_test_eof584:  state.cs = 584; goto _test_eof; 
	_test_eof585:  state.cs = 585; goto _test_eof; 
	_test_eof586:  state.cs = 586; goto _test_eof; 
	_test_eof587:  state.cs = 587; goto _test_eof; 
	_test_eof588:  state.cs = 588; goto _test_eof; 
	_test_eof589:  state.cs = 589; goto _test_eof; 
	_test_eof590:  state.cs = 590; goto _test_eof; 
	_test_eof591:  state.cs = 591; goto _test_eof; 
	_test_eof592:  state.cs = 592; goto _test_eof; 
	_test_eof593:  state.cs = 593; goto _test_eof; 
	_test_eof594:  state.cs = 594; goto _test_eof; 
	_test_eof595:  state.cs = 595; goto _test_eof; 
	_test_eof596:  state.cs = 596; goto _test_eof; 
	_test_eof597:  state.cs = 597; goto _test_eof; 
	_test_eof598:  state.cs = 598; goto _test_eof; 
	_test_eof599:  state.cs = 599; goto _test_eof; 
	_test_eof600:  state.cs = 600; goto _test_eof; 
	_test_eof601:  state.cs = 601; goto _test_eof; 
	_test_eof602:  state.cs = 602; goto _test_eof; 
	_test_eof603:  state.cs = 603; goto _test_eof; 
	_test_eof604:  state.cs = 604; goto _test_eof; 
	_test_eof605:  state.cs = 605; goto _test_eof; 
	_test_eof606:  state.cs = 606; goto _test_eof; 
	_test_eof607:  state.cs = 607; goto _test_eof; 
	_test_eof608:  state.cs = 608; goto _test_eof; 
	_test_eof609:  state.cs = 609; goto _test_eof; 
	_test_eof610:  state.cs = 610; goto _test_eof; 
	_test_eof611:  state.cs = 611; goto _test_eof; 
	_test_eof612:  state.cs = 612; goto _test_eof; 
	_test_eof613:  state.cs = 613; goto _test_eof; 
	_test_eof614:  state.cs = 614; goto _test_eof; 
	_test_eof615:  state.cs = 615; goto _test_eof; 
	_test_eof616:  state.cs = 616; goto _test_eof; 
	_test_eof617:  state.cs = 617; goto _test_eof; 
	_test_eof618:  state.cs = 618; goto _test_eof; 
	_test_eof619:  state.cs = 619; goto _test_eof; 
	_test_eof620:  state.cs = 620; goto _test_eof; 
	_test_eof621:  state.cs = 621; goto _test_eof; 
	_test_eof622:  state.cs = 622; goto _test_eof; 
	_test_eof623:  state.cs = 623; goto _test_eof; 
	_test_eof624:  state.cs = 624; goto _test_eof; 
	_test_eof625:  state.cs = 625; goto _test_eof; 
	_test_eof626:  state.cs = 626; goto _test_eof; 
	_test_eof627:  state.cs = 627; goto _test_eof; 
	_test_eof628:  state.cs = 628; goto _test_eof; 
	_test_eof629:  state.cs = 629; goto _test_eof; 
	_test_eof630:  state.cs = 630; goto _test_eof; 
	_test_eof631:  state.cs = 631; goto _test_eof; 
	_test_eof632:  state.cs = 632; goto _test_eof; 
	_test_eof633:  state.cs = 633; goto _test_eof; 
	_test_eof634:  state.cs = 634; goto _test_eof; 
	_test_eof635:  state.cs = 635; goto _test_eof; 
	_test_eof636:  state.cs = 636; goto _test_eof; 
	_test_eof637:  state.cs = 637; goto _test_eof; 
	_test_eof638:  state.cs = 638; goto _test_eof; 
	_test_eof639:  state.cs = 639; goto _test_eof; 
	_test_eof640:  state.cs = 640; goto _test_eof; 
	_test_eof641:  state.cs = 641; goto _test_eof; 
	_test_eof642:  state.cs = 642; goto _test_eof; 
	_test_eof643:  state.cs = 643; goto _test_eof; 
	_test_eof644:  state.cs = 644; goto _test_eof; 
	_test_eof645:  state.cs = 645; goto _test_eof; 
	_test_eof646:  state.cs = 646; goto _test_eof; 
	_test_eof647:  state.cs = 647; goto _test_eof; 
	_test_eof648:  state.cs = 648; goto _test_eof; 
	_test_eof649:  state.cs = 649; goto _test_eof; 
	_test_eof650:  state.cs = 650; goto _test_eof; 
	_test_eof651:  state.cs = 651; goto _test_eof; 
	_test_eof652:  state.cs = 652; goto _test_eof; 
	_test_eof653:  state.cs = 653; goto _test_eof; 
	_test_eof654:  state.cs = 654; goto _test_eof; 
	_test_eof655:  state.cs = 655; goto _test_eof; 
	_test_eof1360:  state.cs = 1360; goto _test_eof; 
	_test_eof656:  state.cs = 656; goto _test_eof; 
	_test_eof657:  state.cs = 657; goto _test_eof; 
	_test_eof658:  state.cs = 658; goto _test_eof; 
	_test_eof659:  state.cs = 659; goto _test_eof; 
	_test_eof660:  state.cs = 660; goto _test_eof; 
	_test_eof661:  state.cs = 661; goto _test_eof; 
	_test_eof662:  state.cs = 662; goto _test_eof; 
	_test_eof663:  state.cs = 663; goto _test_eof; 
	_test_eof664:  state.cs = 664; goto _test_eof; 
	_test_eof665:  state.cs = 665; goto _test_eof; 
	_test_eof666:  state.cs = 666; goto _test_eof; 
	_test_eof667:  state.cs = 667; goto _test_eof; 
	_test_eof668:  state.cs = 668; goto _test_eof; 
	_test_eof669:  state.cs = 669; goto _test_eof; 
	_test_eof670:  state.cs = 670; goto _test_eof; 
	_test_eof671:  state.cs = 671; goto _test_eof; 
	_test_eof672:  state.cs = 672; goto _test_eof; 
	_test_eof673:  state.cs = 673; goto _test_eof; 
	_test_eof674:  state.cs = 674; goto _test_eof; 
	_test_eof675:  state.cs = 675; goto _test_eof; 
	_test_eof676:  state.cs = 676; goto _test_eof; 
	_test_eof677:  state.cs = 677; goto _test_eof; 
	_test_eof678:  state.cs = 678; goto _test_eof; 
	_test_eof679:  state.cs = 679; goto _test_eof; 
	_test_eof680:  state.cs = 680; goto _test_eof; 
	_test_eof681:  state.cs = 681; goto _test_eof; 
	_test_eof682:  state.cs = 682; goto _test_eof; 
	_test_eof683:  state.cs = 683; goto _test_eof; 
	_test_eof684:  state.cs = 684; goto _test_eof; 
	_test_eof685:  state.cs = 685; goto _test_eof; 
	_test_eof686:  state.cs = 686; goto _test_eof; 
	_test_eof687:  state.cs = 687; goto _test_eof; 
	_test_eof688:  state.cs = 688; goto _test_eof; 
	_test_eof689:  state.cs = 689; goto _test_eof; 
	_test_eof690:  state.cs = 690; goto _test_eof; 
	_test_eof691:  state.cs = 691; goto _test_eof; 
	_test_eof692:  state.cs = 692; goto _test_eof; 
	_test_eof693:  state.cs = 693; goto _test_eof; 
	_test_eof694:  state.cs = 694; goto _test_eof; 
	_test_eof695:  state.cs = 695; goto _test_eof; 
	_test_eof696:  state.cs = 696; goto _test_eof; 
	_test_eof697:  state.cs = 697; goto _test_eof; 
	_test_eof698:  state.cs = 698; goto _test_eof; 
	_test_eof699:  state.cs = 699; goto _test_eof; 
	_test_eof700:  state.cs = 700; goto _test_eof; 
	_test_eof701:  state.cs = 701; goto _test_eof; 
	_test_eof702:  state.cs = 702; goto _test_eof; 
	_test_eof703:  state.cs = 703; goto _test_eof; 
	_test_eof704:  state.cs = 704; goto _test_eof; 
	_test_eof705:  state.cs = 705; goto _test_eof; 
	_test_eof706:  state.cs = 706; goto _test_eof; 
	_test_eof707:  state.cs = 707; goto _test_eof; 
	_test_eof708:  state.cs = 708; goto _test_eof; 
	_test_eof709:  state.cs = 709; goto _test_eof; 
	_test_eof710:  state.cs = 710; goto _test_eof; 
	_test_eof711:  state.cs = 711; goto _test_eof; 
	_test_eof712:  state.cs = 712; goto _test_eof; 
	_test_eof713:  state.cs = 713; goto _test_eof; 
	_test_eof714:  state.cs = 714; goto _test_eof; 
	_test_eof715:  state.cs = 715; goto _test_eof; 
	_test_eof716:  state.cs = 716; goto _test_eof; 
	_test_eof717:  state.cs = 717; goto _test_eof; 
	_test_eof718:  state.cs = 718; goto _test_eof; 
	_test_eof719:  state.cs = 719; goto _test_eof; 
	_test_eof720:  state.cs = 720; goto _test_eof; 
	_test_eof721:  state.cs = 721; goto _test_eof; 
	_test_eof722:  state.cs = 722; goto _test_eof; 
	_test_eof723:  state.cs = 723; goto _test_eof; 
	_test_eof724:  state.cs = 724; goto _test_eof; 
	_test_eof725:  state.cs = 725; goto _test_eof; 
	_test_eof726:  state.cs = 726; goto _test_eof; 
	_test_eof727:  state.cs = 727; goto _test_eof; 
	_test_eof728:  state.cs = 728; goto _test_eof; 
	_test_eof729:  state.cs = 729; goto _test_eof; 
	_test_eof730:  state.cs = 730; goto _test_eof; 
	_test_eof731:  state.cs = 731; goto _test_eof; 
	_test_eof732:  state.cs = 732; goto _test_eof; 
	_test_eof733:  state.cs = 733; goto _test_eof; 
	_test_eof734:  state.cs = 734; goto _test_eof; 
	_test_eof735:  state.cs = 735; goto _test_eof; 
	_test_eof736:  state.cs = 736; goto _test_eof; 
	_test_eof737:  state.cs = 737; goto _test_eof; 
	_test_eof738:  state.cs = 738; goto _test_eof; 
	_test_eof739:  state.cs = 739; goto _test_eof; 
	_test_eof740:  state.cs = 740; goto _test_eof; 
	_test_eof741:  state.cs = 741; goto _test_eof; 
	_test_eof742:  state.cs = 742; goto _test_eof; 
	_test_eof743:  state.cs = 743; goto _test_eof; 
	_test_eof744:  state.cs = 744; goto _test_eof; 
	_test_eof745:  state.cs = 745; goto _test_eof; 
	_test_eof746:  state.cs = 746; goto _test_eof; 
	_test_eof747:  state.cs = 747; goto _test_eof; 
	_test_eof748:  state.cs = 748; goto _test_eof; 
	_test_eof749:  state.cs = 749; goto _test_eof; 
	_test_eof750:  state.cs = 750; goto _test_eof; 
	_test_eof751:  state.cs = 751; goto _test_eof; 
	_test_eof752:  state.cs = 752; goto _test_eof; 
	_test_eof753:  state.cs = 753; goto _test_eof; 
	_test_eof754:  state.cs = 754; goto _test_eof; 
	_test_eof755:  state.cs = 755; goto _test_eof; 
	_test_eof756:  state.cs = 756; goto _test_eof; 
	_test_eof757:  state.cs = 757; goto _test_eof; 
	_test_eof758:  state.cs = 758; goto _test_eof; 
	_test_eof759:  state.cs = 759; goto _test_eof; 
	_test_eof760:  state.cs = 760; goto _test_eof; 
	_test_eof761:  state.cs = 761; goto _test_eof; 
	_test_eof762:  state.cs = 762; goto _test_eof; 
	_test_eof763:  state.cs = 763; goto _test_eof; 
	_test_eof764:  state.cs = 764; goto _test_eof; 
	_test_eof765:  state.cs = 765; goto _test_eof; 
	_test_eof766:  state.cs = 766; goto _test_eof; 
	_test_eof767:  state.cs = 767; goto _test_eof; 
	_test_eof768:  state.cs = 768; goto _test_eof; 
	_test_eof769:  state.cs = 769; goto _test_eof; 
	_test_eof770:  state.cs = 770; goto _test_eof; 
	_test_eof771:  state.cs = 771; goto _test_eof; 
	_test_eof772:  state.cs = 772; goto _test_eof; 
	_test_eof773:  state.cs = 773; goto _test_eof; 
	_test_eof774:  state.cs = 774; goto _test_eof; 
	_test_eof775:  state.cs = 775; goto _test_eof; 
	_test_eof776:  state.cs = 776; goto _test_eof; 
	_test_eof777:  state.cs = 777; goto _test_eof; 
	_test_eof778:  state.cs = 778; goto _test_eof; 
	_test_eof779:  state.cs = 779; goto _test_eof; 
	_test_eof780:  state.cs = 780; goto _test_eof; 
	_test_eof781:  state.cs = 781; goto _test_eof; 
	_test_eof782:  state.cs = 782; goto _test_eof; 
	_test_eof783:  state.cs = 783; goto _test_eof; 
	_test_eof784:  state.cs = 784; goto _test_eof; 
	_test_eof785:  state.cs = 785; goto _test_eof; 
	_test_eof786:  state.cs = 786; goto _test_eof; 
	_test_eof787:  state.cs = 787; goto _test_eof; 
	_test_eof788:  state.cs = 788; goto _test_eof; 
	_test_eof789:  state.cs = 789; goto _test_eof; 
	_test_eof790:  state.cs = 790; goto _test_eof; 
	_test_eof791:  state.cs = 791; goto _test_eof; 
	_test_eof792:  state.cs = 792; goto _test_eof; 
	_test_eof793:  state.cs = 793; goto _test_eof; 
	_test_eof794:  state.cs = 794; goto _test_eof; 
	_test_eof795:  state.cs = 795; goto _test_eof; 
	_test_eof796:  state.cs = 796; goto _test_eof; 
	_test_eof797:  state.cs = 797; goto _test_eof; 
	_test_eof798:  state.cs = 798; goto _test_eof; 
	_test_eof799:  state.cs = 799; goto _test_eof; 
	_test_eof800:  state.cs = 800; goto _test_eof; 
	_test_eof801:  state.cs = 801; goto _test_eof; 
	_test_eof802:  state.cs = 802; goto _test_eof; 
	_test_eof803:  state.cs = 803; goto _test_eof; 
	_test_eof804:  state.cs = 804; goto _test_eof; 
	_test_eof805:  state.cs = 805; goto _test_eof; 
	_test_eof806:  state.cs = 806; goto _test_eof; 
	_test_eof807:  state.cs = 807; goto _test_eof; 
	_test_eof808:  state.cs = 808; goto _test_eof; 
	_test_eof809:  state.cs = 809; goto _test_eof; 
	_test_eof810:  state.cs = 810; goto _test_eof; 
	_test_eof811:  state.cs = 811; goto _test_eof; 
	_test_eof812:  state.cs = 812; goto _test_eof; 
	_test_eof813:  state.cs = 813; goto _test_eof; 
	_test_eof814:  state.cs = 814; goto _test_eof; 
	_test_eof815:  state.cs = 815; goto _test_eof; 
	_test_eof816:  state.cs = 816; goto _test_eof; 
	_test_eof817:  state.cs = 817; goto _test_eof; 
	_test_eof818:  state.cs = 818; goto _test_eof; 
	_test_eof819:  state.cs = 819; goto _test_eof; 
	_test_eof820:  state.cs = 820; goto _test_eof; 
	_test_eof821:  state.cs = 821; goto _test_eof; 
	_test_eof822:  state.cs = 822; goto _test_eof; 
	_test_eof823:  state.cs = 823; goto _test_eof; 
	_test_eof824:  state.cs = 824; goto _test_eof; 
	_test_eof825:  state.cs = 825; goto _test_eof; 
	_test_eof826:  state.cs = 826; goto _test_eof; 
	_test_eof827:  state.cs = 827; goto _test_eof; 
	_test_eof828:  state.cs = 828; goto _test_eof; 
	_test_eof829:  state.cs = 829; goto _test_eof; 
	_test_eof830:  state.cs = 830; goto _test_eof; 
	_test_eof831:  state.cs = 831; goto _test_eof; 
	_test_eof832:  state.cs = 832; goto _test_eof; 
	_test_eof833:  state.cs = 833; goto _test_eof; 
	_test_eof834:  state.cs = 834; goto _test_eof; 
	_test_eof835:  state.cs = 835; goto _test_eof; 
	_test_eof836:  state.cs = 836; goto _test_eof; 
	_test_eof837:  state.cs = 837; goto _test_eof; 
	_test_eof838:  state.cs = 838; goto _test_eof; 
	_test_eof839:  state.cs = 839; goto _test_eof; 
	_test_eof840:  state.cs = 840; goto _test_eof; 
	_test_eof841:  state.cs = 841; goto _test_eof; 
	_test_eof842:  state.cs = 842; goto _test_eof; 
	_test_eof843:  state.cs = 843; goto _test_eof; 
	_test_eof844:  state.cs = 844; goto _test_eof; 
	_test_eof845:  state.cs = 845; goto _test_eof; 
	_test_eof846:  state.cs = 846; goto _test_eof; 
	_test_eof847:  state.cs = 847; goto _test_eof; 
	_test_eof848:  state.cs = 848; goto _test_eof; 
	_test_eof849:  state.cs = 849; goto _test_eof; 
	_test_eof850:  state.cs = 850; goto _test_eof; 
	_test_eof851:  state.cs = 851; goto _test_eof; 
	_test_eof852:  state.cs = 852; goto _test_eof; 
	_test_eof853:  state.cs = 853; goto _test_eof; 
	_test_eof854:  state.cs = 854; goto _test_eof; 
	_test_eof855:  state.cs = 855; goto _test_eof; 
	_test_eof856:  state.cs = 856; goto _test_eof; 
	_test_eof857:  state.cs = 857; goto _test_eof; 
	_test_eof858:  state.cs = 858; goto _test_eof; 
	_test_eof859:  state.cs = 859; goto _test_eof; 
	_test_eof860:  state.cs = 860; goto _test_eof; 
	_test_eof861:  state.cs = 861; goto _test_eof; 
	_test_eof862:  state.cs = 862; goto _test_eof; 
	_test_eof863:  state.cs = 863; goto _test_eof; 
	_test_eof864:  state.cs = 864; goto _test_eof; 
	_test_eof865:  state.cs = 865; goto _test_eof; 
	_test_eof866:  state.cs = 866; goto _test_eof; 
	_test_eof867:  state.cs = 867; goto _test_eof; 
	_test_eof868:  state.cs = 868; goto _test_eof; 
	_test_eof869:  state.cs = 869; goto _test_eof; 
	_test_eof870:  state.cs = 870; goto _test_eof; 
	_test_eof871:  state.cs = 871; goto _test_eof; 
	_test_eof872:  state.cs = 872; goto _test_eof; 
	_test_eof873:  state.cs = 873; goto _test_eof; 
	_test_eof874:  state.cs = 874; goto _test_eof; 
	_test_eof875:  state.cs = 875; goto _test_eof; 
	_test_eof876:  state.cs = 876; goto _test_eof; 
	_test_eof877:  state.cs = 877; goto _test_eof; 
	_test_eof878:  state.cs = 878; goto _test_eof; 
	_test_eof879:  state.cs = 879; goto _test_eof; 
	_test_eof880:  state.cs = 880; goto _test_eof; 
	_test_eof881:  state.cs = 881; goto _test_eof; 
	_test_eof882:  state.cs = 882; goto _test_eof; 
	_test_eof883:  state.cs = 883; goto _test_eof; 
	_test_eof884:  state.cs = 884; goto _test_eof; 
	_test_eof885:  state.cs = 885; goto _test_eof; 
	_test_eof886:  state.cs = 886; goto _test_eof; 
	_test_eof887:  state.cs = 887; goto _test_eof; 
	_test_eof888:  state.cs = 888; goto _test_eof; 
	_test_eof889:  state.cs = 889; goto _test_eof; 
	_test_eof890:  state.cs = 890; goto _test_eof; 
	_test_eof891:  state.cs = 891; goto _test_eof; 
	_test_eof892:  state.cs = 892; goto _test_eof; 
	_test_eof893:  state.cs = 893; goto _test_eof; 
	_test_eof894:  state.cs = 894; goto _test_eof; 
	_test_eof895:  state.cs = 895; goto _test_eof; 
	_test_eof896:  state.cs = 896; goto _test_eof; 
	_test_eof897:  state.cs = 897; goto _test_eof; 
	_test_eof898:  state.cs = 898; goto _test_eof; 
	_test_eof899:  state.cs = 899; goto _test_eof; 
	_test_eof900:  state.cs = 900; goto _test_eof; 
	_test_eof901:  state.cs = 901; goto _test_eof; 
	_test_eof902:  state.cs = 902; goto _test_eof; 
	_test_eof903:  state.cs = 903; goto _test_eof; 
	_test_eof904:  state.cs = 904; goto _test_eof; 
	_test_eof905:  state.cs = 905; goto _test_eof; 
	_test_eof906:  state.cs = 906; goto _test_eof; 
	_test_eof907:  state.cs = 907; goto _test_eof; 
	_test_eof908:  state.cs = 908; goto _test_eof; 
	_test_eof909:  state.cs = 909; goto _test_eof; 
	_test_eof910:  state.cs = 910; goto _test_eof; 
	_test_eof911:  state.cs = 911; goto _test_eof; 
	_test_eof912:  state.cs = 912; goto _test_eof; 
	_test_eof913:  state.cs = 913; goto _test_eof; 
	_test_eof914:  state.cs = 914; goto _test_eof; 
	_test_eof915:  state.cs = 915; goto _test_eof; 
	_test_eof916:  state.cs = 916; goto _test_eof; 
	_test_eof917:  state.cs = 917; goto _test_eof; 
	_test_eof918:  state.cs = 918; goto _test_eof; 
	_test_eof919:  state.cs = 919; goto _test_eof; 
	_test_eof920:  state.cs = 920; goto _test_eof; 
	_test_eof921:  state.cs = 921; goto _test_eof; 
	_test_eof922:  state.cs = 922; goto _test_eof; 
	_test_eof923:  state.cs = 923; goto _test_eof; 
	_test_eof924:  state.cs = 924; goto _test_eof; 
	_test_eof925:  state.cs = 925; goto _test_eof; 
	_test_eof926:  state.cs = 926; goto _test_eof; 
	_test_eof927:  state.cs = 927; goto _test_eof; 
	_test_eof928:  state.cs = 928; goto _test_eof; 
	_test_eof929:  state.cs = 929; goto _test_eof; 
	_test_eof930:  state.cs = 930; goto _test_eof; 
	_test_eof931:  state.cs = 931; goto _test_eof; 
	_test_eof932:  state.cs = 932; goto _test_eof; 
	_test_eof933:  state.cs = 933; goto _test_eof; 
	_test_eof934:  state.cs = 934; goto _test_eof; 
	_test_eof935:  state.cs = 935; goto _test_eof; 
	_test_eof936:  state.cs = 936; goto _test_eof; 
	_test_eof937:  state.cs = 937; goto _test_eof; 
	_test_eof938:  state.cs = 938; goto _test_eof; 
	_test_eof939:  state.cs = 939; goto _test_eof; 
	_test_eof940:  state.cs = 940; goto _test_eof; 
	_test_eof941:  state.cs = 941; goto _test_eof; 
	_test_eof942:  state.cs = 942; goto _test_eof; 
	_test_eof943:  state.cs = 943; goto _test_eof; 
	_test_eof944:  state.cs = 944; goto _test_eof; 
	_test_eof945:  state.cs = 945; goto _test_eof; 
	_test_eof946:  state.cs = 946; goto _test_eof; 
	_test_eof947:  state.cs = 947; goto _test_eof; 
	_test_eof948:  state.cs = 948; goto _test_eof; 
	_test_eof949:  state.cs = 949; goto _test_eof; 
	_test_eof950:  state.cs = 950; goto _test_eof; 
	_test_eof951:  state.cs = 951; goto _test_eof; 
	_test_eof952:  state.cs = 952; goto _test_eof; 
	_test_eof953:  state.cs = 953; goto _test_eof; 
	_test_eof954:  state.cs = 954; goto _test_eof; 
	_test_eof955:  state.cs = 955; goto _test_eof; 
	_test_eof956:  state.cs = 956; goto _test_eof; 
	_test_eof957:  state.cs = 957; goto _test_eof; 
	_test_eof958:  state.cs = 958; goto _test_eof; 
	_test_eof959:  state.cs = 959; goto _test_eof; 
	_test_eof960:  state.cs = 960; goto _test_eof; 
	_test_eof961:  state.cs = 961; goto _test_eof; 
	_test_eof962:  state.cs = 962; goto _test_eof; 
	_test_eof963:  state.cs = 963; goto _test_eof; 
	_test_eof964:  state.cs = 964; goto _test_eof; 
	_test_eof965:  state.cs = 965; goto _test_eof; 
	_test_eof966:  state.cs = 966; goto _test_eof; 
	_test_eof967:  state.cs = 967; goto _test_eof; 
	_test_eof968:  state.cs = 968; goto _test_eof; 
	_test_eof969:  state.cs = 969; goto _test_eof; 
	_test_eof970:  state.cs = 970; goto _test_eof; 
	_test_eof971:  state.cs = 971; goto _test_eof; 
	_test_eof972:  state.cs = 972; goto _test_eof; 
	_test_eof973:  state.cs = 973; goto _test_eof; 
	_test_eof974:  state.cs = 974; goto _test_eof; 
	_test_eof975:  state.cs = 975; goto _test_eof; 
	_test_eof976:  state.cs = 976; goto _test_eof; 
	_test_eof977:  state.cs = 977; goto _test_eof; 
	_test_eof978:  state.cs = 978; goto _test_eof; 
	_test_eof979:  state.cs = 979; goto _test_eof; 
	_test_eof980:  state.cs = 980; goto _test_eof; 
	_test_eof981:  state.cs = 981; goto _test_eof; 
	_test_eof982:  state.cs = 982; goto _test_eof; 
	_test_eof983:  state.cs = 983; goto _test_eof; 
	_test_eof984:  state.cs = 984; goto _test_eof; 
	_test_eof985:  state.cs = 985; goto _test_eof; 
	_test_eof986:  state.cs = 986; goto _test_eof; 
	_test_eof987:  state.cs = 987; goto _test_eof; 
	_test_eof988:  state.cs = 988; goto _test_eof; 
	_test_eof989:  state.cs = 989; goto _test_eof; 
	_test_eof990:  state.cs = 990; goto _test_eof; 
	_test_eof991:  state.cs = 991; goto _test_eof; 
	_test_eof992:  state.cs = 992; goto _test_eof; 
	_test_eof993:  state.cs = 993; goto _test_eof; 
	_test_eof994:  state.cs = 994; goto _test_eof; 
	_test_eof995:  state.cs = 995; goto _test_eof; 
	_test_eof996:  state.cs = 996; goto _test_eof; 
	_test_eof997:  state.cs = 997; goto _test_eof; 
	_test_eof998:  state.cs = 998; goto _test_eof; 
	_test_eof999:  state.cs = 999; goto _test_eof; 
	_test_eof1000:  state.cs = 1000; goto _test_eof; 
	_test_eof1001:  state.cs = 1001; goto _test_eof; 
	_test_eof1002:  state.cs = 1002; goto _test_eof; 
	_test_eof1003:  state.cs = 1003; goto _test_eof; 
	_test_eof1004:  state.cs = 1004; goto _test_eof; 
	_test_eof1005:  state.cs = 1005; goto _test_eof; 
	_test_eof1006:  state.cs = 1006; goto _test_eof; 
	_test_eof1007:  state.cs = 1007; goto _test_eof; 
	_test_eof1008:  state.cs = 1008; goto _test_eof; 
	_test_eof1009:  state.cs = 1009; goto _test_eof; 
	_test_eof1010:  state.cs = 1010; goto _test_eof; 
	_test_eof1011:  state.cs = 1011; goto _test_eof; 
	_test_eof1012:  state.cs = 1012; goto _test_eof; 
	_test_eof1013:  state.cs = 1013; goto _test_eof; 
	_test_eof1014:  state.cs = 1014; goto _test_eof; 
	_test_eof1015:  state.cs = 1015; goto _test_eof; 
	_test_eof1016:  state.cs = 1016; goto _test_eof; 
	_test_eof1017:  state.cs = 1017; goto _test_eof; 
	_test_eof1018:  state.cs = 1018; goto _test_eof; 
	_test_eof1019:  state.cs = 1019; goto _test_eof; 
	_test_eof1020:  state.cs = 1020; goto _test_eof; 
	_test_eof1021:  state.cs = 1021; goto _test_eof; 
	_test_eof1022:  state.cs = 1022; goto _test_eof; 
	_test_eof1023:  state.cs = 1023; goto _test_eof; 
	_test_eof1024:  state.cs = 1024; goto _test_eof; 
	_test_eof1025:  state.cs = 1025; goto _test_eof; 
	_test_eof1026:  state.cs = 1026; goto _test_eof; 
	_test_eof1027:  state.cs = 1027; goto _test_eof; 
	_test_eof1028:  state.cs = 1028; goto _test_eof; 
	_test_eof1029:  state.cs = 1029; goto _test_eof; 
	_test_eof1030:  state.cs = 1030; goto _test_eof; 
	_test_eof1031:  state.cs = 1031; goto _test_eof; 
	_test_eof1032:  state.cs = 1032; goto _test_eof; 
	_test_eof1033:  state.cs = 1033; goto _test_eof; 
	_test_eof1034:  state.cs = 1034; goto _test_eof; 
	_test_eof1035:  state.cs = 1035; goto _test_eof; 
	_test_eof1036:  state.cs = 1036; goto _test_eof; 
	_test_eof1037:  state.cs = 1037; goto _test_eof; 
	_test_eof1038:  state.cs = 1038; goto _test_eof; 
	_test_eof1039:  state.cs = 1039; goto _test_eof; 
	_test_eof1040:  state.cs = 1040; goto _test_eof; 
	_test_eof1041:  state.cs = 1041; goto _test_eof; 
	_test_eof1042:  state.cs = 1042; goto _test_eof; 
	_test_eof1043:  state.cs = 1043; goto _test_eof; 
	_test_eof1044:  state.cs = 1044; goto _test_eof; 
	_test_eof1045:  state.cs = 1045; goto _test_eof; 
	_test_eof1046:  state.cs = 1046; goto _test_eof; 
	_test_eof1047:  state.cs = 1047; goto _test_eof; 
	_test_eof1048:  state.cs = 1048; goto _test_eof; 
	_test_eof1049:  state.cs = 1049; goto _test_eof; 
	_test_eof1050:  state.cs = 1050; goto _test_eof; 
	_test_eof1051:  state.cs = 1051; goto _test_eof; 
	_test_eof1052:  state.cs = 1052; goto _test_eof; 
	_test_eof1053:  state.cs = 1053; goto _test_eof; 
	_test_eof1054:  state.cs = 1054; goto _test_eof; 
	_test_eof1055:  state.cs = 1055; goto _test_eof; 
	_test_eof1056:  state.cs = 1056; goto _test_eof; 
	_test_eof1057:  state.cs = 1057; goto _test_eof; 
	_test_eof1058:  state.cs = 1058; goto _test_eof; 
	_test_eof1059:  state.cs = 1059; goto _test_eof; 
	_test_eof1060:  state.cs = 1060; goto _test_eof; 
	_test_eof1061:  state.cs = 1061; goto _test_eof; 
	_test_eof1062:  state.cs = 1062; goto _test_eof; 
	_test_eof1063:  state.cs = 1063; goto _test_eof; 
	_test_eof1064:  state.cs = 1064; goto _test_eof; 
	_test_eof1065:  state.cs = 1065; goto _test_eof; 
	_test_eof1066:  state.cs = 1066; goto _test_eof; 
	_test_eof1067:  state.cs = 1067; goto _test_eof; 
	_test_eof1068:  state.cs = 1068; goto _test_eof; 
	_test_eof1069:  state.cs = 1069; goto _test_eof; 
	_test_eof1070:  state.cs = 1070; goto _test_eof; 
	_test_eof1071:  state.cs = 1071; goto _test_eof; 
	_test_eof1072:  state.cs = 1072; goto _test_eof; 
	_test_eof1073:  state.cs = 1073; goto _test_eof; 
	_test_eof1074:  state.cs = 1074; goto _test_eof; 
	_test_eof1075:  state.cs = 1075; goto _test_eof; 
	_test_eof1076:  state.cs = 1076; goto _test_eof; 
	_test_eof1077:  state.cs = 1077; goto _test_eof; 
	_test_eof1078:  state.cs = 1078; goto _test_eof; 
	_test_eof1079:  state.cs = 1079; goto _test_eof; 
	_test_eof1080:  state.cs = 1080; goto _test_eof; 
	_test_eof1081:  state.cs = 1081; goto _test_eof; 
	_test_eof1082:  state.cs = 1082; goto _test_eof; 
	_test_eof1083:  state.cs = 1083; goto _test_eof; 
	_test_eof1084:  state.cs = 1084; goto _test_eof; 
	_test_eof1085:  state.cs = 1085; goto _test_eof; 
	_test_eof1086:  state.cs = 1086; goto _test_eof; 
	_test_eof1087:  state.cs = 1087; goto _test_eof; 
	_test_eof1088:  state.cs = 1088; goto _test_eof; 
	_test_eof1089:  state.cs = 1089; goto _test_eof; 
	_test_eof1090:  state.cs = 1090; goto _test_eof; 
	_test_eof1091:  state.cs = 1091; goto _test_eof; 
	_test_eof1092:  state.cs = 1092; goto _test_eof; 
	_test_eof1093:  state.cs = 1093; goto _test_eof; 
	_test_eof1094:  state.cs = 1094; goto _test_eof; 
	_test_eof1095:  state.cs = 1095; goto _test_eof; 
	_test_eof1096:  state.cs = 1096; goto _test_eof; 
	_test_eof1097:  state.cs = 1097; goto _test_eof; 
	_test_eof1098:  state.cs = 1098; goto _test_eof; 
	_test_eof1099:  state.cs = 1099; goto _test_eof; 
	_test_eof1100:  state.cs = 1100; goto _test_eof; 
	_test_eof1101:  state.cs = 1101; goto _test_eof; 
	_test_eof1102:  state.cs = 1102; goto _test_eof; 
	_test_eof1103:  state.cs = 1103; goto _test_eof; 
	_test_eof1104:  state.cs = 1104; goto _test_eof; 
	_test_eof1105:  state.cs = 1105; goto _test_eof; 
	_test_eof1106:  state.cs = 1106; goto _test_eof; 
	_test_eof1107:  state.cs = 1107; goto _test_eof; 
	_test_eof1108:  state.cs = 1108; goto _test_eof; 
	_test_eof1109:  state.cs = 1109; goto _test_eof; 
	_test_eof1110:  state.cs = 1110; goto _test_eof; 
	_test_eof1111:  state.cs = 1111; goto _test_eof; 
	_test_eof1112:  state.cs = 1112; goto _test_eof; 
	_test_eof1113:  state.cs = 1113; goto _test_eof; 
	_test_eof1114:  state.cs = 1114; goto _test_eof; 
	_test_eof1115:  state.cs = 1115; goto _test_eof; 
	_test_eof1116:  state.cs = 1116; goto _test_eof; 
	_test_eof1117:  state.cs = 1117; goto _test_eof; 
	_test_eof1118:  state.cs = 1118; goto _test_eof; 
	_test_eof1119:  state.cs = 1119; goto _test_eof; 
	_test_eof1120:  state.cs = 1120; goto _test_eof; 
	_test_eof1121:  state.cs = 1121; goto _test_eof; 
	_test_eof1122:  state.cs = 1122; goto _test_eof; 
	_test_eof1123:  state.cs = 1123; goto _test_eof; 
	_test_eof1124:  state.cs = 1124; goto _test_eof; 
	_test_eof1125:  state.cs = 1125; goto _test_eof; 
	_test_eof1126:  state.cs = 1126; goto _test_eof; 
	_test_eof1127:  state.cs = 1127; goto _test_eof; 
	_test_eof1128:  state.cs = 1128; goto _test_eof; 
	_test_eof1129:  state.cs = 1129; goto _test_eof; 
	_test_eof1130:  state.cs = 1130; goto _test_eof; 
	_test_eof1131:  state.cs = 1131; goto _test_eof; 
	_test_eof1132:  state.cs = 1132; goto _test_eof; 
	_test_eof1133:  state.cs = 1133; goto _test_eof; 
	_test_eof1134:  state.cs = 1134; goto _test_eof; 
	_test_eof1135:  state.cs = 1135; goto _test_eof; 
	_test_eof1136:  state.cs = 1136; goto _test_eof; 
	_test_eof1137:  state.cs = 1137; goto _test_eof; 
	_test_eof1138:  state.cs = 1138; goto _test_eof; 
	_test_eof1139:  state.cs = 1139; goto _test_eof; 
	_test_eof1140:  state.cs = 1140; goto _test_eof; 
	_test_eof1141:  state.cs = 1141; goto _test_eof; 
	_test_eof1142:  state.cs = 1142; goto _test_eof; 
	_test_eof1143:  state.cs = 1143; goto _test_eof; 
	_test_eof1144:  state.cs = 1144; goto _test_eof; 
	_test_eof1145:  state.cs = 1145; goto _test_eof; 
	_test_eof1146:  state.cs = 1146; goto _test_eof; 
	_test_eof1147:  state.cs = 1147; goto _test_eof; 
	_test_eof1148:  state.cs = 1148; goto _test_eof; 
	_test_eof1149:  state.cs = 1149; goto _test_eof; 
	_test_eof1150:  state.cs = 1150; goto _test_eof; 
	_test_eof1151:  state.cs = 1151; goto _test_eof; 
	_test_eof1152:  state.cs = 1152; goto _test_eof; 
	_test_eof1153:  state.cs = 1153; goto _test_eof; 
	_test_eof1154:  state.cs = 1154; goto _test_eof; 
	_test_eof1155:  state.cs = 1155; goto _test_eof; 
	_test_eof1156:  state.cs = 1156; goto _test_eof; 
	_test_eof1157:  state.cs = 1157; goto _test_eof; 
	_test_eof1158:  state.cs = 1158; goto _test_eof; 
	_test_eof1159:  state.cs = 1159; goto _test_eof; 
	_test_eof1160:  state.cs = 1160; goto _test_eof; 
	_test_eof1161:  state.cs = 1161; goto _test_eof; 
	_test_eof1162:  state.cs = 1162; goto _test_eof; 
	_test_eof1163:  state.cs = 1163; goto _test_eof; 
	_test_eof1164:  state.cs = 1164; goto _test_eof; 
	_test_eof1165:  state.cs = 1165; goto _test_eof; 
	_test_eof1166:  state.cs = 1166; goto _test_eof; 
	_test_eof1167:  state.cs = 1167; goto _test_eof; 
	_test_eof1168:  state.cs = 1168; goto _test_eof; 
	_test_eof1169:  state.cs = 1169; goto _test_eof; 
	_test_eof1170:  state.cs = 1170; goto _test_eof; 
	_test_eof1171:  state.cs = 1171; goto _test_eof; 
	_test_eof1172:  state.cs = 1172; goto _test_eof; 
	_test_eof1173:  state.cs = 1173; goto _test_eof; 
	_test_eof1174:  state.cs = 1174; goto _test_eof; 
	_test_eof1175:  state.cs = 1175; goto _test_eof; 
	_test_eof1176:  state.cs = 1176; goto _test_eof; 
	_test_eof1177:  state.cs = 1177; goto _test_eof; 
	_test_eof1178:  state.cs = 1178; goto _test_eof; 
	_test_eof1179:  state.cs = 1179; goto _test_eof; 
	_test_eof1180:  state.cs = 1180; goto _test_eof; 
	_test_eof1181:  state.cs = 1181; goto _test_eof; 
	_test_eof1182:  state.cs = 1182; goto _test_eof; 
	_test_eof1183:  state.cs = 1183; goto _test_eof; 
	_test_eof1184:  state.cs = 1184; goto _test_eof; 
	_test_eof1185:  state.cs = 1185; goto _test_eof; 
	_test_eof1186:  state.cs = 1186; goto _test_eof; 
	_test_eof1187:  state.cs = 1187; goto _test_eof; 
	_test_eof1188:  state.cs = 1188; goto _test_eof; 
	_test_eof1189:  state.cs = 1189; goto _test_eof; 
	_test_eof1190:  state.cs = 1190; goto _test_eof; 
	_test_eof1191:  state.cs = 1191; goto _test_eof; 
	_test_eof1192:  state.cs = 1192; goto _test_eof; 
	_test_eof1193:  state.cs = 1193; goto _test_eof; 
	_test_eof1194:  state.cs = 1194; goto _test_eof; 
	_test_eof1195:  state.cs = 1195; goto _test_eof; 
	_test_eof1196:  state.cs = 1196; goto _test_eof; 
	_test_eof1197:  state.cs = 1197; goto _test_eof; 
	_test_eof1198:  state.cs = 1198; goto _test_eof; 
	_test_eof1199:  state.cs = 1199; goto _test_eof; 
	_test_eof1200:  state.cs = 1200; goto _test_eof; 
	_test_eof1201:  state.cs = 1201; goto _test_eof; 
	_test_eof1202:  state.cs = 1202; goto _test_eof; 
	_test_eof1203:  state.cs = 1203; goto _test_eof; 
	_test_eof1204:  state.cs = 1204; goto _test_eof; 
	_test_eof1205:  state.cs = 1205; goto _test_eof; 
	_test_eof1206:  state.cs = 1206; goto _test_eof; 
	_test_eof1207:  state.cs = 1207; goto _test_eof; 
	_test_eof1208:  state.cs = 1208; goto _test_eof; 
	_test_eof1209:  state.cs = 1209; goto _test_eof; 
	_test_eof1210:  state.cs = 1210; goto _test_eof; 
	_test_eof1211:  state.cs = 1211; goto _test_eof; 
	_test_eof1212:  state.cs = 1212; goto _test_eof; 
	_test_eof1213:  state.cs = 1213; goto _test_eof; 
	_test_eof1214:  state.cs = 1214; goto _test_eof; 
	_test_eof1215:  state.cs = 1215; goto _test_eof; 
	_test_eof1216:  state.cs = 1216; goto _test_eof; 
	_test_eof1217:  state.cs = 1217; goto _test_eof; 
	_test_eof1218:  state.cs = 1218; goto _test_eof; 
	_test_eof1219:  state.cs = 1219; goto _test_eof; 
	_test_eof1220:  state.cs = 1220; goto _test_eof; 
	_test_eof1221:  state.cs = 1221; goto _test_eof; 
	_test_eof1222:  state.cs = 1222; goto _test_eof; 
	_test_eof1223:  state.cs = 1223; goto _test_eof; 
	_test_eof1224:  state.cs = 1224; goto _test_eof; 
	_test_eof1225:  state.cs = 1225; goto _test_eof; 
	_test_eof1226:  state.cs = 1226; goto _test_eof; 
	_test_eof1227:  state.cs = 1227; goto _test_eof; 
	_test_eof1228:  state.cs = 1228; goto _test_eof; 
	_test_eof1229:  state.cs = 1229; goto _test_eof; 
	_test_eof1230:  state.cs = 1230; goto _test_eof; 
	_test_eof1231:  state.cs = 1231; goto _test_eof; 
	_test_eof1232:  state.cs = 1232; goto _test_eof; 
	_test_eof1233:  state.cs = 1233; goto _test_eof; 
	_test_eof1234:  state.cs = 1234; goto _test_eof; 
	_test_eof1235:  state.cs = 1235; goto _test_eof; 
	_test_eof1236:  state.cs = 1236; goto _test_eof; 
	_test_eof1237:  state.cs = 1237; goto _test_eof; 
	_test_eof1238:  state.cs = 1238; goto _test_eof; 
	_test_eof1239:  state.cs = 1239; goto _test_eof; 
	_test_eof1240:  state.cs = 1240; goto _test_eof; 
	_test_eof1241:  state.cs = 1241; goto _test_eof; 
	_test_eof1242:  state.cs = 1242; goto _test_eof; 
	_test_eof1243:  state.cs = 1243; goto _test_eof; 
	_test_eof1244:  state.cs = 1244; goto _test_eof; 
	_test_eof1245:  state.cs = 1245; goto _test_eof; 
	_test_eof1246:  state.cs = 1246; goto _test_eof; 
	_test_eof1247:  state.cs = 1247; goto _test_eof; 
	_test_eof1248:  state.cs = 1248; goto _test_eof; 
	_test_eof1249:  state.cs = 1249; goto _test_eof; 
	_test_eof1250:  state.cs = 1250; goto _test_eof; 
	_test_eof1251:  state.cs = 1251; goto _test_eof; 
	_test_eof1252:  state.cs = 1252; goto _test_eof; 
	_test_eof1253:  state.cs = 1253; goto _test_eof; 
	_test_eof1254:  state.cs = 1254; goto _test_eof; 
	_test_eof1255:  state.cs = 1255; goto _test_eof; 
	_test_eof1256:  state.cs = 1256; goto _test_eof; 
	_test_eof1257:  state.cs = 1257; goto _test_eof; 
	_test_eof1258:  state.cs = 1258; goto _test_eof; 
	_test_eof1259:  state.cs = 1259; goto _test_eof; 
	_test_eof1260:  state.cs = 1260; goto _test_eof; 
	_test_eof1261:  state.cs = 1261; goto _test_eof; 
	_test_eof1262:  state.cs = 1262; goto _test_eof; 
	_test_eof1263:  state.cs = 1263; goto _test_eof; 
	_test_eof1264:  state.cs = 1264; goto _test_eof; 
	_test_eof1265:  state.cs = 1265; goto _test_eof; 
	_test_eof1266:  state.cs = 1266; goto _test_eof; 
	_test_eof1267:  state.cs = 1267; goto _test_eof; 
	_test_eof1268:  state.cs = 1268; goto _test_eof; 
	_test_eof1269:  state.cs = 1269; goto _test_eof; 
	_test_eof1270:  state.cs = 1270; goto _test_eof; 
	_test_eof1271:  state.cs = 1271; goto _test_eof; 
	_test_eof1272:  state.cs = 1272; goto _test_eof; 
	_test_eof1273:  state.cs = 1273; goto _test_eof; 
	_test_eof1274:  state.cs = 1274; goto _test_eof; 
	_test_eof1275:  state.cs = 1275; goto _test_eof; 
	_test_eof1276:  state.cs = 1276; goto _test_eof; 
	_test_eof1277:  state.cs = 1277; goto _test_eof; 
	_test_eof1278:  state.cs = 1278; goto _test_eof; 
	_test_eof1279:  state.cs = 1279; goto _test_eof; 
	_test_eof1280:  state.cs = 1280; goto _test_eof; 
	_test_eof1281:  state.cs = 1281; goto _test_eof; 
	_test_eof1282:  state.cs = 1282; goto _test_eof; 
	_test_eof1283:  state.cs = 1283; goto _test_eof; 
	_test_eof1284:  state.cs = 1284; goto _test_eof; 
	_test_eof1285:  state.cs = 1285; goto _test_eof; 
	_test_eof1286:  state.cs = 1286; goto _test_eof; 
	_test_eof1287:  state.cs = 1287; goto _test_eof; 
	_test_eof1288:  state.cs = 1288; goto _test_eof; 
	_test_eof1289:  state.cs = 1289; goto _test_eof; 
	_test_eof1290:  state.cs = 1290; goto _test_eof; 
	_test_eof1291:  state.cs = 1291; goto _test_eof; 
	_test_eof1292:  state.cs = 1292; goto _test_eof; 
	_test_eof1293:  state.cs = 1293; goto _test_eof; 
	_test_eof1294:  state.cs = 1294; goto _test_eof; 
	_test_eof1295:  state.cs = 1295; goto _test_eof; 
	_test_eof1296:  state.cs = 1296; goto _test_eof; 
	_test_eof1297:  state.cs = 1297; goto _test_eof; 
	_test_eof1298:  state.cs = 1298; goto _test_eof; 
	_test_eof1299:  state.cs = 1299; goto _test_eof; 
	_test_eof1300:  state.cs = 1300; goto _test_eof; 
	_test_eof1301:  state.cs = 1301; goto _test_eof; 
	_test_eof1302:  state.cs = 1302; goto _test_eof; 
	_test_eof1303:  state.cs = 1303; goto _test_eof; 
	_test_eof1304:  state.cs = 1304; goto _test_eof; 
	_test_eof1305:  state.cs = 1305; goto _test_eof; 
	_test_eof1306:  state.cs = 1306; goto _test_eof; 
	_test_eof1307:  state.cs = 1307; goto _test_eof; 
	_test_eof1308:  state.cs = 1308; goto _test_eof; 
	_test_eof1309:  state.cs = 1309; goto _test_eof; 
	_test_eof1310:  state.cs = 1310; goto _test_eof; 
	_test_eof1311:  state.cs = 1311; goto _test_eof; 
	_test_eof1312:  state.cs = 1312; goto _test_eof; 
	_test_eof1313:  state.cs = 1313; goto _test_eof; 
	_test_eof1314:  state.cs = 1314; goto _test_eof; 
	_test_eof1315:  state.cs = 1315; goto _test_eof; 
	_test_eof1316:  state.cs = 1316; goto _test_eof; 
	_test_eof1317:  state.cs = 1317; goto _test_eof; 
	_test_eof1318:  state.cs = 1318; goto _test_eof; 
	_test_eof1319:  state.cs = 1319; goto _test_eof; 
	_test_eof1320:  state.cs = 1320; goto _test_eof; 
	_test_eof1321:  state.cs = 1321; goto _test_eof; 
	_test_eof1322:  state.cs = 1322; goto _test_eof; 
	_test_eof1323:  state.cs = 1323; goto _test_eof; 
	_test_eof1324:  state.cs = 1324; goto _test_eof; 
	_test_eof1325:  state.cs = 1325; goto _test_eof; 
	_test_eof1326:  state.cs = 1326; goto _test_eof; 
	_test_eof1327:  state.cs = 1327; goto _test_eof; 
	_test_eof1328:  state.cs = 1328; goto _test_eof; 
	_test_eof1329:  state.cs = 1329; goto _test_eof; 
	_test_eof1330:  state.cs = 1330; goto _test_eof; 
	_test_eof1331:  state.cs = 1331; goto _test_eof; 
	_test_eof1332:  state.cs = 1332; goto _test_eof; 
	_test_eof1333:  state.cs = 1333; goto _test_eof; 
	_test_eof1334:  state.cs = 1334; goto _test_eof; 
	_test_eof1335:  state.cs = 1335; goto _test_eof; 
	_test_eof1336:  state.cs = 1336; goto _test_eof; 
	_test_eof1337:  state.cs = 1337; goto _test_eof; 
	_test_eof1338:  state.cs = 1338; goto _test_eof; 
	_test_eof1339:  state.cs = 1339; goto _test_eof; 
	_test_eof1340:  state.cs = 1340; goto _test_eof; 
	_test_eof1341:  state.cs = 1341; goto _test_eof; 
	_test_eof1342:  state.cs = 1342; goto _test_eof; 
	_test_eof1343:  state.cs = 1343; goto _test_eof; 
	_test_eof1344:  state.cs = 1344; goto _test_eof; 
	_test_eof1345:  state.cs = 1345; goto _test_eof; 
	_test_eof1346:  state.cs = 1346; goto _test_eof; 
	_test_eof1347:  state.cs = 1347; goto _test_eof; 
	_test_eof1348:  state.cs = 1348; goto _test_eof; 
	_test_eof1349:  state.cs = 1349; goto _test_eof; 
	_test_eof1350:  state.cs = 1350; goto _test_eof; 

	_test_eof: {}
	if ( ( state.p) == ( state.eof) )
	{
	switch (  state.cs ) {
	case 1354: 
#line 247 "configparser.rl"
	{ init_species(spe); }
	break;
	case 1351: 
#line 285 "configparser.rl"
	{ init_design(des); }
	break;
	case 1355: 
#line 327 "configparser.rl"
	{ init_terrain(ter); }
	break;
	case 1353: 
#line 366 "configparser.rl"
	{ init_levelskin_(lev); }
	break;
#line 19665 "configparser.h"
	}
	}

	_out: {}
	}

#line 405 "configparser.rl"

        // Avoid spurious gcc warnings.
        (void)ConfigParser_first_final;
        (void)ConfigParser_en_strchar_escape;
        (void)ConfigParser_en_one_species;
        (void)ConfigParser_en_one_design;
        (void)ConfigParser_en_one_terrain;
        (void)ConfigParser_en_one_levelskin;
        (void)ConfigParser_en_main;

        if (state.cs == ConfigParser_error) {
            throw std::runtime_error("Parse error. Unconsumed input: " + std::string(state.p, state.pe));
        }

        if (state.ts == 0) {
            have = 0;

        } else {
            have = state.pe - state.ts;
            ::memmove(buf, state.ts, have);
            state.te = buf + (state.te - state.ts);
            state.ts = buf;
        }
    }
}

}

#endif
