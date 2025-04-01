import logging
import discord
import os
import colorlog
import google.generativeai as genai
from libs import db
from discord.ext import commands
from dotenv import load_dotenv
from libs.load_cfg import load_config
load_dotenv()

client = commands.Bot(command_prefix = db.get_prefix, intents = discord.Intents.all())
genai.configure()
config = load_config()

log = logging.getLogger("BoringUtil")
log.setLevel(logging.DEBUG)
# have fun getting sniped from #1
btmc_handler = logging.StreamHandler()
btmc_handler.setFormatter(colorlog.ColoredFormatter(
    "%(blue)s%(name)s %(log_color)s[%(levelname)s]%(cyan)s: %(reset)s%(message)s"
))
log.addHandler(btmc_handler)

cogs = [
    f"cogs.{filename[:-3]}" for filename in os.listdir("./cogs/") if filename.endswith(".py")
]

@client.event
async def on_ready():
    # thx nuke (https://discord.com/channels/1270835271948046497/1270835272397095075/1332769401077891225)
    for cogfile in cogs:
        try:
            await client.load_extension(cogfile)
        except Exception as e:
            log.error(e)
    
    await client.tree.sync()
    await client.change_presence(activity = discord.Game(f"{config['status']} || {config['default_prefix']}help"))
    log.info("Beep boop... Bot is ready")

client.run(os.environ["TOKEN"])