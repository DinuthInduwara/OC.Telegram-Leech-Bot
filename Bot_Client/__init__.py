import pyrogram
import os, json
from dotenv import load_dotenv

load_dotenv()

class config(object):
        TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", '')
        TG_API_ID = os.environ.get("TG_API_ID", 12345)
        TG_API_HASH = os.environ.get("TG_API_HASH", '')
        SUDO_USERS = json.loads(os.environ.get("SUDO_USERS", ''))




plugins = dict(
        root="Bot_Client/plugins"
)
UploadCLI = pyrogram.Client(
        "bot",
        bot_token=config.TG_BOT_TOKEN,
        api_id=config.TG_API_ID,
        api_hash=config.TG_API_HASH,
        plugins=plugins
    )