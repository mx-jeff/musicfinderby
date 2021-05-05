from robots.youtubeRobot import downloadAndConvertToMp3VideosFromYoutube
from robots.moveMusicRobot import moveFile
from robots.reponseMusicRobot import returnMusic

import os

dev = True


def downloadToYoutube(link):
    print('Downloading file...')
    downloadAndConvertToMp3VideosFromYoutube(link)
    print('[DONE] file downloaded')

    if dev:
        print('moving file...')
        music = os.listdir('./audio')
        moveFile()
        print('[DONE] file moved')

    return returnMusic()
