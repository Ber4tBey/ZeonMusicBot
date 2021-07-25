from os import path

from youtube_dl import YoutubeDL

from ..config import DURATION_LIMIT
from ..helpers.errors import DurationLimitError

ytdl = YoutubeDL(
    {
        'format': 'bestaudio/best',
        'geo-bypass': True,
        'nocheckcertificate': True,
        'outtmpl': 'downloads/%(id)s.%(ext)s',
    },
)


def download(url: str) -> str:
    info = ytdl.extract_info(url, False)
    duration = round(info['duration'] / 60)
    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f'Video süresi {DURATION_LIMIT} dakikadan uzun. Kabul edilemez , '
            f'Max limit = {duration} dakika',
        )
    ytdl.download([url])
    return path.join('downloads', f"{info['id']}.{info['ext']}")
