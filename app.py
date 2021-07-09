from flask import Flask, Blueprint
from flask.helpers import flash
from flask_cors import CORS
from src.controller import Musicfinderby
from src.robots.worker import Worker
from src.utils import log
from flask import url_for, redirect, request, send_file
from factory import create_app

core = Musicfinderby()
app = create_app()


@app.route('/')
def index():
    return "Welcome! Use the '/search/' and type the name of your music or type '/download/' if you have the youtube link and '/music' to return music "


@app.route('/search/<string:music>')
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


@app.route('/download/')
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
        Worker(targetLink).run()
        # print('> status 2: ', result)
        # send_file(filename, as_attachment=True, mimetype='audio/mpeg', cache_timeout=-1)
        # find where the file is it
        return "Baixando arquivo, aguarde alguns instantes.."
        # return redirect(url_for('getMusic'))
    
    except Exception as error:
        log(error)
        raise


@app.route('/music')
def getMusic():
    '''
    Return music file if exists
    '''
    try:
        music = core.find_music()
        return send_file(music, as_attachment=True, mimetype='audio/mpeg', cache_timeout=-1)

    except Exception as error:
        log(error)
        return "Música não disponível ou algum erro aconteceu!"

if __name__ == "__main__":
    app.run()
