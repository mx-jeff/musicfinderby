from src.robots.youtube_scrapper_robot import scrapper_youtube_robot
from src.robots.handle_video_youtube import download_and_convert_video_to_mp3


def validade_input(crawler_name):
    music = ''
    while music == '':
        music = str(input(f'{crawler_name} Nome da música: ').strip())
        if music == '':
            print(f'{crawler_name} Campo vazio, Digíte o nome da música!')

    return music
    

class Musicfinderby:
    crawler_name = "[Musicfinderby]"
    
    def __init__(self) -> None:
        print(f'{self.crawler_name} Iniciando crawler...')

    def search_url(self, name_music):
        return scrapper_youtube_robot(self.crawler_name, name_music)
    
    def download_and_convert(self, link):
        download_and_convert_video_to_mp3(self.crawler_name, link)
        return self.file_music.find()    

    def find_music(self):
        return self.file_music.find()
