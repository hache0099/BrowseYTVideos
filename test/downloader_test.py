import sys

sys.path.append("../src")

import yt_downloader as ytdl


# ~ dl = YTDownloader()

def test_results():
    print(ytdl.get_video_opts("https://youtube.com/watch?v=Ff7UhZFt_O8"))


def test_download():
    ytdl.download_video("https://youtube.com/watch?v=Ff7UhZFt_O8", video_format="best")
