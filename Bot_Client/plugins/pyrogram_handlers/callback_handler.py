import os, time, math, threading
import seedir as sd
from Bot_Client import UploadCLI, config
from Bot_Client.plugins.constents.progress_for_pyrogram import progress_for_pyrogram, humanbytes
from Bot_Client.plugins.main_worker.main_worker import MAIN_WORKER
from Bot_Client.plugins.upload_handlers.multi_upload_handler import *
from Bot_Client.plugins.pyrogram_handlers.command_handler import filemanager_cmd



@UploadCLI.on_callback_query()
async def answer(client, update):
    await update.answer(
        f"Button contains: '{update.data}'",
        show_alert=True)
    if update.data == "stop_download":
        await update.message.edit("Stopping download Progress")

    elif 'deletemsg' == update.data:
        await update.message.delete()
        return

    elif "tgupload" == update.data:
        fname = site = None
        data = update.message.reply_to_message.text.split("|")
        if len(data) >= 2:
            fname = data[1].strip()
            if len(data) >= 3:
                site  = data[2].strip()
        url = await MAIN_WORKER.generate_directLinks(data[0].strip(), site)
        print(url)
        await update.answer(f"The file has started downloading..", show_alert=True)
        path = await MAIN_WORKER.download_file(update.message, url, fname, func=MAIN_WORKER.uploadTelegram, prms={"message": update.message})
        return

    elif 'rcloneupload' == update.data:
        if os.path.isfile(f"./Bot_Client/plugins/requirements/{update.message.chat.id}/rclone.conf"):
            await MAIN_WORKER.select_rclone_path(update.message)
        else: await update.message.reply("Please Send Rclone Configuration File")
        return
    
    elif update.data.startswith('D_'):
        details = await UploadCLI.get_messages(update.message.chat.id, int(update.data.split('_')[2]))
        if details.media:
            timex = time.time()
            path = await details.download(f'./downloads/{update.message.chat.id}/', progress=progress_for_pyrogram, progress_args=("File Downloading..", update.message, timex))
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
            config_paths = await MAIN_WORKER.parse_rclone_config(f"./Bot_Client/plugins/requirements/{update.message.chat.id}/rclone.conf")
            path = await MAIN_WORKER.download_file(update.message, url, fname, func=MAIN_WORKER.uploadRclone, prms={"message":update.message,"dest_drive":config_paths[int(update.data.split('_')[1])] })
        return
    
    elif update.data in ['tmp.ninja', 'mixdrop', 'gofile', 'bayfiles', 'transfersh', 'anonfiles']:
        x = await UploadCLI.get_messages(update.message.chat.id, update.message.reply_to_message_id)
        timex = time.time()
        path = await x.download(f'./downloads/{update.message.chat.id}/', progress=progress_for_pyrogram, progress_args=("File Downloading..", update.message, timex))
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
        return

    elif update.data.startswith('fmanager_'):
        x = ('./downloads/', f"./storage/", f'Bot_Client/plugins/requirements/{update.message.chat.id}/',f'./downloads/{update.message.chat.id}/',f'./storage/{update.message.chat.id}/')
        path1, path2, path3, path4, path5 = x
        if update.data == 'fmanager_back':
            await filemanager_cmd(None, update.message, True)
            return

        elif update.data == "fmanager_root_delete":
            deleted_c = []
            for i in x:
                for dirs in os.walk(i):
                    xpath , infolders, infiles = dirs
                    if infiles == [] and infolders == []:
                        os.rmdir(xpath)
                        deleted_c.append(xpath)
            if deleted_c != []:
                msg = ''
                for i in deleted_c:
                    msg += i + '\n'
                await update.message.edit(f"???? ???????????????????????????????????? : ???????????????????????????? ???????????????? ???????????????? ????????????\n\n `{msg}` \nDeleted..!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back To Directory", callback_data="fmanager_back")]]))
                return
            else:
                await update.message.edit(f"???? ???????????????????????????????????? : ???????????????????????????? ???????????????? ???????????????? ???????????? \nNothing Found For Delete", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back To Directory", callback_data="fmanager_back")]]))
                return

        elif update.data == 'fmanager_rootdl':
            path = path1
        elif update.data == 'fmanager_root_ssfolder':
            path = path2
        elif update.data == 'fmanager_config':
            path = path3
        elif update.data == 'fmanager_dls':
            path = path4
        elif update.data == 'fmanager_ssfolder':
            path = path5
        if path:
            if os.path.isdir(path):
                x = sd.seedir(path, style='emoji', printout=False)
                if x:
                    await update.message.edit(update.message.text+'\n\n'+x, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back to Main Directory", callback_data='fmanager_back')]]))
            else: await update.message.edit(update.message.text+'\n\n `Path Is Empty`', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back to Main Directory", callback_data='fmanager_back')]]))

    elif update.data.startswith('ytdl_'):
        await update.message.edit(f"Trying To Download `{update.message.text.strip('????File Name: ')}`"+'\n\n???? ???????????????????????????????????? : ???????????????????????????? ???????????????? ???????????????? ????????????""', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Progress..", callback_data='progress_me')]]))
        data = update.data.split('_')
        message_id, format_id = data[1], data[2]
        x_ = await UploadCLI.get_messages(update.message.chat.id, int(message_id))
        url, fname = await MAIN_WORKER.parse_details_from_message_text(x_.text)
        if not fname: fname = update.message.text.strip("????File Name: ")
        print(url, fname)
        await MAIN_WORKER.ytdl_download(url, format_id, update.message, MAIN_WORKER.uploadTelegram, {"message":update.message} )
     
    elif update.data == "progress_me":
        threads = threading.enumerate()
        for i in threads:
            try:
                if i.name == f"{update.message.chat.id}_{update.message.reply_to_message_id}":
                    percentage = i.downloaded_bytes * 100 / i.total_bytes
                    progress = "[{0}{1}] \nP: {2}%\n".format(
                        ''.join(["???" for i in range(math.floor(percentage / 5))]),
                        ''.join(["???" for i in range(20 - math.floor(percentage / 5))]),
                        round(percentage, 2))
                    tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
                        humanbytes(i.downloaded_bytes),
                        humanbytes(i.total_bytes),
                        humanbytes(i.speed),
                        # elapsed_time if elapsed_time != '' else "0 s",
                        i.eta if i.eta != '' else "0 s"
                    )
                    await update.answer(tmp,show_alert=True)
            except Exception as e:print(e)




