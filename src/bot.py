import nextcord
import os
import nextcord.ext
from nextcord.ext import commands, application_checks
import logging
import _helper as hp
from os import getenv

intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("-"), intents=intents)
cogs = []


"""
Events
"""
@bot.event
async def on_ready():
    print(f"----------\nLogged in as {bot.user}({bot.user.id}).\n----------")

@bot.slash_command()
@application_checks.guild_only()
@application_checks.bot_has_permissions(manage_messages=True, manage_roles=True)
@application_checks.check_any(application_checks.has_permissions(administrator=True))
async def test(interaction: nextcord.Interaction):
    await interaction.send("Success.")


@bot.slash_command()
@application_checks.dm_only()
@application_checks.has_permissions(manage_messages=True)
async def test2(interaction: nextcord.Interaction):
    await interaction.send("Success")

@bot.event
async def on_application_command_error(interaction: nextcord.Interaction, error):
    pass

for file in os.listdir("./src/cogs"):
    """
    Load all cogs in cogs directory.
    """
    if file.endswith(".py"):
        name = file[:-3]
        cog = f"cogs.{name}"
        cogs.append(cog)
        bot.load_extension(cog)
        print(f"Loaded cog {name}.")


bot.run(getenv("TOKEN"))
