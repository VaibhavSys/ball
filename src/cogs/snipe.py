import nextcord
from nextcord.ext import commands
from nextcord.utils import get
import asyncio

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    snipe_message_content = None
    snipe_message_author = None
    snipe_message_id = None

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        global snipe_message_author
        global snipe_message_content
        global snipe_message_id

        snipe_message_content = message.content
        snipe_message_id = message.id
        snipe_message_author = message.author
        await asyncio.sleep(60)

        if message.id == snipe_message_id:
            snipe_message_author = None
            snipe_message_content = None
            snipe_message_id = None


    @commands.command()
    async def snipe(self, ctx):
        global snipe_message_author
        global snipe_message_content
        global snipe_message_id

        embed = nextcord.Embed(title="Sniped that message!", colour=nextcord.Colour.blue())
        embed.description = snipe_message_content
        embed.set_author(name=snipe_message_author, icon_url=snipe_message_author.display_avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Snipe(bot))