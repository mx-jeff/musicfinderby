from robots.clearRobot import clearAudio
from robots.scrapperRobot import getLinkfromYoutube


def searchUrl(music):
    # clearAudio()
    video = str(music)
    link = getLinkfromYoutube(video)
    return link
