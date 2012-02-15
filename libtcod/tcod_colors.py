#
# libtcod 1.5.1 python wrapper
# Copyright (c) 2008,2009,2010 Jice & Mingos
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * The name of Jice or Mingos may not be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY JICE AND MINGOS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL JICE OR MINGOS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

#
# Useful libtcod constants which do not depend on ctypes or library availability.
#
#

class Color:

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    def __repr__(self):
        return "Color(%d,%d,%d)" % (self.r, self.g, self.b)

    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b

# default colors
# grey levels
black=Color(0,0,0)
darkest_grey=Color(31,31,31)
darker_grey=Color(63,63,63)
dark_grey=Color(95,95,95)
grey=Color(127,127,127)
light_grey=Color(159,159,159)
lighter_grey=Color(191,191,191)
lightest_grey=Color(223,223,223)
darkest_gray=Color(31,31,31)
darker_gray=Color(63,63,63)
dark_gray=Color(95,95,95)
gray=Color(127,127,127)
light_gray=Color(159,159,159)
lighter_gray=Color(191,191,191)
lightest_gray=Color(223,223,223)
white=Color(255,255,255)

# sepia
darkest_sepia=Color(31,24,15)
darker_sepia=Color(63,50,31)
dark_sepia=Color(94,75,47)
sepia=Color(127,101,63)
light_sepia=Color(158,134,100)
lighter_sepia=Color(191,171,143)
lightest_sepia=Color(222,211,195)

#standard colors
red=Color(255,0,0)
flame=Color(255,63,0)
orange=Color(255,127,0)
amber=Color(255,191,0)
yellow=Color(255,255,0)
lime=Color(191,255,0)
chartreuse=Color(127,255,0)
green=Color(0,255,0)
sea=Color(0,255,127)
turquoise=Color(0,255,191)
cyan=Color(0,255,255)
sky=Color(0,191,255)
azure=Color(0,127,255)
blue=Color(0,0,255)
han=Color(63,0,255)
violet=Color(127,0,255)
purple=Color(191,0,255)
fuchsia=Color(255,0,255)
magenta=Color(255,0,191)
pink=Color(255,0,127)
crimson=Color(255,0,63)

# dark colors
dark_red=Color(191,0,0)
dark_flame=Color(191,47,0)
dark_orange=Color(191,95,0)
dark_amber=Color(191,143,0)
dark_yellow=Color(191,191,0)
dark_lime=Color(143,191,0)
dark_chartreuse=Color(95,191,0)
dark_green=Color(0,191,0)
dark_sea=Color(0,191,95)
dark_turquoise=Color(0,191,143)
dark_cyan=Color(0,191,191)
dark_sky=Color(0,143,191)
dark_azure=Color(0,95,191)
dark_blue=Color(0,0,191)
dark_han=Color(47,0,191)
dark_violet=Color(95,0,191)
dark_purple=Color(143,0,191)
dark_fuchsia=Color(191,0,191)
dark_magenta=Color(191,0,143)
dark_pink=Color(191,0,95)
dark_crimson=Color(191,0,47)

# darker colors
darker_red=Color(127,0,0)
darker_flame=Color(127,31,0)
darker_orange=Color(127,63,0)
darker_amber=Color(127,95,0)
darker_yellow=Color(127,127,0)
darker_lime=Color(95,127,0)
darker_chartreuse=Color(63,127,0)
darker_green=Color(0,127,0)
darker_sea=Color(0,127,63)
darker_turquoise=Color(0,127,95)
darker_cyan=Color(0,127,127)
darker_sky=Color(0,95,127)
darker_azure=Color(0,63,127)
darker_blue=Color(0,0,127)
darker_han=Color(31,0,127)
darker_violet=Color(63,0,127)
darker_purple=Color(95,0,127)
darker_fuchsia=Color(127,0,127)
darker_magenta=Color(127,0,95)
darker_pink=Color(127,0,63)
darker_crimson=Color(127,0,31)

# darkest colors
darkest_red=Color(63,0,0)
darkest_flame=Color(63,15,0)
darkest_orange=Color(63,31,0)
darkest_amber=Color(63,47,0)
darkest_yellow=Color(63,63,0)
darkest_lime=Color(47,63,0)
darkest_chartreuse=Color(31,63,0)
darkest_green=Color(0,63,0)
darkest_sea=Color(0,63,31)
darkest_turquoise=Color(0,63,47)
darkest_cyan=Color(0,63,63)
darkest_sky=Color(0,47,63)
darkest_azure=Color(0,31,63)
darkest_blue=Color(0,0,63)
darkest_han=Color(15,0,63)
darkest_violet=Color(31,0,63)
darkest_purple=Color(47,0,63)
darkest_fuchsia=Color(63,0,63)
darkest_magenta=Color(63,0,47)
darkest_pink=Color(63,0,31)
darkest_crimson=Color(63,0,15)

# light colors
light_red=Color(255,114,114)
light_flame=Color(255,149,114)
light_orange=Color(255,184,114)
light_amber=Color(255,219,114)
light_yellow=Color(255,255,114)
light_lime=Color(219,255,114)
light_chartreuse=Color(184,255,114)
light_green=Color(114,255,114)
light_sea=Color(114,255,184)
light_turquoise=Color(114,255,219)
light_cyan=Color(114,255,255)
light_sky=Color(114,219,255)
light_azure=Color(114,184,255)
light_blue=Color(114,114,255)
light_han=Color(149,114,255)
light_violet=Color(184,114,255)
light_purple=Color(219,114,255)
light_fuchsia=Color(255,114,255)
light_magenta=Color(255,114,219)
light_pink=Color(255,114,184)
light_crimson=Color(255,114,149)

#lighter colors
lighter_red=Color(255,165,165)
lighter_flame=Color(255,188,165)
lighter_orange=Color(255,210,165)
lighter_amber=Color(255,232,165)
lighter_yellow=Color(255,255,165)
lighter_lime=Color(232,255,165)
lighter_chartreuse=Color(210,255,165)
lighter_green=Color(165,255,165)
lighter_sea=Color(165,255,210)
lighter_turquoise=Color(165,255,232)
lighter_cyan=Color(165,255,255)
lighter_sky=Color(165,232,255)
lighter_azure=Color(165,210,255)
lighter_blue=Color(165,165,255)
lighter_han=Color(188,165,255)
lighter_violet=Color(210,165,255)
lighter_purple=Color(232,165,255)
lighter_fuchsia=Color(255,165,255)
lighter_magenta=Color(255,165,232)
lighter_pink=Color(255,165,210)
lighter_crimson=Color(255,165,188)

# lightest colors
lightest_red=Color(255,191,191)
lightest_flame=Color(255,207,191)
lightest_orange=Color(255,223,191)
lightest_amber=Color(255,239,191)
lightest_yellow=Color(255,255,191)
lightest_lime=Color(239,255,191)
lightest_chartreuse=Color(223,255,191)
lightest_green=Color(191,255,191)
lightest_sea=Color(191,255,223)
lightest_turquoise=Color(191,255,239)
lightest_cyan=Color(191,255,255)
lightest_sky=Color(191,239,255)
lightest_azure=Color(191,223,255)
lightest_blue=Color(191,191,255)
lightest_han=Color(207,191,255)
lightest_violet=Color(223,191,255)
lightest_purple=Color(239,191,255)
lightest_fuchsia=Color(255,191,255)
lightest_magenta=Color(255,191,239)
lightest_pink=Color(255,191,223)
lightest_crimson=Color(255,191,207)

# desaturated colors
desaturated_red=Color(127,63,63)
desaturated_flame=Color(127,79,63)
desaturated_orange=Color(127,95,63)
desaturated_amber=Color(127,111,63)
desaturated_yellow=Color(127,127,63)
desaturated_lime=Color(111,127,63)
desaturated_chartreuse=Color(95,127,63)
desaturated_green=Color(63,127,63)
desaturated_sea=Color(63,127,95)
desaturated_turquoise=Color(63,127,111)
desaturated_cyan=Color(63,127,127)
desaturated_sky=Color(63,111,127)
desaturated_azure=Color(63,95,127)
desaturated_blue=Color(63,63,127)
desaturated_han=Color(79,63,127)
desaturated_violet=Color(95,63,127)
desaturated_purple=Color(111,63,127)
desaturated_fuchsia=Color(127,63,127)
desaturated_magenta=Color(127,63,111)
desaturated_pink=Color(127,63,95)
desaturated_crimson=Color(127,63,79)

# metallic
brass=Color(191,151,96)
copper=Color(197,136,124)
gold=Color(229,191,0)
silver=Color(203,203,203)

# miscellaneous
celadon=Color(172,255,175)
peach=Color(255,159,127)


# background rendering modes
BKGND_NONE = 0
BKGND_SET = 1
BKGND_MULTIPLY = 2
BKGND_LIGHTEN = 3
BKGND_DARKEN = 4
BKGND_SCREEN = 5
BKGND_COLOR_DODGE = 6
BKGND_COLOR_BURN = 7
BKGND_ADD = 8
BKGND_ADDA = 9
BKGND_BURN = 10
BKGND_OVERLAY = 11
BKGND_ALPH = 12
BKGND_DEFAULT=13

def BKGND_ALPHA(a):
    return BKGND_ALPH | (int(a * 255) << 8)

def BKGND_ADDALPHA(a):
    return BKGND_ADDA | (int(a * 255) << 8)

# non blocking key events types
KEY_PRESSED = 1
KEY_RELEASED = 2
# key codes
KEY_NONE = 0
KEY_ESCAPE = 1
KEY_BACKSPACE = 2
KEY_TAB = 3
KEY_ENTER = 4
KEY_SHIFT = 5
KEY_CONTROL = 6
KEY_ALT = 7
KEY_PAUSE = 8
KEY_CAPSLOCK = 9
KEY_PAGEUP = 10
KEY_PAGEDOWN = 11
KEY_END = 12
KEY_HOME = 13
KEY_UP = 14
KEY_LEFT = 15
KEY_RIGHT = 16
KEY_DOWN = 17
KEY_PRINTSCREEN = 18
KEY_INSERT = 19
KEY_DELETE = 20
KEY_LWIN = 21
KEY_RWIN = 22
KEY_APPS = 23
KEY_0 = 24
KEY_1 = 25
KEY_2 = 26
KEY_3 = 27
KEY_4 = 28
KEY_5 = 29
KEY_6 = 30
KEY_7 = 31
KEY_8 = 32
KEY_9 = 33
KEY_KP0 = 34
KEY_KP1 = 35
KEY_KP2 = 36
KEY_KP3 = 37
KEY_KP4 = 38
KEY_KP5 = 39
KEY_KP6 = 40
KEY_KP7 = 41
KEY_KP8 = 42
KEY_KP9 = 43
KEY_KPADD = 44
KEY_KPSUB = 45
KEY_KPDIV = 46
KEY_KPMUL = 47
KEY_KPDEC = 48
KEY_KPENTER = 49
KEY_F1 = 50
KEY_F2 = 51
KEY_F3 = 52
KEY_F4 = 53
KEY_F5 = 54
KEY_F6 = 55
KEY_F7 = 56
KEY_F8 = 57
KEY_F9 = 58
KEY_F10 = 59
KEY_F11 = 60
KEY_F12 = 61
KEY_NUMLOCK = 62
KEY_SCROLLLOCK = 63
KEY_SPACE = 64
KEY_CHAR = 65
# special chars
# single walls
CHAR_HLINE = 196
CHAR_VLINE = 179
CHAR_NE = 191
CHAR_NW = 218
CHAR_SE = 217
CHAR_SW = 192
CHAR_TEEW = 180
CHAR_TEEE = 195
CHAR_TEEN = 193
CHAR_TEES = 194
CHAR_CROSS = 197
# double walls
CHAR_DHLINE = 205
CHAR_DVLINE = 186
CHAR_DNE = 187
CHAR_DNW = 201
CHAR_DSE = 188
CHAR_DSW = 200
CHAR_DTEEW = 185
CHAR_DTEEE = 204
CHAR_DTEEN = 202
CHAR_DTEES = 203
CHAR_DCROSS = 206
# blocks
CHAR_BLOCK1 = 176
CHAR_BLOCK2 = 177
CHAR_BLOCK3 = 178
# arrows
CHAR_ARROW_N = 24
CHAR_ARROW_S = 25
CHAR_ARROW_E = 26
CHAR_ARROW_W = 27
# arrows without tail
CHAR_ARROW2_N = 30
CHAR_ARROW2_S = 31
CHAR_ARROW2_E = 16
CHAR_ARROW2_W = 17
# double arrows
CHAR_DARROW_H = 29
CHAR_DARROW_V = 18
# GUI stuff
CHAR_CHECKBOX_UNSET = 224
CHAR_CHECKBOX_SET = 225
CHAR_RADIO_UNSET = 9
CHAR_RADIO_SET = 10
# sub-pixel resolution kit
CHAR_SUBP_NW = 226
CHAR_SUBP_NE = 227
CHAR_SUBP_N = 228
CHAR_SUBP_SE = 229
CHAR_SUBP_DIAG = 230
CHAR_SUBP_E = 231
CHAR_SUBP_SW = 232
# font flags
FONT_LAYOUT_ASCII_INCOL = 1
FONT_LAYOUT_ASCII_INROW = 2
FONT_TYPE_GREYSCALE = 4
FONT_TYPE_GRAYSCALE = 4
FONT_LAYOUT_TCOD = 8
# color control codes
COLCTRL_1=1
COLCTRL_2=2
COLCTRL_3=3
COLCTRL_4=4
COLCTRL_5=5
COLCTRL_NUMBER=5
COLCTRL_FORE_RGB=6
COLCTRL_BACK_RGB=7
COLCTRL_STOP=8
# renderers
RENDERER_GLSL=0
RENDERER_OPENGL=1
RENDERER_SDL=2
NB_RENDERERS=3
# alignment
LEFT=0
RIGHT=1
CENTER=2

# events
EVENT_KEY_PRESS=1
EVENT_KEY_RELEASE=2
EVENT_KEY=EVENT_KEY_PRESS|EVENT_KEY_RELEASE
EVENT_MOUSE_MOVE=4
EVENT_MOUSE_PRESS=8
EVENT_MOUSE_RELEASE=16
EVENT_MOUSE=EVENT_MOUSE_MOVE|EVENT_MOUSE_PRESS|EVENT_MOUSE_RELEASE
EVENT_ANY=EVENT_KEY|EVENT_MOUSE

FOV_BASIC = 0
FOV_DIAMOND = 1
FOV_SHADOW = 2
FOV_PERMISSIVE_0 = 3
FOV_PERMISSIVE_1 = 4
FOV_PERMISSIVE_2 = 5
FOV_PERMISSIVE_3 = 6
FOV_PERMISSIVE_4 = 7
FOV_PERMISSIVE_5 = 8
FOV_PERMISSIVE_6 = 9
FOV_PERMISSIVE_7 = 10
FOV_PERMISSIVE_8 = 11
FOV_RESTRICTIVE = 12
NB_FOV_ALGORITHMS = 13


