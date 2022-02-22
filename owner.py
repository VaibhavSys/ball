import nextcord.ext
import nextcord.utils
from nextcord.ext import commands, tasks
import keep_alive

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Owner(bot))
