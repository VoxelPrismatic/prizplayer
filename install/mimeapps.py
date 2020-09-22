import os
f = f"/home/{os.getlogin()}/.config/mimeapps.list"
lines = open(f).read().split("\n")

while "audio/prizplaylist=prizplayer.desktop;" in lines:
    lines.remove("audio/prizplaylist=prizplayer.desktop;")

for block in ["[Added Associations]", "[Default Applications]"]:
    l = 0
    for line in lines[:]:
        l += 1
        if line == block:
            lines.insert(l, "audio/prizplaylist=prizplayer.desktop;")
            break

open(f, "w").write("\n".join(lines))
