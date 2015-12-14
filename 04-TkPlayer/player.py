#coding:utf8
import pyglet #AVbin10 is needed
from threading import Thread

class Player():
    parent = None
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

if __name__ == '__main__':
    print 'a pyglet player class implementation'