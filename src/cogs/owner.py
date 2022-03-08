from nextcord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.is_owner()
    # async def list_cogs(self, ctx):
        # await ctx.send(self.)


def setup(bot):
    bot.add_cog(Owner(bot))
