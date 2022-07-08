# ~ import youtube_dl
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from MainWin import YTWin

def main():
    # ~ with youtube_dl.YoutubeDL({}) as ydl:
        # ~ pass
    win = YTWin("YTSearch", 500, 500)
    
    Gtk.main()


if __name__ == "__main__":
    main()
