
import asyncio
import os
import math
import secrets
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser




async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = f"{output_directory}/{secrets.token_hex(nbytes=10).replace('.', '_')}.jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    # width = "90"
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None

# https://github.com/Nekmo/telegram-upload/blob/master/telegram_upload/video.py#L26


async def generate_screen_shots(
    video_file,
    output_directory,
    is_watermarkable,
    wf,
    min_duration,
    no_of_photos
):
    metadata = extractMetadata(createParser(video_file))
    duration = 0
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    if duration > min_duration:
        images = []
        ttl_step = duration // no_of_photos
        current_ttl = ttl_step
        for looper in range(0, no_of_photos):
            ss_img = await take_screen_shot(video_file, output_directory, current_ttl)
            current_ttl = current_ttl + ttl_step
            images.append(ss_img)
        return images
    else:
        return None




async def cult_small_video(video_file, out_put_file_name, start_time, end_time):
    file_genertor_command = [
        "ffmpeg",
        "-hide_banner",
        "-i",
        video_file,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-async",
        "1",
        "-strict",
        "-2",
        "-c",
        "copy",
        out_put_file_name,
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    stderr.decode().strip()
    stdout.decode().strip()
    return out_put_file_name


async def split_file(path, max_size=1800000000, force_docs=False):

    metadata = extractMetadata(createParser(path))

    if metadata.has("duration"):
        total_duration = metadata.get("duration").seconds

    metadata = metadata.exportDictionary()
    try:
        mime = metadata.get("Common").get("MIME type")
    except:
        mime = metadata.get("Metadata").get("MIME type")

    ftype = mime.split("/")[0]
    ftype = ftype.lower().strip()

    split_dir = os.path.join(os.path.dirname(path), secrets.token_hex(nbytes=10).replace('.', '_'))

    if not os.path.isdir(split_dir):
        os.makedirs(split_dir)

    if ftype == "video" and not force_docs:
        total_file_size = os.path.getsize(path)

        parts = math.ceil(total_file_size / max_size)
        # need this to be implemented to remove recursive file split calls
        # remove saftey margin
        # parts += 1

        minimum_duration = total_duration / parts

        # casting to int cuz float Time Stamp can cause errors
        minimum_duration = int(minimum_duration)

        # END: proprietary
        start_time = 0
        end_time = minimum_duration

        base_name = os.path.basename(path)
        input_extension = base_name.split(".")[-1]

        i = 0
        flag = False

        while end_time <= total_duration:

            # file name generate
            parted_file_name = "{}_PART_{}.{}".format(
                str(base_name), str(i).zfill(5), str(input_extension)
            )

            output_file = os.path.join(split_dir, parted_file_name)

            opfile = await cult_small_video(
                path, output_file, str(start_time), str(end_time)
            )

            # adding offset of 3 seconds to ensure smooth playback
            start_time = end_time - 3
            end_time = end_time + minimum_duration
            i = i + 1

            if (end_time > total_duration) and not flag:
                end_time = total_duration
                flag = True
            elif i + 1 == parts:
                end_time = total_duration
                flag = True
            elif flag:
                break

    return split_dir+'/'



