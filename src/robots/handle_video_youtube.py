from __future__ import unicode_literals
import youtube_dl


def download_and_convert_video_to_mp3(crawler_name, url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.cache.remove()
            ydl.download([url])
        except youtube_dl.DownloadError as error:
            print('[ERRO]', error)
            return

    print(str(f'{crawler_name} done!').upper())