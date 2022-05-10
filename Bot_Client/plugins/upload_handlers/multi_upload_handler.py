import requests
import os
from datetime import datetime, timedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def tmpninja(message, path):
    await message.edit("Now Uploading to TmpNinja")
    url = "https://tmp.ninja/upload.php"
    r = requests.post(url, stream=True, files={'files[]': open(f'{path}','rb')})
    x = r.json()
    if r.status_code == 200 and r.json:
        await message.edit(f'File Uploaded successfully !!\n\nFile Name -: `{x["files"][0]["name"]}`\nLink -: {x["files"][0]["url"]}\nExpire Date -: {datetime.now() + timedelta(hours=48)}\n\n🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Link",url=x["files"][0]["url"])]]))
    os.remove(path)

async def mixdrop(message, path, folderId=230548):
	await message.edit("Now Uploading to MixDrop")

	data = {
		'email': 'worldworhackers@gmail.com',
		'key': 'z6jWcKY0HEty5O7Yiq',
		"file": folderId
	}

	url = "https://ul.mixdrop.co/api"

	r = requests.post(url, stream=True, files={'file': open(f'{path}','rb')}, data=data)

	hmm = f'''File Uploaded successfully !!
Server: MixDrop
**~ Link -:** __{"https://mixdrop.co/f/"+r.json()['result']['fileref']}__


NOTE: Files will be deleted after 60 days of inactivity.\n\n🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️'''
	await message.edit(hmm, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Link', url="https://mixdrop.co/f/"+r.json()['result']['fileref'])]]))
	os.remove(path)

async def gofile(message, path, folderID = '45fefe1e-5c95-4b31-9f1b-a6f98503d6ca'):
	await message.edit("Now Uploading to GoFile")
	token = '6h6j0HkfHJIf6WakTkR1le2rgwPJ2Y8q'
	
	data = {
		"token": token,
		"folderId": folderID
	}
	r = requests.get("https://api.gofile.io/getServer")
	r2 = requests.post(f"https://{r.json()['data']['server']}.gofile.io/uploadFile", stream=True, files={'file': open(path,'rb')}, data=data)


	hmm = f'''File Uploaded successfully !!
Server: GoFile
**~ File Link:** __{r2.json()["data"]["downloadPage"]}__
Warning: Files will be deleted after 10 days of inactivity\n\n🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️'''
	await message.edit(hmm, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download", url=r2.json()["data"]["downloadPage"])]]))
	os.remove(path)

async def bayfiles(message, path):
	await message.edit("Now Uploading to Bayfiles")
	url = "https://api.bayfiles.com/upload"
	r = requests.post(url, stream=True, files={'file': open(path,'rb')})

	hmm = f'''File Uploaded successfully !!
	Server: BayFiles
	**~ File Link:** __{r.json()["data"]["file"]["url"]["short"]}__\n\n🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️'''
	await message.edit(hmm, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download", url=r.json()["data"]["file"]["url"]["short"])]]))


	os.remove(path)

async def transfersh(message, path):
	await message.edit("Now Uploading to TransferSH")
	url = f"https://transfer.sh/"
	r = requests.post(url, stream=True, files={'file': open(path,'rb')})

	hmm = f'''File Uploaded successfully !!
Server: TransferSH
**~ File Link:** __{r.text}__
Warning: Files will be deleted after 14 days.\n\n🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️'''
	await message.edit(hmm, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download", url=r.text)]]))
	os.remove(path)



async def anonfiles(message, path):
	await message.edit("Now Uploading to Anonfile")
	url = "https://api.anonfiles.com/upload"
	r = requests.post(url, stream=True, files={'file': open(path,'rb')})
	hmm = f'''File Uploaded successfully !!
Server: AnonFile
**~ File Link:** __{r.json()["data"]["file"]["url"]["short"]}__\n\n🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️'''
	await message.edit(hmm, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download", url=r.json()["data"]["file"]["url"]["short"])]]))

	os.remove(path)


