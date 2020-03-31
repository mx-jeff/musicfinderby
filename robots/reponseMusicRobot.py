import os


def returnMusic():
    filename = ''
    for file in os.listdir('audio'):
        if file.endswith('.mp3'):
            filename = os.path.join('audio', file)

    return filename
