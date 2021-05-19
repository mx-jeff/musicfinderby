from __future__ import unicode_literals
import youtube_dl


def download_and_convert_video_to_mp3(crawler_name, url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(str(f'{crawler_name} done!').upper())

    except Exception as error:
        print(f'{crawler_name} Algo deu errado :(')
        print(f'{crawler_name} Erro: {error}')