# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

def show_queue():
    global music, enqueue, unqueue, now_playing, TERM, queue
    cursor = 0
    offset = 0
    alt = False
    search = ""
    finding = False
    refresh_tag = True
    queue_tag = []
    queue_meta = []
    added = []
    dragging = False
    skip_draw = False
    while True:
        fix_queue()
        if len(queue_tag) != len(queue) or refresh_tag:
            queue_tag = []
            queue_meta = []
            while refresh_tag and queue:
                queue_tag = []
                queue_meta = []
                fix_queue()
                for track in queue:
                    if track == "":
                        refresh_tag = True
                        break
                    tags = tinytag.TinyTag.get(track)
                    ls = [
                        tags.title or track.split(folder_slash)[-1],
                        tags.artist or "<Unknown>",
                        tags.album or track.split(folder_slash)[-2]
                    ]
                    ls.append(track)
                    queue_tag.append(ls)
                    queue_meta.append(tags)
                    refresh_tag = False
        if not skip_draw:
            TERM.hold = True
            clear(0x112211)
            echo("-------==================[ IN QUEUE ]==================-------", center = TERM.w, color = 0x00ff00, font = FONT.b)
            while offset + TERM.h - 5 < cursor and offset + 1 < len(added):
                offset += 1
            while offset > cursor and offset - 1 >= 0:
                offset -= 1
            term.fill(rgb(0x334433), rect = (0, (cursor - offset + 2) * 16 + 12 + TERM.off.y, TERM.px.w, 16))
            if finding:
                search = ' "' + search + '" '
                echo(search, center = TERM.w, char = "-", font = FONT.r)
                search = search[2:-2]
                print(search)
            else:
                echo(" Songs in order ", center = TERM.w, char = "-", font = FONT.r)
            event = None
            added = []
            c = -1
            for track in queue_tag:
                t = track[-1]
                c += 1
                if not finding or any(search.lower() in x.lower() for x in track):
                    added.append(track[-1])
                    if TERM.y == TERM.h - 2 or len(added) - 1 < offset:
                        continue
                    if now_playing == track[-1]:
                        echo_n(color = 0xffffff)
                    else:
                        echo_n(color = 0xaaaaaa)
                    TERM.x = 0
                    if track[:-1] == ["<NULL>", "<Unknown>", "<None>"]:
                        if t.startswith("/home/" + os.getlogin() + "/"):
                            t = "~/" + t.split("/home/" + os.getlogin() + "/", 1)[1]
                        elif t.startswith("C:\\Users\\" + os.getlogin() + "\\"):
                            t = "~\\" + t.split("C:\\Users\\" + os.getlogin() + "\\", 1)[1]
                        echo(t[-70:], font = FONT.r)
                    elif len(track[0]) + len(track[1]) + len(track[2]) < TERM.w:
                        echo_n(f"{track[0]}", font = FONT.b)
                        echo_n(f" in ", font = FONT.r)
                        echo_n(f"{track[2]}", font = FONT.b)
                        echo_n(f" by ", font = FONT.r)
                        echo_n(f"{track[1]}", font = FONT.b)
                    else:
                        echo_n(f"{track[0]}"[-int(TERM.w / 80 * 30):], font = FONT.b)
                        echo_n(f" in ", font = FONT.r)
                        echo_n(f"{track[2]}"[-int(TERM.w / 80 * 20):], font = FONT.b)
                        echo_n(f" by ", font = FONT.r)
                        echo_n(f"{track[1]}"[-int(TERM.w / 80 * 20):], font = FONT.b)
                    seconds = int(queue_meta[c].duration)
                    minutes = int(seconds / 60)
                    seconds %= 60
                    echo(f" {minutes:02}:{seconds:02}", font = FONT.i)
            TERM.foot()
            echo(f"[{cursor + 1}/{len(added)}]", right = TERM.w, char = "-", font = FONT.b, color = 0x008800)
            if alt:
                echo_n("l - Load queue / s - Save queue / f - Toggle search / F1 - More screens")
            else:
                echo_n("ALT - Use shortcut / DEL - Remove / ,/. - Up/down / ENTER - Play now")
            echo(";]", right = TERM.rem)
            redraw()
        evt = None
        event = None
        skip_draw = False
        np = now_playing
        nq = queue
        while evt is None:
            evt = pygame.event.poll()
            if evt.type == 0:
                time.sleep(0.01)
                continue
            try_print(f"\x1b[94;1m{evt.type}\x1b[0m:", evt)
            if evt.type in EVT["QUIT"]:
                kill()
            elif evt.type in [*EVT["INPUT"], *EVT["KEYDOWN"], *EVT["WHEEL"], *EVT["CLICK"], *EVT["MOUSEMOVE"]]:
                event = evt
                rep = False
            elif evt.type in EVT["WINDOW"]:
                event = evt
            else:
                continue
            if np != now_playing or nq != queue:
                print("---")
                evt = evt or 1

        if event is None:
            if np == now_playing:
                skip_draw = True
            if nq != queue:
                refresh_tag = True
                skip_draw = False
            continue
        if event.type in EVT["KEYDOWN"] and event:
            if event.scancode == KEY["UP"]:
                if cursor - 1 >= 0:
                    cursor -= 1
                alt = False
            elif event.scancode == KEY["DOWN"]:
                if cursor + 1 < len(added):
                    cursor += 1
                alt = False
            elif event.scancode == KEY["DEL"] and len(queue) and cursor < len(added):
                queue.remove(added[cursor])
                refresh_tag = True
                alt = False
            elif event.scancode == KEY["ALT"]:
                alt = not alt
            elif event.scancode == KEY["BKSP"] and finding:
                search = search[:-1]
            elif event.scancode == KEY["F1"] and alt:
                return "f1"
            elif event.scancode == KEY["ENTER"]:
                unqueue.append(enqueue)
                enqueue = cursor
                music = next_track(added, music, enqueue)
                try:
                    enqueue = queue.index(now_playing)
                except ValueError:
                    enqueue = cursor
        elif event.type in EVT["INPUT"] and event.text:
            if alt:
                if event.text in __available_keys:
                    return event.text
                elif event.text == "f":
                    finding = not finding
            elif finding and event.text not in ",.":
                search += event.text
            elif event.text == ",":
                if cursor - 1 >= 0:
                    if added != queue:
                        c1 = queue.index(added[cursor])
                        c2 = queue.index(added[cursor - 1])
                    else:
                        c1, c2 = cursor, cursor - 1
                    queue[c1], queue[c2] = added[cursor - 1], added[cursor]
                    cursor -= 1
                    alt = False
                    refresh_tag = True
                    enqueue = queue.index(now_playing)
            elif event.text == ".":
                if cursor + 1 < len(queue):
                    if added != queue:
                        c1 = queue.index(added[cursor])
                        c2 = queue.index(added[cursor + 1])
                    else:
                        c1, c2 = cursor, cursor + 1
                    queue[c1], queue[c2] = added[cursor + 1], added[cursor]
                    cursor += 1
                    alt = False
                    refresh_tag = True
                    enqueue = queue.index(now_playing)
            else:
                og_cur = (cursor, offset)
                cursor = 0
                offset = 0
                for f in queue:
                    if f.lower().startswith(event.text.lower()):
                        break
                    if cursor + 1 < len(queue):
                        cursor += 1
                else:
                    cursor, offset = og_cur
            alt = False
        elif event.type in EVT["WHEEL"]:
            if event.y == 1:
                if cursor - 1 >= 0:
                    cursor -= 1
            elif event.y == -1:
                if cursor + 1 < len(added):
                    cursor += 1
        elif event.type in EVT["CLICK"]:
            if event.button == 1:
                if dragging:
                    dragging = False
                    continue
                kb_press(Key.enter)
            elif event.button == 3:
                alt = not alt
        elif event.type in EVT["MOUSEMOVE"]:
            t1 = cursor
            cursor = offset + min(max(int((event.pos[1] - 16 * 3) / 16), 0), min(TERM.h - 5, len(added) - 1))
            if int(t1) == int(cursor):
                skip_draw = True
            elif event.buttons == (1, 0, 0):
                if added != queue:
                    c1 = queue.index(added[cursor])
                    c2 = queue.index(added[t1])
                else:
                    c1, c2 = cursor, t1
                queue[c1], queue[c2] = added[t1], added[cursor]
                alt = False
                refresh_tag = True
                enqueue = queue.index(now_playing)
                dragging = True
