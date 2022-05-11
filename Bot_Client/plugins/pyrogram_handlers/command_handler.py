from Bot_Client import UploadCLI, config
import os
from pyrogram.filters import video, video_note, audio, photo, document, command, animation, sticker, media, regex
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@UploadCLI.on_message(command(["start"]))
async def start_cmd(client, message):
    msg = f"Hello, {message.chat.first_name + ' ' + message.chat.last_name}\n\ni'm a Telegram URL Upload Bot!   \nPlease send me any direct download URL Link, i can upload to telegram as File/Video"
    await message.reply(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Source", url='https://telegram.com'), InlineKeyboardButton("Contact Us", url='https://t.me/tokiyo_ew')],[InlineKeyboardButton("Help..!", callback_data="helpmebich")]]))

@UploadCLI.on_message(command(["help"]))
async def help_cmd(client, message):
    msg= f"How to Use Me?\n🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️ \n\nFollow These steps!\n1. Send url (`example.domain/File.mp4` | `New Filename.mp4`).\n\nExample:\nhttps://example.zip\nExample with custom filename:\nhttps://example.zip | `my_file.zip`\n\nSupported Sites:\nhttps://telegra.ph/X-URL-Uploader-Supported-Sites-11-01\n\nIf bot didn't respond, contact @tokiyo_ew"
    await message.reply(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Rclone Settings", callback_data='rclone_settings')]]))

@UploadCLI.on_message(regex(r"https?://.* ?"))
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




