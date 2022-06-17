import sys
sys.path.append("../src/gui")
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk

from MainWin import YTWin

def test_main():
    win = YTWin("prueba",500,500)
    
    Gtk.main()

