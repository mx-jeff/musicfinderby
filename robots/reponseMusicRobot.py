import os


def returnMusic():
    filename = os.listdir(os.path.join('audio', '.'))
    return os.path.join('audio', filename[0])
