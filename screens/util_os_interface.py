from typing import List
import asyncio
from mpris_server.adapters import Metadata, PlayState, MprisAdapter, \
  Microseconds, VolumeDecimal, RateDecimal
from mpris_server.base import URI, MIME_TYPES, BEGINNING, DEFAULT_RATE, DbusObj
from mpris_server.server import Server
from mpris_server.adapters import EventAdapter
import mpris_server

class PrizAdapter(MprisAdapter):
    def get_uri_schemes(self) -> List[str]:
        return URI
    def get_mime_types(self) -> List[str]:
        return MIME_TYPES


    def can_quit(self) -> bool:
        return True
    def quit(self):
        kill()


    def get_current_position(self):
        global music
        if music is None:
            return 0
        return music.get_position() * music.get_length() * 1000
    def seek(self, time):
        global music
        music.set_position(max(min((time / 1000) / music.get_length(), 1), 0))
        handle_dbus()
        return music.get_position()


    def next(self):
        global music
        if music:
            music.stop()
    def previous(self):
        global music, queue, unqueue, enqueue, shuffle, paused
        if music is None:
            return
        seconds = max(int(music.get_position() * music.get_length() / 1000), 0)
        if seconds < 5 and unqueue:
            if shuffle:
                enqueue = unqueue.pop()
            else:
                enqueue -= 1
                if enqueue == -1:
                    enqueue += len(queue)
            music = next_track(queue, music, enqueue)
            if paused:
                music.pause()
        elif seconds < 5:
            music.stop()
        else:
            music.set_position(0)
            handle_dbus()


    def play(self):
        global music, paused
        if music:
            music.play()
            paused = False
            handle_dbus()
    def pause(self):
        global music, paused
        if paused:
            return self.play()
        if music:
            music.pause()
            paused = True
            handle_dbus()
    def resume(self):
        self.play()
    def stop(self):
        self.pause()


    def get_volume(self) -> VolumeDecimal:
        global music
        v = 100
        if music:
            v = music.audio_get_volume()
            if music.audio_get_mute():
                return 0
        if v < 100:
            return v / 100
        elif v < 150:
            return v / 150
        elif v < 180:
            return v / 180
        return v / 200
    def set_volume(self, val: VolumeDecimal):
        global music, mpris_event
        v = 1
        if music:
            v = music.audio_get_volume()
        if v < 100:
            val = int(val * 100)
        elif v < 150:
            val = int(val * 150)
        elif v < 180:
            val = int(val * 180)
        else:
            val = int(val * 200)
        if val >= v - 2 and val <= v + 2:
            val = 100
        if music:
            music.audio_set_volume(val)
            mpris_event = True
            music.audio_set_mute(False)
        handle_dbus()



    def get_playstate(self) -> PlayState:
        global paused, music
        if music is None:
            PlayState.STOPPED
        if paused:
            return PlayState.PAUSED
        return PlayState.PLAYING


    def is_repeating(self) -> bool:
        global repeat
        return repeat
    def set_repeating(self, val: bool):
        global repeat
        repeat = val
        handle_dbus()
        return repeat
    def set_loop_status(self, val: str):
        print(val)
#        return self.set_repeating(val)


    def is_playlist(self) -> bool:
        return self.can_go_next() or self.can_go_previous()


    def get_rate(self) -> float:
        return 1.0
    def set_rate(self, val: float):
        pass


    def get_shuffle(self) -> bool:
        global shuffle
        return shuffle
    def set_shuffle(self, val: bool):
        global shuffle
        shuffle = val
        handle_dbus()
        return shuffle


    def get_art_url(self, track):
        pass
    def get_stream_title(self):
        pass


    def is_mute(self) -> bool:
        global music
        if music is None:
            return True
        return music.audio_get_volume() == 0 or music.audio_get_mute()
    def set_mute(self, val: bool):
        global music, volume
        vol = music.audio_get_volume()
        music.audio_set_mute(val)

    def can_go_next(self) -> bool:
        return True
    def can_go_previous(self) -> bool:
        return True
    def can_play(self) -> bool:
        return True
    def can_pause(self) -> bool:
        return True
    def can_seek(self) -> bool:
        return True
    def can_control(self) -> bool:
        return True


    def get_stream_title(self) -> str:
        return "PRIZ PLAYER ;]"


    def metadata(self) -> dict:
        global enqueue, queue, tags, music, folder_slash, now_playing_cover
        if tags is None:
            try_print("\x1b[90;1mNO METADATA\x1b[0m")
            return {
                "xesam:title": "PRIZ PLAYER ;]",
                "mpris:artUrl": "file://" + os.getcwd() + "/assets/icon.png"
            }
        if music is None or music.get_length() == 0:
            t = threading.Timer(0.5, handle_dbus)
            t.start()
        title = tags.title or queue_[enqueue].split(folder_slash)[-1]
        album = tags.album or queue_[enqueue].split(folder_slash)[-2]
        artist = (tags.artist or "").split(", ") or ["<Unknown>"]
        albumartist = (tags.albumartist or "").split(", ") or artist
        try:
            track_num = int(tags.track)
        except:
            track_num = 0
        try:
            comment = [tags.comment]
        except:
            comment = []
        metadata = {
            "mpris:trackid": "/track/1",
            "mpris:length": music.get_length() * 1000 if music else 0,
            "mpris:artUrl": "file://" + now_playing_cover,
            "xesam:url": "file://" + queue[enqueue],
            "xesam:title": title,
            "xesam:artist": artist,
            "xesam:album": album,
            "xesam:albumArtist": [],
            "xesam:discNumber": 0,
            "xesam:trackNumber": track_num,
            "xesam:comment": [],
        }
        try_print(f"\x1b[90;1m{metadata}\x1b[0m")
        return metadata

global mpris
class PrizLoop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global mpris
        my_adapter = PrizAdapter()
        mpris = Server('PRIZ_PLAYER', adapter = my_adapter)
        self.mpris = mpris
        mpris.publish()
        mpris.loop()

prizloop = PrizLoop()

timer_end_of_track()
timer_dbus()
