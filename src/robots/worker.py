import threading
from flask import send_file
from src.controller import Musicfinderby
from server import web

class Worker:
    def __init__(self, filename):
        self.filename = filename
        self.core = Musicfinderby()

        thread = threading.Thread(target=self.run ,args=())
        thread.daemon = True
        thread.start()
    
    def run(self):
        print(f'Spawing a thread for: {self.filename}')
        filename = self.core.download_and_convert(self.filename)
        # find where the file is it

        # with server.app_context():
        return send_file(filename, as_attachment=True, mimetype='audio/mpeg', cache_timeout=-1)
