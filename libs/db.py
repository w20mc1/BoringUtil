import discord
import firebase_admin
from firebase_admin import credentials, firestore_async
from libs.load_cfg import load_config

firebase_admin.initialize_app(credentials.Certificate("config/boringutil-firebase.json"))
db = firestore_async.client()
servers = db.collection("servers")
config = load_config()

async def get_prefix(_, msg: discord.Message):
    if not msg.guild:
        return config["default_prefix"]

    srv_doc = await servers.document(str(msg.guild.id)).get()
    prefix = srv_doc.to_dict().get("prefix", config["default_prefix"]) if srv_doc.exists else config["default_prefix"]
    return prefix