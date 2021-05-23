from src.controller import Musicfinderby
from src.robots.worker import Worker
from src.utils import log
from app import create_server
from flask import url_for, redirect, request

web = create_server()
core = Musicfinderby()

@web.route('/')
def index():
    return "Welcome! Use the '/search/' and type the name of your music or type '/download/' if you have the youtube link "


@web.route('/search/<string:music>')
def searchMusic(music):
    '''
    => search music's link on youtube and call "loadMusic" to download then
    Ex: host/s/music-name

    :param music: <string> Select music of wish
    :return: target video url
    '''
    try:
        url = core.search_url(music)
        print('Url video: ', url)
        return redirect(url_for("loadMusic", url=url))
    
    except Exception as error:
        log(error)
        raise


@web.route('/download/')
def loadMusic():
    '''
    Download music from youtube and convert to mp3
    Ex: host/d?url="video-from-youtube"

    params: <string:music>: specifies music for download
    return: mp3 file

    '''
    try:
        targetLink = request.args.get('url')
        # filename = core.download_and_convert(targetLink)
        Worker(targetLink)
        # send_file(filename, as_attachment=True, mimetype='audio/mpeg', cache_timeout=-1)
        # find where the file is it
        return "Baixando arquivo, aguarde.."
    
    except Exception as error:
        log(error)
        raise



