import pyrogram
import pymongo, os
from dotenv import load_dotenv

load_dotenv()

class config(object):
        MONGODB_URI = os.environ.get("MONGODB_URI", '')
        OUOBACE_URI = os.environ.get("OUOBACE_URI", '')
        TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", '')
        TG_API_ID = os.environ.get("TG_API_ID", 12345)
        TG_API_HASH = os.environ.get("TG_API_HASH", '')
        SUDO_USERS = list(os.environ.get("SUDO_USERS", ''))



MONGO_DB = config.MONGODB_URI
DBCLIENT = pymongo.MongoClient(MONGO_DB)
plugins = dict(
        root="Bot_Client/plugins"
)
OUOBACE = config.OUOBACE_URI
UploadCLI = pyrogram.Client(
        "bot",
        bot_token=config.TG_BOT_TOKEN,
        api_id=config.TG_API_ID,
        api_hash=config.TG_API_HASH,
        plugins=plugins
    )