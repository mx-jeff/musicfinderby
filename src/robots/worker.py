import threading
from flask import send_file
from src.controller import Musicfinderby
from factory import create_app
import concurrent.futures


class Worker:
    def __init__(self, filename):
        self.filename = filename
        self.core = Musicfinderby()
        self.app = create_app()

        # thread = threading.Thread(target=self.run ,args=())
        # thread.daemon = True
        # thread.start()
    
    def run(self):
        with concurrent.futures.ThreadPoolExecutor() as executor: 
            future = executor.submit(self.downloadMusic)
            return_value = future.result()
            return return_value

    def downloadMusic(self):
        with self.app.test_request_context():
            print(f'Spawing a thread for: {self.filename}')
            filename = self.core.download_and_convert(self.filename)
            
            # find where the file is it
            # return send_file(filename, as_attachment=True, mimetype='audio/mpeg', cache_timeout=-1)
            return filename