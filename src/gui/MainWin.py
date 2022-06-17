import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib



class YTWin(Gtk.Window):
	def __init__(self, win_title: str, w, h):
		super().__init__(title=win_title, default_width=w, default_height=h)
		
		self.cancellable = Gio.Cancellable()
		
		self.search = Gtk.SearchEntry()
		self.results = Gtk.CellView()
		
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6,
			      border_width=12)
		
		box.pack_start(self.search, False, True, 0)
		box.pack_start(self.results, False, True, 0)
			
		self.add(box)
		self.show_all()
		self.connect("destroy", Gtk.main_quit)
