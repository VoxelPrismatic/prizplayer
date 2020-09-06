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

EVT = {
    "INPUT": [771],
    "KEY": [769],
    "KEYDOWN": [768],
    "MOUSEMOVE": [1024],
    "WHEEL": [1027],
    "CLICK": [1026],
    "WINDOW": [32768, 32770, 512],
    "QUIT": [256]
}

KEY = {
    "UP": 82,
    "DOWN": 81,
    "LEFT": 80,
    "RIGHT": 79,
    "CTRL": 224,
    "ALT": 226,
    "SHIFT": 225,
    "TAB": 43,
    "ESC": 41,
    "BKSP": 42,
    "ENTER": 40,
    "DEL": 76,
    "INS": 73,
    "PAUSE": 72,
    "SCROLL": 71,
    "PREV_PAGE": 270,
    "NEXT_PAGE": 271,
    "NEXT_SONG": 258,
    "PREV_SONG": 259,
    "PLAY_PAUSE": 261,
    "STAR": 274,

    "F1": 58,
    "F2": 59,
    "F3": 60,
    "F4": 61,
    "F5": 62,
    "F6": 63,
    "F7": 64,
    "F8": 65,
    "F9": 66,
    "F10": 67,
    "F11": 68,
    "F12": 69,
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

echo("         -------================[ PRIZ  PLAYER ]================-------         ", color = 0x00ffff)
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
    }
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
