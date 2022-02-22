import requests
import nextcord
import os
import time
import nextcord.ext
from nextcord.utils import get
from nextcord.ext import commands, tasks
from nextcord.ext.commands import has_permissions,  CheckFailure, check
import json
import logging
from sys import argv
from dotenv import load_dotenv
import keep_alive

#PRESTART 
try:
    load_dotenv()
except: 
    print(".env file not found.")

try:
    arg = argv[1]
    os.system("git remote add origin https://github.com/MouseMoosz/pengoon-bot.git && git fetch && git pull")
    if arg:
        os.system(f"git fetch && git pull origin {arg}")
    else:
        os.system("git fetch && git pull")
except:
    print("Unable to auto-update, manual update needed")
    
#PRESTART END
    
intents = nextcord.Intents.default()
intents.members = True
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix = '-', intents=intents)

#Logging Setup
logger = logging.getLogger('nextcord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    print(f"----------\nLogged in as {bot.user.name}({bot.user.id})\n----------") 


for file in os.listdir("./cogs"): 
    if file.endswith(".py"): 
        name = file[:-3] 
        bot.load_extension(f"cogs.{name}")
        print(f"Loaded cog {name}")
        
keep_alive.keep_alive()
bot.run(TOKEN) 

