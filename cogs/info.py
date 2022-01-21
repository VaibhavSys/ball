import nextcord.ext
import nextcord.utils 
from nextcord.ext import commands, tasks

bot = commands.Bot(command_prefix = '-')

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def info(self, ctx):
        await ctx.send("Smacking Sweats!")
    

    
def setup(bot):
    bot.add_cog(Info(bot))
