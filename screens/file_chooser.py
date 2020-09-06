# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

def file_chooser():
    global hold_display, term_y, term_x
    if sys.executable.startswith("/usr/bin/"):
        folder = "/"
        directory = "/home/" + os.getlogin() + "/Music/"
    else:
        folder = "\\"
        directory = "C:\\Users\\" + os.getlogin() + "\\Music\\"
    ls = [".."] + os.listdir(directory)
    cursor = 0
    offset = 0
    search = ""
    ls.sort()
    finding = False
    alt = False
    prefs = json.loads(open("conf.json").read())
    while True:
        hold_display = True
        clear(0x221115)
        echo("         -------================[ CHOOSE FILES ]================-------         ", color = 0xff0088, font = font_b)
        term.fill(rgb(0x443337), rect = (0, (cursor - offset + 2) * 16 + 12, term_w, 16))
        if finding:
            search = ' "' + search + '" '
            echo_n(f"{search:-^80}", font = font_r)
            search = search[2:-2]
        else:
            echo_n(f"{' ' + directory[-60:] + ' ':-^80}", font = font_r)
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
            if term_y == 28 or file_or_dir not in tls:
                continue
            if os.path.isdir(directory + file_or_dir):
                echo("[ " + file_or_dir[-40:] + "/ ]", color = 0xaaaaaa)
            else:
                if directory + file_or_dir in queue:
                    echo(file_or_dir[-60:], color = 0xffffff)
                else:
                    echo(file_or_dir[-60:], color = 0xaaaaaa)
        if finding and cursor >= len(added) and len(added) != 26:
            cursor = 0
            offset = 0
        term_y = 28
        echo(f"{'[' + str(cursor + 1) + '/' + str(len(added)) + ']':->80}", color = 0x880044, font = font_b)
        if alt:
            echo("a - Toggle all  /  f - Toggle search  /  F1 - More screens                    ;]")
        else:
            echo_n("ALT - Use shortcut  /  ENTER - ")
            if os.path.isdir(directory + ls[cursor]):
                echo_n("Open folder  /  F2 - ")
                if ls[cursor] == ".." and directory in prefs["search_dirs"]:
                    echo("Remove folder from search ;]")
                elif directory + ls[cursor] + "/" not in prefs["search_dirs"]:
                    echo("Add folder to search      ;]")
                else:
                    echo("Remove folder from search ;]")
            elif directory + ls[cursor] in queue:
                echo("Remove file from queue                         ;]")
            else:
                echo("Add file to queue                              ;]")
        redraw()
        evt = pygame.event.wait()
        if evt.type in EVT["QUIT"]:
            kill()
        elif evt.type in [*EVT["INPUT"], *EVT["KEY"], *EVT["KEYDOWN"], *EVT["WHEEL"], *EVT["CLICK"]]:
            event = evt
            rep = False
        elif evt.type in EVT["WINDOW"]:
            pygame.display.update()
        else:
            continue
        print(f"\x1b[94;1m{evt.type}\x1b[0m:", evt)
        if event is None:
            continue
        if event.type in EVT["KEYDOWN"]:
            if event.scancode == KEY["UP"] or event.scancode == KEY["LEFT"]:
                if cursor - 1 >= 0:
                    cursor -= 1
                if offset > cursor and offset - 1 >= 0:
                    offset -= 1
                alt = False
            elif event.scancode == KEY["DOWN"] or event.scancode == KEY["RIGHT"]:
                if cursor + 1 < len(added):
                    cursor += 1
                if offset + 25 < cursor and offset + 1 < len(added):
                    offset += 1
                alt = False
            elif evt.scancode == KEY["ENTER"]:
                if os.path.isdir(directory + added[cursor]):
                    if added[cursor] == "..":
                        directory = directory.rsplit(folder, 2)[0] + folder
                    else:
                        directory = directory + added[cursor] + folder
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
            elif evt.scancode == KEY["BKSP"] and finding:
                search = search[:-1]
            elif evt.scancode == KEY["F1"]:
                return "f1"
            elif evt.scancode == KEY["F2"]:
                if directory + ls[cursor] + "/" in prefs["search_dirs"]:
                    prefs["search_dirs"].remove(directory + ls[cursor] + "/")
                else:
                    prefs["search_dirs"].append(directory + ls[cursor] + "/")
                open("conf.json", "w").write(json.dumps(prefs, indent = "    "))
        elif event.type in EVT["INPUT"]:
            if alt:
                if evt.text in __available_keys:
                    return evt.text
                elif evt.text == "f":
                    finding = not finding
                elif evt.text == "a":
                    for f in ls:
                        if os.path.isdir(directory + f):
                            continue
                        if directory + f in queue:
                            queue.remove(directory + f)
                        else:
                            queue.append(directory + f)
            elif finding:
                search += event.text
            else:
                cursor = 0
                offset = 0
                for f in ls:
                    if f.lower().startswith(event.text.lower()):
                        break
                    if cursor + 1 < len(ls):
                        cursor += 1
                    if offset + 25 < cursor and offset + 1 < len(ls):
                        offset += 1
                else:
                    cursor = 0
                    offset = 0
            alt = False
        elif event.type in EVT["WHEEL"]:
            if event.y == 1:
                if cursor - 1 >= 0:
                    cursor -= 1
                if offset > cursor and offset - 1 >= 0:
                    offset -= 1
                alt = False
            elif event.y == -1:
                if cursor + 1 < len(added):
                    cursor += 1
                if offset + 25 < cursor and offset + 1 < len(added):
                    offset += 1
                alt = False
        elif event.type in EVT["CLICK"]:
            if event.button == 1:
                if os.path.isdir(directory + added[cursor]):
                    if added[cursor] == "..":
                        directory = directory.rsplit(folder, 2)[0] + folder
                    else:
                        directory = directory + added[cursor] + folder
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
            elif event.button == 3:
                alt = not alt
