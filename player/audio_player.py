import vlc
import threading

class AudioPlayer:
    def __init__(self):
        self.player = None

    def play(self, url):
        threading.Thread(target=self._play_thread, args=(url,), daemon=True).start()

    def _play_thread(self, url):
        if self.player:
            self.player.stop()
        self.player = vlc.MediaPlayer(url)
        self.player.play()

    def stop(self):
        if self.player:
            self.player.stop()
