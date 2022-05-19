from datetime import timedelta
import asyncio
import json
import shlex
from pyrogram.types import InlineKeyboardButton
from typing import Dict, List, Optional, Tuple, Union

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



async def cli_call(cmd: Union[str, List[str]]) -> Tuple[str, str]:
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    elif isinstance(cmd, (list, tuple)):
        pass
    else:
        return None, None

    process = await asyncio.create_subprocess_exec(
        *cmd, stderr=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    stdout = stdout.decode().strip()
    stderr = stderr.decode().strip()

    with open("test.txt", "w", encoding="UTF-8") as f:
        f.write(stdout)

    return stdout, stderr


async def get_yt_link_details(url: str) -> Union[Dict[str, str], None]:
    cmd = "youtube-dl --no-warnings --youtube-skip-dash-manifest --dump-json"
    cmd = shlex.split(cmd)
    if "hotstar" in url:
        cmd.append("--geo-bypass-country")
        cmd.append("IN")
    cmd.append(url)

    out, error = await cli_call(cmd)
    if error:
        print(f"Error occured:- {error} for url {url}")
    # sanitize the json
    out = out.replace("\n", ",")
    out = "[" + out + "]"
    try:
        return json.loads(out)[0], None
    except:
        print("Error occured while parsing the json.\n")
        return None, error


async def create_quality_menu(
    url: str,
    message_id,
    short_msg,
    jsons: Optional[str] = None,

):
    if jsons is None:
        data, err = await get_yt_link_details(url)
    else:
        data = jsons


    if data is None:
        return None, err
    else:
        if "_filename" in data:
            file_name = data["_filename"]
        else:file_name = "untitled.mp4"

        unique_formats = dict()
        for i in data.get("formats"):
            colity_format = i.get("format_note")
            file_size = i.get("filesize")
            d_format = i.get("format_id")
            url = i.get("url")
            if colity_format is None:
                colity_format = i.get("height")
            unique_formats[colity_format] = {"size": file_size, "url": url, "d_format": d_format}

        buttons = list()
        for i in unique_formats.keys():
            if i == "tiny":
                text = f"tiny [{human_readable_bytes(unique_formats[i]['size'])}] ➡️"
                callback_data = f'{short_msg}_{message_id}_{unique_formats[i]["d_format"]}'
                buttons.append([InlineKeyboardButton(text, callback_data=callback_data)])
            else:
                text = f"{i} - [{human_readable_bytes(unique_formats[i]['size'])}] ➡️"
                callback_data = f'{short_msg}_{message_id}_{unique_formats[i]["d_format"]}'
                buttons.append([InlineKeyboardButton(text, callback_data=callback_data)])


    return (buttons, file_name), None




