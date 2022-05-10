import mimetypes, os, time
from Bot_Client import UploadCLI
from Bot_Client.plugins.constents.progress_for_pyrogram import progress_for_pyrogram


async def get_type(path):
    kind = mimetypes.guess_type(path)
    if 'image' in kind[0]:
        return "photo"
    elif "audio" in kind[0]:
        return "audio"
    elif "video" in kind[0]:
        return "video"
    else:
        return "document"




    
async def upload_tg(message, path):
    tg_upload_type = await get_type(path)
    start_time = time.time()

    try:
        if tg_upload_type == "photo":
            await UploadCLI.send_photo(message.chat.id, photo=path, caption=os.path.basename(path), progress=progress_for_pyrogram, progress_args=("Now Uploading..", message, start_time))
        elif tg_upload_type == "audio":
            await UploadCLI.send_audio(message.chat.id, audio=path, title=os.path.basename(path), progress=progress_for_pyrogram, progress_args=("Now Uploading..", message, start_time))
        elif tg_upload_type == "video":
            await UploadCLI.send_video(message.chat.id, video=path, file_name=os.path.basename(path), progress=progress_for_pyrogram, progress_args=("Now Uploading..", message, start_time))
        elif tg_upload_type == "document":
            await UploadCLI.send_document(message.chat.id, document=path, file_name=os.path.basename(path), progress=progress_for_pyrogram, progress_args=("Now Uploading..", message, start_time))
        await message.delete()
    except Exception as e:
        await message.edit(e)
    
        