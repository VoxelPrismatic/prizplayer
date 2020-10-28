# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

import threading
import logging
import pydub
logging.basicConfig(level = 'INFO')

just_enqueued = 0
enqueue = 0
music = None
media = None
prefs = json.loads(open("conf.json").read())
repeat = prefs["repeat"]
shuffle = prefs["shuffle"]
single = prefs["single"]
paused = False
tags = None
in_player = False
now_playing = ""
now_playing_cover = ""
history = []
unqueue = []
lastqueue = []
openedqueue = []
openedtime = time.monotonic()
sound = None
wait_for_sound = True
sound_itme = 0
sound_samples = []

def vlc_callback(*a, **kw):
    print(a, kw)

def pydub_sound(*queue_):
    global enqueue, sound, wait_for_sound, sound_samples
    wait_for_sound = True
    print("\n" * 10, "LOADING")
    sound = pydub.AudioSegment.from_file(queue_[enqueue])
    aud = sound.raw_data
    samp = []
    #for b in range(0, len(aud), 2):
        #samp.append(-(aud[b + 1] - aud[b] + 1))
    sound_samples = samp
    print("\n" * 10, "---")
    wait_for_sound = False

def handle_player_click(event, seconds, forceclick = False):
    global TERM, music, enqueue, queue, unqueue, shuffle, repeat, single, paused
    try:
        pos = event.pos
    except:
        pos = pygame.mouse.get_pos()
    try:
        try:
            btns = [event.button]
        except:
            btns = [event.buttons]
    except:
        btns = pygame.mouse.get_pressed()
    if forceclick:
        btns = [1, 3]
    half = TERM.w / 2
    if pos[1] >= (TERM.h - 4) * FONT.size + TERM.border.y and pos[1] <= (TERM.h - 3) * FONT.size + TERM.border.y:
        if pos[0] >= (half - 2) * FONT.width and pos[0] <= (half + 6) * FONT.width:
            #Play/pause
            kb_press(Key.space)
        elif pos[0] >= (half - 11) * FONT.width and pos[0] <= (half - 5) * FONT.width:
            #Rewind
            kb_press(Key.left)
        elif pos[0] >= (half + 9) * FONT.width and pos[0] <= (half + 15) * FONT.width:
            #Fast forward
            kb_press(Key.right)
        elif pos[0] >= (half - 20) * FONT.width and pos[0] <= (half - 14) * FONT.width:
            #Previous
            kb_press(Key.shift, ",")
        elif pos[0] >= (half + 18) * FONT.width and pos[0] <= (half + 24) * FONT.width:
            #Next
            kb_press(Key.shift, ".")
    elif pos[1] >= (TERM.h - 6) * FONT.size + TERM.border.y and pos[1] <= (TERM.h - 5) * FONT.size + TERM.border.y and any(btns):
        x = pos[0] - TERM.border.x - FONT.width #Beginning bracket
        if x >= 0 and x <= TERM.px.w - TERM.border.x - FONT.width:
            music.set_position(x / (TERM.px.w - 2 * (TERM.border.x + FONT.width)))
    elif pos[1] >= (TERM.h - 2) * FONT.size + TERM.border.y and pos[1] <= (TERM.h - 1) * FONT.size + TERM.border.y and any(btns):
        if pos[0] <= FONT.width * 3 + TERM.border.x:
            kb_press("s")
        elif pos[0] >= FONT.width * 5 + TERM.border.x and pos[0] <= FONT.width * 7 + TERM.border.x :
            kb_press("r")

def ss(n):
    #Strip special, just returns lowercase with numbers and letters and _-
    n = n.lower()
    nn = ""
    for l in n:
        if l in "abcdefghijklmnopqrstuvwxyz1234567890_-":
            nn += l
    return nn

def fix_image(img):
    headers = [
        b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46', # JFIF
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52' #PNG
    ]
    for header in headers:
        if header in img and not img.startswith(header):
            img = header + img.split(header, 1)[-1]
    return img

def fix_queue(again = True):
    global queue
    queue2 = []
    for que in queue:
        if que:
            if os.path.isdir(que):
                queue2.extend(grab_files(que))
            elif any(que.lower().endswith(x) for x in file_formats):
                queue2.append(que)
            elif que.lower().endswith(".prz"):
                queue2.extend(open(que).read().split("\n"))
    queue = queue2
    while "" in queue:
        queue.remove("")
    if again:
        fix_queue(False)
        if queue:
            open(s(f"./queues/LATEST.PRZ"), "w+").write("\n".join(queue))


def next_track(queue_, music, enqueue):
    global unqueue, tags, now_playing, mpris, cover, player, media, now_playing_cover, paused, sound
    fix_queue()
    if music is not None:
        music.stop()
        music.set_mrl(queue_[enqueue])
    else:
        music = vlc.MediaPlayer(queue_[enqueue])
    #media = vlc.Media(queue_[enqueue])
    #media.parse()
    music.play()
    t = threading.Timer(0.01, pydub_sound, queue_)
    t.start()
    i = music.get_instance()
    i.set_app_id("com.priz.player", "1.4.8.BETA", "x-audio-prizplaylist")
    i.set_user_agent("PRIZ PLAYER ;]", "PrizPlayer/1.4.8.BETA")
    paused = False
    try_print(f"\x1b[92;1mPlaying track {enqueue}\x1b[0m")
    try:
        if now_playing_cover:
            os.remove(s(now_playing_cover))
    except:
        pass
    try:
        tags = tinytag.TinyTag.get(queue_[enqueue], image = True)
        cover = tags.get_image() or open(s("./assets/icon.png"), "rb").read()
    except:
        tags = tinytag.TinyTag.get(queue_[enqueue])
        cover = open(s("./assets/icon.png"), "rb").read()
    cover = fix_image(cover)
    now_playing = queue_[enqueue]
    title = tags.title or queue_[enqueue].split(folder_slash)[-1]
    album = tags.album or queue_[enqueue].split(folder_slash)[-2]
    artist = tags.artist or "anonymous"
    now_playing_cover = os.getcwd() + f"/assets/{ss(artist)}-{ss(album)}-{ss(title)}"
    open(s(now_playing_cover), "wb+").write(cover)
    while len(unqueue) >= 500:
        unqueue = unqueue[1:]
    handle_dbus()
    open(s(f"./queues/LATEST.PRZ"), "w+").write("\n".join(queue))
    return music

def timer_end_of_track():
    global queue, lastqueue, in_player, now_playing, music, mpris, openedqueue, openedtime
    global mpris_event
    try:
        if queue != lastqueue and queue:
            lastqueue = queue
            if music:
                if enqueue >= len(queue):
                    if now_playing in queue:
                        enqueue = queue.endex(now_playing) - 1
                    else:
                        enqueue = len(queue) - 1
                        music = next_track(queue, music, enqueue)
            handle_dbus()
        if not in_player:
            try_print(":D")
            check_end_of_track()
        else:
            try_print(";]")
    except Exception as ex:
        try:
            open(f"/home/{os.getlogin()}/.config/prizplayer/tb.txt", "w+").write(
                f"\n{str(type(ex))[8:-2]}: {ex}"
                "\n".join(traceback.format_tb(ex.__traceback__))
            )
        except:
            pass
    if openedqueue != open(s("./cache/adding")).read().split("\n"):
        openedtime = time.monotonic()
        openedqueue = open(s("./cache/adding")).read().split("\n")
    elif openedqueue and time.monotonic() - openedtime > 0.5:
        openedtime = time.monotonic()
        for thing in openedqueue:
            if thing not in queue:
                queue.append(thing)
        openedqueue = []
        fix_queue()
        open(s("./cache/adding"), "w").write("")
        mpris_event = True
    t = threading.Timer(0.1, timer_end_of_track)
    t.start()

def timer_dbus():
    handle_dbus()
    t = threading.Timer(10, timer_dbus)
    t.start()

def check_end_of_track():
    global enqueue, unqueue, music, queue, paused, shuffle, repeat, single, tags
    global alt_cover, media
    fix_queue()
    if (music is None or now_playing not in queue) and queue:
        music = next_track(queue, music, min(enqueue, len(queue) - 1))
        if paused:
            music.pause()
    elif music and not queue:
        music.stop()
        music = None
        media = None
        tags = None
        handle_dbus()
        return
    elif music is None:
        return
    i = music.get_instance()
    i.set_app_id("com.priz.player", "1.4.8.BETA", "x-audio-prizplaylist")
    i.set_user_agent("PRIZ PLAYER ;]", "PrizPlayer/1.4.8.BETA")
    if str(music.get_state()) not in ["State.Ended", "State.Stopped"]:
        pass
    elif single:
        try_print("\x1b[95;1mSINGLE TRACK\x1b[0m")
        unqueue.append(enqueue)
        music = next_track(queue, music, enqueue)
    elif shuffle and not repeat:
        try_print("\x1b[95;1mSHUFFLE ONCE\x1b[0m")
        unqueue.append(enqueue)
        while enqueue in unqueue[-len(queue) + 1:] and len(queue) > 1:
            enqueue = random.choice(range(len(queue)))
        music = next_track(queue, music, enqueue)
    elif shuffle and repeat:
        try_print("\x1b[95;1mSHUFFLE LOOP\x1b[0m")
        unqueue.append(enqueue)
        old_enqueue = enqueue
        while enqueue == old_enqueue and len(queue) > 1:
            enqueue = random.choice(range(len(queue)))
        music = next_track(queue, music, enqueue)
    elif repeat and not single:
        try_print("\x1b[95;1mREPEAT ALL\x1b[0m")
        unqueue.append(enqueue)
        enqueue += 1
        if enqueue == len(queue):
            enqueue = 0
        music = next_track(queue, music, enqueue)
    else:
        try_print("\x1b[95;1mNEXT TRACK\x1b[0m")
        unqueue.append(enqueue)
        enqueue += 1
        if enqueue == len(queue):
            enqueue = 0
            paused = True
        music = next_track(queue, music, enqueue)
        try_print(music.get_state())
        if enqueue == 0:
            time.sleep(0.1)
            music.pause()
            paused = True
    try_print(music.get_state())
    if str(music.get_state()) == "State.Stopped":
        music.play()
        music.pause()

def handle_dbus(event = True):
    try:
        global mpris, mpris_event, music
        if music:
            i = music.get_instance()
            i.set_app_id("com.priz.player", "1.4.8.BETA", "x-audio-prizplaylist")
            i.set_user_agent("PRIZ PLAYER ;]", "PrizPlayer/1.4.8.BETA")

        #try_print(dir(mpris))
        mpris_event = event
        mpris_server.base.dbus_emit_changes(
            mpris.player,
            ["Metadata", "PlaybackStatus", "Volume", "Shuffle", "LoopStatus"]
        )
    except:
        pass

def show_player():
    global enqueue, music, repeat, shuffle, single, queue
    global paused, tags, unqueue, in_player, mpris_event
    global TERM, sound, wait_for_sound, sound_samples
    prefs = json.loads(open(s("./conf.json")).read())
    alt = False
    ctrl = False
    in_player = True
    skip_draw = False
    dragging = False
    mpris_event = False
    old_width_samples = []
    width_averaging = 3
    samples_width = 64
    tmss = time.monotonic()
    while True:
        fix_queue()
        if not skip_draw or mpris_event:
            TERM.hold = True
            clear(0x112222)
            echo("--------===============[ PRIZ PLAYER ;] ]===============--------", center = TERM.w, color = 0x00ffff, font = FONT.b)
            echo("-" * TERM.w, font = FONT.r)
        if len(queue):
            if not skip_draw or mpris_event:
                enqueue = min(enqueue, len(queue) - 1)
                if music is None:
                    music = next_track(queue, music, enqueue)
                i = music.get_instance()
                i.set_app_id("com.priz.player", "1.4.8.BETA", "x-audio-prizplaylist")
                i.set_user_agent("PRIZ PLAYER ;]", "PrizPlayer/1.4.8.BETA")
                try:
                    tags = tinytag.TinyTag.get(queue[enqueue], image = True)
                    cover = tags.get_image() or open(s("./assets/icon.png"), "rb").read()
                except:
                    tags = tinytag.TinyTag.get(queue[enqueue])
                    cover = open(s("./assets/icon.png"), "rb").read()
                cover = fix_image(cover)
                title = tags.title or queue_[enqueue].split(folder_slash)[-1]
                album = tags.album or queue_[enqueue].split(folder_slash)[-2]
                artist = tags.artist or "<Unknown>"
                echo_s(title, off_width = 20, font = FONT.b)
                echo_s(album, off_width = 20, font = FONT.r)
                echo_s(artist, off_width = 20, font = FONT.i)
                echo()

                echo_n("CHANNELS ] ", font = FONT.r)
                if tags.channels == 2:
                    echo("STEREO", font = FONT.b)
                else:
                    echo("MONO", font = FONT.b)
                samples = tags.samplerate
                echo_n(" SAMPLES ] ", font = FONT.r)
                if samples > 1_000:
                    echo(f"{samples / 1_000:.1f} KHz", font = FONT.b)
                else:
                    echo(f"{samples} Hz", font = FONT.b)
                bitrate = tags.bitrate
                echo_n(" BITRATE ] ", font = FONT.r)
                echo(f"{bitrate:.0f} Kb/s", font = FONT.b)
                echo_n("RELEASED ] ", font = FONT.r)
                echo(tags.year or "0000", font = FONT.b)

                try:
                    img = pygame.Surface.convert(
                        pygame.image.load(
                            io.BytesIO(cover)
                        ).convert_alpha()
                    )
                except:
                    img = pygame.Surface.convert(
                        pygame.image.load(
                            open(s("./assets/icon.png"), "rb")
                        )
                    )

                img = pygame.transform.smoothscale(img, IMG.hw)
                term.blit(img, (TERM.px.w - IMG.w - TERM.border.x, 2 * FONT.size + TERM.border.y, IMG.w, IMG.h))
                TERM.y = TERM.h - 4
                echo_n(font = FONT.b)
                play_color = 0x00ffff
                pos = pygame.mouse.get_pos()
                try_print(pos)
                if pos[1] >= (TERM.h - 4) * FONT.size + TERM.border.y and pos[1] <= (TERM.h - 3) * FONT.size + TERM.border.y:
                    try_print(".")
                    half = TERM.w / 2
                    if pos[0] >= (half - 2) * FONT.width and pos[0] <= (half + 6) * FONT.width:
                        color = 0xffffff
                    else:
                        color = 0x00ffff
                    echo("                  [   /  ]                  ", center = TERM.w, color = color)
                    play_color = color
                    TERM.y -= 1
                    if pos[0] >= (half - 11) * FONT.width and pos[0] <= (half - 5) * FONT.width:
                        color = 0xffffff
                    else:
                        color = 0x00ffff
                    echo("         [    ]                             ", center = TERM.w, color = color)
                    TERM.y -= 1
                    echo("           <<                               ", center = TERM.w, y_offset = 1)
                    TERM.y -= 1
                    if pos[0] >= (half + 9) * FONT.width and pos[0] <= (half + 15) * FONT.width:
                        color = 0xffffff
                    else:
                        color = 0x00ffff
                    echo("                             [    ]         ", center = TERM.w, color = color)
                    TERM.y -= 1
                    echo("                               >>           ", center = TERM.w, y_offset = 1)
                    TERM.y -= 1
                    if pos[0] >= (half - 20) * FONT.width and pos[0] <= (half - 14) * FONT.width:
                        color = 0xffffff
                    else:
                        color = 0x00ffff
                    echo("[ /  ]                                      ", center = TERM.w, color = color)
                    TERM.y -= 1
                    echo("   <                                        ", center = TERM.w, y_offset = 1)
                    TERM.y -= 1
                    if pos[0] >= (half + 18) * FONT.width and pos[0] <= (half + 24) * FONT.width:
                        color = 0xffffff
                    else:
                        color = 0x00ffff
                    echo("                                      [  / ]", center = TERM.w, color = color)
                    TERM.y -= 1
                    echo("                                        >   ", center = TERM.w, y_offset = 1)
                else:
                    echo("[ /  ]   [    ]   [   /  ]   [    ]   [  / ]", center = TERM.w)
                    TERM.y -= 1
                    echo("   <       <<                  >>       >   ", center = TERM.w, y_offset = 1)
                echo("-PREV-   -RWND-   -=    =-   -FFWD-   -NEXT-", center = TERM.w, color = 0x008888)
                TERM.y -= 2
                if paused:
                    echo("> ", center = TERM.w, y_offset = 1, color = play_color)
                    echo("PLAY", center = TERM.w, color = 0x008888)
                else:
                    echo("/ ", center = TERM.w, color = play_color)
                    echo("STOP", center = TERM.w, color = 0x008888)
                if shuffle:
                    echo_n("[~]-")
                else:
                    echo_n("[=]-")
                if repeat:
                    echo_n("[O]")
                elif single:
                    echo_n("[1]")
                else:
                    echo_n("[-]")
                echo_n("-[        ]")
                vol = music.audio_get_volume() if not music.audio_get_mute() else 0
                vols = [
                    #[Start, offset, color]
                    [0, 100, 0x008888],  #Blue: 0-100
                    [100, 50, 0x888800], #Yellow: 100-150
                    [150, 30, 0x884400], #Orange: 150-180
                    [180, 20, 0x880000]  #Red: 180-200
                ]
                for x, y, z in vols:
                    term.fill(
                        rgb(z),
                        rect = (
                            9 * FONT.width + TERM.border.x,
                            TERM.y * FONT.size + TERM.border.y + round(FONT.width * 3 / 4),
                            8 * FONT.width * min(max(0, vol - x) / y, 1),
                            FONT.width
                        )
                    )
                echo(f"[{vol}%]-[{enqueue + 1}/{len(queue)}]", right = TERM.rem, char = "-")
                if ctrl:
                    echo_n("CTRL // q - Show queue  /  m - Show albums")
                elif alt:
                    echo_n("ALT // <- - Prev track  /  -> - Next track  /  F1 - Help")
                else:
                    echo_n("ALT/CTRL - Shortcut  /  ")
                    if single:
                        echo_n("r - No loop  /  ")
                    elif repeat:
                        echo_n("r - Loop one  /  ")
                    else:
                        echo_n("r - Loop all  /  ")
                    if shuffle:
                        echo_n("s - No shuffle")
                    else:
                        echo_n("s - Shuffle")
                echo(";]", right = TERM.rem)
            skip_draw = False
            seconds = int(music.get_length() / 1000)
            total_time = seconds
            minutes = int(seconds / 60)
            seconds %= 60
            song_time = f"{minutes:02}:{seconds:02}"
            last_position = -1
            handle_dbus(event = False)
            vol = music.audio_get_volume()
            mute = music.audio_get_mute()
            #tracks = media.tracks_get()
            event = None
            mpris_event = False
            resync_ms = False
            while event is None and str(music.get_state()) not in ["State.Ended", "State.Stopped"] and \
                not mpris_event and vol == music.audio_get_volume() and mute == music.audio_get_mute():
                TERM.hold = True
                tt = time.monotonic()
                if music.get_position() != last_position:
                    if last_position != -1 or old_width_samples == []:
                        mtt = time.monotonic()
                    #try_print(unqueue)
                    #try_print(music.audio_get_volume())
                    #try_print(dir(music))
                    #try_print(music.get_media().get_stats(None))
                    #try_print(json.dumps(music.get_instance().vlm_show_media(""), indent = 4))
                    #try_print(dir(tracks))
                    #try_print(dir(vlc))
                    #try_print(music.get_state())
                    seconds = max(int(music.get_position() * music.get_length() / 1000), 0)
                    rem_sec = total_time - seconds
                    minutes = int(seconds / 60)
                    seconds %= 60
                    rem_min = int(rem_sec / 60)
                    rem_sec %= 60
                    TERM.y = TERM.h - 7
                    rem_time = f"-{rem_min:02}:{rem_sec:02}"
                    term.fill(rgb(0x112222), rect = (0, TERM.y * FONT.size + TERM.border.y, TERM.px.w, FONT.size * 3))
                    echo(f"{minutes:02}:{seconds:02}", font = FONT.b, color = 0x00ffff)
                    TERM.y -= 1
                    echo(song_time, right = TERM.w)
                    echo("[" + "]".rjust(TERM.w - 1))
                    TERM.y -= 1
                    term.fill(
                        rgb(0x00ffff), rect = (
                            FONT.width + TERM.border.x,
                            TERM.y * FONT.size + TERM.border.y + round(FONT.width * 3 / 4),
                            (TERM.px.w - TERM.off.x * 2 - (FONT.width + TERM.border.x) * 2) * music.get_position(),
                            FONT.width
                        )
                    )
                    TERM.y += 1
                    echo(rem_time, right = TERM.w)
                    last_position = music.get_position()
                    try_print(time.monotonic(), last_position)
                if False:#not paused and not wait_for_sound:
                    print("\x1b[93;1m", int((time.monotonic() - tmss) * 1000), music.get_time(), int(music.get_length() * music.get_position()), "\x1b[0m")
                    nnn = int((time.monotonic() - tmss) * 1000) / music.get_time()
                    print("\x1b[94;1m", nnn, "\x1b[0m")
                    try:
                        old_width_samples.append(width_samples)
                        if len(old_width_samples) == width_averaging:
                            old_width_samples = old_width_samples[1:]
                    except:
                        pass
#                    sound_sample_length_ms = len(sound_samples) / tags.samplerate * 1000 / tags.channels
 #                   music_length_ms = music.get_length()
                    ms = music.get_length() * music.get_position() + (time.monotonic() - mtt) * 1000# + (music_length_ms - sound_sample_length_ms) / 2
                    ms *= 8 * nnn - 7# (len(sound_samples) / tags.samplerate * 1000 / tags.channels) / music.get_length()
                    ms = round(ms)
                    #print("\x1b[93;1m", ms, music.get_time(), "\x1b[0m")
                    rt = int(tags.samplerate / 1000)
                    #ms = int((time.monotonic() - tmss) * 1000) / (2.5 * nnn - 1.5)
                    #samples = sound_samples[ms * rt * tags.channels:(ms + 64) * rt * tags.channels]
                    samples = sound[ms:ms+64].get_array_of_samples()
                    #print(samples)
                    width_samples = []
                    step = 16
                    voldub = music.audio_get_volume() / 100
                    try:
                        for sample in range(0, len(samples), step):
                            #print(samples[sample:sample + step])
                            width_samples.append(abs(sum(samples[sample:sample + step])) / step / 510 * 2 * voldub)
                        #print(width_samples)
                        #print(width_samples, len(width_samples), TERM.w)
                        if old_width_samples:
                            n_s = -1
                            max_samples = []
                            for old_samples in old_width_samples:
                                n_s += 1
                                if n_s == 0:
                                    for x in range(min(len(old_samples), len(width_samples))):
                                        if width_samples[x] > old_samples[x]:
                                            try:
                                                for y in range(len(old_width_samples)):
                                                    old_width_samples[y][x] = width_samples[x]
                                            except IndexError:
                                                #Lazy check
                                                pass
                                        width_samples[x] += old_samples[x]
                                else:
                                    for x in range(min(len(old_samples), len(width_samples))):
                                        width_samples[x] += old_samples[x]
                            for x in range(len(width_samples)):
                                width_samples[x] /= (len(old_width_samples) + 1)
                        height = TERM.px.h - 20 * FONT.size - TERM.border.y
                        bar_width = (TERM.px.w - 2 * TERM.border.x) / len(width_samples)
                        term.fill(rgb(0x112222), rect = (0, 12 * FONT.size + TERM.border.y, TERM.px.w, height))
                        for x in range(len(width_samples)):
                            term.fill(
                                rgb(0x00ffff), rect = (
                                    bar_width * x + TERM.border.x,
                                    12 * FONT.size + TERM.border.y + height - height * min(width_samples[x], 1),
                                    (bar_width * 1.5),
                                    height * min(width_samples[x], 1)
                                )
                            )
                            if width_samples[x] > 1:
                                temp_sample = min(width_samples[x] - 1, 1)
                                term.fill(
                                    rgb(0xff0000), rect = (
                                        bar_width * x + TERM.border.x,
                                        12 * FONT.size + TERM.border.y + height - height * temp_sample,
                                        (bar_width * 1.5),
                                        height * temp_sample
                                    )
                                )
                    except (ZeroDivisionError, IndexError, pydub.exceptions.TooManyMissingFrames):
                        TERM.y = TERM.h - 9
                        echo("*end of track", center = TERM.w, cls = True)
                    time.sleep(max(samples_width / 1000 - time.monotonic() + tt, 0))
                else:
                    TERM.y = TERM.h - 9
                    #if paused:
                        #echo("*paused", center = TERM.w, cls = True)
                    #else:
                        #echo("just a sec ;]", center = TERM.w, cls = True)
                    time.sleep(samples_width / 1000)
                redraw()
                for evt in pygame.event.get():
                    if evt.type in EVT["QUIT"]:
                        kill()
                    elif evt.type in [*EVT["INPUT"], *EVT["MOUSEMOVE"], *EVT["KEYDOWN"], *EVT["WHEEL"], *EVT["CLICK"]]:
                        event = evt
                    elif evt.type in EVT["WINDOW"]:
                        mpris_event = True
                        if evt.type == 32768 and evt.gain == 1 and evt.state == 1:
                            handle_player_click(None, None, True)


            check_end_of_track()
            try:
                try_print(f"\x1b[94;1m{evt.type}\x1b[0m:", event)
            except NameError:
                continue
            if event is None:
                skip_draw = not mpris_event
                continue
            if event.type in EVT["KEYUP"]:
                pygame.key.set_repeat(500, 50)
            if event.type in EVT["KEYDOWN"]:
                if event.scancode == KEY["PLAY_PAUSE"]:
                    paused = not paused
                    if paused:
                        music.pause()
                    else:
                        ms = music.get_time()
                        music.play()
                if event.scancode == KEY["LEFT"]:
                    if alt:
                        kb_press(Key.shift, ",")
                        ms = music.get_time()
                        alt = False
                        tmss = time.monotonic()
                    else:
                        music.set_position(max(music.get_position() - 5000 / music.get_length(), 0))
                        pygame.key.set_repeat(500, 500)
                        tmss += 5
                elif event.scancode == KEY["RIGHT"]:
                    if alt:
                        kb_press(Key.shift, ".")
                        alt = False
                    else:
                        music.set_position(min(music.get_position() + 5000 / music.get_length(), 1))
                        pygame.key.set_repeat(500, 500)
                        tmss -= 5
                    ms = music.get_time()
                elif event.scancode == KEY["UP"]:
                    music.audio_set_volume(min(200, int(music.audio_get_volume() / 2) * 2 + 2))
                    pygame.key.set_repeat(500, 5)
                elif event.scancode == KEY["DOWN"]:
                    music.audio_set_volume(max(0, int(music.audio_get_volume() / 2) * 2 - 2))
                    pygame.key.set_repeat(500, 5)
                elif event.scancode == KEY["ALT"]:
                    alt = not alt
                    ctrl = False
                elif event.scancode == KEY["F1"] and alt:
                    in_player = False
                    return "f1"
                elif event.scancode == KEY["CTRL"]:
                    ctrl = not ctrl
                    alt = False
            elif event.type in EVT["INPUT"] and event.text:
                if ctrl:
                    if event.text in __available_keys:
                        in_player = False
                        return event.text
                if alt:
                    if event.text in "+=":
                        FONT.change_size(FONT.size + 2)
                    elif event.text in "-_":
                        FONT.change_size(FONT.size - 2)
                if event.text in " pPkK":
                    if paused:
                        music.play()
                        ms = music.get_time()
                    else:
                        music.pause()
                    paused = not paused
                    if str(music.get_state()) == "State.Ended":
                        music = next_track(queue, music, enqueue)
                        paused = False
                elif event.text in "rR":
                    if not repeat and not single:
                        repeat = True
                        single = False
                    elif repeat and not single:
                        repeat = False
                        single = True
                    elif not repeat and single:
                        repeat = False
                        single = False
                elif event.text in "sS":
                    shuffle = not shuffle
                elif event.text in "<":
                    if seconds < 5 and unqueue:
                        if shuffle:
                            enqueue = unqueue.pop()
                        else:
                            enqueue -= 1
                            if enqueue == -1:
                                enqueue += len(queue)
                        music = next_track(queue, music, enqueue)
                    elif seconds < 5:
                        music.stop()
                    else:
                        music.set_position(0)
                    ms = music.get_time()
                elif event.text in ">":
                    music.stop()
                    try_print(music.get_state())
                    ms = music.get_time()
            elif event.type in EVT["WHEEL"]:
                if event.y:
                    music.audio_set_volume(min(200, music.audio_get_volume() + event.y))
                else:
                    music.set_position(max(min(music.get_position() - 2000 * event.x / music.get_length(), 1), 0))
                    ms = music.get_time()
            elif event.type in EVT["CLICK"]:
                handle_player_click(event, seconds)
            elif event.type in EVT["MOUSEMOVE"]:
                skip_draw = True
                if any(event.buttons):
                    already = pos[1] >= (TERM.h - 9) * FONT.size and pos[1] <= (TERM.h - 2) * FONT.size
                    not_ready = pos[1] >= (TERM.h - 5) * FONT.size and pos[1] <= (TERM.h - 4) * FONT.size
                    if dragging and already or not_ready:
                        dragging = True
                        x = pos[0] - TERM.border.x - FONT.width #Beginning bracket
                        if x >= 0 and x <= TERM.px.w - TERM.border.x - FONT.width:
                            music.set_position(x / (TERM.px.w - 2 * (TERM.border.x + FONT.width)))
                            ms = music.get_time()
                            skip_draw = False
                    else:
                        dragging = False
                elif pos[1] >= (TERM.h - 4):
                    skip_draw = False
                    dragging = False
                else:
                    skip_draw = True
                    dragging = False
        else:
            echo("Nothing is in the queue")
            if open("./queues/LATEST.PRZ").read().strip():
                echo("Hit ENTER to load the most recent queue")
            else:
                echo("Nothing is in the recent queue either")
            TERM.foot()
            echo("-" * TERM.w, font = FONT.b, color = 0x008888)
            echo_n("Press a shortcut key")
            echo(";]", right = TERM.rem)
            redraw()
            evt = None
            while not queue and evt is None:
                evt = pygame.event.poll()
                if evt.type == 0:
                    time.sleep(0.01)
                    continue
                if evt.type in EVT["QUIT"]:
                    kill()
                elif evt.type in [*EVT["INPUT"], *EVT["KEYDOWN"]]:
                    event = evt
                    rep = False
                else:
                    continue
                if event.type in EVT["KEYDOWN"]:
                    if event.scancode == KEY["ENTER"]:
                        try:
                            enqueue = int(prefs["enqueue"])
                        except:
                            enqueue = 0
                        queue = open("./queues/LATEST.PRZ").read().split("\n")
                        in_player = False
                        return "p"
                elif event.type in EVT["INPUT"] and event.text:
                    if evt.text in __available_keys:
                        in_player = False
                        return evt.text
                    elif event.text in "+=":
                        FONT.change_size(FONT.size + 2)
                    elif event.text in "-_":
                        FONT.change_size(FONT.size - 2)

