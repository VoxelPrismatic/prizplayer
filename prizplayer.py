#!/bin/python3

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

import os
import time
import sys
import json
import io
import signal
from eyed3 import id3
import eyed3
import vlc
import pygame
import random
import traceback

print("\x1b[2A\x1b[94;1mPRIZ PLAYER ;]\x1b[0m\x1b[0K\n\x1b[2K")

def kill():
    os.system(f"kill -s 9 {os.getpid()}")

def rgb(hx):
    st = f"{hx:06x}"
    r = st[0:2]
    g = st[2:4]
    b = st[4:6]
    return int(r, 16), int(g, 16), int(b, 16)

queue = []

term_w = 660
term_h = 500
term = pygame.display.set_mode((0, 0))
pygame.mixer.quit()
img = pygame.Surface.convert(pygame.image.load("./assets/icon.png"))
pygame.display.set_icon(img)
pygame.display.set_caption("PRIZ PLAYER ;]")
pygame.display.update()
term = pygame.display.set_mode((term_w, term_h))
pygame.init()
term_y = 0
term_x = 0
bg_color = 0x112222
hold_display = False

font_size = 16
font_b = pygame.font.Font('./font/UbuntuMono-B.ttf', font_size)
font_bi = pygame.font.Font('./font/UbuntuMono-BI.ttf', font_size)
font_r = pygame.font.Font('./font/UbuntuMono-R.ttf', font_size)
font_ri = pygame.font.Font('./font/UbuntuMono-RI.ttf', font_size)
cur_font = font_r
cur_color = 0x112222

class Keys:
    def __init__(self, *codes):
        self.codes = codes
    def __eq__(self, other: int):
        return any(other == code for code in self.codes)
    def __contains__(self, other: int):
        return any(other == code for code in self.codes)
    def __list__(self):
        return self.codes
    def __iter__(self):
        for code in self.codes:
            yield code

EVT = {
    "INPUT": Keys(771),
    "KEY": Keys(769),
    "KEYDOWN": Keys(768),
    "KEYUP": Keys(769),
    "MOUSEMOVE": Keys(1024),
    "WHEEL": Keys(1027),
    "CLICK": Keys(1026),
    "WINDOW": Keys(32768, 32770, 512),
    "QUIT": Keys(256)
}

KEY = {
    "UP": Keys(82),
    "DOWN": Keys(81),
    "LEFT": Keys(80),
    "RIGHT": Keys(79),

    "CTRL": Keys(224, 228),
    "ALT": Keys(226, 230),
    "SHIFT": Keys(225, 229),
    "CTX": Keys(101),
    "ESC": Keys(41),
    "DEL": Keys(76),
    "INS": Keys(73),
    "TAB": Keys(43),
    "BKSP": Keys(42),
    "ENTER": Keys(40, 88),
    "PAUSE": Keys(72),

    "SCROLL_LOCK": Keys(71),
    "NUM_LOCK": Keys(83),
    "CAPS_LOCK": Keys(57),

    "PREV_PAGE": Keys(270),
    "NEXT_PAGE": Keys(271),

    "NEXT_SONG": Keys(258),
    "PREV_SONG": Keys(259),
    "PLAY_PAUSE": Keys(261),

    "STAR": Keys(274),

    "PAGE_UP": Keys(75),
    "PAGE_DOWN": Keys(78),
    "HOME": Keys(74),
    "END": Keys(77),

    "F1": Keys(58),
    "F2": Keys(59),
    "F3": Keys(60),
    "F4": Keys(61),
    "F5": Keys(62),
    "F6": Keys(63),
    "F7": Keys(64),
    "F8": Keys(65),
    "F9": Keys(66),
    "F10": Keys(67),
    "F11": Keys(68),
    "F12": Keys(69),
}

def redraw():
    global hold_display
    hold_display = False
    pygame.display.update()

def put(txt, x, y, color = cur_color, font = cur_font, cls = True):
    x += 10
    y += 10
    global cur_font, cur_color, bg_color, hold_display
    cur_font = font
    cur_color = color
    text = cur_font.render(txt, True, rgb(cur_color))
    ls = text.get_rect()
    ls[0] += x
    ls[1] += y
    if cls:
        term.fill(rgb(bg_color), rect = ls)
    ls[2] += x
    ls[3] += y
    term.blit(text, ls)
    if not hold_display:
        pygame.display.update()


def echo(txt = " ", color = None, font = None):
    global term_x, term_y
    global cur_font, cur_color
    put(txt, term_x * 8, term_y * 16, color or cur_color, font or cur_font, cls = False)
    term_y += 1
    term_x = 0


def echo_n(txt = " ", color = None, font = None):
    global term_x, term_y
    global cur_font, cur_color
    put(txt, term_x * 8, term_y * 16, color or cur_color, font or cur_font, cls = False)
    term_x += len(txt)


def clear(color = None):
    global term_x, term_y, bg_color, hold_display
    term.fill(rgb(color or bg_color), rect = (0, 0, term_w, term_h))
    if not hold_display:
        pygame.display.update()
    term_y = 0
    term_x = 0
    bg_color = color or bg_color


clear()
echo("ree", color = 0x112222, font = font_b)
clear()

echo("         -------===============[ PRIZ PLAYER ;] ]===============-------         ", color = 0x00ffff)
echo()
echo_n("Welcome to the ", color = 0xeeeeee, font = font_r)
echo("PRIZ PLAYER!", font = font_b)
echo()
echo("Press 'o' to open a playlist or file", font = font_r)
echo()
echo("For Linux users, press ALT+SHIFT+F12 to re-enable compositing")
echo()
echo(f"{' CREDITS ':-^80}")
echo("Created by PRIZ ;]")
echo_n("> Twitter: ", font = font_r)
echo("@VoxelPrismatic", font = font_b)
echo_n("> Discord: ", font = font_r)
echo("PRIZ ;]#9244", font = font_b)
echo_n("> Website: ", font = font_r)
echo("https://voxelprismatic.github.io/", font = font_b)
echo(font = font_r)
echo("Resources")
echo_n("> PyGame ", font = font_b)
echo(pygame.__version__, font = font_r)
echo_n("> eyeD3 ", font = font_b)
echo(eyed3.version, font = font_r)
echo_n("> VLC ", font = font_b)
echo(vlc.__version__, font = font_r)
echo()
echo(f"{' TAG YOUR MUSIC ':-^80}")
echo("Windows/macOS users - Use MP3TAG: https://mp3tag.de/")
echo("Linux users --------- Use EasyTAG: https://wiki.gnome.org/Apps/EasyTAG")
echo("> Available on Debian and Ubuntu via apt-get")

term_y = 28
echo("--------------------------------------------------------------------------------", color = 0x008888, font = font_b)
echo("o - Open file  /  m - Your albums  /  F1 - More screens                       ;]")

pygame.key.set_repeat(500, 50)

__available_keys = []

screens = [
    "file_chooser",
    "show_queue",
    "show_shortcuts",
    "show_prefs",
    "show_albums",
    "show_player",
    "save_queue",
    #"util_os_interface"
]

for screen in screens:
    print("\x1b[93;1mLOADING:\x1b[0m", "./screens/" + screen + ".py")
    exec(open("./screens/" + screen + ".py").read())

def _screen_management_(l):
    times_around = 0
    keys = {
        "o": file_chooser,
        "q": show_queue,
        "f1": show_shortcuts,
        "l": show_prefs,
        "m": show_albums,
        "p": show_player,
        "s": save_queue,
    }
    for key in list(keys):
        keys[key.upper()] = keys[key]
    global __available_keys
    __available_keys = list(keys)
    while True:
        try:
            l = keys[l]()
        except KeyError:
            raise NotImplementedError("That key wasn't added yet")

try:
    _screen_management_(None)
except NotImplementedError:
    pass

try:
    while True:
        evt = pygame.event.wait()
        if evt.type in EVT["QUIT"]:
            kill()
        elif evt.type in EVT["WINDOW"]:
            pygame.display.update()
        elif evt.type in EVT["INPUT"]:
            if evt.text in __available_keys:
                _screen_management_(evt.text)
        elif evt.type in EVT["KEY"] and evt.scancode == KEY["F1"]:
            _screen_management_("f1")
        print(f"\x1b[94;1m{evt.type}\x1b[0m:", evt)
        print(dir(evt))
except Exception as ex:
    open("/home/priz/TRANSFER/prizplayer/tb.txt", "w+").write(f"""
{str(type(ex))[8:-2]}: {ex}
""" + "\n".join(traceback.format_tb(ex.__traceback__))
)
    raise ex
