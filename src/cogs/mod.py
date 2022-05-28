import datetime
import time
import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, application_checks
import nextcord.utils


class Mod(commands.Cog):
    """
    Moderate your guild with these mighty commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(manage_roles=True)
    )
    @application_checks.guild_only()
    async def role(
        self,
        interaction: nextcord.Interaction,
    ):
        """
        The main command for other role subcommands.
        """
        pass

    @role.subcommand()
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(manage_roles=True)
        )
    @application_checks.guild_only()
    async def add(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        role: nextcord.Role = SlashOption(required=True)
    ):
        """
        Add a role to a member.
        """
        if (interaction.user.top_role < role):
            return await interaction.send(f"{role.name} is higher than you in role hierarchy.")
        elif (interaction.user.top_role > member.top_role) is False:
            return await interaction.send(f"You are lower than {member} in role hierarchy.")
        elif (interaction.user.top_role > role) is False:
            return await interaction.send(f"Your top role is lower than {role.name}.")

        await member.add_roles(role)
        await interaction.send(f"{member} has been given the role \'{role.name}\'.")

    @role.subcommand()
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(manage_roles=True)
    )
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
        if (interaction.user.top_role < role):
            return await interaction.send(f"{role.name} is higher than you in role hierarchy.")
        elif (interaction.user.top_role > member.top_role) is False:
            return await interaction.send(f"You are lower than {member} in role hierarchy.")
        elif (interaction.user.top_role > role) is False:
            return await interaction.send(f"Your top role is lower than {role.name}.")

        await member.remove_roles(role)
        await interaction.send(f"{member} has been removed from role \'{role.name}\'")

    @nextcord.slash_command(description="Timeout a member.")
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(moderate_members=True)
        )
    @application_checks.guild_only()
    async def mute(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        time: str = SlashOption(required=False),
        reason: str = SlashOption(required=False)
    ):
        """
        Use the discord timeout feature to timeout a member, max time is 1 week.
        """
        if (interaction.user == member):
            return await interaction.send("You cannot issue yourself a mute.")
        elif (interaction.guild.owner == member):
            return await interaction.send("You cannot issue the guild owner a mute.")
        elif interaction.user.top_role == member.top_role:
            return await interaction.send(f"You are equal to {member} in role hierarchy")
        elif (interaction.user.top_role > member.top_role) is False:
            return await interaction.send(f"You are lower than {member} in role hierarchy.")

        unit = ""

        if not time:
            time = 10
        else:
            unit = time[-1]
            time = int(time[:-1])

        if unit == "":
            unit = "m"

        if unit == "s" and time < 604800:
            delta = datetime.timedelta(seconds=time)
        elif unit == "m" and time < 10080:
            delta = datetime.timedelta(minutes=time)
        elif unit == "h" and time < 168:
            delta = datetime.timedelta(hours=time)
        elif unit == "d" and time < 7:
            delta = datetime.timedelta(days=time)
        elif unit == "w" and time < 1:
            delta = datetime.timedelta(weeks=time)
        else:
            return await interaction.send("Invalid time/unit or time is more than 1 week.")

        await member.edit(timeout=delta, reason=reason)
        await interaction.send(f"{member} has been timed out with reason \'{reason}\' for {f'{time}{unit}'}.")

    @nextcord.slash_command(description="Traditonal mute a member.")
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True)
    )
    @application_checks.guild_only()
    async def tmute(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        reason: str = SlashOption(required=False)
    ):
        """
        Traditional mute a user by adding a muted role with no permissions to send messages,
        speak in voice channels, react to messages and requesting to join stages.
        """
        if (interaction.user == member):
            return await interaction.send("You cannot issue yourself a mute.")
        elif (interaction.guild.owner == member):
            return await interaction.send("You cannot issue the guild owner a mute.")
        elif interaction.user.top_role == member.top_role:
            return await interaction.send(f"You are equal to {member} in role hierarchy")
        elif (interaction.user.top_role > member.top_role) is False:
            return await interaction.send(f"You are lower than {member} in role hierarchy.")
        
        muted = nextcord.utils.get(interaction.guild.roles, name="Muted")
        if not muted:
            muted = await interaction.guild.create_role(
                name="Muted",
                reason="Used for muting."
            )
            for channel in interaction.guild.channels:
                await channel.set_permissions(
                    muted,
                    send_messages=False,
                    speak=False,
                    request_to_speak=False,
                    add_reactions=False
                )

        await member.add_roles(muted)
        await interaction.send(f"{member} has been muted with reason \'{reason}\'.")

    @nextcord.slash_command()
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(moderate_members=True)
    )
    @application_checks.guild_only()
    async def unmute(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        reason: str = SlashOption(required=False)
    ):
        """
        Remove a member from timeout.
        """
        if (interaction.user == member):
            return await interaction.send("You cannot unmute yourself.")
        elif (interaction.guild.owner == member):
            return await interaction.send("You cannot issue the guild owner a unmute.")
        elif interaction.user.top_role == member.top_role:
            return await interaction.send(f"You are equal to {member} in role hierarchy")
        elif (interaction.user.top_role > member.top_role) is False:
            return await interaction.send(f"You are lower than {member} in role hierarchy.")

        await member.edit(timeout=None, reason=reason)
        await interaction.send(f"{member} has been removed from timeout with reason \'{reason}\'.")

    @nextcord.slash_command(description="Traditonal unmute a member.")
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True)
        )
    @application_checks.guild_only()
    async def tunmute(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        reason: str = SlashOption(required=False)
    ):
        """
        Traditional unmute, unmute a member muted by traditional mute.
        """
        if (interaction.user == member):
            return await interaction.send("You cannot unmute yourself.")
        elif (interaction.guild.owner == member):
            return await interaction.send("You cannot issue the guild owner a unmute.")
        elif interaction.user.top_role == member.top_role:
            return await interaction.send(f"You are equal to {member} in role hierarchy")
        elif (interaction.user.top_role > member.top_role) is False:
            return await interaction.send(f"You are lower than {member} in role hierarchy.")

        muted = nextcord.utils.get(interaction.guild.roles, name="Muted")
        await member.remove_roles(muted)
        await interaction.send(f"{member} has been unmuted with reason \'{reason}\'.")

    @nextcord.slash_command()
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(kick_members=True)
    )
    @application_checks.guild_only()
    async def kick(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        reason: str = SlashOption(required=False)
    ):
        """
        Kick a member from the guild.
        """
        if interaction.user == member:
            return await interaction.send("You cannot issue yourself a kick.")
        elif (interaction.guild.owner == member):
            return await interaction.send("You cannot issue the guild owner a kick.")
        elif interaction.user.top_role == member.top_role:
            return await interaction.send(f"You are equal to {member} in role hierarchy")
        elif (interaction.user.top_role > member.top_role) is False:
            return await interaction.send(f"You are lower than {member} in role hierarchy.")

        await member.kick(reason=reason)
        await interaction.send(f"{member}({member.id}) has kicked with reason '{reason}'.")

    @nextcord.slash_command()
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(ban_members=True)
    )
    @application_checks.guild_only()
    async def ban(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        reason: str = SlashOption(required=False)
    ):
        """
        Ban a member from the guild.
        """
        if interaction.user == member:
            return await interaction.send("You cannot issue yourself a ban.")
        elif (interaction.guild.owner == member):
            return await interaction.send("You cannot issue the guild owner a ban.")
        elif interaction.user.top_role == member.top_role:
            return await interaction.send(f"You are equal to {member} in role hierarchy")
        elif (interaction.user.top_role > member.top_role) is False:
            return await interaction.send(f"You are lower than {member} in role hierarchy.")

        await member.ban(reason=reason)
        await interaction.send(f"{member} ({member.id}) has been banned with reason \'{reason}\'.")

    @nextcord.slash_command()
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(ban_members=True)
        )
    @application_checks.guild_only()
    async def unban(
        self,
        interaction: nextcord.Interaction,
        member: str = SlashOption(required=True),
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
                    member_name, member_discriminator
            ):
                await interaction.guild.unban(user, reason=reason)
                await interaction.send(f"{user.name}#{user.discriminator} has been unbanned with reason \'{reason}\'.")

    @nextcord.slash_command(description="Lock a channel.")
    @application_checks.check_any(
        application_checks.is_owner(),
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
        await channel.set_permissions(
            interaction.guild.default_role,
            overwrite=overwrites
            )
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
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True)
        )
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
        await channel.set_permissions(
            interaction.guild.default_role, overwrite=overwrite
        )
        await interaction.send(f'{channel.mention} unlocked.')

    @unlock.on_autocomplete("channel")
    async def unlock_autocomplete(
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
            channel for channel in text_channels if channel.lower().startswith(
                channel.lower()
                )
        ]
        await interaction.response.send_autocomplete(get_near_channel)

    @nextcord.slash_command()
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True)
    )
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
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True)
        )
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
            interval = datetime.timedelta(seconds=interval).total_seconds()
        elif unit == "m":
            interval = datetime.timedelta(minutes=interval).total_seconds()

        await interaction.channel.edit(slowmode_delay=interval)
        if interval > 0:
            await interaction.send(f"Slowmode interval is now {interval}.")
        else:
            await interaction.send("Slowmode has been disabled.")

    @nextcord.slash_command()
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(manage_nicknames=True)
    )
    @application_checks.guild_only()
    async def setnick(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        nick: str = SlashOption(required=True)
    ):
        """
        Change a member's nickname.
        """
        if interaction.user.top_role == member.top_role:
            return await interaction.send(f"You are equal to {member} in role hierarchy")
        elif (interaction.guild.owner == member):
            return await interaction.send("You cannot change the nickname for the guild owner.")
        elif (interaction.user.top_role > member.top_role) is False:
            return await interaction.send(f"You are lower than {member} in role hierarchy.")

        previous_nick = member.display_name
        await member.edit(nick=nick)
        await interaction.send(f"{interaction.user}({interaction.user.id}) changed {member}\'s nickname from \'{previous_nick}\' to '{nick}'. ")

    @nextcord.slash_command(guild_ids=[923519688871411732, 975659726052413520])
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True)
        )
    @application_checks.guild_only()
    async def warn(
        self,
        interaction: nextcord.Interaction
    ):
        """
        The main command for other warn subcommands.
        """
        pass

    @warn.subcommand(name="add")
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True)
        )
    @application_checks.guild_only()
    async def add_warn(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True),
        reason: str = SlashOption(required=False)
    ):
        """
        Add a warning to a member in the guild.
        """
        if interaction.user == member:
            return await interaction.send("You cannot issue yourself a warning.")
        elif (interaction.guild.owner == member):
            return await interaction.send("You cannot issue the guild owner a warning.")
        elif interaction.user.top_role == member.top_role:
            return await interaction.send(f"You are equal to {member} in role hierarchy")
        elif (interaction.user.top_role > member.top_role) is False:
            return await interaction.send(f"You are lower than {member} in role hierarchy.")

        await interaction.response.defer()
        cursor = self.bot.create_connection().cursor()
        warn_id = self.bot.db.add_warn(
            cursor,
            member.id,
            interaction.user.id,
            interaction.guild.id,
            time.time(), reason
        )
        cursor.close()
        cursor.connection.commit()
        cursor = self.bot.create_connection().cursor()
        warn_count = self.bot.db._warn_count(
            cursor,
            member.id,
            interaction.guild.id
        )
        await interaction.send(f"Warned {member} for \'{reason}\'. This is their warning {warn_count}.")
        cursor.close()
        cursor.connection.commit()

    @warn.subcommand(name="remove")
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True)
        )
    @application_checks.guild_only()
    async def remove_warn(
        self,
        interaction: nextcord.Interaction,
        warn_id: int = SlashOption(required=True)
    ):
        """
        Remove a warning from a member in the guild.
        """
        await interaction.response.defer()
        cursor = self.bot.create_connection().cursor()
        cursor.execute(f"SELECT user_id FROM warns WHERE warn_id = {warn_id};")
        member_id = cursor.fetchone()
        member = nextcord.utils.get(interaction.guild.members, id=member_id)

        if (interaction.user == member):
            return await interaction.send("You cannot remove a warning from yourself.")
        elif (interaction.guild.owner == member):
            return await interaction.send("You cannot remove a warning from the guild owner..")
        elif (interaction.user.top_role == member.top_role):
            return await interaction.send(f"You are equal to {member} in role hierarchy.")
        elif (interaction.user.top_role > member.top_role) is False:
            return await interaction.send(f"You are lower than {member} in role hierarchy.")

        remove_warn = self.bot.db.remove_warn(
            cursor, warn_id, interaction.guild.id
            )
        if remove_warn == "InvalidWarn":
            return await interaction.send(f"Invalid Warn ID #{warn_id}.")
        elif remove_warn == "GuildNoMatch":
            return await interaction.send(f"Warning #{warn_id} was not issued in this guild.")

        await interaction.send(f"Removed warn #{warn_id}.")
        cursor.close()
        cursor.connection.commit()

    @warn.subcommand(name="list")
    @application_checks.check_any(
        application_checks.is_owner(),
        application_checks.has_permissions(manage_messages=True)
        )
    @application_checks.guild_only()
    async def list_warns(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member = SlashOption(required=True)
    ):
        """
        List all the warns of a member in the guild.
        """
        await interaction.response.defer()
        cursor = self.bot.create_connection().cursor()
        member_warns = self.bot.db.list_warns(
            cursor,
            member.id,
            interaction.guild.id
        )
        warn_count = self.bot.db._warn_count(
            cursor,
            member.id,
            interaction.guild.id
        )
        embed = nextcord.Embed(
            title=f"{member}'s Warns | {warn_count}",
            colour=member.colour
        )
        for warn in member_warns:
            datetime_obj = datetime.datetime.fromtimestamp(int(warn["time"]))
            datetime_format = datetime_obj.strftime("%Y-%m-%d")
            moderator = nextcord.utils.get(
                interaction.guild.members,
                id=warn["moderator_id"]
            )
            embed.add_field(
                name=f"#{warn['warn_id']} | {datetime_format}",
                value=f"""
                Responsible Moderator: {moderator}
                Reason: {warn['reason']}
                """
            )
        await interaction.send(embed=embed)
        cursor.close()
        cursor.connection.commit()

    @warn.subcommand(name="info")
    async def warn_info(
        self,
        interaction: nextcord.Interaction,
        warn_id: int = SlashOption(required=True)
    ):
        """
        Get information about a warning.
        """
        await interaction.response.defer()
        cursor = self.bot.create_connection().cursor()
        warn = self.bot.db.warn_info(cursor, warn_id, interaction.guild.id)
        if warn == "GuildNoMatch":
            return await interaction.send(f"Warning #{warn_id} was not issued in this guild.")
        if warn == "InvalidWarn":
            return await interaction.send(f"Invalid Warn ID #{warn_id}.")
        member = nextcord.utils.get(
            interaction.guild.members, id=warn["user_id"]
        )
        moderator = nextcord.utils.get(
            interaction.guild.members, id=warn["moderator_id"]
        )
        embed = nextcord.Embed(title=f"#{warn_id} Info", colour=member.colour)
        datetime_obj = datetime.datetime.fromtimestamp(int(warn["time"]))
        datetime_format = datetime_obj.strftime("%d %B %Y, %I:%M %p")
        embed.add_field(name="Member", value=member)
        embed.add_field(name="Responsible Moderator", value=moderator)
        embed.add_field(name="Time", value=datetime_format)
        embed.add_field(name="Reason", value=warn["reason"])
        await interaction.send(embed=embed)
        cursor.close()
        cursor.connection.commit()


def setup(bot):
    bot.add_cog(Mod(bot))
