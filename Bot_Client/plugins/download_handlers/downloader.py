import requests
import os
import mimetypes
import math
import sys
import time
from threading import Thread

class Filedownloade(Thread):
    def __init__(self, url, file_name=None, display_progress=True):
        super(Filedownloade, self).__init__()
        self.url = url
        self.display_progress = display_progress
        self.Ifstopped = False
        self.downloading_speed = 0
        self.progress_bar = display_progress
        self.elapsed_time = 0
        self.file_name = file_name
        self.session = requests.Session()
        self.file_size = 0
        self._contents = None
        self.file_Mimetype = None
        self.started_time = time.time()
        self.completed_size = 0
        self.presentage = 0
        self.bar = "[]"
        self.estimated_total_time = 0

    def kill_thread(self):
        self.Ifstopped = True


    def _request(self, url):
        res = self.session.get(url, stream=True, allow_redirects=True)
        self._contents = res
        self.file_Mimetype = res.headers.get('content-type')
        self.file_size = int(res.headers.get('content-length'))
        self.file_name = self.gen_fileDownloadPath(url)

    def run(self):
        return self._worker_download(self.url, self.file_name, self.progress_bar)

    
    def _worker_download(self, url, filename=None, display_progress=True):
        if not self._contents:
            self._request(url)
        if not filename:
            if not os.path.isdir('./downloads/'):
                os.makedirs('./downloads/')
            filename = self.file_name
        else: self.file_name = filename 
        with open(self.file_name, 'wb') as f:
            if self.file_size is None:
                f.write(self._contents.content)
            else:
                for data in self._contents.iter_content(chunk_size=max(int(self.file_size/1000), 1024*1024)):
                    if self.Ifstopped:
                        print("Download Progress Stopped......")
                        os.remove(filename)
                        raise ValueError("Stopping download")
                        
                    self.completed_size += len(data)
                    f.write(data)
                    self.progress_generator()
                    if display_progress:
                        self.display_progress_bar()
            return filename

                

    def gen_fileDownloadPath(self, url):
        filename = url.split("/")[-1].replace('%', ' ').strip()
        if filename == "":
            filename = url.split("/")[-2].replace('%', ' ').strip()
        if '.' in filename:
            if "?" or '=' in filename.split(".")[-1] and self.file_Mimetype != None:
                filename = filename+mimetypes.guess_extension(self.file_Mimetype)
        if '.' not in filename and self.file_Mimetype != None:
            filename = filename+mimetypes.guess_extension(self.file_Mimetype)
        return filename

    def progress_generator(self):
        now = time.time()
        diff = now - self.started_time
        if round(diff % 10.00) == 0 or self.completed_size == self.file_size:
            self.presentage = self.completed_size * 100 / self.file_size
            self.downloading_speed = self.completed_size / diff
            elapsed_time = round(diff) * 1000
            time_to_completion = round((self.file_size - self.completed_size) / self.downloading_speed) * 1000
            self.estimated_total_time = elapsed_time + time_to_completion
            self.elapsed_time = self.TimeFormatter(elapsed_time)
            self.estimated_total_time = self.TimeFormatter(self.estimated_total_time)
            self.bar = "[{0}{1}] \nP: {2}%\n".format(
                ''.join(["█" for i in range(math.floor(self.presentage / 5))]),
                ''.join(["░" for i in range(20 - math.floor(self.presentage / 5))]),
                round(self.presentage, 2))

    def display_progress_bar(self):
        tmp = self.bar + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
            self.humanbytes(self.completed_size),
            self.humanbytes(self.file_size),
            self.humanbytes(self.downloading_speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            self.estimated_total_time if self.estimated_total_time != '' else "0 s"
        )
        sys.stdout.write(tmp)
        sys.stdout.flush()



    def humanbytes(self, size):
        # https://stackoverflow.com/a/49361727/4723940
        # 2**10 = 1024
        if not size:
            return ""
        power = 2**10
        n = 0
        Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
        while size > power:
            size /= power
            n += 1
        return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


    def TimeFormatter(self, milliseconds: int) -> str:
        seconds, milliseconds = divmod(int(milliseconds), 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        tmp = ((str(days) + "d, ") if days else "") + \
            ((str(hours) + "h, ") if hours else "") + \
            ((str(minutes) + "m, ") if minutes else "") + \
            ((str(seconds) + "s, ") if seconds else "") + \
            ((str(milliseconds) + "ms, ") if milliseconds else "")
        return tmp[:-2]


