import threading
from src.controller import Musicfinderby
from factory import create_app


class Worker:
    def __init__(self):
        self.core = Musicfinderby()
        self.app = create_app()
        self.thread = threading.Thread()
        
    def donwload(self, filename):
        with self.app.test_request_context():
            print(f'Spawing a thread for: {filename}')
            self.core.download_and_convert(filename)

    def run(self, filename):
        self.thread = threading.Thread(target=self.donwload, args=[filename])
        self.thread.daemon = True
        self.thread.start()

    def done(self):
        return self.thread.is_alive()