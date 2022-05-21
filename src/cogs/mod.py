import nextcord
import nextcord.utils
from nextcord.ext import commands, application_checks
from datetime import timedelta
from nextcord import SlashOption


class Mod(commands.Cog):
    """
    Moderate your guild with these mighty commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(manage_roles=True))
    @application_checks.guild_only()
    async def role(
        self,
        interaction: nextcord.Interaction,
        ):
        """
        Main command for other role sub-commands.
        """
        pass


    @role.subcommand()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(manage_roles=True))
    @application_checks.guild_only()
    async def add(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        role: nextcord.Role = SlashOption(required=True)
        ):
        await member.add_roles(role)
        await interaction.send(f"{member} has been given the role {role}({role.id}) by {interaction.user}({interaction.user.id})")


    @role.subcommand()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(manage_roles=True))
    @application_checks.guild_only()
    async def remove(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        role: nextcord.Role = SlashOption(required=True)
        ):
        """
        Remove a role from a member.
        """
        await member.remove_roles(role)
        await interaction.send(f"{member} has been removed from {role.name}({role.id}) role by {interaction.user}({interaction.user.id})")


    @nextcord.slash_command(description="Timeout a member.")
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(moderate_members=True))
    @application_checks.guild_only()
    async def timeout(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        time: str = SlashOption(required=False),
        *,
        reason: str = SlashOption(required=False)
        ):
        """
        Use the discord timeout feature to timeout a member, max time is 1 week.
        """
        unit = ""

        if not time:
            time = 10
        else:
            unit = time[-1]
            time = int(time[:-1])

        if unit == "":
            unit = "m"

        if unit == "s" and time < 604800:
            delta = timedelta(seconds=time)
        elif unit == "m" and time < 10080:
            delta = timedelta(minutes=time)
        elif unit == "h" and time < 168:
            delta = timedelta(hours=time)
        elif unit == "d" and time < 7:
            delta = timedelta(days=time)
        elif unit == "w" and time < 1:
            delta = timedelta(weeks=time)
        else:
            return await interaction.send("Invalid time/unit or time is more than 1 week.")

        await member.edit(timeout=delta, reason=reason)
        await interaction.send(f"{member} has been timed out by {interaction.user}({interaction.user.id}) with reason '{reason}' for {f'{time}{unit}'}.")


    @nextcord.slash_command(description="Traditonal mute a member.")
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True))
    @application_checks.guild_only()
    async def tmute(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        *,
        reason: str = SlashOption(required=False)
        ):
        """
        Traditional mute a user by adding a muted role with no permissions to send messages,
        speak in voice channels, react to messages and requesting to join stages.
        """
        muted = nextcord.utils.get(interaction.guild.roles, name="Muted")

        if not muted:
            muted = await interaction.guild.create_role(name="Muted", reason="Used for muting.")
            for channel in interaction.guild.channels:
                await channel.set_permissions(muted, send_messages=False, speak=False, request_to_speak=False, add_reactions=False)

        await member.add_roles(muted)
        await interaction.send(f"{member} has been muted by {interaction.user}({interaction.user.id}) with reason '{reason}'.")


    @nextcord.slash_command()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(moderate_members=True))
    @application_checks.guild_only()
    async def unmute(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        *,
        reason: str = SlashOption(required=False)
        ):
        """
        Remove a member from timeout.
        """
        await member.edit(timeout=None, reason=reason)
        await interaction.send(f"{member} has been removed from timeout by {interaction.user}({interaction.user.id}) with reason '{reason}'.")

    @nextcord.slash_command(description="Traditonal unmute a member.")
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True))
    @application_checks.guild_only()
    async def tunmute(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        *,
        reason: str = SlashOption(required=False)
        ):
        """
        Traditional unmute, unmute a member muted by traditional mute.
        """
        muted = nextcord.utils.get(interaction.guild.roles, name="Muted")
        await member.remove_roles(muted)
        await interaction.send(f"{member} has been unmuted by {interaction.user}({interaction.user.id}) with reason '{reason}'.")


    @nextcord.slash_command()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(kick_members=True))
    @application_checks.guild_only()
    async def kick(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        *,
        reason: str = SlashOption(required=False)
        ):
        """
        Kick a member from the guild.
        """
        await member.kick(reason=reason)
        await interaction.send(f"{member}({member.id}) has kicked by {interaction.user}({interaction.user.id}) with reason '{reason}'.")


    @nextcord.slash_command()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(ban_members=True))
    @application_checks.guild_only()
    async def ban(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        *,
        reason: str = SlashOption(required=False)
        ):
        """
        Ban a member from the guild.
        """
        await member.ban(reason=reason)
        await interaction.send(f"{member}({member.id}) has been banned by {interaction.user}({interaction.user.id}) with reason '{reason}'.")


    @nextcord.slash_command()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(ban_members=True))
    @application_checks.guild_only()
    async def unban(
        self,
        interaction: nextcord.Interaction,
        member: str = SlashOption(required=True),
        *,
        reason: str = SlashOption(required=False)
        ):
        """
        Unban a previously banned member from the guild.
        """
        banned_users = await interaction.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (
                    member_name, member_discriminator):
                await interaction.guild.unban(user, reason=reason)
                await interaction.send(f"{user.name}#{user.discriminator} has been unbanned by {interaction.user}({interaction.user.id}) with reason '{reason}'.")


    @nextcord.slash_command(description="Lock a channel.")
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True))
    @application_checks.guild_only()
    async def lock(
        self,
        interaction: nextcord.Interaction,
        channel: str = SlashOption(required=False)
        ):
        """
        Lock a channel, restrict sending messages permission to @everyone role.
        """
        channel = nextcord.utils.get(interaction.guild.text_channels, name=channel) or interaction.channel
        overwrites = channel.overwrites_for(interaction.guild.default_role)
        overwrites.send_messages = False
        await channel.set_permissions(interaction.guild.default_role, overwrite=overwrites)
        await interaction.send(f'{channel.mention} locked.')


    @lock.on_autocomplete("channel")
    async def lock_autocomplete(
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


    @nextcord.slash_command()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True))
    @application_checks.guild_only()
    async def unlock(
        self,
        interaction: nextcord.Interaction,
        channel: str = SlashOption(required=False)
        ):
        """
        Unlock a previously locked channel.
        """
        channel = nextcord.utils.get(interaction.guild.text_channels, name=channel) or interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = None
        await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.send(f'{channel.mention} unlocked.')


    @unlock.on_autocomplete("channel")
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


    @nextcord.slash_command()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True))
    @application_checks.guild_only()
    async def purge(
        self,
        interaction: nextcord.Interaction,
        limit: int = SlashOption(required=True)
        ):
        """
        Delete messages in bulk.
        """
        await interaction.channel.purge(limit=limit)
        await interaction.send(f"Purged {limit} messages.", delete_after=2)


    @nextcord.slash_command()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True))
    @application_checks.guild_only()
    async def slowmode(
        self,
        interaction: nextcord.Interaction,
        interval: int = SlashOption(required=False),
        unit: str = SlashOption(required=False)
        ):
        """Changes channel's slowmode setting.
        Use without parameters to disable.
        """
        if unit is None:
            unit = "s"

        if unit == "s":
            interval = timedelta(seconds=interval).total_seconds()
        elif unit == "m":
            interval = timedelta(minutes=interval).total_seconds()

        await interaction.channel.edit(slowmode_delay=interval)
        if interval > 0:
            await interaction.send(f"Slowmode interval is now {interval}.")
        else:
            await interaction.send("Slowmode has been disabled.")

    @nextcord.slash_command()
    @application_checks.check_any(application_checks.is_owner(),
        application_checks.has_permissions(manage_nicknames=True))
    @application_checks.guild_only()
    async def setnick(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        *,
        nick: str = SlashOption(required=True)
        ):
        """
        Change a member's nickname.
        """
        previous_nick = member.display_name
        await member.edit(nick=nick)
        await interaction.send(f"{interaction.user}({interaction.user.id}) changed {member}\'s nickname from \'{previous_nick}\' to '{nick}'. ")


def setup(bot):
    bot.add_cog(Mod(bot))
