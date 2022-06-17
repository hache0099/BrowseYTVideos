import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib


class YTWin(Gtk.Window):
    def __init__(self, win_title: str, w, h):
        super().__init__(title=win_title, default_width=w, default_height=h)

        self.show_all()
        self.connect("destroy", Gtk.main_quit)
