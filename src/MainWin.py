import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib, Gdk


from scraper import YTScraper, InvalidQueryError


class YTWin(Gtk.Window):
	def __init__(self, win_title: str, w, h):
		super().__init__(title=win_title, default_width=w, default_height=h)
		
		self.cancellable = Gio.Cancellable()
		self.Scraper = YTScraper()
		
		self.search_textbox = Gtk.SearchEntry()
		self.search_textbox.connect("activate", self.on_search_entry_event)
		
		self.search_button = Gtk.Button(label="Search")
		self.search_button.connect("clicked", self.on_search_button_pressed)
		
		self.cancel_button = Gtk.Button(label="Cancel")
		self.cancel_button.connect("clicked", self.on_cancel_clicked)
		self.cancel_button.set_sensitive(False)
		
		self.results_cells = Gtk.TreeView()
		
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6,
			      border_width=6)
		
		box.pack_start(self.search_textbox, False, True, 0)
		box.pack_start(self.search_button, False, True, 0)
		box.pack_start(self.cancel_button, False, True, 0)
		box.pack_start(self.results_cells, True, True, 0)
			
		self.add(box)
		self.show_all()
		self.connect("destroy", Gtk.main_quit)
		
		self.button_tuple = (
		self.search_button,
		self.cancel_button,
		)
	
	
	def on_search_button_pressed(self, button):
		self.toggle_buttons(False)
		self.start_search(self.search_textbox.get_text())
	
	
	def start_search(self, query):
		print(f"{query=}")
		# ~ self.toggle_buttons()
		task = Gio.Task().new(self, self.cancellable, self.on_task_finished)
		task.set_return_on_cancel(True)
		# ~ print(task)
		
		task.run_in_thread(self._call_scraper)
	
	
	def _call_scraper(self, task, source_obj, callback_data, cancellable):
		# ~ print("_call_scraper:", args)
		results = self.Scraper(self.search_textbox.get_text())
		if not task.return_error_if_cancelled():
			print(results)
			return results
	
	
	def on_cancel_clicked(self, button):
		self.toggle_buttons(True)
		print("task cancelled")
		self.cancellable.cancel()
	
	
	def toggle_buttons(self, value: bool):
		self.search_button.set_sensitive(value)
		self.cancel_button.set_sensitive(not value)
		
	
	def on_search_entry_event(self, widget):
		self.toggle_buttons(False)
		self.start_search(widget.get_text())
	
	
	def on_task_finished(self, source_obj, task, *args):
		print("task cancelled", task.return_error_if_cancelled())
		# ~ print("task value:", task.propagate_pointer())
		self.toggle_buttons(True)
		self.cancellable.reset()
