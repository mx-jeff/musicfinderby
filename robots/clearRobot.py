import os
import shutil


def clearAudio():
    try:
        location = "./audio/"
        shutil.rmtree(os.path.join(location, './'))
        os.mkdir('audio')
    except:
        os.mkdir('audio')