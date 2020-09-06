# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

def show_queue():
    global hold_display, term_y, term_x, queue
    cursor = 0
    offset = 0
    alt = False
    search = ""
    finding = False
    queue_tag = []
    for track in queue:
        tags = id3.tag.Tag()
        tags.parse(open(track, "rb"))
        queue_tag.append([tags.title or "<NULL>", tags.artist or "<Unknown>", tags.album or "<None>", track])
    while True:
        if len(queue_tag) != len(queue):
            queue_tag = []
            for track in queue:
                tags = id3.tag.Tag()
                tags.parse(open(track, "rb"))
                queue_tag.append([tags.title or "<NULL>", tags.artist or "<Unknown>", tags.album or "<None>"])
        hold_display = True
        clear(0x112211)
        echo("         -------==================[ IN QUEUE ]==================-------         ", color = 0x00ff00, font = font_b)
        term.fill(rgb(0x334433), rect = (0, (cursor - offset + 2) * 16 + 12, term_w, 16))
        if finding:
            search = ' "' + search + '" '
            echo_n(f"{search:-^80}", font = font_r)
            search = search[2:-2]
        else:
            echo_n(f"{' Songs in order ':-^80}", font = font_r)
        echo(color = 0xaaaaaa)
        event = None
        tls = queue_tag[offset:]
        added = []
        for track in tls:
            if term_y == 28:
                break
            if not finding or any(search.lower() in track[x] for x in range(3)):
                if track[:-1] == ["<NULL>", "<Unknown>", "<None>"]:
                    t = track[-1]
                    if t.startswith("/home/" + os.getlogin() + "/"):
                        t = "~/" + t.split("/home/" + os.getlogin() + "/", 1)[1]
                    echo(t[-75:], font = font_r)
                elif len(track[0]) + len(track[1]) + len(track[2]) < 80:
                    echo_n(f"{track[0]}", font = font_b)
                    echo_n(f" in ", font = font_r)
                    echo_n(f"{track[2]}", font = font_b)
                    echo_n(f" by ", font = font_r)
                    echo(f"{track[1]}", font = font_b)
                else:
                    echo_n(f"{track[0]}"[-30:], font = font_b)
                    echo_n(f" in ", font = font_r)
                    echo_n(f"{track[2]}"[-21:], font = font_b)
                    echo_n(f" by ", font = font_r)
                    echo(f"{track[1]}"[-21:], font = font_b)
        term_y = 28
        echo(f"{'[' + str(cursor + 1) + '/' + str(len(queue)) + ']':->80}", font = font_b, color = 0x008800)
        if alt:
            echo("p - Player  /  s - Save queue  /  f - Toggle search  /  F1 - More screens     ;]")
        else:
            echo("ALT - Use shortcut / DEL - Remove from queue / , - Move up / . - Move down    ;]")
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
                if cursor + 1 < len(queue):
                    cursor += 1
                if offset + 25 < cursor and offset + 1 < len(queue):
                    offset += 1
                alt = False
            elif evt.scancode == KEY["DEL"] and len(queue):
                queue.remove(queue[cursor])
                alt = False
            elif evt.scancode == KEY["ALT"]:
                alt = True
            elif evt.scancode == KEY["BKSP"] and finding:
                search = search[:-1]
            elif evt.scancode == KEY["F1"] and alt:
                return "f1"
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
                for f in queue:
                    if f.lower().startswith(event.text.lower()):
                        break
                    if cursor + 1 < len(queue):
                        cursor += 1
                    if offset + 25 < cursor and offset + 1 < len(queue):
                        offset += 1
            alt = False
