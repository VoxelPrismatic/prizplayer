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
        echo("-------=================[ SHORTCUTS ]=================--------", center = TERM.w, color = 0x00ff88, font = FONT.b)
        echo_n(' These keys can be used anywhere ', center = TERM.w, font = FONT.r, char = "-")
        echo(color = 0xaaaaaa)
        event = None
        keys = {
            "ALT + o": "Open file",
            "ALT + p": "Player",
            "ALT + q": "Show queue",
            "ALT + s": "Save queue",
            "ALT + l": "Load queue",
            "ALT + c": "Configuration",
            "ALT + m": "Show your albums",
            "ALT + F1": "This screen",
            "ALT + t": "Tips & Tricks",
        }
        for key in keys:
            echo_n(" " * 16 + key + " ", left = int(TERM.w / 2), char = "-", color = 0xeeeeee if TERM.y % 2 else 0xaaaaaa)
            echo(" " + keys[key] + " " * 16, right = int(TERM.w / 2), char = "-")
        echo()
        echo(' PLAYER ONLY ', center = TERM.w, char = "-")
        echo()
        keys = {
            "r": "Repeat all/one/none",
            "s": "Shuffle on/off",
            "ALT + ->": "Next track",
            "SHIFT + .": "Next track",
            "ALT + <-": "Prev track",
            "SHIFT + ,": "Prev track",
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
        echo_n("Be sure to press alt")
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
