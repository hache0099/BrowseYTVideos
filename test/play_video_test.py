import sys

sys.path.append("../src")

from play_video import YTPlayer

player = YTPlayer()


def test_video():
    player.set_video("-1YmyJW0O6o")
