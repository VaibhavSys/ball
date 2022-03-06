import nextcord.ext
import nextcord.utils 
from nextcord.ext import commands, tasks
from datetime import timedelta

dfprefix = "-"

class Mod(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(brief="Add role to a user", description="Add role to a user")
	@commands.check_any(commands.is_owner() or commands.has_permissions(manage_roles=True))
	@commands.guild_only()
	async def addrole(self, ctx, member: nextcord.Member, roles: nextcord.Role):
		await member.add_roles(roles)
		await ctx.send(f"{member.mention} has been given role(s) {roles.name}({roles.id}) by {ctx.author.mention}")

	@addrole.error
	async def addrole_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingPermissions):
			await ctx.send(f"{ctx.author.mention}: You do not have enough permissions (Manage Roles) to use this command.")
		elif isinstance(error, commands.errors.MemberNotFound):
			await ctx.send(f"{ctx.author.mention}: I coudn't find that member.")
		elif isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("I do not have the required permissions to do that, or the member you are trying to add the role to has a role higher than me.")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send(f"Missing arguments: Please use the command like '{dfprefix}addrole <member> <role>'")
		else:
			await ctx.send("Adding role Failed")
	
	@commands.command(brief="Remove role from a user", description="Remove role from a user")
	@commands.check_any(commands.is_owner() or commands.has_permissions(manage_roles=True))
	@commands.guild_only()
	async def rmrole(self, ctx, member: nextcord.Member, roles: nextcord.Role):
		await member.remove_roles(roles)
		await ctx.send(f"{member.mention} has been removed from {roles.name}({roles.id}) role(s) by {ctx.author.mention}")
	
	@rmrole.error
	async def rmrole_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingPermissions):
			await ctx.send(f"{ctx.author.mention}: You do not have enough permissions (Manage Roles) to use this command.")
		elif isinstance(error, commands.errors.MemberNotFound):
			await ctx.send(f"{ctx.author.mention}: I coudn't find that member.")
		elif isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("I do not have the required permissions to do that, or the member you are trying to remove the role from has a role higher than me.")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send(f"Missing arguments: Please use the command like '{dfprefix}rmrole <member> <role>'")
		else:
			await ctx.send("Removing role Failed")
			
	@commands.command(brief="Mute a user", description="Mute a user")
	@commands.check_any(commands.is_owner() or commands.has_permissions(manage_messages=True))
	@commands.guild_only()
	async def mute(self, ctx, member: nextcord.Member, *, reason=None):
		mutedRole = nextcord.utils.get(ctx.guild.roles, name="Muted")
		async def makeMuted():
			if not mutedRole:
				try:
					muted = await ctx.guild.create_role(name="Muted", reason="Used for muting.")
					for channel in ctx.guild.channels:
						await channel.set_permissions(muted, send_messages=False)

				except nextcord.Forbidden:
					return await ctx.send("I don\'t have permissions to make muted role.")

		if not mutedRole:
			await makeMuted()

		await member.add_roles(mutedRole)
		await ctx.send(f"{member} has been muted by {ctx.author.mention} with reason '{reason}'")

	@mute.error
	async def mute_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("Missing Argument: member")
		elif isinstance(error, commands.errors.MemberNotFound):
			await ctx.send(f"{ctx.author.mention}: I coudn't find that member.")
		else:
			await ctx.send(f"Mute failed: {error}")
			
	@commands.command(brief="Unmute a user", description="Unmute a user")
	@commands.check_any(commands.is_owner() or commands.has_permissions(manage_messages=True))
	@commands.guild_only()
	async def unmute(self, ctx, user: nextcord.Member, *, reason=None):
		await user.remove_roles(nextcord.utils.get(ctx.guild.roles, name="Muted"))
		await ctx.send(f"{user.mention} has been unmuted by {ctx.author.mention} with reason '{reason}'")
	
	@unmute.error
	async def unmute_error(self, ctx, error):
		if isinstance(error, commands.errors.MemberNotFound):
			await ctx.send(f"I coudn't find that member.")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("Missing Argument: member")
		else:
			await ctx.send(f"Unmute failed: {error}")
		
	@commands.command(brief="Mute a user in voice channel", description="Mute a user in voice channel")
	@commands.check_any(commands.is_owner() or commands.has_guild_permissions(mute_members=True))
	@commands.guild_only()
	async def vcmute(self, ctx, member : nextcord.Member, *, reason=None):
		await member.edit(mute = True)
		await ctx.send(f"{member} has been successfully voice-muted by {ctx.author.mention} with reason '{reason}'")
		
	@vcmute.error
	async def vcmute_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingPermissions):
			await ctx.send(f"{ctx.author.mention}: You do not have enough permissions (Mute Members) to use this command.")
		elif isinstance(error, commands.errors.MemberNotFound):
			await ctx.send(f"{ctx.author.mention}: I coudn't find that member.")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("Missing Argument: member")
		else:
			await ctx.send(f"Voice-mute failed: {error}")
		
	@commands.command(brief="Unmute a user in voice channel", description="Unmute a user in voice channel")
	@commands.check_any(commands.is_owner() or commands.has_permissions(mute_members=True))
	@commands.guild_only()
	async def vcunmute(self, ctx, member : nextcord.Member, *, reason=None):
		await member.edit(mute = False)
		await ctx.send(f"{member} has been successfully voice-unmuted by {ctx.author.mention} with reason '{reason}'")	
	
	@vcunmute.error
	async def vcunmute_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingPermissions):
			await ctx.send(f"{ctx.author.mention}: You do not have enough permissions (Mute Members) to use this command.")
		elif isinstance(error, commands.errors.MemberNotFound):
			await ctx.send(f"{ctx.author.mention}: I coudn't find that member.")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("Missing Argument: member")
		else:
			await ctx.send(f"Voice unmute failed: {error}")
	
	@commands.command(brief="Kick a user from guild", description="Kick a user from guild")
	@commands.check_any(commands.is_owner() or commands.has_permissions(kick_members=True))
	@commands.guild_only()
	async def kick(self, ctx, member: nextcord.Member, *, reason=None):
		await ctx.guild.kick(user=member, reason=reason)
		await ctx.send(f"User {member}({member.id})) has kicked by {ctx.author.mention} with reason '{reason}''.")
	
	@kick.error
	async def kick_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingPermissions):
			await ctx.send(f"{ctx.author.mention}: You do not have enough permissions (Kick Members) to use this command.")
		elif isinstance(error, commands.errors.MemberNotFound):
			await ctx.send("I coudn't find that member.")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send("Missing Required Argument: Member")
		else:
			await ctx.send("Kick Failed")
			
	@commands.command(brief="Ban a user from guild", description="Ban a user from guild")
	@commands.check_any(commands.is_owner() or commands.has_permissions(ban_members=True))
	@commands.guild_only()
	async def ban(self, ctx, member : nextcord.Member, *, reason=None):
		await member.ban(reason=reason)
		await ctx.send(f"{member} has been banned by {ctx.author.mention} with reason '{reason}'.")
		
	@ban.error
	async def ban_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingPermissions):
			await ctx.send(f"{ctx.author.mention}: You do not have enough permissions (Ban Members) to use this command.")
		elif isinstance(error, commands.errors.MemberNotFound):
			await ctx.send(f"{ctx.author.mention}: I coudn't find that member.")
		elif isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("I do not have the required permissions to do that, or the member you are trying to ban has a role higher than me.")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send(f"Missing arguments: Please use the command like '{dfprefix}ban <member> (reason)'")		
		else:
			await ctx.send("Ban Failed")
			
	@commands.command(brief="Unban a user from guild", description="Unban a user from guild")
	@commands.check_any(commands.is_owner() or commands.has_permissions(ban_members=True))
	@commands.guild_only()
	async def unban(self, ctx, *, member, reason=None):
		banned_users = await ctx.guild.bans()
		member_name, member_discriminator = member.split("#")

		for ban_entry in banned_users:
			user = ban_entry.user

			if (user.name, user.discriminator) == (member_name, member_discriminator):
				await ctx.guild.unban(user, reason=reason)
				await ctx.send(f"{user.name}#{user.discriminator} has been unbanned by {ctx.author.mention} with reason '{reason}'")

	@unban.error
	async def unban_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingPermissions):
			await ctx.send(f"{ctx.author.mention}: You do not have enough permissions (Ban Members) to use this command.")
		elif isinstance(error, commands.errors.MemberNotFound):
			await ctx.send(f"{ctx.author.mention}: I coudn't find that member.")
		elif isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("I do not have the requried permissions (Ban Members) to do that.")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send(f"Missing arguments: Please use the command like '{dfprefix}unban <member> (reason)'")
		else:
			await ctx.send("Unban Failed")
			
	@commands.command(brief="Lock a channel", description="Lock a channel. Noone without special permission can chat in a locked channel")
	@commands.check_any(commands.is_owner() or commands.has_permissions(manage_messages=True))
	@commands.guild_only()
	async def lock(self, ctx, channel : nextcord.TextChannel = None):
		channel = channel or ctx.channel
		try:
			overwrite = channel.overwrites_for(ctx.guild.default_role)
			overwrite.send_messages = False
			await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
			await ctx.send('Channel locked.')
		except nextcord.Forbidden:
			await ctx.send("I do not have enough permissions to perform this action.")
			
	@lock.error
	async def lock_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingPermissions):
			await ctx.send("You are missing Manage Messages permission(s) to run this command.")
	
	@commands.command(brief="Unlock a channel", description="Unlock a channel")
	@commands.check_any(commands.is_owner() or commands.has_permissions(manage_messages=True))
	@commands.guild_only()
	async def unlock(self, ctx, channel : nextcord.TextChannel = None):
		channel = channel or ctx.channel
		try:
			overwrite = channel.overwrites_for(ctx.guild.default_role)
			overwrite.send_messages = None
			await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
			await ctx.send('Channel unlocked.')	
		except nextcord.Forbidden:
			await ctx.send("I do not have enough permissions to perform this action.")
		
	@unlock.error
	async def unlock_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingPermissions):
			await ctx.send("You are missing Manage Messages permission(s) to run this command.")
			
	
	@commands.command(brief="Delete messages in a channel", description="Delete a certian amount of messages in a channel")
	@commands.check_any(commands.is_owner() or commands.has_permissions(manage_messages=True))
	@commands.guild_only()
	async def purge(self, ctx, *, limit: int):
		try:
			await ctx.channel.purge(limit=limit)
			await ctx.send(f"Purged {limit} messages.", delete_after=3)
		except nextcord.Forbidden:
			await ctx.send("I do not have enough permissions to perform this action.")
		
	@purge.error
	async def purge_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingPermissions):
			await ctx.send("You do not have enough permissions (Manage Messages) to do that")
	
	@commands.command(brief="Change a channel's slowmode setting", description="Use the command without any args to disable slowmode")
	@commands.guild_only()
	@commands.check_any(commands.is_owner() or commands.has_permissions(manage_messages=True))
	async def slowmode(self, ctx, interval: int = 0, unit = "s"):
		"""Changes channel's slowmode setting.
		Interval can be anything from 0 seconds to 6 hours.
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
