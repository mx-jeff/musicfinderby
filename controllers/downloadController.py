from robots.youtubeRobot import downloadAndConvertToMp3VideosFromYoutube
from robots.moveMusicRobot import moveFile
from robots.reponseMusicRobot import returnMusic


def downloadToYoutube(link):
    print('Downloading file...')
    downloadAndConvertToMp3VideosFromYoutube(link)
    print('DONE! file downloaded')
    print('moving file...')
    moveFile()
    print('Done! file moved')
    return returnMusic()
