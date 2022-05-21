import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, application_checks


class ModVC(commands.Cog):
    """
    Moderation commands related to voice channels.
    """
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_guild_permissions(mute_members=True))
    @application_checks.guild_only()
    async def voice(self, interaction: nextcord.Interaction):
        """
        Main command for other voice mod subcommands.
        """
        pass


    @voice.subcommand()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_guild_permissions(mute_members=True))
    @application_checks.guild_only()
    async def mute(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        *,
        reason: str = SlashOption(required=False)
        ):
        await member.edit(mute=True, reason=reason)
        await interaction.send(f"{member} has been successfully voice-muted by {interaction.user.mention} with reason '{reason}'")


    @voice.subcommand()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_guild_permissions(mute_members=True))
    @application_checks.guild_only()
    async def unmute(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        *,
        reason: str = SlashOption(required=False)
        ):
        """
        Voice unmute a member so that they can talk in a voice channel again.
        """
        await member.edit(mute=False, reason=reason)
        await interaction.send(f"{member} has been successfully voice-unmuted by {interaction.user.mention} with reason '{reason}'")


    @voice.subcommand()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_guild_permissions(mute_members=True))
    @application_checks.guild_only()
    async def deafen(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        *,
        reason: str = SlashOption(required=False)
        ):
        """
        Deafen a member so that they cannot hear anything in a voice channel.
        """
        await member.edit(deafen=True, reason=reason)
        await interaction.send(f"{member} has been deafened by {interaction.user.mention} with reason '{reason}.'")


    @voice.subcommand()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_guild_permissions(mute_members=True))
    @application_checks.guild_only()
    async def undeafen(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        *,
        reason: str = SlashOption(required=False)
        ):
        """
        Undeafen a member so that they can hear in a voice channel again.
        """
        await member.edit(deafen=False, reason=reason)
        await interaction.send(f"{member} has been undeafened by {interaction.user.mention} with reason '{reason}.'")


def setup(bot):
    bot.add_cog(ModVC(bot))