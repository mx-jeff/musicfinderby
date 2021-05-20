from src.app import Musicfinderby
from src.utils import log
from flask import Flask, send_file, url_for, redirect, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

core = Musicfinderby()

@app.route('/')
def index():
    return "Welcome! Use the '/search/' and type the name of your music or type '/download/' if you have the youtube link "


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
        filename = core.download_and_convert(targetLink)

        # find where the file is it
        return send_file(filename, as_attachment=True, mimetype='audio/mpeg', cache_timeout=-1)
    
    except Exception as error:
        log(error)
        raise

if __name__ == "__main__":
    app.run()

