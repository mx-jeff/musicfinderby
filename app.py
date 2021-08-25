from time import sleep
from flask_executor import Executor
from flask_cors import CORS
from src.robots.music_file import Music
from src.controller import Musicfinderby
from src.utils import log
from flask import url_for, redirect, request, send_file
from factory import create_app

core = Musicfinderby()
app = create_app()
executor = Executor(app)
CORS(app) # expose_headers=["Content-Disposition"]

#config
app.config['EXECUTOR_MAX_WORKERS'] = 1
app.config['EXECUTOR_TYPE'] = 'thread'
app.config['EXECUTOR_PROPAGATE_EXCEPTIONS'] = True
NAME = "music"


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
        Music().remove()
        executor.submit_stored(NAME, core.download_and_convert, targetLink)
        
        return redirect(url_for('getMusic'))
    
    except Exception as error:
        log(error)
        raise


@app.route('/music')
def getMusic():
    '''
    Return music file if exists
    '''
    if executor.futures.done(NAME):
        try:
            future = executor.futures.pop(NAME)
            music = core.find_music()
            print('Future: ', future.result())
            return send_file(music, as_attachment=True, mimetype='audio/mpeg', cache_timeout=-1)

        except Exception as error:
            print('Error: ', error)
            log(error)
            return "Música não disponível ou algum erro aconteceu!"


    else:
        sleep(10)
        return redirect(url_for('getMusic'))

if __name__ == "__main__":
    app.run()
