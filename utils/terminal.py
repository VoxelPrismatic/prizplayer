from .folder_slash import *
import pygame
import time
import json
import sys
import unicodedata
import subprocess

compositor = ""

if sys.platform == "linux":
    proc = subprocess.run(["inxi", "-Sxx"], capture_output = True)
    open("/home/priz/TRANSFER/prizplayer/kwin.txt", "wb+").write(proc.stdout)
    if b"wm: kwin" in proc.stdout or b"wm\x03 kwin" in proc.stdout:
        proc = subprocess.run(["qdbus", "org.kde.KWin", "/Compositor", "active"], capture_output = True)
        if b"true" in proc.stdout:
            compositor = "org.kde.KWin"


term = pygame.display.set_mode((0, 0))
pygame.mixer.quit()
img = pygame.Surface.convert(pygame.image.load("./assets/icon.png"))
pygame.display.set_icon(img)
pygame.display.set_caption("PRIZ PLAYER ;]")
prefs = json.loads(open("conf.json").read())
term = pygame.display.set_mode(prefs["size"], pygame.RESIZABLE)
pygame.display.update()
pygame.init()

if compositor == "org.kde.KWin":
    print(compositor)
    import pynput
    from pynput.keyboard import Key
    kb = pynput.keyboard.Controller()
    proc = subprocess.run(["qdbus", "org.kde.KWin", "/Compositor", "active"], capture_output = True).stdout
    if b"false" in proc:
        kb.press(Key.alt_l)
        kb.press(Key.shift)
        kb.press(Key.f12)
        kb.release(Key.alt_l)
        kb.release(Key.shift)
        kb.release(Key.f12)
        subprocess.run(["qdbus", "org.kde.KWin", "/Compositor", "resume"])

print(pygame.display.get_wm_info())

bg_color = 0x112222
hold_display = False

class Font():
    def __init__(self):
        self.size = 16
        self.b = pygame.font.Font(s('./assets/font/UbuntuMono-B.ttf'), self.size)
        self.bi = pygame.font.Font(s('./assets/font/UbuntuMono-BI.ttf'), self.size)
        self.r = pygame.font.Font(s('./assets/font/UbuntuMono-R.ttf'), self.size)
        self.ri = pygame.font.Font(s('./assets/font/UbuntuMono-RI.ttf'), self.size)
    @property
    def i(self):
        return self.ri

FONT = Font()

cur_font = FONT.r
cur_color = 0x112222

def rgb(hx):
    st = f"{hx:06x}"
    r = st[0:2]
    g = st[2:4]
    b = st[4:6]
    return int(r, 16), int(g, 16), int(b, 16)

class Term():
    class Dump():
        def __init__(self):
            self.x = 0
            self.y = 0

        @property
        def w(self): return self.x
        @property
        def h(self): return self.y

        @property
        def c(self): return self.x
        @property
        def r(self): return self.y

        def __setattr__(self, key, val):
            if key in ["w", "c"]:
                self.x = val
            elif key in ["h", "r"]:
                self.y = val
            else:
                self.__dict__[key] = val

    class Size(Dump):
        def __init__(self, up):
            self.up = up

        @property
        def x(self):
            return int((self.up.px.w - 20) / 8)
        @property
        def y(self):
            return int((self.up.px.h - 20) / 16)


    class Offset(Dump):
        def __init__(self, up):
            self.up = up

        @property
        def x(self):
            return (self.up.px.x - 20 - self.up.size.w * 8) / 2
        @property
        def y(self):
            return (self.up.px.y - 20 - self.up.size.h * 16) / 2

    class Border(Dump):
        def __init__(self, up):
            self.up = up

        @property
        def x(self):
            return (self.up.px.x - self.up.size.w * 8) / 2
        @property
        def y(self):
            return (self.up.px.y - self.up.size.h * 16) / 2


    def __init__(self, width, height):
        self.off = self.Offset(self)
        self.size = self.Size(self)
        self.border = self.Border(self)
        self.px = self.Dump()
        self.px.x = width
        self.px.y = height
        self.cur = self.Dump()
        self.hold = False

    @property
    def x(self):
        return self.cur.x
    @property
    def y(self):
        return self.cur.y
    @property
    def w(self):
        return self.size.x
    @property
    def h(self):
        return self.size.y
    @property
    def rem(self):
        return self.w - self.x

    def foot(self):
        self.y = self.h - 2

    def __setattr__(self, key, val):
        if key == "x":
            self.cur.x = val
        elif key == "y":
            self.cur.y = val
        elif key == "w":
            self.size.x = val
        elif key == "h":
            self.size.y = val
        else:
            self.__dict__[key] = val

TERM = Term(*pygame.display.get_window_size())

def handle_resize():
    global last_resize
    w, h = pygame.display.get_window_size()
    if w < 640 or h < 480:
        print(w, h)
        wh = (max(w, 640), max(h, 480))
        flag = pygame.HWSURFACE | pygame.DOUBLEBUF
        pygame.display.set_mode(wh, flags = flag)
        pygame.display.set_mode(wh, flags = flag | pygame.RESIZABLE)
    TERM.px.w, TERM.px.h = pygame.display.get_window_size()

def redraw():
    global TERM
    TERM.hold = False
    handle_resize()
    border_color = rgb(int(hex(bg_color).replace("22", "ff").replace("15", "88").replace("11", "00")[2:], 16))
    border_width = 2
    term.fill(border_color, rect = (0, 0, TERM.px.w, border_width))
    term.fill(border_color, rect = (0, TERM.px.h - border_width, TERM.px.w, border_width))
    term.fill(border_color, rect = (0, 0, border_width, TERM.px.h))
    term.fill(border_color, rect = (TERM.px.w - border_width, 0, border_width, TERM.px.h))
    pygame.display.update()

def put(txt, x, y, color = None, font = None, cls = True, y_offset = 0, x_offset = 0, center = 0, right = 0, left = 0, char = " "):
    global cur_font, cur_color, bg_color, TERM
    x += TERM.border.x + x_offset
    y += TERM.border.y + y_offset
    font = font or cur_font
    color = color or cur_color
    cur_font = font
    cur_color = color
    txtt = ""
    for c in txt:
        try:
            if "COMBINING" not in unicodedata.name(c):
                txtt += c
        except Exception as ex:
            print(c)
            print(ex)
    txt = txtt
    if center:
        txt = txt.center(center, char)
    elif right:
        txt = txt.rjust(right, char)
    elif left:
        txt = txt.ljust(left, char)
    text = cur_font.render(txt, True, rgb(cur_color))
    ls = text.get_rect()
    ls[0] += x
    ls[1] += y
    if cls:
        term.fill(rgb(bg_color), rect = ls)
    ls[2] += x
    ls[3] += y
    term.blit(text, ls)
    if not TERM.hold:
        pygame.display.update()
    return txt


def echo(txt = " ", **kw):
    global TERM
    global cur_font, cur_color
    put(txt, TERM.x * 8, TERM.y * 16, cls = False, **kw)
    TERM.x = 0
    TERM.y += 1


def echo_n(txt = " ", **kw):
    global TERM
    global cur_font, cur_color
    txt = put(txt, TERM.x * 8, TERM.y * 16, cls = False, **kw)
    TERM.x += len(txt)
    if txt == " ":
        TERM.x -= 1


def clear(color = None):
    global TERM, bg_color
    term.fill(rgb(color or bg_color), rect = (0, 0, TERM.px.w, TERM.px.h))
    if not TERM.hold:
        pygame.display.update()
    TERM.x = 0
    TERM.y = 0
    bg_color = color or bg_color

def echo_s(txt, off_width = 0, indent = 0, **kw):
    global TERM
    for word in txt.split():
        if len(word) + TERM.x > TERM.w - off_width:
            echo()
            TERM.x = indent
        echo_n(word + " ", **kw)
    echo()
