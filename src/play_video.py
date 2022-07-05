import shutil
import subprocess
from custom_exceptions import ProcessVideoError

class YTPlayer:
    def __init__(self):
        self.video_to_play = ""
    
    
    def set_video(self, video_id: str):
        self.video_to_play = "https://youtube.com/watch?v=" + video_id
    
    
    def play_video(self):
        process = subprocess.Popen([shutil.which("mpv"), self.video_to_play], stdin=PIPE, stderr=PIPE)
        
        return process
        # ~ print("return_code=", process.returncode)
        # ~ print("stderr=", process.stderr)
        # ~ try:
            # ~ process.check_returncode()
        # ~ except subprocess.CalledProcessError as e:
            # ~ raise ProcessVideoError(*e.args) from e
