import os
import shutil


def clearAudio():
    target = "audio"
    files = os.listdir(target)

    for item in files:
        if item.endswith(".mp3"):
            os.remove(os.path.join(target, item))