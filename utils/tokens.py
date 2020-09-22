# NOTICE: This program is licensed under GPLv2. That means all programs or
# projects using this code must remain opensource. Feel free to edit as you
# please, but no warranty is provided. More info is in the LICENSE file
# located in the root of the repository.

class Keys:
    def __init__(self, *codes):
        self.codes = codes
    def __eq__(self, other: int):
        return any(other == code for code in self.codes)
    def __contains__(self, other: int):
        return any(other == code for code in self.codes)
    def __list__(self):
        return self.codes
    def __iter__(self):
        for code in self.codes:
            yield code

EVT = {
    "INPUT": Keys(771),
    "KEY": Keys(769),
    "KEYDOWN": Keys(768),
    "KEYUP": Keys(769),
    "MOUSEMOVE": Keys(1024),
    "WHEEL": Keys(1027),
    "CLICK": Keys(1026),
    "WINDOW": Keys(32768, 32760, 512),
    "QUIT": Keys(256)
}

KEY = {
    "UP": Keys(82),
    "DOWN": Keys(81),
    "LEFT": Keys(80),
    "RIGHT": Keys(79),

    "CTRL": Keys(224, 228),
    "ALT": Keys(226, 230),
    "SHIFT": Keys(225, 229),
    "CTX": Keys(101),
    "ESC": Keys(41),
    "DEL": Keys(76),
    "INS": Keys(73),
    "TAB": Keys(43),
    "BKSP": Keys(42),
    "ENTER": Keys(40, 88),
    "PAUSE": Keys(72),

    "SCROLL_LOCK": Keys(71),
    "NUM_LOCK": Keys(83),
    "CAPS_LOCK": Keys(57),

    "PREV_PAGE": Keys(270),
    "NEXT_PAGE": Keys(271),

    "NEXT_SONG": Keys(258),
    "PREV_SONG": Keys(259),
    "PLAY_PAUSE": Keys(261),

    "STAR": Keys(274),

    "PAGE_UP": Keys(75),
    "PAGE_DOWN": Keys(78),
    "HOME": Keys(74),
    "END": Keys(77),

    "F1": Keys(58),
    "F2": Keys(59),
    "F3": Keys(60),
    "F4": Keys(61),
    "F5": Keys(62),
    "F6": Keys(63),
    "F7": Keys(64),
    "F8": Keys(65),
    "F9": Keys(66),
    "F10": Keys(67),
    "F11": Keys(68),
    "F12": Keys(69),
}
