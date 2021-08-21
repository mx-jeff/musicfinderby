import threading
from flask import send_file
from flask.helpers import url_for
from werkzeug.utils import redirect
from src.controller import Musicfinderby
from factory import create_app
import concurrent.futures 


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