import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gio, Glib

class YTWin(Gtk.Window):
	def __init__(self, win_title: str):
		super().__init__(win_title)
		

# ~ def main():
    # ~ pass


# ~ if __name__ == "__main__":
    # ~ main()
