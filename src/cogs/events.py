import random
from nextcord.ext import commands
import nextcord.utils
import _helper as hp
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
        if not muted:  # If the muted role doesn't exist, return.
            return
        await channel.set_permissions(muted, send_messages=False, speak=False, request_to_speak=False, add_reactions=False)


    @commands.Cog.listener(name="on_message")
    async def afk_listener(self, message):
        """
        When a AFK member sends a message, remove them from AFK and remove '(AFK)' from their name.
        """
        if message.guild is None:
            return

        if message.author.id in afks.keys():
            afks.pop(message.author.id)
            try:
                await message.author.edit(nick=self._remove(message.author.display_name))

            except nextcord.Forbidden:
                await message.channel.send("I couldn't remove '(AFK)' from your name!")

            await message.channel.send(f"Welcome back {message.author.mention}, I removed your AFK.")

        for id, reason in afks.items():
            member = nextcord.utils.get(message.guild.members, id=id)
            if (message.reference and member == (await message.channel.fetch_message(message.reference.message_id)).author) or member in message.mentions:
                await message.reply(f"{member} is AFK: {reason}")


    @commands.Cog.listener(name="on_message")
    async def someone_listener(self, message):
        """
        When a member pings 'someone' role, all members from that role are removed and a random human member
        is assigned that role.
        """
        if message.guild is None:
            return

        role = nextcord.utils.get(message.guild.roles, name="someone")
        if role in message.role_mentions and message.author.bot is False:
            for member in role.members:
                await member.remove_roles(role)
                hp.logger.info(f"{member} no longer has the someone role.")
            someone = random.choice(message.guild.humans)
            hp.logger.info(f"{someone} now has the someone role.")
            await someone.add_roles(role)


def setup(bot):
    bot.add_cog(Events(bot))
