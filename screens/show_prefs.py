# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

def show_prefs():
    global hold_display, term_y, term_x
    cursor = 0
    offset = 0
    alt = False
    search = ""
    finding = False
    insert = False
    prefs = json.loads(open("conf.json").read())
    while True:
        hold_display = True
        clear(0x221111)
        echo("         --------==============[ MUSIC  LOCATIONS ]==============-------         ", color = 0xff0000, font = font_b)
        term.fill(rgb(0x4433333), rect = (0, (cursor - offset + 2) * 16 + 12, term_w, 16))
        if finding or insert:
            search = ' "' + search + '" '
            echo_n(f"{search:-^80}", font = font_r)
            search = search[2:-2]
        else:
            echo_n(f"{' Where to search for music ':-^80}", font = font_r)
        echo(color = 0xaaaaaa)
        event = None
        tls = prefs["search_dirs"][offset:]
        for file_or_dir in tls:
            if term_y == 28:
                break
            echo(file_or_dir[-60:], color = 0xaaaaaa)
        term_y = 28
        echo(f"{'[' + str(cursor + 1) + '/' + str(len(prefs['search_dirs'])) + ']':->80}", color = 0x880000, font = font_b)
        if alt:
            echo("o - Open files  /  p - Player  /  q - Show queue  /  f - Toggle search        ;]")
        else:
            echo("ALT - Use shortcut / DEL - Remove from list / INS - Add to list               ;]")
        redraw()
        evt = pygame.event.wait()
        if evt.type in EVT["QUIT"]:
            kill()
        elif evt.type in [*EVT["INPUT"], *EVT["KEY"], *EVT["KEYDOWN"]]:
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
            if event.scancode == KEY["UP"]:
                if cursor - 1 >= 0:
                    cursor -= 1
                if offset > cursor and offset - 1 >= 0:
                    offset -= 1
                alt = False
            elif event.scancode == KEY["DOWN"]:
                if cursor + 1 < len(prefs["search_dirs"]):
                    cursor += 1
                if offset + 25 < cursor and offset + 1 < len(prefs["search_dirs"]):
                    offset += 1
                alt = False
            elif evt.scancode == KEY["DEL"]:
                prefs["search_dirs"].remove(prefs["search_dirs"][cursor])
                alt = False
            elif evt.scancode == KEY["ALT"]:
                alt = True
            elif evt.scancode == KEY["BKSP"] and finding:
                search = search[:-1]
            elif evt.scancode == KEY["INS"]:
                return "o"
        elif event.type in EVT["INPUT"]:
            if alt:
                if evt.text in __available_keys:
                    return evt.text
                elif evt.text == "f":
                    finding = not finding
            elif finding:
                search += event.text
            else:
                cursor = 0
                offset = 0
                for f in prefs["search_dirs"]:
                    if f.lower().startswith(event.text.lower()):
                        break
                    if cursor + 1 < len(prefs["search_dirs"]):
                        cursor += 1
                    if offset + 25 < cursor and offset + 1 < len(prefs["search_dirs"]):
                        offset += 1
            alt = False
