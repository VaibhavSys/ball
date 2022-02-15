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
#import keep_alive

TOKEN = os.environ['TOKEN']
bot = commands.Bot(command_prefix = '-')
 
#Logging Setup
logger = logging.getLogger('nextcord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    print(f"----------\nLogged in as {bot.user.name}({bot.user.id})\n----------") 

    
# @bot.command()
# async def ping(ctx):
    # await ctx.send(f'Pong! {round (bot.latency * 1000)} ms')

@bot.command()
async def sayhi(ctx):
  await ctx.send("Hello! I am a helikopter which will take you whereever you want.")

@bot.command()
async def joke(ctx):
    url = 'https://api.chucknorris.io/jokes/random'
    response = requests.get(url)
    o = json.loads(response.text)
    await ctx.send(o["value"])

@commands.has_permissions(administrator = True)


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    print("Shutting down bot...")
    await bot.close()

for file in os.listdir("./cogs"): 
    if file.endswith(".py"): 
        name = file[:-3] 
        bot.load_extension(f"cogs.{name}")
#keep_alive.keep_alive()        
bot.run(TOKEN) 

