import nextcord.ext
import nextcord.utils
from nextcord.ext import commands
from afks import afks


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _remove(self, name):
        """
        For AFK command, removes the AFK from name and returns the previous nickname of member
        """
        
        if "(AFK)" in name.split():
            return " ".join(name.split()[1:])

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """
        For traditional mute.
        Every time a channel is created, restrict 'Muted' role from sending messages,
        speak in voice channels, react to messages and requesting to join stages.
        """

        muted = nextcord.utils.get(channel.guild.roles, name="Muted")
        if not muted: # If the muted role doesn't exist, return.
            return

        await channel.set_permissions(muted, send_messages=False, speak=False, request_to_speak=False, add_reactions=False)


    @commands.Cog.listener()
    async def on_message(self, message):
        """
        When a AFK member sends a message, remove them from AFK and remove '(AFK)' from thier name.
        """

        if message.author.id in afks.keys():
            afks.pop(message.author.id)
            try:
                await message.author.edit(nick=self._remove(message.author.display_name))

            except nextcord.Forbidden:
                await message.channel.send("I couldn't remove '(AFK)' from your name!")

            await message.channel.send(f"Welcome back {message.author.mention}, I removed your AFK.")

        for id, reason in afks.items():
            member = nextcord.utils.get(message.guild.members, id = id)
            if (message.reference and member == (await message.channel.fetch_message(message.reference.message_id)).author) or member.id in message.raw_mentions:
                await message.reply(f"{member} is AFK: {reason}")


def setup(bot):
    bot.add_cog(Events(bot))
