import sys

sys.path.append("../src")

import pytest
from play_video import YTPlayer
from custom_exceptions import ProcessVideoError

player = YTPlayer()


def test_video():
    player.set_video("-1YmyJW0O6o") # Adivina la canción
    player.play_video()


def test_invalid_id():
    player.set_video("no")
    with pytest.raises(ProcessVideoError):
        player.play_video()
