from robots.youtubeRobot import downloadAndConvertToMp3VideosFromYoutube
from robots.moveMusicRobot import moveFile
from robots.reponseMusicRobot import returnMusic


def downloadToYoutube(link):
    downloadAndConvertToMp3VideosFromYoutube(link)
    moveFile()
    return returnMusic()
