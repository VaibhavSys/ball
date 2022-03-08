import nextcord
import nextcord.ext
import nextcord.utils
from nextcord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, ctx):
        for channel in ctx.guild.channels:
            muted = nextcord.utils.get(ctx.guild.roles, name="Muted")
            await channel.set_permissions(muted, send_messages=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message):
            await message.channel.send("You can type -help for more info.")


def setup(bot):
    bot.add_cog(Events(bot))
