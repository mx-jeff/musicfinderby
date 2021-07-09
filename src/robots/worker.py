import threading
from flask import send_file
from flask.helpers import url_for
from werkzeug.utils import redirect
from src.controller import Musicfinderby
from factory import create_app
import concurrent.futures 


class Worker:
    def __init__(self, filename):
        self.filename = filename
        self.core = Musicfinderby()
        self.app = create_app()
        
    def donwload(self):
        with self.app.test_request_context():
            print(f'Spawing a thread for: {self.filename}')
            self.core.download_and_convert(self.filename)
            
            # find where the file is it
            # return send_file(filename, as_attachment=True, mimetype='audio/mpeg', cache_timeout=-1)
            return 'Arquivo baixado'

    def run(self):
        thread = threading.Thread(target=self.donwload ,args=())
        thread.daemon = True
        thread.start()

        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     future = executor.submit(self.donwload)
        #     return_value = future.result()
        #     print('> Status 1: ', return_value)
        #     return return_value