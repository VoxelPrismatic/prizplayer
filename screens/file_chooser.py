# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

def file_chooser():
    global TERM, queue, folder_slash
    if folder_slash == "/":
        directory = "/home/" + os.getlogin() + "/Music/"
    else:
        directory = "C:\\Users\\" + os.getlogin() + "\\Music\\"
    ls = [".."] + os.listdir(directory)
    cursor = 0
    offset = 0
    search = ""
    ls.sort()
    finding = False
    alt = False
    ctrl = False
    added = []
    prefs = json.loads(open("conf.json").read())
    skip_draw = False
    while True:
        if not skip_draw:
            while offset + TERM.h - 5 < cursor and offset + 1 < len(added):
                offset += 1
            while offset > cursor and offset - 1 >= 0:
                offset -= 1
            TERM.hold = True
            clear(0x221115)
            echo("--------================[ CHOOSE FILES ]================--------", center = TERM.w, color = 0xff0088, font = FONT.b)
            term.fill(rgb(0x443337), rect = cursor_highlight(cursor - offset + 2))
            if finding:
                search = ' "' + search + '" '
                echo_n(search, center = TERM.w, char = "-", font = FONT.r)
                search = search[2:-2]
            else:
                echo_n(f" {directory[-TERM.w + 10:]} ", center = TERM.w, char = "-", font = FONT.r)
            echo(color = 0xaaaaaa)
            event = None
            for thing in ls[:]:
                if os.path.isdir(directory + thing):
                    continue
                elif not any(thing.lower().endswith(x) for x in file_formats):
                    ls.remove(thing)
            added = []
            tls = ls[offset:]
            for file_or_dir in ls:
                if finding:
                    if search.lower() not in file_or_dir.lower():
                        continue
                added.append(file_or_dir)
                if TERM.y == TERM.h - 2 or file_or_dir not in tls:
                    continue
                if os.path.isdir(directory + file_or_dir):
                    echo("[ " + file_or_dir[:TERM.w + 10] + "/ ]", color = 0xaaaaaa)
                else:
                    if directory + file_or_dir in queue:
                        echo(file_or_dir[:TERM.w + 10], color = 0xffffff)
                    else:
                        echo(file_or_dir[:TERM.w + 10], color = 0xaaaaaa)
            if finding and cursor >= len(added) and len(added) != 26:
                cursor = 0
                offset = 0
            TERM.foot()
            echo(f"[{cursor + 1}/{len(added)}]", right = TERM.w, char = "-", color = 0x880044, font = FONT.b)
            if ctrl:
                echo_n("CTRL // q - Show queue  /  p - Show player  /  F1 - Help")
            if alt:
                echo_n("ALT // a - Toggle all  /  f - Toggle search")
            else:
                echo_n("CTRL/ALT - Shortcut  /  ENTER - ")
                if os.path.isdir(directory + ls[cursor]):
                    echo_n("Open folder  /  F2 - ")
                    if ls[cursor] == ".." and directory in prefs["search_dirs"]:
                        echo_n("Remove from search")
                    elif directory + ls[cursor] + "/" not in prefs["search_dirs"]:
                        echo_n("Add to search")
                    else:
                        echo_n("Remove from search")
                elif directory + ls[cursor] in queue:
                    echo_n("Remove file from queue")
                else:
                    echo_n("Add file to queue")
            echo(";]", right = TERM.rem)
            redraw()
        evt = None
        event = None
        skip_draw = False
        while evt is None:
            evt = pygame.event.wait()
            if evt.type in EVT["QUIT"]:
                kill()
            elif evt.type in [*EVT["INPUT"], *EVT["MOUSEMOVE"], *EVT["KEYDOWN"], *EVT["WHEEL"], *EVT["CLICK"]]:
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
                if cursor + 1 < len(added):
                    cursor += 1
                alt = False
            elif evt.scancode == KEY["ENTER"]:
                if os.path.isdir(directory + added[cursor]):
                    if added[cursor] == "..":
                        directory = directory.rsplit(folder_slash, 2)[0] + folder_slash
                    else:
                        directory = directory + added[cursor] + folder_slash
                    ls = [".."] + os.listdir(directory)
                    ls.sort()
                    cursor = 0
                    offset = 0
                else:
                    if directory + added[cursor] in queue:
                        queue.remove(directory + added[cursor])
                    else:
                        queue.append(directory + added[cursor])
                alt = False
            elif evt.scancode == KEY["ALT"]:
                alt = not alt
                ctrl = False
            elif event.scancode == KEY["CTRL"]:
                ctrl = not ctrl
                alt = False
            elif evt.scancode == KEY["BKSP"] and finding:
                search = search[:-1]
            elif evt.scancode == KEY["F1"] and alt:
                return "f1"
            elif evt.scancode == KEY["F2"]:
                if directory + ls[cursor] + folder_slash in prefs["search_dirs"]:
                    prefs["search_dirs"].remove(directory + ls[cursor] + folder_slash)
                else:
                    prefs["search_dirs"].append(directory + ls[cursor] + folder_slash)
                open("conf.json", "w").write(json.dumps(prefs, indent = "    "))
        elif event.type in EVT["INPUT"] and event.text:
            if ctrl:
                if evt.text in __available_keys:
                    return evt.text
            elif alt:
                if evt.text == "f":
                    finding = not finding
                elif evt.text == "a":
                    for f in ls:
                        if os.path.isdir(directory + f):
                            continue
                        if directory + f in queue:
                            queue.remove(directory + f)
                        else:
                            queue.append(directory + f)
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
                for f in added:
                    if f.lower().startswith(event.text.lower()):
                        break
                    if cursor + 1 < len(ls):
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
            if event.button == 1:
                kb_press(Key.enter)
            elif event.button == 3:
                alt = not alt
        elif event.type in EVT["MOUSEMOVE"]:
            t1 = cursor
            cursor = offset + mouse_cursor(event, 3, 5, added)
            if int(t1) == int(cursor):
                skip_draw = True
