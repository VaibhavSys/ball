import nextcord
from nextcord.ext import commands
from nextcord.utils import get
import asyncio

snipe_message_content = {}
snipe_message_author = {}
snipe_message_id = {}

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        global snipe_message_author
        global snipe_message_content
        global snipe_message_id

        snipe_message_content[message.channel.id] = message.content
        snipe_message_id[message.channel.id] = message.id
        snipe_message_author[message.channel.id] = message.author
        await asyncio.sleep(60)

        if message.id == snipe_message_id:
            snipe_message_author[message.channel.id] = None
            snipe_message_content[message.channel.id] = None
            snipe_message_id[message.channel.id] = None


    @commands.command()
    async def snipe(self, ctx):
        """
        Get the last deleted message in a channel.
        """
        global snipe_message_author
        global snipe_message_content
        global snipe_message_id

        try:
            embed = nextcord.Embed(title="Sniped that message!", colour=nextcord.Colour.blue())
            embed.description = snipe_message_content[ctx.channel.id]
            embed.add_field(name="Message ID", value=snipe_message_id)
            embed.set_author(name=snipe_message_author[ctx.channel.id], icon_url=snipe_message_author[ctx.channel.id].display_avatar.url)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=embed)

        except KeyError:
            embed = nextcord.Embed(title="Ran out of bullets.", colour=nextcord.Colour.blue())
            embed.description = "No message recently deleted found in this channel."
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Snipe(bot))