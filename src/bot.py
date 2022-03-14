import nextcord
import os
import nextcord.ext
from nextcord.ext import commands
import logging
#import keep_alive
from os import getenv

intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="-", intents=intents)
cogs = []


# Logging Setup
logger = logging.getLogger('nextcord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='nextcord.log', encoding='utf-8', mode='w'
)

handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
)
logger.addHandler(handler)


# Events
@bot.event
async def on_connect():
    print("----------\nConnected successfully.\n----------")


@bot.event
async def on_ready():
    print(f"----------\nLogged in as {bot.user}({bot.user.id}).\n----------")


@bot.event
async def on_disconnect():
    print("Disconnected.")

for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        cog = f"cogs.{name}"
        cogs.append(cog)
        bot.load_extension(cog)
        print(f"Loaded cog {name}.")


#keep_alive.keep_alive()
bot.run(getenv("TOKEN"))
