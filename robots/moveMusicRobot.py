import os


def moveFile():
    actualDir = os.listdir('.')
    for directory in actualDir:
        if directory.endswith('.mp3'):
            print(f'moving {directory}...')
            os.rename(directory, f"audio/{directory}")
            
            print(directory + "Selected")
            print('Done!')
