import nextcord.ext
import nextcord.utils
from nextcord.ext import commands
from datetime import timedelta



class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check_any(commands.is_owner(),
        commands.has_permissions(manage_roles=True))
    @commands.guild_only()
    async def addrole(self, ctx, member: nextcord.Member, roles: nextcord.Role):
        """
        Add a role to a member.
        """
        await member.add_roles(roles)
        await ctx.send(f"{member.mention} has been given role(s) {roles.name}({roles.id}) by {ctx.author.mention}")


    @commands.command()
    @commands.check_any(commands.is_owner(),
        commands.has_permissions(manage_roles=True))
    @commands.guild_only()
    async def rmrole(self, ctx, member: nextcord.Member, roles: nextcord.Role):
        """
        Remove a role from a member.
        """
        await member.remove_roles(roles)
        await ctx.send(f"{member.mention} has been removed from {roles.name}({roles.id}) role(s) by {ctx.author.mention}")


    @commands.command(brief="Timeout a member.")
    @commands.check_any(commands.is_owner(),
        commands.has_permissions(manage_messages=True))
    @commands.guild_only()
    async def mute(self, ctx, member: nextcord.Member, time="10m", *, reason=None):
        """
        Use the discord timeout feature to timeout a member, max time is 1 week.
        """
        unit = time[-1]
        time = int(time[:-1])
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
            return await ctx.send("Invalid time/unit or time is more than 1 week.")

        await member.edit(timeout=delta, reason=reason)
        await ctx.reply(f"{member.mention} has been timed out by {ctx.author.mention} with reason '{reason}' for {f'{time}{unit}'}.")


    @commands.command(brief="Traditonal mute a member.")
    @commands.check_any(commands.is_owner()
                        or commands.has_permissions(manage_messages=True))
    @commands.guild_only()
    async def tmute(self, ctx, member: nextcord.Member, *, reason=None):
        """
        Traditional mute a user by adding a muted role with no permissions to send messages,
        speak in voice channels, react to messages and requesting to join stages.
        """
        muted = nextcord.utils.get(ctx.guild.roles, name="Muted")

        if not muted:    
            muted = await ctx.guild.create_role(name="Muted", reason="Used for muting.")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted, send_messages=False, speak=False, request_to_speak=False, add_reactions=False)

        await member.add_roles(muted)
        await ctx.reply(f"{member} has been muted by {ctx.author.mention} with reason '{reason}'")

    @commands.command()
    @commands.check_any(commands.is_owner(),
        commands.has_permissions(moderate_members=True))
    @commands.guild_only()
    async def unmute(self, ctx, member: nextcord.Member, *, reason=None):
        """
        Remove a member from timeout.
        """
        
        await member.edit(timeout=None, reason=reason)
        await ctx.reply(f"{member.mention} has been removed from timeout by {ctx.author.mention} with reason '{reason}'.")

    @commands.command(brief="Traditonal unmute a member.")
    @commands.check_any(commands.is_owner(),
        commands.has_permissions(manage_messages=True))
    @commands.guild_only()
    async def tunmute(self, ctx, member: nextcord.Member, *, reason=None):
        """
        Traditional unmute, unmute a member muted by traditional mute.
        """
        
        mutedrole = nextcord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mutedrole)
        await ctx.reply(f"{ctx.author.mention} has been unmuted by {ctx.author.mention} with reason '{reason}'")

    @commands.command(brief="Voice-mute a member.")
    @commands.check_any(commands.is_owner(),
        commands.has_guild_permissions(mute_members=True))
    @commands.guild_only()
    async def vcmute(self, ctx, member: nextcord.Member, *, reason=None):
        """
        Voice-mute a member so that they cannot talk in a voice channel anymore.
        """
        
        await member.edit(mute=True)
        await ctx.reply(f"{member} has been successfully voice-muted by {ctx.author.mention} with reason '{reason}'")


    @commands.command(brief="Voice-unmute a member.")
    @commands.check_any(commands.is_owner(),
        commands.has_guild_permissions(mute_members=True))
    @commands.guild_only()
    async def vcunmute(self, ctx, member: nextcord.Member, *, reason=None):
        """
        Voice-unmute a member so that they can talk in a voice channel again.
        """
        
        await member.edit(mute=False)
        await ctx.reply(f"{member} has been successfully voice-unmuted by {ctx.author.mention} with reason '{reason}'")


    @commands.command()
    @commands.check_any(commands.is_owner(),
        commands.has_permissions(kick_members=True))
    @commands.guild_only()
    async def kick(self, ctx, member: nextcord.Member, *, reason=None):
        """
        Kick a user from the guild.
        """
        
        await ctx.guild.kick(user=member, reason=reason)
        await ctx.send(f"User {member}({member.id})) has kicked by {ctx.author.mention} with reason '{reason}''.")


    @commands.command()
    @commands.check_any(commands.is_owner(),
        commands.has_permissions(ban_members=True))
    @commands.guild_only()
    async def ban(self, ctx, member: nextcord.Member, *, reason=None):
        """
        Ban a member from the guild.
        """
        
        await member.ban(reason=reason)
        await ctx.send(f"{member} has been banned by {ctx.author.mention} with reason '{reason}'.")


    @commands.command()
    @commands.check_any(commands.is_owner(),
        commands.has_permissions(ban_members=True))
    @commands.guild_only()
    async def unban(self, ctx, *, member, reason=None):
        """
        Unban a previously banned member from the guild.
        """
        
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (
                    member_name, member_discriminator):
                await ctx.guild.unban(user, reason=reason)
                await ctx.send(f"{user.name}#{user.discriminator} has been unbanned by {ctx.author.mention} with reason '{reason}'")

    @commands.command(brief="Lock a channel.")
    @commands.check_any(commands.is_owner(),
        commands.has_permissions(manage_messages=True))
    @commands.guild_only()
    async def lock(self, ctx, channel: nextcord.TextChannel = None):
        """
        Lock a channel, restrict sending messages permission to @everyone role.
        """
        
        channel = channel or ctx.channel
        try:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send('Channel locked.')
        except nextcord.Forbidden:
            await ctx.send("I do not have enough permissions to perform this action.")


    @commands.command(breif="Unlock a channel.")
    @commands.check_any(commands.is_owner(),
        commands.has_permissions(manage_messages=True))
    @commands.guild_only()
    async def unlock(self, ctx, channel: nextcord.TextChannel = None):
        """
        Unlock a previously locked channel.
        """
        channel = channel or ctx.channel
        try:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send('Channel unlocked.')
        except nextcord.Forbidden:
            await ctx.send("I do not have enough permissions to perform this action.")


    @commands.command()
    @commands.check_any(commands.is_owner(),
        commands.has_permissions(manage_messages=True))
    @commands.guild_only()
    async def purge(self, ctx, *, limit: int):
        """
        Delete messages in bulk.
        """
        await ctx.channel.purge(limit=limit)
        await ctx.send(f"Purged {limit} messages.", delete_after=3)


    @commands.command()
    @commands.guild_only()
    @commands.check_any(commands.is_owner(),
        commands.has_permissions(manage_messages=True))
    async def slowmode(self, ctx, interval: int = 0, unit="s"):
        """Changes channel's slowmode setting.
        Use without parameters to disable.
        """
        
        if unit == "s":
            interval = timedelta(seconds=interval).total_seconds()
        elif unit == "m":
            interval = timedelta(minutes=interval).total_seconds()

        await ctx.channel.edit(slowmode_delay=interval)
        if interval > 0:
            await ctx.send(f"Slowmode interval is now {interval}.")
        else:
            await ctx.send("Slowmode has been disabled.")


def setup(bot):
    bot.add_cog(Mod(bot))
