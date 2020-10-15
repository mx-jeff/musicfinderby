from controllers.downloadController import downloadToYoutube
from flask import Flask, send_file, url_for, redirect, request
from controllers.searchController import searchUrl
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Welcome!"


@app.route('/s/<string:music>')
def searchMusic(music):
    '''
    => search music's link on youtube and call "loadMusic" to download then
    Ex: host/s/music-name

    :param music: <string> Select music of wish
    :return: target video url
    '''
    url = searchUrl(music)
    return redirect(url_for("loadMusic", url=url))


@app.route('/d/')
def loadMusic():
    '''
    Download music from youtube and convert to mp3
    Ex: host/d?url="video-from-youtube"

    params: <string:music>: specifies music for download
    return: mp3 file

    '''
    targetLink = request.args.get('url')
    filename = downloadToYoutube(targetLink)

    if filename == '':
        return f"[ERRO] Aquivo não baixado! Tente novamente" 

    print('DONE!, Sending your file...')

    # add app in path do get file
    
    return send_file(filename, as_attachment=True, mimetype='audio/mpeg', cache_timeout=-1)

if __name__ == "__main__":
    app.run()
