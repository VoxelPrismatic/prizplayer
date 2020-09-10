# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

enqueue = 0
just_enqueued = 0
music = None
repeat = False
shuffle = False
single = False
paused = False
tags = None
volume = 100
history = []
unqueue = []

def next_track(queue, music, enqueue):
    global unqueue
    music.stop()
    del music
    print(f"\x1b[92;1mPlaying track {enqueue}\x1b[0m")
    music = vlc.MediaPlayer(queue[enqueue])
    music.play()
    while len(unqueue) >= 500:
        unqueue = unqueue[1:]
    return music

def handle_dbus():
    global music, tags, repeat, shuffle, single, volume
    global player_props
    props = {
        "Volume": volume,
        "Shuffle": shuffle,
        "LoopStatus": repeat,
        "Rate": 1.0
    }
    for prop in props:
        player_props.Set('org.mpris.MediaPlayer2.Player', prop, props[prop])

def show_player():
    global enqueue, music, term_y, hold_display, repeat, shuffle, single
    global paused, term_x, tags, volume, unqueue
    prefs = json.loads(open("./conf.json").read())
    alt = False
    while True:
        hold_display = True
        clear(0x112222)
        echo("         -------===============[ PRIZ PLAYER ;] ]===============-------         ", color = 0x00ffff, font = font_b)
        echo("-" * 80, font = font_r)
        if len(queue):
            if not music:
                music = vlc.MediaPlayer(queue[enqueue])
                music.play()
                print(music)
                print(dir(music))
            tags = id3.tag.Tag()
            tags.parse(open(queue[enqueue], "rb"))
            echo(tags.title, font = font_b)
            echo(tags.album, font = font_r)
            echo(tags.artist, font = font_ri)
            try:
                cover = tags.frame_set[b'APIC'][0].image_data
            except:
                cover = open("./assets/icon.png", "rb").read()
            img = pygame.Surface.convert(
                pygame.image.load(
                    io.BytesIO(cover or open("./assets/icon.png", "rb").read())
                ).convert_alpha()
            )
            img = pygame.transform.smoothscale(img, (156, 156))
            term.blit(img, (term_w - 166, 48, 156, 156))
            term_y = 26
            echo_n(font = font_b)
            if paused:
                echo("                  [ /< ]   [ << ]   [  >\\  ]   [ >> ]   [ >/ ]")
                echo("                   -PREV-   -RWND-   --PLAY--   -FFWD-   -NEXT-", color = 0x008888)
            else:
                echo("                  [ /< ]   [ << ]   [  //  ]   [ >> ]   [ >/ ]")
                echo("                   -PREV-   -RWND-   --STOP--   -FFWD-   -NEXT-", color = 0x008888)
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
            echo(f"{'[' + str(enqueue + 1) + '/' + str(len(queue)) + ']':->73}")
            if alt:
                echo_n("F1 - More Screens  /  <- - Prev track  /  -> - Next track")
            else:
                echo_n("ALT - Shortcut  /  ")
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
            echo(" " * (78 - term_x) + ";]")
            event = None
            seconds = int(music.get_length() / 1000)
            total_time = seconds
            minutes = int(seconds / 60)
            seconds %= 60
            song_time = f"{minutes:02}:{seconds:02}"
            last_position = -1
            while event is None and str(music.get_state()) not in ["State.Ended", "State.Stopped"]:
                if music.get_position() != last_position:
                    print(unqueue)
                    #print(dir(music))
                    #print(dir(vlc))
                    print(music.get_state())
                    hold_display = True
                    seconds = max(int(music.get_position() * music.get_length() / 1000), 0)
                    rem_sec = total_time - seconds
                    minutes = int(seconds / 60)
                    seconds %= 60
                    rem_min = int(rem_sec / 60)
                    rem_sec %= 60
                    term_y = 23
                    rem_time = f"-{rem_min:02}:{rem_sec:02}"
                    term.fill(rgb(0x112222), rect = (0, term_y * 16 + 12, term_w, 48))
                    echo(f"{minutes:02}:{seconds:02}", font = font_b, color = 0x00ffff)
                    term_y -= 1
                    echo(f"{song_time:>80}")
                    echo(f"[{']':>79}")
                    term_y -= 1
                    term.fill(rgb(0x00ffff), rect = (18, term_y * 16 + 16, (term_w - 36) * music.get_position(), 8))
                    term_y += 1
                    echo(f"{rem_time:>80}")
                    last_position = music.get_position()
                    print(time.monotonic(), last_position)
                    redraw()
                time.sleep(0.01)
                for evt in pygame.event.get():
                    if evt.type in EVT["QUIT"]:
                        kill()
                    elif evt.type in [*EVT["INPUT"], *EVT["KEY"], *EVT["KEYDOWN"], *EVT["WHEEL"], *EVT["CLICK"]]:
                        event = evt
                        rep = False
                    elif evt.type in EVT["WINDOW"]:
                        pygame.display.update()
            if str(music.get_state()) not in ["State.Ended", "State.Stopped"]:
                pass
            elif single:
                unqueue.append(enqueue)
                music = next_track(queue, music, enqueue)
            elif shuffle and not repeat:
                unqueue.append(enqueue)
                while enqueue in unqueue[-len(queue) + 1:] and len(queue) > 1:
                    enqueue = random.choice(range(len(queue)))
                music = next_track(queue, music, enqueue)
            elif shuffle and repeat:
                unqueue.append(enqueue)
                old_enqueue = enqueue
                while enqueue == old_enqueue and len(queue) > 1:
                    enqueue = random.choice(range(len(queue)))
                music = next_track(queue, music, enqueue)
            elif repeat and not single:
                unqueue.append(enqueue)
                enqueue += 1
                if enqueue == len(queue):
                    enqueue = 0
                music = next_track(queue, music, enqueue)
            else:
                unqueue.append(enqueue)
                print("\x1b[95;1mNEXT TRACK\x1b[0m")
                enqueue += 1
                if enqueue == len(queue):
                    enqueue = 0
                    paused = True
                music = next_track(queue, music, enqueue)
                print(music.get_state())
                if paused:
                    time.sleep(0.1)
                    music.pause()
            if str(music.get_state()) == "State.Stopped":
                music.play()
                music.pause()
            if event:
                if event.type in EVT["KEYUP"]:
                    pygame.key.set_repeat(500, 50)
                if event.type in EVT["KEYDOWN"]:
                    if event.scancode == KEY["PLAY_PAUSE"]:
                        paused = not paused
                        if paused:
                            music.pause()
                        else:
                            music.play()
                    if event.scancode == KEY["LEFT"]:
                        if alt:
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
                        else:
                            music.set_position(music.get_position() - 5000 / music.get_length())
                            pygame.key.set_repeat(500, 500)
                        alt = False
                    elif event.scancode == KEY["RIGHT"]:
                        if alt:
                            music.stop()
                            print(music.get_state())
                        else:
                            music.set_position(music.get_position() + 5000 / music.get_length())
                            pygame.key.set_repeat(500, 500)
                        alt = False
                    elif evt.scancode == KEY["ALT"]:
                        alt = not alt
                elif event.type in EVT["INPUT"] and event.text:
                    if alt:
                        if evt.text in __available_keys:
                            return evt.text
                    if evt.text in " pPkK":
                        if paused:
                            music.play()
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
                    elif event.text in ">":
                        music.stop()
                        print(music.get_state())


        else:
            echo("Nothing is in the queue")
            term_y = 28
            redraw()
            echo("-" * 80, font = font_b, color = 0x008888)
            echo("o - Open file  /  m - Your albums  /  F1 - More screens                       ;]")
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
            if event.type in EVT["INPUT"] and event.text:
                if evt.text in __available_keys:
                    return evt.text
