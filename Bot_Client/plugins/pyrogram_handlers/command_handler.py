from Bot_Client import UploadCLI
import pyrogram
from pyrogram.filters import video, video_note, audio, photo, document, animation, sticker, media
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@UploadCLI.on_message(pyrogram.filters.command(["start"]))
async def start_cmd(client, message):
    msg = f"Hello, {message.chat.first_name + ' ' + message.chat.last_name}\n\ni'm a Telegram URL Upload Bot!   \nPlease send me any direct download URL Link, i can upload to telegram as File/Video"
    await message.reply(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Source", url='https://telegram.com'), InlineKeyboardButton("Contact Us", url='https://t.me/tokiyo_ew')],[InlineKeyboardButton("Help..!", callback_data="helpmebich")]]))

@UploadCLI.on_message(pyrogram.filters.command(["help"]))
async def help_cmd(client, message):
    msg= f"How to Use Me?\n🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️ \n\nFollow These steps!\n1. Send url (`example.domain/File.mp4` | `New Filename.mp4`).\n\nExample:\nhttps://example.zip\nExample with custom filename:\nhttps://example.zip | `my_file.zip`\n\nSupported Sites:\nhttps://telegra.ph/X-URL-Uploader-Supported-Sites-11-01\n\nIf bot didn't respond, contact @tokiyo_ew"
    await message.reply(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Rclone Settings", callback_data='rclone_settings')]]))

@UploadCLI.on_message(pyrogram.filters.regex(r"https?://.* ?"))
async def filter_links(client, message):
    await message.reply("Choose ..", reply_markup=pyrogram.types.InlineKeyboardMarkup([[
            pyrogram.types.InlineKeyboardButton('Telegram Leech', callback_data='tgupload'),
            pyrogram.types.InlineKeyboardButton('Rclone Upload', callback_data='rcloneupload'),
            pyrogram.types.InlineKeyboardButton('Close Menu', callback_data='deletemsg')
        ]]), quote=True)


@UploadCLI.on_message(document)
async def filter_links(client, message):
    if message.document.file_name == 'rclone.conf':
        await message.download(f"./Bot_Client/plugins/requirements/{message.chat.id}/rclone.conf")
        await message.reply("Rclone Configuration File Download", quote=True)
    await message.reply("Select Site You Wont To Upload This File", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("AnonFile.com", callback_data='anonfiles'), InlineKeyboardButton("Transfre.Sh", callback_data='transfersh'), InlineKeyboardButton("BayFiles.com", callback_data='bayfiles')],[InlineKeyboardButton("Gofile.IO", callback_data='gofile'), InlineKeyboardButton("MixDrop.co", callback_data='mixdrop'), InlineKeyboardButton("TMP.Ninja", callback_data='tmp.ninja')],[InlineKeyboardButton("Rclone", callback_data='rcloneupload'), InlineKeyboardButton("Close Menu", callback_data='deletemsg')]]),  quote=True)
    



@UploadCLI.on_message(video | video_note | audio | photo | animation | sticker | media)
async def filter_links(client, message):
    await message.reply("Select Site You Wont To Upload This File", quote=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("AnonFile.com", callback_data='anonfiles'), InlineKeyboardButton("Transfre.Sh", callback_data='transfersh'), InlineKeyboardButton("BayFiles.com", callback_data='bayfiles')],[InlineKeyboardButton("Gofile.IO", callback_data='gofile'), InlineKeyboardButton("MixDrop.co", callback_data='mixdrop'), InlineKeyboardButton("TMP.Ninja", callback_data='tmp.ninja')],[InlineKeyboardButton("Rclone", callback_data='rcloneupload'), InlineKeyboardButton("Close Menu", callback_data='deletemsg')]]))


