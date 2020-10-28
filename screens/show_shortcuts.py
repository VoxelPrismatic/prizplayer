# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

def show_shortcuts():
    global TERM, queue
    while True:
        TERM.hold = True
        clear(0x112215)
        echo("--------=================[ SHORTCUTS ]=================--------", center = TERM.w, color = 0x00ff88, font = FONT.b)
        echo_n(' These keys can be used anywhere ', center = TERM.w, font = FONT.r, char = "-")
        echo(color = 0xaaaaaa)
        event = None
        keys = {
            "CTRL + o": "Open file",
            "CTRL + p": "Player",
            "CTRL + q": "Show queue",
            "CTRL + s": "Save queue",
            "CTRL + l": "Load queue",
            "CTRL + c": "Configuration",
            "CTRL + m": "Show your albums",
            "CTRL + t": "Tips & Tricks",
            "ALT + F1": "This screen",
            "ALT + +": "Increase font size",
            "ALT + -": "Decrease font size"
        }
        for key in keys:
            echo_n(" " * 16 + key + " ", left = int(TERM.w / 2), char = "-", color = 0xeeeeee if TERM.y % 2 else 0xaaaaaa)
            echo(" " + keys[key] + " " * 16, right = int(TERM.w / 2), char = "-")
        echo()
        echo(' PLAYER ONLY ', center = TERM.w, char = "-", color = 0x00ff88)
        echo()
        keys = {
            "r": "Repeat all/one/none",
            "s": "Shuffle on/off",
            "ALT + ->": "Next track",
            "ALT + <-": "Prev track",
            "->": "Fast forward",
            "<-": "Rewind",
            "SPACE": "Pause",
            "UP": "Volume up",
            "DOWN": "Volume down"
        }
        for key in keys:
            echo_n(" " * 16 + key + " ", left = int(TERM.w / 2), char = "-", color = 0xaaaaaa if TERM.y % 2 else 0xeeeeee)
            echo(" " + keys[key] + " " * 16, right = int(TERM.w / 2), char = "-")
        TERM.foot()
        echo("-" * TERM.w, color = 0x008844, font = FONT.b)
        echo_n("Press a shortcut key")
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
            elif event.text in "+=":
                FONT.change_size(FONT.size + 2)
            elif event.text in "-_":
                FONT.change_size(FONT.size - 2)
