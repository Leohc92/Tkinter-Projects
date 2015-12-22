#coding:utf8
import pyglet #AVbin10 is needed
from threading import Thread
import time

FWDREWNDTIME = 20

class Player():
    parent = None
    paused = False
    stopped = False
    current_time = 0
    vol = 0.0
    def play_media(self):
        try:
            self.myplayer = pyglet.media.Player()    
            self.myplayer.push_handlers(on_eos=self.what_next)         
            self.source = pyglet.media.load(self.parent.currentTrack)
            self.myplayer.queue(self.source)
            self.myplayer.play()
            pyglet.app.run()
        except:
            pass

    def what_next(self):
        if self.stopped:
            self.stopped = False
            return None
        if self.parent.loopv.get() == 1:
            return None
        if self.parent.loopv.get() == 2:
            self.parent.launch_play()
        if self.parent.loopv.get() == 3:
            self.fetch_next_track()

    def fetch_next_track(self):
        try:
            next_trackindx = self.parent.alltracks.index(self.parent.currentTrack) + 1
            self.parent.currentTrack = self.parent.alltracks[next_trackindx]
            self.parent.launch_play()
        except:
            print 'end of list'

    def current_time(self):
        try:
            current_time = self.myplayer.time
        except:
            current_time = 0
        return current_time

    def song_len(self):
        try:
            self.song_length = self.source.duration
        except:
            self.song_length = 0
        return self.song_length

    def start_play_thread(self):
        player_thread = Thread(target = self.play_media)
        player_thread.start()
        time.sleep(1)
        self.song_len()

    def pause(self):
        try:
            self.myplayer.pause()
            self.paused = True
        except:
            pass

    def fast_fwd(self):
        try:
            current_time = self.myplayer.time
            self.myplayer.seek(current_time+FWDREWNDTIME)
        except:
            pass

    def rewind(self):
        try:
            current_time = self.myplayer.time
            self.myplayer.seek(current_time-FWDREWNDTIME)
        except:
            pass

    def set_vol(self, vol):
        try:
            self.myplayer.volumne = vol
        except:
            pass

    def mute(self):
        try:
            self.myplayer.volumne = 0
            self.parent.volscale.set(0.0)
        except:
            pass

    def unmute(self):
        self.set_vol(self.vol)
        self.parent.volscale.set(0.3)


if __name__ == '__main__':
    print 'a pyglet player class implementation'