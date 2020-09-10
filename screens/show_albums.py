# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

file_formats = [
    ".3gp", ".asf", ".avi", ".dvr-ms", ".flv",
    ".mkv", ".midi", ".mid", ".qtff", ".mp4",
    ".mp3", ".mp2", ".mpeg", ".m4a", ".ogg",
    ".ogm", ".wav", ".aiff", ".mxf", ".vob",
    ".rm", ".aac", ".ac3", ".alac", ".amr",
    ".dts", ".xm", ".flac", ".mace", ".mod",
    ".opus", ".pls", ".qcp", ".qdm2", ".qdmc",
    ".wma", ".wmv", ".webm", ".ogv"
]

def grab_files(root):
    ls = []
    for f in os.listdir(root):
        try:
            ls.extend(grab_files(root + f + "/"))
        except:
            if any(f.lower().endswith(x) for x in file_formats):
                ls.append(root + f)
    return ls

def show_albums():
    global hold_display, term_y, term_x
    cursor = 0
    offset = 0
    tracker = 0
    clear(0x111522)
    echo("         -------===============[ FINDING ALBUMS ]===============-------         ", color = 0x0088ff, font = font_b)
    echo("-" * 80, font = font_r)
    echo("Give me just a moment, I'm searching for your music")
    term_y = 28
    echo("--------------------------------------------------------------------------------", color = 0x004488, font = font_b)
    echo("                                                                              ;]")
    prefs = json.loads(open("conf.json").read())
    albums = {}
    music = []
    cursor_album = {}
    finding = False
    search = ""
    alt = False
    term_y = 3
    echo("Locating...")
    for directory in prefs["search_dirs"]:
        music.extend(grab_files(directory))
    echo("Parsing...")
    for track in music:
        tags = id3.tag.Tag()
        tags.parse(open(track, "rb"))
        if tags is None:
            continue
        print(dir(tags))
#        print(tags.file_info.)
        try:
            albums[tags.album]["Tracks"][tags.track_num[0]] = {"file": track, "name": tags.title, "cover": None}
            try:
                albums[tags.album]["Tracks"][tags.track_num[0]]["cover"] = \
                    tags.frame_set[b'APIC'][0].image_data
            except:
                pass
        except:
            dic = {}
            try:
                dic["Year"] = tags.recording_date.year
            except:
                dic["Year"] = "<Unknown>"
            dic["Album"] = tags.album or track.split("/")[-2]
            print(dic["Album"])
            dic["Artist"] = tags.artist or "<Unknown>"
            dic["Tracks"] = {}
            albums[tags.album] = dic
            albums[tags.album]["Tracks"][tags.track_num[0]] = {"file": track, "name": tags.title, "cover": None}
            try:
                img = tags.frame_set[b'APIC'][0].image_data
                albums[tags.album]["Tracks"][tags.track_num[0]]["cover"] = img
                albums[tags.album]["Cover"] = img
            except:
                pass
    for album in albums:
        cursor_album[len(cursor_album)] = album
    while True:
        hold_display = True
        none_found = False
        clear(0x111522)
        echo("         -------================[ YOUR  ALBUMS ]================-------         ", color = 0x0088ff, font = font_b)
        if finding:
            search = ' "' + search + '" '
            echo_n(f"{search:-^80}", font = font_r)
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
                print(cursor, og_cur)
            print(",")
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
        if not finding:
            echo_n(f"{' ' + album_info['Album'] + ' ':-^80}", font = font_r)
        echo(color = 0xffffff)
        event = None
        echo(album_info["Album"], font = font_b)
        echo(album_info["Artist"], font = font_ri)
        echo()
        num_tracks = str(len(album_info["Tracks"]))
        echo_n(num_tracks + " track", font = font_r)
        if num_tracks == "1":
            echo()
        else:
            echo("s")
        echo("Released in " + str(album_info["Year"]))
        if offset == 0:
            echo(color = 0xaaaaaa)
        else:
            echo("  ...", font = font_b, color = 0xaaaaaa)
        term.fill(rgb(0x333744), rect = (0, (tracker - offset + 8) * 16 + 12, term_w, 16))


        t_nums = list(album_info["Tracks"])
        t_og = {}
        t_bk = t_nums
        count = -1
        for i in range(len(t_nums)):
            count += 1
            if type(t_nums[i]) != int:
                t_nums[i] = count
                t_og[count] = i
        t_nums.sort()


        try:
            album_info["Cover"]
        except:
            album_info["Cover"] = open("./assets/icon.png", "rb").read()
        img = pygame.Surface.convert(
            pygame.image.load(
                io.BytesIO(album_info["Cover"] or open("./assets/icon.png", "rb").read())
            ).convert_alpha()
        )
        img = pygame.transform.smoothscale(img, (156, 156))
        term.blit(img, (term_w - 166, 48, 156, 156))

        for track in t_nums[offset:]:
            try:
                if album_info['Tracks'][track]['file'] in queue:
                    echo_n(color = 0xffffff)
                else:
                    echo_n(color = 0xaaaaaa)
                echo_n(f"{track:0>2}] ", font = font_r)
                echo(album_info['Tracks'][track]['name'] or "<NULL>", font = font_b)
            except KeyError:
                echo_n(f"{track:0>2}] ", font = font_r)
                try:
                    echo(str(album_info["Tracks"][t_bk[t_og[track]]]['name']), font = font_b)
                except KeyError:
                    echo("<NULL>", font = font_b)
            if term_y == 27 and track != t_nums[-1]:
                echo("  ...", color = 0xaaaaaa)
                break
        term_y = 27
        echo("<" + " " * 78 + ">", font = font_b, color = 0xffffff)
        echo(f"{'[' + str(cursor + 1) + '/' + str(len(albums)) + ']':->80}", color = 0x004488)
        if alt:
            echo("a - Toggle all tracks in queue  /  f - Toggle search  /  F1 - More screens    ;]")
        elif tracker + 1 in list(album_info['Tracks']) and album_info['Tracks'][tracker + 1]['file'] in queue:
            echo("ALT - Use shortcut  /  ENTER - Remove from queue                              ;]")
        else:
            echo("ALT - Use shortcut  /  ENTER - Add to queue                                   ;]")
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
            if event.scancode == KEY["LEFT"]:
                if cursor - 1 >= 0:
                    cursor -= 1
                else:
                    cursor = len(albums) - 1
                offset = 0
                tracker = 0
                alt = False
            elif event.scancode == KEY["RIGHT"]:
                if cursor + 1 < len(albums):
                    cursor += 1
                else:
                    cursor = 0
                offset = 0
                tracker = 0
                alt = False
            elif event.scancode == KEY["UP"]:
                if tracker - 1 >= 0:
                    tracker -= 1
                if offset > tracker and offset - 1 >= 0:
                    offset -= 1
                alt = False
            elif event.scancode == KEY["DOWN"]:
                if tracker + 1 < len(album_info["Tracks"]):
                    tracker += 1
                if offset + 18 < tracker and offset + 1 < len(album_info["Tracks"]):
                    offset += 1
                alt = False
            elif evt.scancode == KEY["ENTER"]:
                f = album_info['Tracks'][tracker + 1]['file']
                if f in queue:
                    queue.remove(f)
                else:
                    queue.append(f)
                alt = False
            elif evt.scancode == KEY["ALT"]:
                alt = not alt
            elif evt.scancode == KEY["BKSP"] and finding:
                search = search[:-1]
            elif evt.scancode == KEY["F1"]:
                return "f1"
        elif event.type in EVT["INPUT"] and event.text:
            if alt:
                if evt.text in __available_keys:
                    return evt.text
                elif evt.text == "f":
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
                if tracker - 1 >= 0:
                    tracker -= 1
                if offset > tracker and offset - 1 >= 0:
                    offset -= 1
                alt = False
            elif event.y == -1:
                if tracker + 1 < len(album_info["Tracks"]):
                    tracker += 1
                if offset + 18 < tracker and offset + 1 < len(album_info["Tracks"]):
                    offset += 1
                alt = False
            elif event.x == 1:
                if cursor - 1 >= 0:
                    cursor -= 1
                else:
                    cursor = len(albums) - 1
                offset = 0
                tracker = 0
                alt = False
            elif event.x == -1:
                if cursor + 1 < len(albums):
                    cursor += 1
                else:
                    cursor = 0
                offset = 0
                tracker = 0
                alt = False
        elif event.type in EVT["CLICK"]:
            if event.button == 1:
                f = album_info['Tracks'][tracker + 1]['file']
                if f in queue:
                    queue.remove(f)
                else:
                    queue.append(f)
                alt = False
            elif event.button == 3:
                alt = not alt
