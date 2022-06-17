import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib, Gdk



class YTWin(Gtk.Window):
	def __init__(self, win_title: str, w, h):
		super().__init__(title=win_title, default_width=w, default_height=h)
		
		self.cancellable = Gio.Cancellable()
		
		self.search_textbox = Gtk.SearchEntry()
		self.search_textbox.connect("key_press_event", self.on_search_entry_event)
		
		self.search_button = Gtk.Button(label="Search")
		self.search_button.connect("clicked", self.on_search_button_pressed)
		
		self.cancel_button = Gtk.Button(label="Cancel")
		self.cancel_button.connect("clicked", self.on_cancel_clicked)
		self.cancel_button.set_sensitive(False)
		
		self.results_cells = Gtk.CellView()
		
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6,
			      border_width=12)
		
		box.pack_start(self.search_textbox, False, True, 0)
		box.pack_start(self.search_button, False, True, 0)
		box.pack_start(self.cancel_button, False, True, 0)
		box.pack_start(self.results_cells, False, True, 0)
			
		self.add(box)
		self.show_all()
		self.connect("destroy", Gtk.main_quit)
		
		self.button_list = [
		self.search_button,
		self.cancel_button,
		]
	
	
	def on_search_button_pressed(self, button):
		pass
	
	
	def start_search(self, *args):
		print("start_search=", args)
	
	
	def on_cancel_clicked(self):
		pass
	
	
	def toggle_buttons(self, button):
		pass
	
	
	def on_search_entry_event(self, w, event):
		if Gdk.keyval_name(event.keyval).lower() == "return":
			start_search()
