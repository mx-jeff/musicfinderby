from robots.youtubeRobot import downloadAndConvertToMp3VideosFromYoutube
from robots.moveMusicRobot import moveFile
from robots.reponseMusicRobot import returnMusic

import os

def downloadToYoutube(link):
    print('Downloading file...')
    downloadAndConvertToMp3VideosFromYoutube(link)
    print('[DONE] file downloaded')
    print('moving file...')
    music = os.listdir('.')
    print(f'[FILE] {music}')
    moveFile()
    print('[DONE] file moved')
    return returnMusic()
