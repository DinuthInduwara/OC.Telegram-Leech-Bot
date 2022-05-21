from youtube_dl import YoutubeDL

import logging



LOGGER = logging.getLogger(__name__)






async def process_link(link):
    output = []
    with YoutubeDL() as ydl:
        result = ydl.extract_info(link, download=False)
        name = ''
        name = ydl.prepare_filename(result) if name == "" else name
        for i in result.get("formats"):
            format_id = i.get("format_id")
            displya_format = i.get("format")
            filesize = i.get("filesize")
            url = i.get("url")
            output.append({
                "format_id": format_id,
                "displya_format": displya_format,
                "filesize":filesize,
                "url" : url
            })
    return output