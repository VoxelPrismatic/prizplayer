# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

def load_queue():
    global TERM, queue, folder_slash
    cursor = 0
    offset = 0
    name = ""
    finding = False
    alt = False
    prefs = json.loads(open("conf.json").read())
    skip_draw = False
    while True:
        if not skip_draw:
            TERM.hold = True
            clear(0x151122)
            echo("-------=================[ LOAD QUEUE ]=================-------", center = TERM.w, color = 0x8800ff, font = FONT.b)
            term.fill(rgb(0x373344), rect = (0, (cursor - offset + 2) * 16 + 12 + TERM.off.y, TERM.px.w, 16))
            if finding:
                search = ' "' + search + '" '
                echo_n(search, center = TERM.w, char = "-", font = FONT.r)
                search = search[2:-2]
            else:
                echo_n(f" Pick a queue ", center = TERM.w, char = "-", font = FONT.r)
            echo(color = 0xaaaaaa)
            ls = []
            for f in os.listdir(s(f"./queues/")):
                if f.lower().endswith(".prz"):
                    if name.lower() not in f.lower() and finding:
                        continue
                    ls.append(f)
                    if TERM.y <= TERM.h - 3:
                        echo_n(f[:-4], color = 0xaaaaaa, font = FONT.r)
                        echo(".PRZ", font = FONT.ri)
            while offset + TERM.h - 6 < cursor and offset + 1 < len(ls):
                offset += 1
            while offset > cursor and offset - 1 >= 0:
                offset -= 1
            TERM.foot()
            echo(f"[{cursor + 1}/{len(ls)}]", right = TERM.w, char = "-", font = FONT.b, color = 0x440088)
            if alt:
                echo_n("f - Toggle search  /  ENTER - Append to queue  /  F1 - More screens")
            else:
                echo_n("ALT - Use Shortcut  /  ENTER - Load queue")
            echo(";]", right = TERM.rem)
            redraw()
        evt = None
        event = None
        skip_draw = False
        while evt is None:
            evt = pygame.event.wait()
            if evt.type in EVT["QUIT"]:
                kill()
            elif evt.type in [*EVT["INPUT"], *EVT["KEYDOWN"], *EVT["CLICK"], *EVT["WHEEL"], *EVT["MOUSEMOVE"]]:
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
            if evt.scancode == KEY["BKSP"]:
                name = name[:-1]
            elif evt.scancode == KEY["ALT"]:
                alt = not alt
            elif evt.scancode == KEY["ENTER"]:
                f = open(s(f"./queues/{ls[cursor]}")).read().split("\n")
                if alt:
                    queue.extend(f)
                else:
                    queue = f
                return "q"
            elif event.scancode == KEY["UP"]:
                if cursor - 1 >= 0:
                    cursor -= 1
                alt = False
            elif event.scancode == KEY["DOWN"]:
                if cursor + 1 < len(ls):
                    cursor += 1
                alt = False
            elif event.scancode == KEY["F1"] and alt:
                return "f1"
        elif event.type in EVT["INPUT"]:
            if alt:
                if event.text in __available_keys:
                    return event.text
            elif finding:
                name += event.text
        elif event.type in EVT["WHEEL"]:
            if event.y == 1:
                if cursor - 1 >= 0:
                    cursor -= 1
            elif event.y == -1:
                if cursor + 1 < len(ls):
                    cursor += 1
        elif event.type in EVT["CLICK"]:
            if event.button == 1:
                kb_press(Key.enter)
            elif event.button == 3:
                alt = not alt
        elif event.type in EVT["MOUSEMOVE"]:
            t1 = cursor
            cursor = offset + min(max(int((event.pos[1] - 16 * 3) / 16), 0), min(TERM.h - 5, len(ls) - 1))
            if int(t1) == int(cursor):
                skip_draw = True
