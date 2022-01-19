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
client = nextcord.Client()
client = commands.Bot(command_prefix = '-') #put your own prefix here

@client.event
async def on_ready():
    print("Bot is online.") 
    
    
@client.command()
async def ping(ctx):
    await ctx.send("pong!") 

@client.command()
async def kick(ctx, member: nextcord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has kicked.')

@client.command()
async def sayhi(ctx):
  await ctx.send("Hello! I am a helikopter which will take you whereever you want.")

@client.command()
async def joke(ctx):
    url = 'https://api.chucknorris.io/jokes/random'
    response = requests.get(url)
    o = json.loads(response.text)
    await ctx.send(o["value"])
#The below code bans player.
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : nextcord.Member, *, reason = None):
    await member.ban(reason = reason)

#The below code unbans player.
@client.command()
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

@client.command()
async def addrole(ctx, user: nextcord.Member, role: nextcord.Role):
    await user.add_roles(role)
    await ctx.send(f"hey {ctx.author.name}, {user.name} has been giving a role called: {role.name}")

@client.command()
async def rmrole(ctx, user: nextcord.Member, role: nextcord.Role):
    await user.remove_roles(role)
    await ctx.send(f"hey {ctx.author.name}, {user.name} has been removed from a role called: {role.name}")

@client.command()
@commands.is_owner()
async def shutdown(ctx):
    print("Shutting down bot...")
    await client.close()

keep_alive.keep_alive()
client.run(TOKEN) 

