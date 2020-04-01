import os


def moveFile():
    actualDir = os.listdir('.')
    for directory in actualDir:
        if directory.endswith('.mp3'):
            print(f'moving {directory}...')
            os.system(f'mv "{directory}" audio')
            
            print(directory + "Selected")
            print('Done!')
