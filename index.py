from controllers.mainController import downloadToYoutube
from flask import Flask, send_file

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome!"


@app.route('/d/<string:music>')
def loadMusic(music):
    '''
    Download music from youtube
    Ex: host/d/music-name

    params: <string:music>: specifies music for download
    return: mp3 file

    '''
    filename = downloadToYoutube(music)
    
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run()