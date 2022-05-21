
from youtube_dl import YoutubeDL
import os


with open("test.txt", 'w') as f:

    def printin(message):
        print(type(message))
        f.write(str(message) +"\n")


    opts = {
        "format": '140', 
        "progress_hooks":[printin],
        "forcefilename":"main.mp3"
        }


    link = "https://www.youtube.com/watch?v=3yTbWsvDpAQ"

    os.chdir("downloads")
    with YoutubeDL(opts) as ydl:
        x = ydl.download([link])