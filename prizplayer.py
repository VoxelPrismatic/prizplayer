#!/bin/python3

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository
import time
import argparse
import os
from utils.folder_slash import *
import subprocess

file_formats = [
    ".3gp", ".asf", ".avi", ".dvr-ms", ".flv",
    ".mkv", ".midi", ".mid", ".qtff", ".mp4",
    ".mp3", ".mp2", ".mpeg", ".m4a", ".ogg",
    ".ogm", ".wav", ".aiff", ".mxf", ".vob",
    ".rm", ".aac", ".ac3", ".alac", ".amr",
    ".dts", ".xm", ".flac", ".mace", ".mod",
    ".opus", ".pls", ".qcp", ".qdm2", ".qdmc",
    ".wma", ".wmv", ".webm", ".ogv"
]

def grab_files(root, fmts = file_formats):
    files = []
    if root[-1] != "/":
        root += "/"
    for dp, dn, fn in os.walk(root, followlinks = True):
        for f in fn:
            if any(f.lower().endswith(x) for x in fmts):
                files.append(os.path.join(dp, f))
    return files

parser = argparse.ArgumentParser()
parser.add_argument('files', help = "List of files to add to queue right away", nargs = '*')
args = parser.parse_args()

running = False

if folder_slash == "/":
    commands = [
        ["pgrep", "prizplayer"],
        ["pidof", "-x", "prizplayer.py"],
        ["ps", "h", "-C", "prizplayer.py", "-o", "pid"]
    ]
    for command in commands:
        try:
            proc = subprocess.run(command, capture_output = True)
            print(proc.stdout.strip(), proc.stdout.strip() == f"{os.getpid()}".encode())
            if proc.stdout.strip() != f"{os.getpid()}".encode():
                running = True
        except:
            pass

if running:
    q = open(s("./cache/adding"), "r").read()
    q += "\n"
    if "\n".join(args.files) not in q:
        q += "\n".join(args.files)
    open(s("./cache/adding"), "w").write(q.strip())
    exit()
open(s("./cache/running"), "w+").write("True")

from utils.tokens import *
from utils.terminal import *

import sys
import json
import io
import signal
import vlc
import random
import traceback
import base64
import tinytag
import pynput
from pynput.keyboard import Key
import pygame

def try_print(*a, **kw):
    try:
        print(*a, **kw)
    except (BrokenPipeError, OSError):
        pass

try_print("\x1b[2A\x1b[94;1mPRIZ PLAYER ;]\x1b[0m\x1b[0K\n\x1b[2K")

kb = pynput.keyboard.Controller()

def kb_press(*keys):
    global kb
    for key in keys:
        kb.press(key)
    for key in list(keys)[::-1]:
        kb.release(key)

def kill():
    global tags, queue, shuffle, repeat, single
    try:
        os.remove(s(f"./assets/{ss(tags.artist)}-{ss(tags.album)}-{ss(tags.title)}"))
    except:
        pass
    if queue:
        open("./queues/LATEST.PRZ", "w+").write("\n".join(queue))
    prefs = json.loads(open(s("./conf.json")).read())
    prefs["shuffle"] = shuffle
    prefs["repeat"] = repeat
    prefs["single"] = single
    prefs["size"] = list(pygame.display.get_window_size())
    open("conf.json", "w+").write(json.dumps(prefs, indent = 4))
    open("./cache/running", "w+").write("False")
    os.system(f"kill -s 9 {os.getpid()}")

queue = []

pygame.key.set_repeat(500, 50)

__available_keys = []

screens = [
    "file_chooser",
    "show_queue",
    "show_shortcuts",
    "show_prefs",
    "show_albums",
    "save_queue",
    "load_queue",
    "show_player",
    "show_tricks",
    "util_os_interface",
]

if sys.executable.startswith("/"):
    folder_slash = "/"
else:
    folder_slash = "\\"

def s(dr):
    return dr.replace("/", folder_slash)

for screen in screens:
    try_print("\x1b[93;1mLOADING:\x1b[0m", "./screens/" + screen + ".py")
    exec(open(s(f"./screens/" + screen + ".py")).read())

handle_dbus()

def _screen_management_(l):
    times_around = 0
    keys = {
        "o": file_chooser,
        "q": show_queue,
        "f1": show_shortcuts,
        "c": show_prefs,
        "m": show_albums,
        "p": show_player,
        "s": save_queue,
        "l": load_queue,
        "t": show_tricks,
    }
    for key in list(keys):
        keys[key.upper()] = keys[key]
    global __available_keys, in_player
    __available_keys = list(keys)
    if l is None:
        return
    while True:
        global in_player
        l = keys[l]()
        in_player = False
        pygame.key.set_repeat(500, 50)

try:
    _screen_management_(None)
except NotImplementedError:
    pass

try:
    doit = True
    if args.files:
        queue = args.files
        fix_queue()
        _screen_management_("p")
        doit = False
    skip_draw = False
    while doit:
        if not skip_draw:
            TERM.hold = True
            clear(0x112222)
            echo("-------===============[ PRIZ PLAYER ;] ]===============-------", color = 0x00ffff, center = TERM.w, font = FONT.b)
            echo()
            echo_n("Welcome to the ", color = 0xeeeeee, font = FONT.r)
            echo("PRIZ PLAYER!", font = FONT.b)
            echo()
            echo("Press 'o' to open a playlist or file", font = FONT.r)
            echo()
            echo("For Linux users, press ALT+SHIFT+F12 to re-enable compositing")
            echo()
            echo(" TAG YOUR MUSIC ", center = TERM.w, char = "-", )
            echo("Visit https://prz0.github.io/prizplayer/wiki/tagging")
            TERM.foot()
            TERM.y -= 1
            echo("PRIZ ;] // voxelprismatic.github.io // @VoxelPrismatic", center = TERM.w, color = 0x00ffff, font = FONT.b)
            echo("-" * TERM.w, color = 0x008888)
            echo_n("o - Open file  /  m - Your albums  /  F1 - More screens")
            echo(";]", right = TERM.rem)
            redraw()
        skip_draw = True
        evt = pygame.event.wait()
        if evt.type in EVT["QUIT"]:
            kill()
        elif evt.type in EVT["WINDOW"]:
            redraw()
            skip_draw = False
        elif evt.type in EVT["INPUT"]:
            if evt.text in __available_keys:
                _screen_management_(evt.text)
        elif evt.type in EVT["KEY"] and evt.scancode == KEY["F1"]:
            _screen_management_("f1")
        try_print(f"\x1b[94;1m{evt.type}\x1b[0m:", evt)
        try_print(dir(evt))
except Exception as ex:
    try:
        open(f"/home/{os.getlogin()}/.config/prizplayer/tb.txt", "w+").write(
            f"\n{str(type(ex))[8:-2]}: {ex}"
            "\n".join(traceback.format_tb(ex.__traceback__))
        )
    except:
        pass
    raise ex
