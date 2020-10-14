from robots.clearRobot import clearAudio
from robots.scrapperRobot import getLinkfromYoutube


def searchUrl(music):
    clearAudio()
    video = str(music)
    print("Getting link's video")
    link = getLinkfromYoutube(video)
    print('DONE! moving to download...')
    return link
