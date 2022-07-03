import sys
sys.path.append("../src")
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk

from MainWin import YTWin

def test_main():
    win = YTWin("prueba", 500,500)
    
    Gtk.main()

def test_diff_link():
    win = YTWin("prueba", 500,500, yt_link="https://inv.riverside.rocks/api/v1/search")
    
    Gtk.main()
# ~ test_main()
