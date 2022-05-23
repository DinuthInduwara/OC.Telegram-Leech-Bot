import re, os, json, asyncio
from Bot_Client import UploadCLI
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from Bot_Client.plugins.download_handlers.downloader import Filedownloade 
from Bot_Client.plugins.download_handlers.direct_linkGeneratr import gen_link
from Bot_Client.plugins.upload_handlers.telegram_uploder import upload_tg, get_type
from Bot_Client.plugins.upload_handlers.rclone_upload import rclone_Upload
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import Bot_Client.plugins.video_processing.ffmpeg_handler as video_processing
from Bot_Client.plugins.download_handlers.ytdl_handler import YTdl_Download_Handler, process_link

class main_worker:
    async def generate_directLinks(self, link: str, dtype: str):
        return await gen_link(link, dtype)

    async def download_file(self, message: any,  url:str,  filename=None, func=None, prms:dict=None):
        await message.edit('The file has started downloading⏬⏬', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(".o((⊙﹏⊙))o.", url="https://t.me/+qvJ4LlkWlSs1YTI1")]]))
        if filename:
            filename = os.path.join(f"downloads/{message.chat.id}/{filename}")

        downloadCLI = Filedownloade(url,message, filename, func, prms)
        downloadCLI.start()
        return True
        

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
        url = await rclone_Upload(path, message, dest_drive)
        await message.edit(f"Public URL: {url}\n\n🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('URL', url=url)]]))
        try:await self.generate_screen_shots_and_send(message, path)
        except:pass
        finally: 
            try:
                if path:
                    os.remove(path)
            except FileNotFoundError: pass
    
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
        
    async def ytdl_download(self, url, format_id, message, func, args):
        # obj = YTdl_Download_Handler(url, format_type=format_id, message=message, func=func, args=args)
        # obj.start()
        out, name , err = await process_link(url)
        if err: await message.edit(f"Cant Process Link: {err}")
        link = None
        for i in out:
            if i.get("format_id") == format_id: link = i.get("url")
        if link: return await self.download_file(message, url, name, func=self.uploadTelegram, prms={"message":message})
        else: await message.edit(f"Something went wrong with the link. Please try again later or recheck the link your link.")


    async def create_ytdl_quality_menu(self, url, message, short_msg):
        try:
            if 'id' in json.loads(str(message)): msgid= message.id
            else: msgid = message.message_id
            out, _ , err = await process_link(url)
            if err: return None, err
            m_list =  [InlineKeyboardButton(f"{i.get('filesize')} {i.get('displya_format').split('-')[1:][0]}", callback_data=f"{short_msg}_{msgid}_{i.get('format_id')}") for i in out]
            
            output = []
            for i in range(0, len(m_list), 2): # Slicing Inline Keyboard Buttons
                l = m_list[i: i+2]
                output.append(l)
            return output, None
        except Exception as e: return None, e

    async def parse_details_from_message_text(self, text):
        fname = fname = None
        if len(text.split(" ")) > 1:
            url = text.split(' ')[1]
            if len(text.split('|')) > 1:
                fname = text.split('|')[-1]
            return  url, fname
        else: return  None, None


MAIN_WORKER = main_worker()