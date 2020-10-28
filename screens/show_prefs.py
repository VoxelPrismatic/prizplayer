# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

def show_prefs():
    global TERM
    cursor = 0
    offset = 0
    alt = False
    ctrl = False
    search = ""
    finding = False
    insert = False
    prefs = json.loads(open("conf.json").read())
    skip_draw = False
    while True:
        if not skip_draw:
            while offset + TERM.h - 5 < cursor and offset + 1 < len(added):
                offset += 1
            while offset > cursor and offset - 1 >= 0:
                offset -= 1
            TERM.hold = True
            clear(0x221111)
            echo("--------==============[ MUSIC  LOCATIONS ]==============-------", center = TERM.w, color = 0xff0000, font = FONT.b)
            term.fill(rgb(0x4433333), rect = cursor_highlight(cursor - offset + 2))
            if finding or insert:
                search = ' "' + search + '" '
                echo_n(search, center = TERM.w, char = "-", font = FONT.r)
                search = search[2:-2]
            else:
                echo_n(" Where to search for music ", center = TERM.w, char = "-", font = FONT.r)
            echo(color = 0xaaaaaa)
            event = None
            tls = prefs["search_dirs"][offset:]
            for file_or_dir in tls:
                if TERM.y == TERM.h - 2:
                    break
                echo(file_or_dir[-TERM.w + 10:], color = 0xaaaaaa)
            TERM.foot()
            echo(f"[{cursor + 1}/{len(prefs['search_dirs'])}]", right = TERM.w, char = "-", color = 0x880000, font = FONT.b)
            if ctrl:
                echo_n("CTRL // o - Open files  /  p - Show player  /  F1 - Help")
            if alt:
                echo_n("ALT // f - Toggle search")
            else:
                echo_n("ALT/CTRL - shortcut / DEL - Remove from list / INS - Add to list")
            echo(";]", right = TERM.rem)
            redraw()
        evt = None
        event = None
        skip_draw = False

        while evt is None:
            evt = pygame.event.wait()
            if evt.type in EVT["QUIT"]:
                kill()
            elif evt.type in [*EVT["INPUT"], *EVT["KEYDOWN"], *EVT["WHEEL"], *EVT["CLICK"], *EVT["MOUSEMOVE"]]:
                event = evt
                rep = False
            elif evt.type in EVT["WINDOW"]:
                event = evt
            else:
                continue

        try_print(f"\x1b[94;1m{evt.type}\x1b[0m:", evt)
        if event is None:
            skip_draw = True
            continue
        if event.type in EVT["KEYDOWN"]:
            if event.scancode == KEY["UP"]:
                if cursor - 1 >= 0:
                    cursor -= 1
                alt = False
            elif event.scancode == KEY["DOWN"]:
                if cursor + 1 < len(prefs["search_dirs"]):
                    cursor += 1
                alt = False
            elif evt.scancode == KEY["DEL"]:
                prefs["search_dirs"].remove(prefs["search_dirs"][cursor])
                alt = False
            elif evt.scancode == KEY["ALT"]:
                alt = not alt
                ctrl = False
            elif event.scancode == KEY["CTRL"]:
                ctrl = not ctrl
                alt = False
            elif evt.scancode == KEY["BKSP"] and finding:
                search = search[:-1]
            elif evt.scancode == KEY["INS"]:
                open("conf.json", "w+").write(json.dumps(prefs, indent = 4))
                return "o"
            elif event.scancode == KEY["F1"] and alt:
                open("conf.json", "w+").write(json.dumps(prefs, indent = 4))
                return "f1"
        elif event.type in EVT["INPUT"] and event.text:
            if ctrl:
                if evt.text in __available_keys:
                    open("conf.json", "w+").write(json.dumps(prefs, indent = 4))
                    return evt.text
            elif alt:
                if evt.text == "f":
                    finding = not finding
                elif event.text in "+=":
                    FONT.change_size(FONT.size + 2)
                elif event.text in "-_":
                    FONT.change_size(FONT.size - 2)
            elif finding:
                search += event.text
            else:
                og_cur = (cursor, offset)
                cursor = 0
                offset = 0
                for f in prefs["search_dirs"]:
                    if f.lower().startswith(event.text.lower()):
                        break
                    if cursor + 1 < len(prefs["search_dirs"]):
                        cursor += 1
                else:
                    cursor, offset = og_cur
            alt = False
        elif event.type in EVT["WHEEL"]:
            if event.y == 1:
                if offset - 1 >= 0:
                    offset -= 1
                    if offset + TERM.h - 5 < cursor and cursor - 1 >= 0:
                        cursor -= 1
                elif cursor - 1 >= 0:
                    cursor -= 1
            elif event.y == -1:
                if offset + 1 < len(added) - (TERM.h - 5):
                    offset += 1
                    if offset > cursor and cursor + 1 < len(added):
                        cursor += 1
                elif cursor + 1 < len(added):
                    cursor += 1
        elif event.type in EVT["CLICK"]:
            if event.button == 3:
                alt = not alt
        elif event.type in EVT["MOUSEMOVE"]:
            t1 = cursor
            cursor = offset + mouse_cursor(event, 3, 5, prefs["search_dirs"])
            if int(t1) == int(cursor):
                skip_draw = True
