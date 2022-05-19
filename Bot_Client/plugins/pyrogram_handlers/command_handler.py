from Bot_Client import UploadCLI, config
import os, subprocess
from pyrogram.filters import video, video_note, audio, photo, document, command, animation, sticker, media, regex
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Bot_Client.plugins.main_worker.main_worker import MAIN_WORKER


@UploadCLI.on_message(command(["start"]))
async def start_cmd(client, message):
    msg = f"Hello, {message.chat.first_name + ' ' + message.chat.last_name}\n\ni'm a Telegram URL Upload Bot!   \nPlease send me any direct download URL Link, i can upload to telegram as File/Video"
    await message.reply(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Source", url='https://telegram.com'), InlineKeyboardButton("Contact Us", url='https://t.me/tokiyo_ew')],[InlineKeyboardButton("Help..!", callback_data="helpmebich")]]))

@UploadCLI.on_message(command(["help"]))
async def help_cmd(client, message):
    msg= f"How to Use Me?\n🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️ \n\nFollow These steps!\n1. Send url (`example.domain/File.mp4` | `New Filename.mp4`).\n\nExample:\nhttps://example.zip\nExample with custom filename:\nhttps://example.zip | `my_file.zip`\n\nSupported Sites:\nhttps://telegra.ph/X-URL-Uploader-Supported-Sites-11-01\n\nIf bot didn't respond, contact @tokiyo_ew"
    await message.reply(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Rclone Settings", callback_data='rclone_settings')]]))

@UploadCLI.on_message(regex(r"^https?://.* ?"))
async def filter_links(client, message):
    await message.reply("Choose ..", reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton('Telegram Leech', callback_data='tgupload'),
            InlineKeyboardButton('Rclone Upload', callback_data='rcloneupload'),
            InlineKeyboardButton('Close Menu', callback_data='deletemsg')
        ]]), quote=True)


@UploadCLI.on_message(document)
async def filter_documents(client, message):
    if message.document.file_name == 'rclone.conf':
        await message.download(f"./Bot_Client/plugins/requirements/{message.chat.id}/rclone.conf")
        await message.reply("Rclone Configuration File Download", quote=True)
    await message.reply("Select Site You Wont To Upload This File", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("AnonFile.com", callback_data='anonfiles'), InlineKeyboardButton("Transfre.Sh", callback_data='transfersh'), InlineKeyboardButton("BayFiles.com", callback_data='bayfiles')],[InlineKeyboardButton("Gofile.IO", callback_data='gofile'), InlineKeyboardButton("MixDrop.co", callback_data='mixdrop'), InlineKeyboardButton("TMP.Ninja", callback_data='tmp.ninja')],[InlineKeyboardButton("Rclone", callback_data='rcloneupload'), InlineKeyboardButton("Close Menu", callback_data='deletemsg')]]),  quote=True)
    



@UploadCLI.on_message(video | video_note | audio | photo | animation | sticker | media)
async def filter_media(client, message):
    await message.reply("Select Site You Wont To Upload This File", quote=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("AnonFile.com", callback_data='anonfiles'), InlineKeyboardButton("Transfre.Sh", callback_data='transfersh'), InlineKeyboardButton("BayFiles.com", callback_data='bayfiles')],[InlineKeyboardButton("Gofile.IO", callback_data='gofile'), InlineKeyboardButton("MixDrop.co", callback_data='mixdrop'), InlineKeyboardButton("TMP.Ninja", callback_data='tmp.ninja')],[InlineKeyboardButton("Rclone", callback_data='rcloneupload'), InlineKeyboardButton("Close Menu", callback_data='deletemsg')]]))


@UploadCLI.on_message(command(["filemanager"]))
async def filemanager_cmd(client, message, before=False):
    path1 = f'Bot_Client/plugins/requirements/{message.chat.id}/'
    path2 = f'./downloads/{message.chat.id}/'
    path3 = f'./storage/{message.chat.id}/'
    paths = []

    if int(message.from_user.id) in config.SUDO_USERS:
        paths.append([InlineKeyboardButton("Root Download", callback_data='fmanager_rootdl')])
        paths.append([InlineKeyboardButton("Root Media", callback_data='fmanager_root_ssfolder')])
        paths.append([InlineKeyboardButton("Delete Empty", callback_data='fmanager_root_delete')])

    if os.path.isdir(path1) and os.listdir(path1) != []:
        paths.append([InlineKeyboardButton("Configurations", callback_data='fmanager_config')])
    if os.path.isdir(path2) and os.listdir(path2) != []:
        paths.append([InlineKeyboardButton("Download Folder", callback_data='fmanager_dls')])
    if os.path.isdir(path3) and os.listdir(path3) != []:
        paths.append([InlineKeyboardButton("Generated Media", callback_data='fmanager_ssfolder')])

    if before:
        if paths == []:
            await message.edit("Your File Manager Is Empty🤦🤷🤷\n\n🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️")
        else:
            await message.edit("Your File Manager..\n\n🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️", reply_markup=InlineKeyboardMarkup(paths))

    else:
        if paths == []:
            await message.reply("Your File Manager Is Empty🤦🤷🤷\n\n🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️")
        else:
            await message.reply("Your File Manager..\n\n🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️", reply_markup=InlineKeyboardMarkup(paths))



@UploadCLI.on_message(command(["shell"]))
async def shell_cmd(client, message):
    cmd = message.text.split(' ', 1)
    if len(cmd) == 1:
        await message.reply_text('No command to execute was given.')
        return
    cmd = cmd[1]
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if stdout:
        reply += f"*Stdout*\n`{stdout}`\n"
    if stderr:
        reply += f"*Stderr*\n`{stderr}`\n"
    if len(reply) > 3000:
        doc = 'Bot_Client/plugins/requirements/shell_output.txt'
        with open(doc, 'w') as file:
            file.write(reply)
        await message.reply_document(doc)
    else:
        if len(reply) > 1:
            await message.reply(reply)


@UploadCLI.on_message(command(["ytdl"]))
async def ytdl_cmd(client, message):
    msg = await message.reply("Processing Message 😁👀", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("༼ つ ◕_◕ ༽つ", url="https://t.me/+qvJ4LlkWlSs1YTI1")]]),  quote=True)
    url , fname = await MAIN_WORKER.parse_details_from_message_text(message.text)
    print(url, fname)
    if url:
        qualitys, errors = await MAIN_WORKER.create_ytdl_quality_menu(url, message, short_msg="ytdl")
        if fname == None: fname = qualitys[1]
        if errors: await msg.edit(f"Cant Process url becouse:{errors}")
        else: await msg.edit(f"📁File Name: `{fname}`", reply_markup=InlineKeyboardMarkup(qualitys[0]))
        return




