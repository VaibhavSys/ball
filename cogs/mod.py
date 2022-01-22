import nextcord.ext
import nextcord.utils 
from nextcord.ext import commands, tasks

dfprefix = "-"
bot = commands.Bot(command_prefix = dfprefix)

class Mod(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	@commands.has_permissions(manage_roles=True)
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
	
	@commands.command(pass_context=True)
	@commands.has_permissions(manage_roles=True)
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
	
	@commands.command(pass_context=True)
	@commands.has_guild_permissions(mute_members=True)
	async def vcmute(self, ctx, member : nextcord.Member, *, reason=None):
		await member.edit(mute = True)
		await ctx.send(f"{member} has been successfully voice-muted by {ctx.author.mention} with reason '{reason}'")
		
	@vcmute.error
	async def vcmute_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingPermissions):
			await ctx.send(f"{ctx.author.mention}: You do not have enough permissions (Mute Members) to use this command.")
		elif isinstance(error, commands.errors.MemberNotFound):
			await ctx.send(f"{ctx.author.mention}: I coudn't find that member.")
		elif isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("I do not have the required permissions to do that, or the member you are trying to voice-mute has a role higher than me.")
		else:
			await ctx.send("Voice mute failed.")
		
	@commands.command(pass_context=True)
	@commands.has_guild_permissions(mute_members=True)
	async def vcunmute(self, ctx, member : nextcord.Member, *, reason=None):
		await member.edit(mute = False)
		await ctx.send(f"{member} has been successfully voice-unmuted by {ctx.author.mention} with reason '{reason}'")	
	
	@vcunmute.error
	async def vcunmute_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingPermissions):
			await ctx.send(f"{ctx.author.mention}: You do not have enough permissions (Mute Members) to use this command.")
		elif isinstance(error, commands.errors.MemberNotFound):
			await ctx.send(f"{ctx.author.mention}: I coudn't find that member.")
		elif isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("I do not have the required permissions to do that, or the member you are trying to voice-unmute has a role higher than me.")
		else:
			await ctx.send("Voice unmute failed.")
	
	@commands.command(pass_context=True)
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member: nextcord.Member, *, reason=None):
		await ctx.guild.kick(user=member, reason=reason)
		await ctx.send(f"User {member}({member.id})) has kicked by {ctx.author.mention} with reason '{reason}''.")
	
	@kick.error
	async def kick_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingPermissions):
			await ctx.send(f"{ctx.author.mention}: You do not have enough permissions (Kick Members) to use this command.")
		elif isinstance(error, commands.errors.MemberNotFound):
			await ctx.send(f"{ctx.author.mention}: I coudn't find that member.")
		elif isinstance(error, commands.errors.CommandInvokeError):
			await ctx.send("I do not have the required permissions to do that, or the member you are trying to kick has a role higher than me.")
		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.send(f"Missing arguments: Please use the command like '{dfprefix}kick <member> (reason)'")
		else:
			await ctx.send("Kick Failed")
			
	@commands.command(pass_context=True)
	@commands.has_permissions(ban_members=True)
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
			
	@commands.command(pass_context=True)
	@commands.has_permissions(ban_members=True)
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
			
def setup(bot):
	bot.add_cog(Mod(bot))
