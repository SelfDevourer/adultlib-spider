import os
import threading

import requests


class DownloadThread(threading.Thread):

    def __init__(self, arg):
        super(DownloadThread, self).__init__()
        self.arg = arg

    def run(self):
        folder = os.path.split(self.arg[1])[0]
        if not os.path.exists(folder):
            os.makedirs(folder)
        if not os.path.exists(self.arg[1]):
            response = requests.get(self.arg[0])
            with open(self.arg[1], 'wb') as f:
                f.write(response.content)
            print('Download %s is done' % self.arg[1])
