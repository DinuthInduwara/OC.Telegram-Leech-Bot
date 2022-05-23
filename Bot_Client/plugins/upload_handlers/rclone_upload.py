import subprocess, re, time, asyncio
from datetime import date
from pyrogram.errors import FloodWait
from Bot_Client.plugins.constents.progress_for_pyrogram import progress_for_pyrogram

async def rclone_Upload(path, message, dest_drive):
    today = date.today()
    d2 = today.strftime("%B %d %Y")
    CONF_PATH = f"./Bot_Client/plugins/requirements/{message.chat.id}/rclone.conf"
    folder = f"{dest_drive}:{today.strftime('%Y')}/{d2}"


    rclone_copy_cmd = [
        "rclone",
        "copy",
        f"--config={CONF_PATH}",
        str(path),
        folder,
        "-f",
        "- *.!qB",
        "--buffer-size=1M",
        "-P",
    ]

    rclone_pr = subprocess.Popen(rclone_copy_cmd, stdout=subprocess.PIPE)
    rcres = await rclone_process_display(rclone_pr, message, path, folder, CONF_PATH)
    return rcres

    



async def rclone_process_display(process, message, path, destfolder, confif_path):
    blank = 0
    sleeps = False
    try:
        while True:

            data = process.stdout.readline().decode()
            data = data.strip()
            mat = re.findall(r"Transferred:.*ETA.*", data)

            if mat is not None:
                if len(mat) > 0:
                    sleeps = True
                    try:
                        start = time.time()
                        
                        g = re.findall(r'Transferred:\s+\\t\s+(\d+\s\w+)[ /]+(\d+\s\w+)[\s,]+(\d+%),\s+([\d.\s\w/]+).+(ETA\s\d+\w+)', str(mat))
                        if len(g) > 0:
                            noww, totall, present, speedd, eta = g[0]
                            print(int(noww.split(' ')[0]), int(totall.split(' ')[0]), present, speedd, eta)
                            current = int(noww.split(' ')[0])
                            total = int(totall.split(' ')[0])
                            await progress_for_pyrogram(current, total, "Uploding Using Rclone", message, start)
                            
                    except Exception as e:print(e)
                       


            if data == "":
                blank += 1
                if blank <= 20:
                    break
            else:
                blank = 0

            if sleeps:
                sleeps = False
                process.stdout.flush()
        await message.edit("Upload Complete")
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        await message.edit(e)
    


    # rclone_json = [
    #     "rclone",
    #     "lsjson",
    #     f"--config={confif_path}",
    #     f"\"{destfolder}/{path.split('/')[-1]}\"",
    # ]


    try:
        # rclone_json = f"rclone lsjson --config={confif_path} \"{destfolder}/{path.split('/')[-1]}\""
        rclone_json = ["rclone", "link", f"--config={confif_path}", f"{destfolder}/{path.split('/')[-1]}"]
        process = subprocess.Popen(rclone_json, stdout=subprocess.PIPE)
        data = process.stdout.read().decode().strip()
        return data
        # data = json.loads(stdout)
        # id = data[0]["ID"]
        # name = data[0]["Name"]
        # await message.edit(f"https://drive.google.com/file/d/{id}/view?usp=sharing\n`{name}`")
    except Exception as e:print(e)
    





