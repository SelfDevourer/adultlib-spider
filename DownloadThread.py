import os
import threading

import requests


class DownloadThread(threading.Thread):

    def __init__(self, arg):
        super(DownloadThread, self).__init__()
        self.arg = arg

    def run(self):
        file_name = self.arg[1]
        folder = 'E:/workspace/adultlib/src/main/resources/static/covers/'
        file = folder + file_name + '.jpg'
        if not os.path.exists(folder):
            os.makedirs(folder)
        if not os.path.exists(file):
            url = self.arg[0]
            response = requests.get(url)
            with open(file, 'wb') as f:
                f.write(response.content)
            print('Download %s is done' % file_name)
