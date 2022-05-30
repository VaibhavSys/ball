import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, application_checks
import nextcord.utils
from afks import afks


class Info(commands.Cog):
    """
    Get information about stuff.
    """

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    async def ping(
        self,
        interaction: nextcord.Interaction
    ):
        """
        Get the latency of the bot.
        """
        await interaction.send(f'Pong! {round (self.bot.latency * 1000)} ms')

    @nextcord.slash_command()
    @application_checks.guild_only()
    async def userinfo(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True)
    ):
        """
        Get information about a member.
        """
        member = member or interaction.user
        joined_at = member.joined_at.strftime("%d %B %Y, %I:%M %p")
        created_at = member.created_at.strftime("%d %B %Y, %I:%M %p")

        embed = nextcord.Embed(
            title=f"UserInfo of {member}",
            colour=nextcord.Colour.green()
            )
        embed.set_footer(
            text=f"Requested by {interaction.user}",
            icon_url=interaction.user.display_avatar
            )
        embed.set_image(url=member.display_avatar.url)
        if member.banner is not None:
            embed.set_thumbnail(url=member.banner)
        embed.add_field(name="Colour", value=member.colour)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Account Creation Time", value=created_at)
        embed.add_field(name="Guild Join Time", value=joined_at)
        embed.add_field(name="Bot", value=member.bot)
        embed.add_field(name="Discord Representative", value=member.system)
        embed.add_field(name="Top Role", value=member.top_role.mention)
        await interaction.send(embed=embed)

    @nextcord.slash_command()
    async def guildinfo(self, interaction: nextcord.Interaction):
        """
        Get information about the guild.
        """
        humans = 0
        bots = 0

        for human in interaction.guild.humans:
            humans += 1

        for bot in interaction.guild.bots:
            bots += 1

        embed = nextcord.Embed(
            title=f"Guild info of {interaction.guild.name}",
            colour=nextcord.Colour.green())
        embed.set_footer(
            text=f"Requested by {interaction.user}",
            icon_url=interaction.user.display_avatar.url)
        if interaction.guild.icon is not None:

            embed.set_image(url=interaction.guild.icon.url)
        if interaction.guild.banner is not None:
            embed.set_thumbnail(url=interaction.guild.banner)
        embed.add_field(name="Owner", value=interaction.guild.owner)
        embed.add_field(name="ID", value=interaction.guild.id)
        embed.add_field(name="Total Members", value=interaction.guild.member_count)
        embed.add_field(name="Humans", value=humans)
        embed.add_field(name="Bots", value=bots)
        embed.add_field(name="Creation Time", value=interaction.guild.created_at.strftime("%d %B %Y, %I:%M %p"))
        embed.add_field(name="Verification Level", value=interaction.guild.verification_level)
        await interaction.send(embed=embed)

    @nextcord.slash_command()
    async def afk(
        self,
        interaction: nextcord.Interaction,
        *,
        reason="Not provided."
    ):
        """
        Go afk and optionally provide a reason.
        """
        member = interaction.user
        if member.id in afks.keys():
            afks.pop(member.id)
        else:
            try:
                await member.edit(nick=f"(AFK) {member.display_name}")

            except:
                pass

        afks[member.id] = reason
        embed = nextcord.Embed(title=":zzz: Member AFK", description=f"{member} is AFK right now.", color=member.color)
        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name="AFK Note: ", value=reason)
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
