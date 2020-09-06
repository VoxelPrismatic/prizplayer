# #] PRIZ PLAYER ;]
A music player with a terminal aesthetic

# #] REASON
As a Kubuntu user, I've been using KDE's Elisa for quite a while. Elisa is a slow music player that 
for some reason plays the same track several times in a row in shuffle mode and cannot enter single track
mode. I decided to make my own music player with a terminal aesthetic because that looks neat.

# #] NOTICE
This is still in the alpha phase, so you're going to have to install VLC and Python 3.7+ yourself.

For linux users, do not use the provided desktop file, because that is for my use only for now. 

### #] Current missing features:
- Repeat
- Shuffle
- Single track
- Adjusting queue
- Switching to a different screen from the player
- Skip track
- Fast forward
- Previous track
- Rewind
- Save queue
- Refresh music on request rather than doing so every single time

### #] Current existing features:
- File chooser
- Album/music locator
  - Allows you to add a full album or songs from an album
  - 5x faster than Elisa: 10s vs 2s
- Cover art viewer
- Player
- Queue
- Play/pause

# #] SCREENSHOTS [v0.8 alpha]
![Startup screen](https://media.discordapp.net/attachments/569698278271090728/752224892040249374/unknown.png)
![Album viewer](https://media.discordapp.net/attachments/569698278271090728/752225328813834280/unknown.png)
![File chooser](https://media.discordapp.net/attachments/569698278271090728/752225455171698839/unknown.png)
![Queue viewer](https://media.discordapp.net/attachments/569698278271090728/752225691667529829/unknown.png)
![Locations](https://media.discordapp.net/attachments/569698278271090728/752225833506308127/unknown.png)
![Player](https://media.discordapp.net/attachments/569698278271090728/752226100901445642/unknown.png)

# #] Formats
PRIZ PLAYER uses VLC as it's backend, so it supports most all file formats. Here is a list 
of files you can view within the viewer. If you know of the extensions to other formats that VLC
supports, feel free to let me know under the issues tab.

`.3gp`, `.asf`, `.avi`, `.dvr-ms`, `.flv`,
`.mkv`, `.midi`, `.mid`, `.qtff`, `.mp4`,
`.mp3`, `.mp2`, `.mpeg`, `.m4a`, `.ogg`,
`.ogm`, `.wav`, `.aiff`, `.mxf`, `.vob`,
`.rm`, `.aac`, `.ac3`, `.alac`, `.amr`,
`.dts`, `.xm`, `.flac`, `.mace`, `.mod`,
`.opus`, `.pls`, `.qcp`, `.qdm2`, `.qdmc`,
`.wma`, `.wmv`, `.webm`, `.ogv`
