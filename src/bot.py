import os
import logging
import psycopg2
import nextcord
import nextcord.ext
from nextcord.ext import commands, application_checks
import db
import _helper as hp

intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("-"), intents=intents)
bot.db = db


def create_connection():
    connection = psycopg2.connect(
        host=hp.POSTGRESQL_HOST,
        database=hp.POSTGRESQL_DATABASE,
        user=hp.POSTGRESQL_USER,
        password=hp.POSTGRESQL_PASSWORD
    )
    return connection


bot.create_connection = create_connection
cogs = []


# Events
@bot.event
async def on_ready():
    print(f"----------\nLogged in as {bot.user}({bot.user.id}).\n----------")


@bot.event
async def on_application_command_error(interaction: nextcord.Interaction, error):
    """
    For hiding traceback
    """
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


bot.run(os.getenv("TOKEN"))
