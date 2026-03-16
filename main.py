# ffmpeg/ffprobe для pydub и yt-dlp в контейнере (Railway)
import os
import warnings

os.environ["PATH"] = "/usr/bin:" + os.environ.get("PATH", "")
# Подавить предупреждение pydub и задать явные пути к ffmpeg/ffprobe
warnings.filterwarnings("ignore", message=".*ffmpeg or avconv.*", module="pydub.utils")
try:
    from pydub import AudioSegment
    AudioSegment.converter = "/usr/bin/ffmpeg"
    AudioSegment.ffprobe = "/usr/bin/ffprobe"
except Exception:
    pass

from run import Bot
from utils import asyncio


async def main():
    await Bot.initialize()
    await Bot.run()


asyncio.run(main())
