from controllers.downloadController import downloadToYoutube
from flask import Flask, send_file, url_for, redirect, request
from controllers.searchController import searchUrl
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


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
    url = searchUrl(music)
    print(url)
    return redirect(url_for("loadMusic", url=url))


@app.route('/download/')
def loadMusic():
    '''
    Download music from youtube and convert to mp3
    Ex: host/d?url="video-from-youtube"

    params: <string:music>: specifies music for download
    return: mp3 file

    '''
    targetLink = request.args.get('url')
    filename = downloadToYoutube(targetLink)

    # find where the file is it
    try:
        return send_file(filename, as_attachment=True, mimetype='audio/mpeg', cache_timeout=-1)

    except Exception as error:
        print(error)
        return f"[ERRO] Aquivo não baixado! Tente novamente"


if __name__ == "__main__":
    app.run()
