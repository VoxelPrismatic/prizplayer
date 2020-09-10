# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

def show_shortcuts():
    global hold_display, term_y, term_x, queue
    while True:
        hold_display = True
        clear(0x112215)
        echo("         -------=================[ SHORTCUTS ]=================--------         ", color = 0x00ff88, font = font_b)
        echo_n(f"{' These keys can be used anywhere ':-^80}", font = font_r)
        echo(color = 0xaaaaaa)
        event = None
        keys = {
            "ALT + o": "Open file",
            "ALT + p": "Player",
            "ALT + q": "Show queue",
            "ALT + l": "Show where I find music",
            "ALT + m": "Show your albums"
        }
        for key in keys:
            echo_n(f'{" " * 15 + key + " ":-<40}', color = 0xeeeeee if term_y % 2 else 0xaaaaaa)
            echo(f'{" " + keys[key] + " " * 15:->40}')
        echo()
        echo(f"{'PLAYER ONLY':-^80}")
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
        }
        for key in keys:
            echo_n(f'{" " * 15 + key + " ":-<40}', color = 0xeeeeee if term_y % 2 else 0xaaaaaa)
            echo(f'{" " + keys[key] + " " * 15:->40}')
        term_y = 28
        echo("--------------------------------------------------------------------------------", color = 0x008844, font = font_b)
        echo("Be sure to press alt                                                          ;]")
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
        elif event.type in EVT["INPUT"] and event.text:
            if evt.text in __available_keys:
                return evt.text
