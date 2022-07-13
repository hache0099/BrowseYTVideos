import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib, Gdk

from scraper import YTScraper
from dataclasses import astuple
from play_video import YTPlayer
from ContextMenu import ContextMenuList
from custom_exceptions import InvalidQueryError, RequestError, ProcessVideoError


class YTWin(Gtk.ApplicationWindow):
	def __init__(self, win_title: str, w, h, yt_link=None):
		super().__init__(title=win_title, default_width=w, default_height=h)
		
		self.last_size_w = w
		
		self.cancellable = Gio.Cancellable()
		self.Scraper = YTScraper(yt_link)
		self.player = YTPlayer()
		self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
		
		self.info_status = Gtk.Statusbar()
		self.status_context = self.info_status.get_context_id("video status")
		
		self.context_menu = ContextMenuList()
		self.context_menu.connect_callback(self.on_menuitem_activate)
		
		self.error_bar = Gtk.InfoBar()
		self.error_bar.set_message_type(Gtk.MessageType.ERROR)
		self.error_bar.connect("response", self.on_infobar_response)
		self.error_label = Gtk.Label()
		self.error_label.set_text("Error: ")
		self.error_label.set_max_width_chars(20)
		err_content = self.error_bar.get_content_area()
		err_content.add(self.error_label)
		self.error_bar.set_show_close_button(True)
		
		self.search_textbox = Gtk.SearchEntry()
		self.search_textbox.connect("activate", self.on_search_entry_event)
		
		self.main_button = Gtk.Button(label="Search")
		self.main_button.connect("clicked", self.on_main_button_pressed)
		
		search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5,
			      border_width=0)
		search_box.pack_start(self.search_textbox, True, True, 0)
		search_box.pack_start(self.main_button, False, True, 0)
		
		# ~ self.cancel_button = Gtk.Button(label="Cancel")
		# ~ self.cancel_button.connect("clicked", self.on_cancel_clicked)
		# ~ self.cancel_button.set_sensitive(False)
		
		result_list = Gtk.ListStore(str,str,str,str)
		self.tree_iters = []
		
		self.results_cells = Gtk.TreeView(model=result_list)
		self.results_cells.set_headers_visible(True)
		self.results_cells.set_headers_clickable(True)
		self.results_cells.connect("button-press-event", self.on_treeview_button_press)
		self.results_cells.connect("row-activated", self.on_treeview_row_activated)
		
		self.scrolled = Gtk.ScrolledWindow()
		self.scrolled.add(self.results_cells)
		
		self.create_listview()
		
		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6,
			      border_width=6)
		
		box.pack_start(self.error_bar, False, True, 0)
		box.pack_start(search_box, False,True,0)
		# ~ box.pack_start(self.search_textbox, False, True, 0)
		# ~ box.pack_start(self.main_button, False, True, 0)
		# ~ box.pack_start(self.cancel_button, False, True, 0)
		box.pack_start(self.scrolled, True, True, 0)
		box.pack_start(self.info_status, False, True, 0)
			
		self.add(box)
		self.add(self.context_menu)
		self.show_all()
		# ~ self.connect("configure-event", self.configure_callback)
		self.connect("destroy", Gtk.main_quit)
		
		# ~ self.info_bar.hide()
		self.error_bar.hide()
		
		self.info_bar_dict = {
			# ~ "info" : (self.info_bar, self.info_label),
			"error": (self.error_bar, self.error_label),
		}
		# ~ self.button_tuple = (
		# ~ self.main_button,
		# ~ self.cancel_button,
		# ~ )
	
	########### FIXME ###########
	def configure_callback(self, source_obj, event, *args):
		print("configure:", event.type)
		new_size = event.width
		
		# ~ if new_size != self.last_size_w:
			# ~ try:
				# ~ self.resize_columns()
			# ~ except Exception as e:
				# ~ print(e.args)
			# ~ finally:
				# ~ self.last_size_w = new_size
	
	
	def create_listview(self):
		renderer = Gtk.CellRendererText()
		
		column_list = (
			Gtk.TreeViewColumn("Título", renderer, text=1),
			Gtk.TreeViewColumn("Duración", renderer, text=2),
			Gtk.TreeViewColumn("Canal", renderer, text=3),
			# ~ Gtk.TreeViewColumn("Link", renderer, text=0),
		)
		# ~ column_list[3].set_visible(False)
		for col in column_list:
			col.set_clickable(True)
			col.set_resizable(True)
			col.set_expand(True)
			col.set_min_width(10)
			self.results_cells.append_column(col)
		
		# ~ self.resize_columns()
	
	
	def on_main_button_pressed(self, button):
		label = button.get_label().lower()
		print("main button label =", label)
		set_sensitive : bool = None
		
		if label == "search":
			self.start_search(self.search_textbox.get_text())
			set_sensitive = False
		elif label == "cancel":
			print("this should be cancelled")
			self.cancellable.cancel()
			set_sensitive = True
	
		self.toggle_treeview(set_sensitive)
	
	# ~ def on_search_button_pressed(self, button):
		# ~ self.toggle_treeview(False)
		# ~ self.start_search(self.search_textbox.get_text())
	
	
	def start_search(self, query):
		print(f"{query=}")
		# ~ self.toggle_treeview()
		task = Gio.Task().new(self, self.cancellable, self.on_task_finished)
		task.set_return_on_cancel(True)
		# ~ print(task)
		
		task.run_in_thread(self._call_scraper)
	
	
	def _call_scraper(self, task, source_obj, callback_data, cancellable):
		# ~ print("_call_scraper:", args)
		try:
			results = self.Scraper(self.search_textbox.get_text())
		except (InvalidQueryError, RequestError) as e:
			#TODO: Decidir si usar un popup o un BarStatus
			print(e.args)
			self.set_info_bar("error", str(e.args))
		else:
			# ~ print("is cancelled =", cancellable.is_cancelled())
			if not self.cancellable.is_cancelled():
				# ~ print(results)
				# ~ print("Si fue cancelado esto no se debería ejecutar")
				self.show_results(results)
				# ~ return results
			self.cancellable.reset()
	
	
	# ~ def on_cancel_clicked(self, button):
		# ~ self.toggle_treeview(True)
		# ~ print("task cancelled")
		# ~ self.cancellable.cancel()
	
	
	def toggle_treeview(self, value: bool):
		# ~ self.main_button.set_sensitive(value)
		# ~ self.cancel_button.set_sensitive(not value)
		self.main_button.set_label("Search" if value else "Cancel")
		self.results_cells.set_sensitive(value)
		
	
	def on_search_entry_event(self, widget):
		self.toggle_treeview(False)
		self.start_search(widget.get_text())
	
	
	def on_task_finished(self, source_obj, task, *args):
		print("task cancelled", task.return_error_if_cancelled())
		# ~ print("task value:", task.propagate_pointer())
		self.toggle_treeview(True)
		# ~ self.cancellable.reset()

	
	def show_results(self, results):
		self.results_cells.set_model(None)
		new_model = Gtk.ListStore(str,str,str,str)
		for res in results:
			new_model.append(list(astuple(res)))
		
		self.results_cells.set_model(new_model)
		# ~ print(f"{self.results_cells.get_allocation().width=}")
		# ~ self.results_cells.columns_autosize()
		
		self.resize_columns()
		
	########### FIXME ###########
	def resize_columns(self):
		tree = self.results_cells
		width = tree.get_allocation().width
		proportions = {
			"título": 70,
			"duración": 10,
			"canal": 20,
		}
		
		for col in tree.get_columns():
			# ~ print(f"{col.get_title()=},{col.get_width()=},{col.get_spacing()=}")
			
			perc : int = proportions[col.get_title().lower()]
			col.set_fixed_width(int(width * (perc / 100)))
	
	
	def on_treeview_row_activated(self, tree, path, column):
		selection = tree.get_selection()
		
		model, treeiter = selection.get_selected()
		
		self.player.set_video(model[treeiter][0])
		
		# ~ self.set_info_bar("info", model[treeiter][1])
		self.show_status_bar("Ahora reproduciendo: " + model[treeiter][1])
		
		self.player.play_video()

		# ~ task = Gio.Task().new(self, None, self.on_task_finished)
		# ~ task.set_name("play_video")
		# ~ task.run_in_thread(self.play_video)
	
	
	def play_video(self, task, source_obj, callback_data, cancellable):
		# ~ print(callback_data)
		self.player.play_video()


	def show_status_bar(self, msg: str = ""):
		self.info_status.push(self.status_context, msg)


	def set_info_bar(self, bar_type : str, msg: str = ""):
		bar, label = self.info_bar_dict[bar_type]
		
		label.set_text(label.get_text() + msg)
		
		if not bar.get_visible():
			bar.show()


	def on_infobar_response(self, infobar, response_id):
		infobar.hide()


	def on_menuitem_activate(self, menu_item):
		label = menu_item.get_label().lower()
		
		if label == "reproducir":
			self.on_treeview_row_activated(self.results_cells, None, None)
		elif label == "descargar":
			####### TODO #######
			pass
		elif label == "copiar link":
			video_id = "https://youtube.com/watch?v=" + self.get_video_id()
			self.clipboard.set_text(video_id,-1)
			self.clipboard.store()
			print(video_id)


	def on_treeview_button_press(self, treeview, event):
		if event.button == 3:
			try:
				path, column, x, y = treeview.get_path_at_pos(int(event.x), int(event.y))
			except TypeError as e:
				pass
			else:
				tree_iter = treeview.get_model().get_iter(path)
				# ~ self.context_menu.set_selected(path, column)
				self.context_menu.popup_at_pointer()


	def get_video_id(self) -> str:
		selection = self.results_cells.get_selection()
		
		model, treeiter = selection.get_selected()
		
		return model[treeiter][0]
