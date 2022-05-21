import requests
import os
import mimetypes
import asyncio
import time
from threading import Thread
from Bot_Client.plugins.constents.progress_for_pyrogram import progress_for_pyrogram
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
class Filedownloade(Thread):
    def __init__(self, url, message=None, file_name=None, func=None, prms=None):
        super(Filedownloade, self).__init__()
        self.func = func
        self.params = prms
        

        self.url = url
        self.extension = None
        self.message = message
        self.file_name = file_name
        self.session = requests.Session()
        self.file_size = 0
        self.file_Mimetype = None
        self.started_time = 0
        self.completed_size = 0
        self.presentage = 0

        self.estimated_total_time = 0

    def kill_thread(self):
        raise ValueError("Download thread is terminating")

    def run(self):
        path = asyncio.run(self._worker_download(self.url, self.file_name))
        if not self.func:
            return path
        asyncio.run(self._before_worker(path))
    
    async def _before_worker(self, path):
        self.params["path"] = path
        await self.func(**self.params)



    
    async def _worker_download(self, url, filename=None):
        res = self.session.get(url, stream=True, allow_redirects=True)
        self.started_time = time.time()
        self.file_Mimetype = res.headers.get('content-type')
        self.file_size = int(res.headers.get('content-length'))
        self.extension = mimetypes.guess_extension(self.file_Mimetype)
        if not self.file_name:self.file_name = self.gen_fileDownloadPath(url)
        


        
        if not os.path.isdir(os.path.dirname(self.file_name)):
            os.makedirs(os.path.dirname(self.file_name))
        if not filename:
            filename = self.file_name
        
        else: self.file_name = filename 
        with open(self.file_name, 'wb') as f:
            if self.file_size is None:
                f.write(res.content)
            else:
                for data in res.iter_content(chunk_size=max(int(self.file_size/1000), 1024*1024)):
                    self.completed_size += len(data)
                    f.write(data)
                    await progress_for_pyrogram(self.completed_size, self.file_size, f"{self.file_name} is downloading", self.message, self.started_time, InlineKeyboardMarkup([[InlineKeyboardButton("Stop Task", callback_data=f"stop_{self.name}")]]))
          
            return filename

                

    def gen_fileDownloadPath(self, url):
        if self.file_name: return self.file_name
        filename = url.split("/")[-1].replace('%', ' ').strip()
        if filename == "":
            filename = url.split("/")[-2].replace('%', ' ').strip()
        if '.' in filename:
            if "?" or '=' in filename.split(".")[-1] and self.file_Mimetype != None:
                filename = filename+self.extension
        if '.' not in filename and self.file_Mimetype != None:
            filename = filename+self.extension
        return os.path.join(f"downloads/{self.message.chat.id}/{filename}")

    
    



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


