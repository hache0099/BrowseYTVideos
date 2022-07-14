import youtube_dl as ytdl


def get_video_opts(video_id: str) -> dict:
    if not video_id.startswith("https://"):
        video_id = "https://youtube.com/watch?v=" + video_id
    
    with ytdl.YoutubeDL() as ytl:
        results = ytl.extract_info(video_id, download=False)
    
    return results


def download_video(video_id, video_format):
    ytdl_opts = {"format": video_format}
    
    with ytdl.YoutubeDL(ytdl_opts) as ytl:
        ytl.download([video_id])
