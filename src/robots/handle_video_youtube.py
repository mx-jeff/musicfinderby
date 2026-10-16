from __future__ import unicode_literals
import sys
import yt_dlp as youtube_dl
from time import sleep


class YDLLogger:
    def debug(self, msg):
        if not msg.startswith('[debug]'):
            print(f'[yt-dlp] {msg}', flush=True)

    def info(self, msg):
        print(f'[yt-dlp] {msg}', flush=True)

    def warning(self, msg):
        print(f'[yt-dlp][WARNING] {msg}', flush=True)

    def error(self, msg):
        print(f'[yt-dlp][ERROR] {msg}', file=sys.stderr, flush=True)


def download_and_convert_video_to_mp3(crawler_name, url):
    last = {'pct': -10}

    def progress_hook(d):
        if d['status'] == 'downloading':
            pct = int(float(d.get('_percent_str', '0').strip().rstrip('%') or 0))
            if pct - last['pct'] >= 10:
                last['pct'] = pct
                print(f'[yt-dlp] {pct}% {d.get("_speed_str", "").strip()}', flush=True)
        elif d['status'] == 'finished':
            print(f'{crawler_name} Download concluído, convertendo para mp3...', flush=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'logger': YDLLogger(),
        'progress_hooks': [progress_hook],
        'retries': 5,
        'fragment_retries': 5,
        'extractor_retries': 3,
        'sleep_interval_requests': 1,
    }

    print(f'{crawler_name} Baixando: {url}', flush=True)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        for tentativa in range(3):
            try:
                ydl.download([url])
                break
            except youtube_dl.DownloadError as error:
                print(f'{crawler_name} [ERRO] tentativa {tentativa + 1}: {error}', flush=True)
                if tentativa == 2:
                    return
                sleep(5)

    print(f'{crawler_name} DONE!', flush=True)