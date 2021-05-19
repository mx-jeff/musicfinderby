from src.robots.youtube_scrapper_robot import scrapper_youtube_robot
from src.robots.handle_video_youtube import download_and_convert_video_to_mp3
from src.robots.music_file import Music


def validade_input(crawler_name):
    music = ''
    while music == '':
        music = str(input(f'{crawler_name} Nome da música: ').strip())
        if music == '':
            print(f'{crawler_name} Campo vazio, Digíte o nome da música!')

    return music
    

def handleMusic():
    crawler_name = "[Musicfinderby]"
    print(f'{crawler_name} Iniciando crawler...')
    name_music = validade_input(crawler_name)

    link = scrapper_youtube_robot(crawler_name, name_music)
    download_and_convert_video_to_mp3(crawler_name, link)
    
    file_music = Music(crawler_name)
    music = file_music.find()    
    file_music.remove()
