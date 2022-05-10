import os, time
from Bot_Client.plugins.constents.progress_for_pyrogram import progress_for_pyrogram
from Bot_Client import UploadCLI, config
from Bot_Client.plugins.main_worker.main_worker import MAIN_WORKER
from Bot_Client.plugins.upload_handlers.multi_upload_handler import *

@UploadCLI.on_callback_query()
async def answer(client, update):
    # await update.answer(
    #     f"Button contains: '{update.data}'",
    #     show_alert=True)


    if 'deletemsg' == update.data:
        await update.message.delete()


    if "tgupload" == update.data:
        fname = site = None
        data = update.message.reply_to_message.text.split("|")
        if len(data) >= 2:
            fname = data[1].strip()
            if len(data) >= 3:
                site  = data[2].strip()
        url = await MAIN_WORKER.generate_directLinks(data[0].strip(), site)
        print(url)
        await update.answer(f"The file has started downloading..", show_alert=True)
        path = await MAIN_WORKER.download_file(update.message, url, fname)
        await MAIN_WORKER.uploadTelegram(update.message, path)


    if 'rcloneupload' == update.data:
        if os.path.isfile(f"./Bot_Client/plugins/requirements/{update.message.chat.id}/rclone.conf"):
            await MAIN_WORKER.select_rclone_path(update.message)
        else: await update.message.reply("Please Send Rclone Configuration File")
    
    if update.data.startswith('D_'):
        details = await UploadCLI.get_messages(update.message.chat.id, int(update.data.split('_')[2]))
        if details.media:
            timex = time.time()
            path = await details.download('./downloads/', progress=progress_for_pyrogram, progress_args=("File Downloading..", update.message, timex))
            config_paths = await MAIN_WORKER.parse_rclone_config(f"./Bot_Client/plugins/requirements/{update.message.chat.id}/rclone.conf")
            await MAIN_WORKER.uploadRclone(update.message, path, config_paths[int(update.data.split('_')[1])])
        else:
            fname = site = None
            data = details.text.split("|")
            if len(data) >= 2:
                fname = data[1].strip()
                if len(data) >= 3:
                    site  = data[2].strip()
            url = await MAIN_WORKER.generate_directLinks(data[0].strip(), site)
            print(url)
            await update.answer(f"The file has started downloading..", show_alert=True)
            path = await MAIN_WORKER.download_file(update.message, url, fname)
            print(path)
            config_paths = await MAIN_WORKER.parse_rclone_config(f"./Bot_Client/plugins/requirements/{update.message.chat.id}/rclone.conf")
            await MAIN_WORKER.uploadRclone(update.message, path, config_paths[int(update.data.split('_')[1])])
    

    if update.data in ['tmp.ninja', 'mixdrop', 'gofile', 'bayfiles', 'transfersh', 'anonfiles']:
        x = await UploadCLI.get_messages(update.message.chat.id, update.message.reply_to_message_id)
        timex = time.time()
        path = await x.download('./downloads/', progress=progress_for_pyrogram, progress_args=("File Downloading..", update.message, timex))
        if update.data == 'tmp.ninja':
            await tmpninja(update.message, path)
        elif update.data == 'mixdrop':
            if int(update.message.from_user.id) in config.SUDO_USERS:
                await mixdrop(update.message, path, 230546)
            else:await mixdrop(update.message, path)
        elif update.data == 'gofile':
            if int(update.message.from_user.id) in config.SUDO_USERS:
                await gofile(update.message, path, "97ae8dbe-5f46-452e-b7ce-e2cccd5638b2")
            else: await gofile(update.message, path)
        elif update.data == 'bayfiles':
            await bayfiles(update.message, path)
        elif update.data == 'transfersh':
            await transfersh(update.message, path)
        elif update.data == 'anonfiles':
            await anonfiles(update.message, path)









            