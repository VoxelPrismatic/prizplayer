# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

import pickle

try:
    open("./cache/albums.pickle")
    refresh_cache = False
except:
    refresh_cache = True


class IOTags():
    def __init__(self, tags):
        self.album = tags.album
        self.albumartist = tags.albumartist
        self.artist = tags.artist
        self.audio_offset = tags.audio_offset
        self.bitrate = tags.bitrate
        self.comment = tags.comment
        self.composer = tags.composer
        self.disc = tags.disc
        self.disc_total = tags.disc_total
        self.duration = tags.duration
        self.filesize = tags.filesize
        self.genre = tags.genre
        self.samplerate = tags.samplerate
        self.title = tags.title
        self.track = tags.track
        self.track_total = tags.track_total
        self.year = tags.year
        self.image_data = tags.get_image()

    def get_image(self):
        return self.image_data

def show_albums():
    global TERM, folder_slash, refresh_cache
    cursor = 0
    offset = 0
    tracker = 0
    TERM.hold = True
    clear(0x111522)
    echo("--------===============[ FINDING ALBUMS ]===============--------", center = TERM.w, color = 0x0088ff, font = FONT.b)
    echo("-" * TERM.w, font = FONT.r)
    echo("Just a sec, I'm searching for your music")
    TERM.foot()
    echo("-" * TERM.w, color = 0x004488, font = FONT.b)
    echo(";]", right = TERM.w)
    redraw()
    cursor_album = {}
    finding = False
    search = ""
    alt = False
    ctrl = False
    prefs = json.loads(open("conf.json").read())
    blank_cover = open(s(f"./assets/icon.png"), "rb").read()
    if refresh_cache:
        albums = {}
        music = []
        TERM.y = 3
        echo("Locating...")
        for directory in prefs["search_dirs"]:
            music.extend(grab_files(directory))
        echo("Parsing...")
        t_n = 0
        for track in music:
            try_print(f"\x1b[93;1m{track}\x1b[0m")
            t_n += 1
            try:
                tags = tinytag.TinyTag.get(track, image = True)
                cover = tags.get_image() or blank_cover
            except Exception as ex:
                tags = tinytag.TinyTag.get(track)
                cover = blank_cover
            iotags = IOTags(tags)
            cover = fix_image(cover)
            try_print(tags)
            title = tags.title or track.split(folder_slash)[-1]
            album = tags.album or track.split(folder_slash)[-2]
            track_num = int(tags.track or t_n)
            try:
                #input(tags)
                albums[album]["Tracks"][track_num] = {
                    "file": track,
                    "name": title,
                    "cover": cover,
                    "tags": iotags
                }
            except:
                t_n = 1
                track_num = int(tags.track or t_n)
                dic = {}
                dic["Year"] = tags.year or "<Unknown>"
                dic["Album"] = album
                try_print(dic["Album"])
                artist = tags.artist or "<Unknown>"
                dic["Artist"] = artist
                dic["Tracks"] = {}
                albums[album] = dic
                albums[album]["Tracks"][track_num] = {
                    "file": track,
                    "name": title,
                    "cover": cover,
                    "tags": iotags
                }
        echo("Caching...")
        open(s("./cache/albums.pickle"), "wb+").write(pickle.dumps(albums))
    else:
        TERM.y = 3
        echo("Loading cache...")
        redraw()
        try:
            albums = pickle.loads(open(s("./cache/albums.pickle"), "rb").read())
        except EOFError:
            refresh_cache = True
            return "m"
    refresh_cache = False
    for album in albums:
        cursor_album[len(cursor_album)] = album
    skip_draw = False
    pygame.event.clear()
    while True:
        if not skip_draw:
            TERM.hold = True
            none_found = False
            clear(0x111522)
            echo("--------===============[ YOUR ALBUMS ;] ]===============--------", center = TERM.w, color = 0x0088ff, font = FONT.b)
            if finding:
                search = ' "' + search + '" '
                echo_n(search, center = TERM.w, char = "-", font = FONT.r)
                search = search[2:-2]
                cursor = max(0, cursor)
                og_cur = cursor - 1
                if og_cur == -1:
                    og_cur = len(albums) - 1
                while search.lower() not in \
                        str(cursor_album[cursor]).lower() and \
                        search.lower() not in albums[cursor_album[cursor]]["Artist"].lower() and \
                        cursor != og_cur:
                    cursor += 1
                    if cursor == len(albums):
                        cursor = 0
                    if cursor == og_cur:
                        none_found = True
                    try_print(cursor, og_cur)
                try_print(",")
            try:
                if none_found:
                    raise KeyError("No album found")
                album_info = albums[cursor_album[cursor]]
            except KeyError:
                album_info = {
                    "Year": "0000",
                    "Album": "<NULL>",
                    "Artist": "Try adding a folder to search in",
                    "Cover": None,
                    "Tracks": []
                }
            while offset + TERM.h - 12 < tracker and offset + 1 < len(album_info["Tracks"]):
                offset += 1
            while offset > tracker and offset - 1 >= 0:
                offset -= 1
            if not finding:
                echo_n(f" {album_info['Album']} ", center = TERM.w, char = "-", font = FONT.r)
            echo(color = 0xffffff)
            event = None
            echo(album_info["Album"], font = FONT.r)
            echo(album_info["Artist"], font = FONT.i)
            echo()
            num_tracks = str(len(album_info["Tracks"]))
            echo_n(num_tracks + " track", font = FONT.r)
            if num_tracks == "1":
                echo()
            else:
                echo("s")
            echo("Released in " + str(album_info["Year"]))
            if offset == 0:
                echo(color = 0xaaaaaa)
            else:
                echo("  ...", font = FONT.b, color = 0xaaaaaa)
            term.fill(rgb(0x333744), rect = cursor_highlight(tracker - offset + 8))

            t_nums = list(album_info["Tracks"])
            t_og = {}
            t_bk = t_nums
            count = -1
            track = 0
            for i in range(len(t_nums)):
                count += 1
                if count == tracker:
                    track = t_nums[i]
                if type(t_nums[i]) != int:
                    t_nums[i] = count
                    t_og[count] = i
            t_nums.sort()
            try:
                img = pygame.Surface.convert(
                    pygame.image.load(
                        io.BytesIO(album_info["Tracks"][track]["cover"])
                    ).convert_alpha()
                )
            except:
                img = pygame.Surface.convert(
                    pygame.image.load(
                        io.BytesIO(blank_cover)
                    ).convert_alpha()
                )

            img = pygame.transform.smoothscale(img, IMG.hw)
            term.blit(img, (TERM.px.w - IMG.w - TERM.border.x, 2 * FONT.size + TERM.border.y, IMG.w, IMG.h))
            c = -1
            for track in t_nums[offset:]:
                c += 1
                try:
                    if album_info['Tracks'][track]['file'] in queue:
                        echo_n(color = 0xffffff)
                    else:
                        echo_n(color = 0xaaaaaa)
                    TERM.x = 1
                    seconds = int(album_info['Tracks'][track]['tags'].duration or 0)
                    minutes = int(seconds / 60)
                    seconds %= 60
                    echo_n(f"{track:0>2}] ", font = FONT.r)
                    n = album_info['Tracks'][track]['name'] or album_info['Tracks'][track]['file'].split(s("/"))[-1]
                    if len(n) > TERM.w - 38 and tracker - offset == c:
                        term.fill(rgb(0x333744), rect = cursor_highlight(tracker - offset + 8))
                        TERM.x = 1
                        echo_n(f"{track:0>2}] ", font = FONT.r)
                        if len(n) > TERM.w - 13:
                            echo_n(f"{n[:TERM.w - 16]}... ", font = FONT.b)
                        else:
                            echo_n(n, font = FONT.b)
                        echo(f" {minutes:02}:{seconds:02}", font = FONT.i)
                    elif len(n) > TERM.w - 25:
                        echo(n[:TERM.w - 28] + "...", font = FONT.b)
                    else:
                        echo_n(n, font = FONT.b)
                        if tracker - offset == c:
                            echo(f" {minutes:02}:{seconds:02}", font = FONT.i)
                        else:
                            echo()
                except KeyError:
                    echo_n(f" {track:0>2}] ", font = FONT.r)
                    try:
                        echo(str(album_info["Tracks"][t_bk[t_og[track]]]['name']), font = FONT.b)
                    except KeyError:
                        echo(album_info['Tracks'][list(album_info['Tracks'])[c]]['file'].split(s("/"))[-1], font = FONT.b)
                if TERM.y == TERM.h - 3 and track != t_nums[-1]:
                    echo("  ...", color = 0xaaaaaa, font = FONT.b)
                    break
            TERM.y = TERM.h - 3
            echo("<" + ">".rjust(TERM.w - 1), font = FONT.b, color = 0xffffff)
            echo(f"[{cursor + 1}/{len(albums)}]".rjust(TERM.w, "-"), color = 0x004488)
            if ctrl:
                echo_n("CTRL // p - Show player  /  q - Show queue")
            elif alt:
                echo_n("ALT // a - Toggle all tracks in queue  /  f - Toggle search  /  F1 - Help")
            else:
                if tracker + 1 in list(album_info['Tracks']) and album_info['Tracks'][tracker + 1]['file'] in queue:
                    echo_n("ALT/CTRL - Use shortcut  /  ENTER - Remove from queue")
                else:
                    echo_n("ALT/CTRL - Use shortcut  /  ENTER - Add to queue")
                echo_n("  /  F5 - Refresh")
            echo(";]", right = TERM.rem)
            redraw()

        evt = None
        event = None
        skip_draw = False
        while evt is None:
            evt = pygame.event.wait()
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

        print(list(album_info["Tracks"]))

        if event is None:
            skip_draw = True
            continue
        if event.type in EVT["KEYDOWN"]:
            if event.scancode == KEY["LEFT"]:
                if cursor - 1 >= 0:
                    cursor -= 1
                else:
                    cursor = len(albums) - 1
                if finding:
                    og_cur = cursor + 1
                    if og_cur == len(albums):
                        og_cur = 0
                    while search.lower() not in \
                            str(cursor_album[cursor]).lower() and \
                            search.lower() not in albums[cursor_album[cursor]]["Artist"].lower() and \
                            cursor != og_cur:
                        cursor -= 1
                        if cursor == -1:
                            cursor = len(albums) - 1
                        if cursor == og_cur:
                            none_found = True
                        try_print(cursor, og_cur)
                offset = 0
                tracker = 0
                alt = False
                ctrl = False
            elif event.scancode == KEY["RIGHT"]:
                if cursor + 1 < len(albums):
                    cursor += 1
                else:
                    cursor = 0
                offset = 0
                tracker = 0
                alt = False
                ctrl = False
            elif event.scancode == KEY["UP"]:
                if tracker - 1 >= 0:
                    tracker -= 1
                alt = False
                ctrl = False
            elif event.scancode == KEY["DOWN"]:
                if tracker + 1 < len(album_info["Tracks"]):
                    tracker += 1
                alt = False
                ctrl = False
            elif event.scancode == KEY["ENTER"]:
                try:
                    f = album_info['Tracks'][tracker + 1]['file']
                except KeyError:
                    try:
                        f = album_info["Tracks"][list(album_info["Tracks"])[tracker]]['file']
                    except IndexError:
                        continue
                if f in queue:
                    queue.remove(f)
                else:
                    queue.append(f)
                alt = False
                ctrl = False
            elif event.scancode == KEY["ALT"]:
                alt = not alt
                ctrl = False
            elif event.scancode == KEY["BKSP"] and finding:
                search = search[:-1]
            elif event.scancode == KEY["F1"] and alt:
                return "f1"
            elif event.scancode == KEY["F5"]:
                refresh_cache = True
                return "m"
            elif event.scancode == KEY["CTRL"]:
                ctrl = not ctrl
                alt = False
        elif event.type in EVT["INPUT"] and event.text:
            if ctrl:
                if evt.text in __available_keys:
                    return evt.text
            elif alt:
                if evt.text == "f":
                    finding = not finding
                elif evt.text == "a":
                    for track in t_nums:
                        try:
                            f = album_info["Tracks"][track]["file"]
                        except KeyError:
                            f = album_info["Tracks"][t_bk[t_og[track]]]['file']
                        if f in queue:
                            queue.remove(f)
                        else:
                            queue.append(f)
                elif event.text in "+=":
                    FONT.change_size(FONT.size + 2)
                elif event.text in "-_":
                    FONT.change_size(FONT.size - 2)
            elif finding:
                search += event.text
            else:
                txt = event.text.lower()
                if any(str(cursor_album[c]).lower().startswith(txt) for c in cursor_album):
                    cursor += 1
                    if cursor == len(albums):
                        cursor = 0
                    while not str(cursor_album[cursor]).lower().startswith(txt):
                        cursor += 1
                        if cursor == len(albums):
                            cursor = 0
            alt = False
        elif event.type in EVT["WHEEL"]:
            if event.y == 1:
                if offset - 1 >= 0:
                    offset -= 1
                    if offset + TERM.h - 12 < tracker and tracker - 1 >= 0:
                        tracker -= 1
                elif tracker - 1 >= 0:
                    tracker -= 1
            elif event.y == -1:
                if offset + 1 < len(album_info["Tracks"]) - (TERM.h - 12):
                    offset += 1
                    if offset > tracker and tracker + 1 < len(album_info["Tracks"]):
                        tracker += 1
                elif tracker + 1 < len(album_info["Tracks"]):
                    tracker += 1
            elif event.x == 1:
                kb_press(Key.left)
            elif event.x == -1:
                kb_press(Key.right)
        elif event.type in EVT["CLICK"]:
            if event.button == 1:
                if event.pos[1] >= (TERM.h - 3) * FONT.size + TERM.border.y and event.pos[0] <= FONT.width * 2 + TERM.border.x:
                    kb_press(Key.left)
                elif event.pos[1] >= (TERM.h - 3) * FONT.size + TERM.border.y and event.pos[0] >= (TERM.w - 2) * FONT.width - TERM.border.x:
                    kb_press(Key.right)
                else:
                    kb_press(Key.enter)
                alt = False
                ctrl = False
            elif event.button == 3:
                alt = not alt
        elif event.type in EVT["MOUSEMOVE"]:
            t1 = tracker
            tracker = offset + mouse_cursor(event, 9, 12, album_info["Tracks"])
            if t1 == tracker:
                skip_draw = True
