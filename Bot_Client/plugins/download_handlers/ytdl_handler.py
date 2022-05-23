import os, time, asyncio
from datetime import timedelta
from youtube_dl import YoutubeDL
from Bot_Client.plugins.constents.progress_for_pyrogram import progress_for_pyrogram
from threading import Thread

def human_readable_bytes(value, digits=2, delim="", postfix=""):
    """Return a human-readable file size."""
    if value is None:
        return None
    chosen_unit = "B"
    for unit in ("KiB", "MiB", "GiB", "TiB"):
        if value > 1000:
            value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{value:.{digits}f}" + delim + chosen_unit + postfix


def human_readable_timedelta(seconds, precision=0):
    """Return a human-readable time delta as a string."""
    pieces = []
    value = timedelta(seconds=seconds)

    if value.days:
        pieces.append(f"{value.days}d")

    seconds = value.seconds

    if seconds >= 3600:
        hours = int(seconds / 3600)
        pieces.append(f"{hours}h")
        seconds -= hours * 3600

    if seconds >= 60:
        minutes = int(seconds / 60)
        pieces.append(f"{minutes}m")
        seconds -= minutes * 60

    if seconds > 0 or not pieces:
        pieces.append(f"{seconds}s")

    if not precision:
        return "".join(pieces)

    return "".join(pieces[:precision])


async def process_link(link):
    output = []
    try:    
        with YoutubeDL() as ydl:
            result = ydl.extract_info(link, download=False)
            name = ydl.prepare_filename(result)
            for i in result.get("formats"):
                format_id = i.get("format_id")
                displya_format = i.get("format")
                filesize = i.get("filesize")
                format_note = i.get("format_note") 
                url = i.get("url")
                output.append({
                    "format_id": format_id,
                    "displya_format": displya_format,
                    "filesize":human_readable_bytes(filesize),
                    "url": url,
                    "format_note":format_note
                })
        return output, name,  None

    except Exception as e: return None, None , e



class YTdl_Download_Handler(Thread):
    def __init__(self, url, format_type, message,  download_folder="./downloads/", func=None, args=None):
        super(YTdl_Download_Handler, self).__init__()
        self.format_type = format_type
        self.func = func
        self.args = args
        self.url = url
        self.download_folder = download_folder
        self.message= message


        self.status = ""
        self.downloaded_bytes = 0
        self.total_bytes = 0
        self.filename = None
        self.eta = 0
        self.speed = 0
        # self.presentage = "0%"
        self.started_time = None


    def run(self):
        self.started_time = time.time()
        print(self.message)
        self.setName(f"{self.message.chat.id}_{self.message.reply_to_message_id}")
        asyncio.run(self.manage_workflow())
    
    async def manage_workflow(self):
        original_path = os.getcwd()
        filename = self._download(self.url)


        if self.func is None:
            return os.path.join(self.download_folder, filename)
        
   
        self.args["path"] = filename
        await self.func(**self.args)


    def _download(self, url):
        if not os.path.isdir(self.download_folder): # check if the folder avaibale
            os.makedirs(self.download_folder) 

        os.chdir(self.download_folder) # Change working directory to the download folder

        with YoutubeDL({"format": self.format_type,"progress_hooks":[self._progress_generater]}) as ydl:
            ydl.download([url])
        return self.filename




    def _progress_generater(self, dic):
        if dic.get("status") == "downloading":
            self.status = dic.get("status")
            self.downloaded_bytes = int(dic.get("downloaded_bytes"))
            self.total_bytes = int(dic.get("total_bytes"))
            self.filename = dic.get('filename')

            # if self.loop: self.loop.run_until_complete(progress_for_pyrogram(self.downloaded_bytes, self.total_bytes, f"Status: {self.status}", self.message, self.started_time))

            self.eta = dic.get("_eta_str")
            self.speed = dic.get("_speed_str")
            # self.presentage = dic.get("_percent_str")
  
        
        elif dic.get("status") == "finished":
            self.status = dic.get("status")
            self.filename = dic.get('filename')


    def stop_download(self):
        raise ValueError("Download Stopping..")

 
