import re, os, json, asyncio
from Bot_Client import UploadCLI
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from Bot_Client.plugins.download_handlers.downloader import Filedownloade 
from Bot_Client.plugins.download_handlers.direct_linkGeneratr import gen_link
from Bot_Client.plugins.download_handlers.file_downloader import download
from Bot_Client.plugins.upload_handlers.telegram_uploder import upload_tg, get_type
from Bot_Client.plugins.upload_handlers.rclone_upload import rclone_Upload
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import Bot_Client.plugins.video_processing.ffmpeg_handler as video_processing
from Bot_Client.plugins.download_handlers.ytdl_handler import create_quality_menu, get_yt_link_details

class main_worker:
    async def generate_directLinks(self, link, dtype):
        return await gen_link(link, dtype)

    async def download_file(self, message,  url,  filename=None):
        if filename:
            filename = os.path.join(f"downloads/{message.chat.id}/{filename}")
        downloadCLI = Filedownloade(url,message, filename)
        downloadCLI.start()
        x = None
        while downloadCLI.is_alive():
            await asyncio.sleep(4)
            if 'id' in json.loads(str(message)):
                msgid= message.id
            else: msgid = message.message_id
            msg = await UploadCLI.get_messages(message.chat.id, msgid)
            if msg.text == "Stopping download Progress":
                    downloadCLI.kill_thread()
                    os.remove(downloadCLI.file_name)
                    return None
            elif downloadCLI.bar != x:
                x = downloadCLI.bar
                try: await msg.edit_text(downloadCLI.progress_bar, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Stop Task", callback_data="stop_download")]]))
                except Exception as e:print(e)
        return downloadCLI.file_name

    async def uploadTelegram(self, message, path):
        if path==None:
            return
        paths = []
        if type(path) == str:
            paths.append(path)
        if type(path) == list:
            paths = path

        for i in paths:
            if os.path.getsize(i) > 1900000000:
                if await get_type(i) == "video":
                    paths.remove(i)
                    vids_folder = await self.split_video(i)
                    [paths.append(vids_folder+i) for i in os.listdir(vids_folder)]


        for i in paths:
            try:
                await upload_tg(message, i)
                
                try:
                    await self.generate_screen_shots_and_send(message, i)
                except Exception as e:
                    print(e)
                finally:os.remove(i)
            except Exception as e:
                await message.reply(f"`{i}` file cant upload becouse: {e}")
        await message.delete()

    async def generate_screen_shots_and_send(self, message, path, ss_count=6):
        metadata = extractMetadata(createParser(path))
        try:
            output_file = f"./storage/{message.chat.id}/"
            if metadata != None:
                if not os.path.isdir(output_file):
                    os.makedirs(output_file)
                total_duration = metadata.get("duration").seconds/60
                await video_processing.generate_screen_shots(path, output_file, False, None, total_duration, ss_count)
                photo_list = [i for i in os.listdir(output_file)]
                await UploadCLI.send_media_group(message.chat.id, [InputMediaPhoto(output_file+i.strip()) for i in photo_list])
                [os.remove(output_file+i) for i in photo_list]
        except Exception as e:
            await UploadCLI.send_message(message.chat.id, "Failed to upload ScreenShots Becouse:{}".format(e))
        finally:
                os.remove(path)

    async def uploadRclone(self, message, path , dest_drive):
        await rclone_Upload(path, message, dest_drive)
        try:await self.generate_screen_shots_and_send(message, path)
        except:pass
        finally: 
            if path:
                os.remove(path)
    
    async def parse_rclone_config(self, path):
        with open(path, 'r') as f:
            x =  re.findall(r"\[(.*)\]", f.read())
            return [i.strip() for i in x]
            
    async def select_rclone_path(self, message):
        configpath = await self.parse_rclone_config(f"./Bot_Client/plugins/requirements/{message.chat.id}/rclone.conf")
        inline_keyboard = [[InlineKeyboardButton(n, callback_data=f"D_{i}_{message.reply_to_message_id}")] for i, n in enumerate(configpath)]
        await message.edit("Select Rclone Configuration", reply_markup=InlineKeyboardMarkup(inline_keyboard))

    async def list_files_and_folders(self, path):
        folders = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        files = [d for d in os.listdir(path) if os.path.isfile(os.path.join(path, d))]
        return{"files": files, "folders": folders}
    
    async def list_splitter(self, list_, spliting_count) -> list:
        output = []
        for i in range(0 , len(list_), spliting_count):
            l = list_[i: i+spliting_count]
            output.append(l)
        return output
            
    async def split_video(self, path, max_size=1900000000):
        return await video_processing.split_file(path, max_size)
        
    async def ytdl_download(self, url, path, format_id, message):
        data, err = await get_yt_link_details(url)
        if err:
            return None, err
        nurl = [i.get("url") for i in data.get("formats") if format_id == i.get("format_id")][0]
        if nurl == None or nurl == ():
            return None, err
        try: 
            return await self.download_file(message, nurl, path), None
        except Exception as e: return None, e

        
    async def create_ytdl_quality_menu(self, url, message, short_msg):
        if 'id' in json.loads(str(message)): msgid= message.id
        else: msgid = message.message_id
        return await create_quality_menu(url, msgid, short_msg)

    async def parse_details_from_message_text(self, text):
        fname = fname = None
        if len(text.split(" ")) > 1:
            url = text.split(' ')[1]
            if len(text.split('|')) > 1:
                fname = text.split('|')[-1]
            return  url, fname
        else: return  None, None


MAIN_WORKER = main_worker()