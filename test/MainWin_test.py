import sys
sys.path.append("../src/gui")
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk

from MainWin import YTWin

def main():
    win = YTWin("prueba")
    
    Gtk.main()


if __name__ == "__main__":
    main()
