from robots.youtubeRobot import downloadAndConvertToMp3VideosFromYoutube
from robots.moveMusicRobot import moveFile
from robots.scrapperRobot import getLinkfromYoutube
from robots.clearRobot import clearAudio
from robots.reponseMusicRobot import returnMusic


def downloadToYoutube(music):
    #clearAudio()
    video = str(music)
    link = getLinkfromYoutube(video)
    downloadAndConvertToMp3VideosFromYoutube(link)
    moveFile()
    return returnMusic()
