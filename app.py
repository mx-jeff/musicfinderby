import os
from flask_executor import Executor
from flask_cors import CORS
from src.robots.music_file import Music
from src.controller import Musicfinderby
from src.utils import log
from flask import request, send_file, jsonify
from factory import create_app

core = Musicfinderby()
app = create_app()
executor = Executor(app)
CORS(app, expose_headers=["Content-Disposition"])

# config
app.config['EXECUTOR_MAX_WORKERS'] = 1
app.config['EXECUTOR_TYPE'] = 'thread'
app.config['EXECUTOR_PROPAGATE_EXCEPTIONS'] = True
NAME = "music"


@app.route('/api')
def index():
    return "Welcome! Use '/search/<name>' to find a music, '/download/?url=<youtube link>' to start the download and '/music' to get the mp3 file."


@app.route('/search/<string:music>')
def searchMusic(music):
    '''
    Search the music's link on youtube
    Ex: host/search/music-name

    :return: json with the target video url
    '''
    try:
        url = core.search_url(music)
        print('Url video: ', url, flush=True)
        return jsonify(url=url)
    except Exception as error:
        log(error)
        return jsonify(error=str(error)), 500


@app.route('/download/')
def loadMusic():
    '''
    Start the download/conversion to mp3 in background
    Ex: host/download/?url=<video-from-youtube>

    :return: 202 when the download has started
    '''
    target_link = request.args.get('url')
    if not target_link:
        return jsonify(error='url obrigatória'), 400

    print('Download solicitado:', target_link, flush=True)
    try:
        Music().remove()
        executor.submit_stored(NAME, core.download_and_convert, target_link)
        return jsonify(status='started'), 202
    except Exception as error:
        log(error)
        return jsonify(error=str(error)), 500


@app.route('/music')
def getMusic():
    '''
    202 while the download is running, the mp3 file when it is done
    '''
    try:
        if not executor.futures.done(NAME):
            return jsonify(status='running'), 202
    except KeyError:
        return jsonify(error='nenhum download em andamento'), 404

    try:
        future = executor.futures.pop(NAME)
        filename = future.result()
        music = core.find_music()
        if not filename or not music:
            return jsonify(error='música não disponível'), 404

        music_path = os.path.abspath(music)        # resolve a partir do cwd (/app/downloads)
        download_name = os.path.basename(music_path)  # tira o "./" do nome

        print('Future: ', download_name, flush=True)
        return send_file(
            music_path,
            as_attachment=True,
            download_name=download_name,
            mimetype='audio/mpeg',
            max_age=0,
        )
    except Exception as error:
        print('Error: ', error, flush=True)
        log(error)
        return jsonify(error=str(error)), 500


if __name__ == "__main__":
    app.run()