from robots.youtubeRobot import downloadAndConvertToMp3VideosFromYoutube
from robots.moveMusicRobot import moveFile
from robots.reponseMusicRobot import returnMusic

import os

dev = False


def downloadToYoutube(link):
    print('Downloading file...')
    downloadAndConvertToMp3VideosFromYoutube(link)
    print('[DONE] file downloaded')

    if dev:
        print('moving file...')
        music = os.listdir('./audio')
        print(f'[FILE] {music}')
        moveFile()
        print('[DONE] file moved')

    return returnMusic()
