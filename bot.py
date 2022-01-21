import keep_alive
import requests
import nextcord
import os
import time
import nextcord.ext
from nextcord.utils import get
from nextcord.ext import commands, tasks
from nextcord.ext.commands import has_permissions,  CheckFailure, check
import json

TOKEN = os.environ['TOKEN']
bot = commands.Bot(command_prefix = '-') #put your own prefix here

@bot.event
async def on_ready():
    print("Bot is online.") 

    
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round (bot.latency * 1000)} ms')

@bot.command()
async def sayhi(ctx):
  await ctx.send("Hello! I am a helikopter which will take you whereever you want.")

@bot.command()
async def joke(ctx):
    url = 'https://api.chucknorris.io/jokes/random'
    response = requests.get(url)
    o = json.loads(response.text)
    await ctx.send(o["value"])
#The below code bans player.
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : nextcord.Member, *, reason = None):
    await member.ban(reason = reason)

#The below code unbans player.
@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


@bot.command()
async def rmrole(ctx, user: nextcord.Member, role: nextcord.Role):
    await user.remove_roles(role)
    await ctx.send(f"hey {ctx.author.name}, {user.name} has been removed from a role called: {role.name}")

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    print("Shutting down bot...")
    await bot.close()

for file in os.listdir("./cogs"): 
    if file.endswith(".py"): 
        name = file[:-3] 
        bot.load_extension(f"cogs.{name}")
        
keep_alive.keep_alive()
bot.run(TOKEN) 

