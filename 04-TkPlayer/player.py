#coding:utf8
import pyglet #AVbin10 is needed
from threading import Thread
import time

FWDREWNDTIME = 20

class Player():
    parent = None
    vol = 0.0
    def play_media(self):
        try:
            self.myplayer = pyglet.media.Player()             
            self.source = pyglet.media.load(self.parent.currentTrack)
            self.myplayer.queue(self.source)
            self.myplayer.play()
            pyglet.app.run()
        except:
            pass

    def start_play_thread(self):
        player_thread = Thread(target = self.play_media)
        player_thread.start()

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