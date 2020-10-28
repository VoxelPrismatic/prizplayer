# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

def save_queue():
    global TERM, queue
    name = ""
    cursor = 0
    offset = 0
    linux = folder_slash == "/"
    alt = False
    ctrl = False
    ls = []
    skip_draw = False
    while True:
        if not skip_draw:
            TERM.hold = True
            clear(0x222511)
            echo("--------=================[ SAVE QUEUE ]=================--------", center = TERM.w, color = 0xff8800, font = FONT.b)
            term.fill(rgb(0x334433), rect = cursor_highlight(cursor - offset + 3))
            echo("-" * TERM.w, font = FONT.r)
            echo_n(f"File name ] {name}", color = 0xffffff)
            echo(".PRZ", font = FONT.i, color = 0xaaaaaa)
            ls = []
            for f in os.listdir(f".{folder_slash}queues{folder_slash}"):
                if f.lower().endswith(".prz") and name.lower() in f.lower():
                    ls.append(f)
                    if TERM.y <= TERM.h - 3:
                        echo_n(f[:-4], color = 0xaaaaaa, font = FONT.r)
                        echo(".PRZ", font = FONT.ri)
            while offset + TERM.h - 6 < cursor and offset + 1 < len(ls):
                offset += 1
            while offset > cursor and offset - 1 >= 0:
                offset -= 1
            TERM.foot()
            echo(f"[{cursor + 1}/{len(ls)}]", right = TERM.w, char = "-", font = FONT.b, color = 0x884400)
            if ctrl:
                echo_n("CTRL // q - Show queue  /  p - Show player  /  F1 - Help")
            elif alt:
                echo_n("ALT // Search is automatic based on inputted filename")
            else:
                echo_n("ALT/CTRL - Shortcut  /  F2 - Use this file name  /  ENTER - Save queue")
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
                f = open(f".{folder_slash}queues{folder_slash}" + name + ".PRZ", "w+")
                f.write("\n".join(queue))
                f.close()
                return "q"
            elif event.scancode == KEY["UP"]:
                if cursor - 1 >= 0:
                    cursor -= 1
                alt = False
            elif event.scancode == KEY["DOWN"]:
                if cursor + 1 < len(ls):
                    cursor += 1
                alt = False
            elif event.scancode == KEY["F2"]:
                name = ls[cursor][:-4]
            elif event.scancode == KEY["F1"] and alt:
                return "f1"
        elif event.type in EVT["INPUT"]:
            if alt:
                if event.text in __available_keys:
                    return event.text
                elif event.text in "+=":
                    FONT.change_size(FONT.size + 2)
                elif event.text in "-_":
                    FONT.change_size(FONT.size - 2)
            else:
                if event.text in "/\\?%*:\"><" and not linux:
                    continue
                elif event.text in "/" and linux:
                    continue
                elif len(name) == 50:
                    continue
                name += event.text
        elif event.type in EVT["WHEEL"]:
            if event.y == 1:
                if offset - 1 >= 0:
                    offset -= 1
                    if offset + TERM.h - 6 < cursor and cursor - 1 >= 0:
                        cursor -= 1
                elif cursor - 1 >= 0:
                    cursor -= 1
            elif event.y == -1:
                if offset + 1 < len(ls) - (TERM.h - 6):
                    offset += 1
                    if offset > cursor and cursor + 1 < len(ls):
                        cursor += 1
                elif cursor + 1 < len(ls):
                    cursor += 1
        elif event.type in EVT["CLICK"]:
            if event.button == 1:
                name = ls[cursor][:-4]
            elif event.button == 3:
                alt = not alt
        elif event.type in EVT["MOUSEMOVE"]:
            t1 = cursor
            cursor = offset + mouse_cursor(event, 3, 6, ls)
            if int(t1) == int(cursor):
                skip_draw = True
