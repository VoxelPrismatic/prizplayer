#!/bin/bash

echo -e "\e[94;1mPRIZ PLAYER ;]\e[0m"
echo -e "\e[94v1.4.8 BETA\e[0m"
echo -e "\e[93;1mNOTICE:\e[0m This installer is compatible with Linux distros that use APT or DNF."
echo
echo -e "\e[92;1mPlease enter your password to automatically install/update dependencies\e[0m"
{
    sudo echo "Thanks!"
} || {
    echo -e "\e[91;1mERROR: No password given\e[0m"
    echo -e "The installation cannot continue."
    exit
}

{
    echo -e "\e[95;1mTrying APT\e[0m"
    sudo apt install python3 python3-dev python3-vlc python3-pip python3-dbus vlc -y
    sudo apt upgrade python3 python3-dev python3-vlc python3-pip python3-dbus vlc -y
} || {
    echo -e "\e[95;1mTrying DNF\e[0m"
    sudo dnf install python3-devel python3-pip python3-dbus
    sudo dnf upgrade python3-devel python3-pip python3-dbus
    sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
    sudo dnf install http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-rawhide.noarch.rpm
    sudo dnf install python-vlc
#     } || {
#         echo -e "\e[95;1mTrying RPM\e[0m"
#
#     } || {
#         echo -e "\e[95;1mTrying PACMAN\e[0m"
#         pacman -S vlc
} || {
    echo -e "\e[91;1mCannot install python3, python3-dev, python3-vlc, python3-pip."
    echo -e "Please install them with your package manager\e[0m"
    echo "The installation cannot continue."
    exit
}

echo -e "\e[92;1mInstalling dependencies in Python\e[0m"
python3 -m pip install -r req.txt

echo -e "\e[92;1mSeting up application\e[0m"

mkdir ~/.config/prizplayer 2> /dev/null

echo -e "\e[90m> Creating and installing DESKTOP file\e[0m"
echo "#!/usr/bin/env xdg-open" > prizplayer.desktop
echo "[Desktop Entry]" >> prizplayer.desktop
echo "Name=PRIZ PLAYER ;]" >> prizplayer.desktop
echo "Path=/home/$(whoami)/.config/prizplayer" >> prizplayer.desktop
echo "Comment=A music player with a terminal aesthetic" >> prizplayer.desktop
echo "GenericName=Music Player" >> prizplayer.desktop
echo "Exec=/home/$(whoami)/.config/prizplayer/prizplayer.py" >> prizplayer.desktop
echo "Icon=/home/$(whoami)/.config/prizplayer/assets/icon.png" >> prizplayer.desktop
echo "Type=Application" >> prizplayer.desktop
echo "Categories=Audio;AudioVideo" >> prizplayer.desktop
echo "MimeType=audio/aac;audio/mp4;audio/mpeg;audio/mpegurl;audio/vnd.rn-realaudio;audio/vorbis;audio/x-flac;audio/x-mp3;audio/x-mpegurl;audio/x-ms-wma;audio/x-musepack;audio/x-oggflac;audio/x-pn-realaudio;audio/x-scpls;audio/x-speex;audio/x-vorbis;audio/x-wav;application/x-ogm-audio;audio/x-vorbis+ogg;audio/ogg;audio/prizplaylist;inode/directory;" >> prizplayer.desktop

cp prizplayer.desktop ~/.config/prizplayer/prizplayer.desktop
sudo desktop-file-install ~/.config/prizplayer/prizplayer.desktop

echo -e "\e[90m> Creating and installing MIME type\e[0m"
echo '<?xml version="1.0" encoding="utf-8"?>' > prizplaylist.xml
echo '<mime-type xmlns="http://www.freedesktop.org/standards/shared-mime-info" type="audio/prizplaylist">' >> prizplaylist.xml
echo '  <!--Created automatically by update-mime-database. DO NOT EDIT!-->' >> prizplaylist.xml
echo '  <comment>PRIZ PLAYLIST ;]</comment>' >> prizplaylist.xml
echo "  <icon name=\"/home/$(whoami)/.config/prizplayer/assets/icon.png\"/>" >> prizplaylist.xml
echo '  <glob-deleteall/>' >> prizplaylist.xml
echo '  <glob pattern="*.PRZ"/>' >> prizplaylist.xml
echo '  <glob pattern="*.PRz"/>' >> prizplaylist.xml
echo '  <glob pattern="*.PrZ"/>' >> prizplaylist.xml
echo '  <glob pattern="*.Prz"/>' >> prizplaylist.xml
echo '  <glob pattern="*.pRZ"/>' >> prizplaylist.xml
echo '  <glob pattern="*.pRz"/>' >> prizplaylist.xml
echo '  <glob pattern="*.prZ"/>' >> prizplaylist.xml
echo '  <glob pattern="*.prz"/>' >> prizplaylist.xml
echo '</mime-type>' >> prizplaylist.xml

cp prizplaylist.xml ~/.local/share/mime/audio/prizplaylist.xml

update-mime-database ~/.local/share/mime 2> /dev/null

python3 mimeapps.py

echo -e "\e[90m> Copying application\e[0m"

cp ../screens ~/.config/prizplayer/screens -R 2> /dev/null
cp ../cache ~/.config/prizplayer/cache -n -R 2> /dev/null
cp ../queues ~/.config/prizplayer/queues -R -n 2> /dev/null
cp ../assets ~/.config/prizplayer/assets -R 2> /dev/null
cp ../utils ~/.config/prizplayer/utils -R 2> /dev/null
cp ../conf.json ~/.config/prizplayer/conf.json -R -n 2> /dev/null
cp ../prizplayer.py ~/.config/prizplayer/prizplayer.py -R 2> /dev/null
cp ../LICENSE ~/.config/prizplayer/LICENSE -R 2> /dev/null

chmod +x ~/.config/prizplayer/prizplayer.py
