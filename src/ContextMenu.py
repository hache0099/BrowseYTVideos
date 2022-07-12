import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio


# ~ def CustomItem(Gtk.Menuitem):
    # ~ def __init__(self):
        # ~ super().__init__()


class ContextMenuList(Gtk.Menu):
    def __init__(self):
        super().__init__()
        
        self.play_item = Gtk.MenuItem().new_with_label("Reproducir")
        self.append(self.play_item)
        
        self.download_item = Gtk.MenuItem().new_with_label("Descargar")
        self.append(self.download_item)
        
        self.show_all()
