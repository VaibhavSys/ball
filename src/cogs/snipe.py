import nextcord
from nextcord.ext import commands, application_checks
import nextcord.utils
import asyncio
from nextcord import SlashOption

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
        snipe_message_author[message.channel.id] = None
        snipe_message_content[message.channel.id] = None
        snipe_message_id[message.channel.id] = None


    @nextcord.slash_command()
    async def snipe(
        self,
        interaction: nextcord.Interaction,
        channel: str = SlashOption(required=False)
        ):
        """
        Get the last deleted message in a channel.
        """
        global snipe_message_author
        global snipe_message_content
        global snipe_message_id
        channel = nextcord.utils.get(interaction.guild.text_channels, name=channel) or interaction.channel

        try:
            embed = nextcord.Embed(title="Sniped that message!", colour=nextcord.Colour.blue())
            embed.description = snipe_message_content[channel.id]
            embed.add_field(name="Message ID", value=snipe_message_id[channel.id])
            embed.set_author(name=snipe_message_author[channel.id], icon_url=snipe_message_author[channel.id].display_avatar.url)
            embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
            await interaction.send(embed=embed)

        except KeyError:
            embed = nextcord.Embed(title="Ran out of bullets.", colour=nextcord.Colour.blue())
            embed.description = f"No message recently deleted found in {channel}."
            embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.display_avatar.url)
            await interaction.send(embed=embed)


    @snipe.on_autocomplete("channel")
    async def snipe_autocomplete(
        self,
        interaction: nextcord.Interaction,
        channel: str
        ):
        text_channels = []
        for channel in interaction.guild.text_channels:
            text_channels.append(channel.name)

        if not channel:
            await interaction.response.send_autocomplete(text_channels)
            return

        get_near_channel = [
        channel for channel in text_channels if channel.lower().startswith(channel.lower())
        ]
        await interaction.response.send_autocomplete(get_near_channel)


def setup(bot):
    bot.add_cog(Snipe(bot))