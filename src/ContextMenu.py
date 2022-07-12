import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio


# ~ def CustomItem(Gtk.Menuitem):
    # ~ def __init__(self):
        # ~ super().__init__()


class ContextMenuList(Gtk.Menu):
    def __init__(self):
        super().__init__()
        
        # ~ self.play_item = Gtk.MenuItem().new_with_label("Reproducir")
        # ~ self.append(self.play_item)
        
        # ~ self.download_item = Gtk.MenuItem().new_with_label("Descargar")
        # ~ self.append(self.download_item)
        
        self.item_dir = self._generate_items((
        "Reproducir",
        "Descargar",
        "Copiar Link",
        ))
        
        self.show_all()
    

    def _generate_items(self, items: tuple[str]) -> dict:
        item_dir = {}
        for item_label in items:
            menuitem = Gtk.MenuItem().new_with_label(item_label)
            self.append(menuitem)
            
            item_dir[item_label] = menuitem
        
        return item_dir
    
    
    def get_item_dir(self) -> dict:
        return self.item_dir
