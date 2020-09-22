# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

def show_tricks():
    global TERM, queue
    while True:
        TERM.hold = True
        clear(0x221122)
        echo("--------=================[ TIPS AND TRICKS ]=================--------", center = TERM.w, color = 0xff00ff, font = FONT.b)
        echo_n(' Tricks with MPRIS ', center = TERM.w, font = FONT.r, char = "-")
        echo()
        echo_s(
            "MPRIS is the communication standard that allows you to control the music player from, say, your bluetooth speaker/earbuds. "
            "These tricks only apply to MPRIS devices.", 
            color = 0xffffff)
        echo(color = 0xaaaaaa)
        echo("1] You can seek through the song")
        echo("2] You can jump to the next or previous tracks")
        echo("3] Hitting STOP will be the same as hitting PLAY/PAUSE")
        echo("4] You can adjust the volume if your device supports it")
        echo("5] If you just touch the volume slider, it'll be set to 100%")
        echo("6] You can go up to 200% volume, just move the slider to the end")
        TERM.foot()
        echo("-" * TERM.w, color = 0x880088, font = FONT.b)
        echo_n("*MPRIZ  /  Press a key shortcut key")
        echo(";]", right = TERM.rem)
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
        try_print(f"\x1b[94;1m{evt.type}\x1b[0m:", evt)
        if event is None:
            continue
        elif event.type in EVT["INPUT"] and event.text:
            if evt.text in __available_keys:
                return evt.text
