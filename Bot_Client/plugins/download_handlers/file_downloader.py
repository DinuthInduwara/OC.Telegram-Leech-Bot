# import sys
import requests
import time
import mimetypes
from Bot_Client.plugins.constents.progress_for_pyrogram import progress_for_pyrogram

def filenamegen(url, content_type):
    filename = url.split("/")[-1].replace('%', ' ').strip()
    if filename == "":
        filename = url.split("/")[-2].replace('%', ' ').strip()
    if '.' not in filename:
        filename = filename+mimetypes.guess_extension(content_type)
    return filename



async def download(url,message,  filename=None):
    response = requests.get(url, stream=True, allow_redirects=True)
    if filename == None or "." not in filename:
        filename = filenamegen(url, response.headers.get('content-type').strip())
    filename = './downloads/'+filename
    total = response.headers.get('content-length')
    curr_time = time.time()

    
    with open(filename, 'wb') as f:
        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                # done = int(50*downloaded/total)
                done = int(downloaded/total)
                
                await progress_for_pyrogram(downloaded, total, "Now Downloading..", message, curr_time)
                
                # sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                # sys.stdout.flush()
    # sys.stdout.write('\n')
    return filename






