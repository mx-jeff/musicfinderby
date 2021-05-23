import threading
from flask import send_file
from src.controller import Musicfinderby
from factory import create_app


class Worker:
    def __init__(self, filename):
        self.filename = filename
        self.core = Musicfinderby()
        self.app = create_app()

        thread = threading.Thread(target=self.run ,args=())
        thread.daemon = True
        thread.start()
    
    def run(self):
        print(f'Spawing a thread for: {self.filename}')
        filename = self.core.download_and_convert(self.filename)
        # find where the file is it

        with self.app.app_context():
            return send_file(filename, as_attachment=True, mimetype='audio/mpeg', cache_timeout=-1)
