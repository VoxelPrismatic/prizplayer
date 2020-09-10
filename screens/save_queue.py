# NOTICE: This file is executed, not imported.

# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

def save_queue():
    name = ""
    alt = False
    linux = os.getcwd().startswith("/")
    while True:
        hold_display = True
        clear(0x222511)
        echo("         -------=================[ SAVE QUEUE ]=================-------         ", color = 0xff8800, font = font_b)
        echo("-" * 80, font = font_r)
        echo()
        echo_n(f"File name ] {name}", color = 0xffffff)
        echo(".PRZ", font = font_ri)
        evt = pygame.event.wait()
        if evt.type in EVT["QUIT"]:
            kill()
        elif evt.type in [*EVT["INPUT"], *EVT["KEYDOWN"]]:
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
            if evt.scancode == KEY["BKSP"] and finding:
                name = name[:-1]
            elif evt.scancode == KEY["ALT"]:
                alt = not alt
            elif evt.scancode == KEY["ENTER"]:
                try:
                    f = open("./queues/" + name + ".PRZ", "w+")
                except:
                    f = open(".\\queues\\" + name + ".PRZ", "w+")
                f.write("\n".join(queue))
                f.close()
                return "q"
        elif event.type in EVT["INPUT"]:
            if alt:
                if event.text in __available_keys:
                    return event.text
            else:
                if event.text in "/\\?%*:\"><" and not linux:
                    continue
                elif event.text in "/" and linux:
                    continue
                name += event.text
