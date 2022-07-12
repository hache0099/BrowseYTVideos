import sys
sys.path.append("../src")

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk
from ContextMenu import ContextMenuList


class MyWin(Gtk.Window):
    def __init__(self):
        super().__init__(title="Test", default_width=500,default_height=500)
        
        self.menu = ContextMenuList()
        
        self.connect("button-press-event", self.on_mouse_clicked)
        
        self.add(self.menu)
        
        self.show_all()
        self.connect("destroy", Gtk.main_quit)


    def on_mouse_clicked(self, widget, event):
        if event.button == 3:
            self.menu.popup_at_pointer()


def test_win():
    win = MyWin()
    
    Gtk.main()
