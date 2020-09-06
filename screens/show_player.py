# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

enqueue = 0
music = None
repeat = False
shuffle = False
single = False
paused = False
history = []

#def start_music()

def show_player():
    global enqueue, music, term_y, hold_display, repeat, shuffle, single, paused
    prefs = json.loads(open("./conf.json").read())
    unqueue = []
    while True:
        hold_display = True
        clear(0x112222)
        echo("         -------================[ PRIZ  PLAYER ]================-------         ", color = 0x00ffff, font = font_b)
        echo("-" * 80, font = font_r)
        if len(queue):
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
            if not music or music.get_position() == 1:
                music = vlc.MediaPlayer(queue[enqueue])
                music.play()
                print(music)
                print(dir(music))
            term_y = 26
            echo_n(font = font_b)
            if paused:
                echo("                  [ |< ]   [ << ]   [  >   ]   [ >> ]   [ >| ]")
                echo("                   -PREV-   -RWND-   --PLAY--   -FFWD-   -NEXT-", color = 0x008888)
            else:
                echo("                  [ |< ]   [ << ]   [  ||  ]   [ >> ]   [ >| ]")
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
            if not shuffle:
                if single:
                    echo("ALT - Shortcut / r - No loop / s - Shuffle /  SHIFT Arrow - Prev/Next         ;]")
                elif repeat:
                    echo("ALT - Shortcut / r - Loop single / s - Shuffle / SHIFT + Arrow - Prev/Next    ;]")
                else:
                    echo("ALT - Shortcut / r - Loop all / s - Shuffle / SHIFT + Arrow - Prev/Next       ;]")
            else:
                if single:
                    echo("ALT - Shortcut / r - No loop / s - No shuffle / SHIFT + Arrow - Prev/Next     ;]")
                elif repeat:
                    echo("ALT - Shortcut / r - Loop single / s - No shuffle / SHIFT + Arrow - Prev/Next ;]")
                else:
                    echo("ALT - Shortcut / r - Loop all / s - No shuffle / SHIFT + Arrow - Prev/Next    ;]")
            event = None
            seconds = int(music.get_length() / 1000)
            minutes = int(seconds / 60)
            seconds %= 60
            song_time = f"{minutes:02}:{seconds:02}"
            last_position = -1
            last_time = time.monotonic()
            while event is None and time.monotonic() - last_time < 0.5:
                if music.get_position() != last_position:
                    hold_display = True
                    last_time = time.monotonic()
                    seconds = int(music.get_position() * music.get_length() / 1000)
                    minutes = int(seconds / 60)
                    seconds %= 60
                    term_y = 23
                    term.fill(rgb(0x112222), rect = (0, term_y * 16 + 12, term_w, 32))
                    echo(f"{minutes:02}:{seconds:02}", font = font_b, color = 0x00ffff)
                    term_y -= 1
                    echo(f"{song_time:>80}")
                    echo(f"[{']':>79}")
                    term_y -= 1
                    term.fill(rgb(0x00ffff), rect = (18, term_y * 16 + 16, (term_w - 36) * music.get_position(), 8))
                    last_position = music.get_position()
                    print(last_time, last_position)
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
            if music.get_position() < 1:
                pass
            elif single:
                music.play()
            elif shuffle and not repeat:
                unqueue.append(enqueue)
                while enqueue in unqueue:
                    enqueue = random.choice(range(len(queue)))
                del music
                music = vlc.MediaPlayer(queue[enqueue])
                music.play()
            elif shuffle and repeat:
                old_enqueue = enqueue
                while enqueue == old_enqueue:
                    enqueue = random.choice(range(len(queue)))
                del music
                music = vlc.MediaPlayer(queue[enqueue])
                music.play()
            elif repeat and not single:
                enqueue += 1
                if enqueue == len(queue):
                    enqueue = 0
                del music
                music = vlc.MediaPlayer(queue[enqueue])
                music.play()
            else:
                enqueue += 1
                if enqueue == len(queue):
                    enqueue = 0
                    paused = True
                del music
                music = vlc.MediaPlayer(queue[enqueue])
                if not paused:
                    music.play()
            if event:
                if event.type in EVT["INPUT"]:
                    if evt.text in " pPkK":
                        if paused:
                            music.play()
                        else:
                            music.pause()
                        paused = not paused
                    #elif evt.text == "j":

        else:
            echo("Nothing is in the queue")
            redraw()
