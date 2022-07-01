import subprocess


class YTPlayer:
    def __init__(self):
        self.video_to_play = ""
    
    
    def set_video(self, video_id: str):
        self.video_to_play = "https://youtube.com/watch?v=" + video_id
    
    
    def play_video(self):
        stdout = subprocess.run(["mpv", self.video_to_play], capture_output=True)
